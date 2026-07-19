#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes opencode to load it (via the
native `skill` tool) for a set of queries. Outputs results as JSON.
"""

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md

# Custom env var to prevent recursive opencode nesting.
CHILD_ENV = "SKILL_CREATOR_EVAL_CHILD"


def find_project_root() -> Path:
    """Find the project root by walking up from cwd.

    Checks for .opencode/, .git/ so the temp skill lands where
    opencode will discover it.
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".opencode").is_dir() or (parent / ".git").is_dir():
            return parent
    return current


def _skill_content(skill_dir_name: str, skill_description: str) -> str:
    """Build a minimal SKILL.md with YAML frontmatter for opencode discovery.

    Uses YAML block scalar (|) to safely handle descriptions containing
    colons, newlines, or other YAML-significant characters.
    """
    return (
        f"---\n"
        f"name: {skill_dir_name}\n"
        f"description: |\n"
        f"  {skill_description}\n"
        f"---\n\n"
        f"# {skill_dir_name}\n"
    )


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Places a temporary SKILL.md under .opencode/skills/<skill_name>/
    so opencode discovers it, then invokes `opencode run --format json`.
    Parses the JSON output to detect whether the native `skill` tool was
    called with the target skill name.
    """
    unique_id = uuid.uuid4().hex[:8]
    # opencode skill names must be ≤ 64 chars.  Reserve room for suffix + UUID.
    max_name = 64 - len("-eval-") - len(unique_id)
    base = skill_name[:max_name] if len(skill_name) > max_name else skill_name
    skill_dir_name = f"{base}-eval-{unique_id}"
    skill_dir = Path(project_root) / ".opencode" / "skills" / skill_dir_name
    skill_file = skill_dir / "SKILL.md"

    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(_skill_content(skill_dir_name, skill_description))

        cmd = [
            "opencode",
            "run",
            query,
            "--format", "json",
            "--dir", str(project_root),
        ]
        if model:
            cmd.extend(["--model", model])

        # Prevent recursive nesting inside a parent opencode session.
        env = {**os.environ, CHILD_ENV: "1"}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=env,
        )

        triggered = False
        start_time = time.time()
        buffer = ""

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                # Process line-delimited JSON events as they arrive.
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Detect a tool_use event for the `skill` tool.
                    if _event_triggers_skill(event, skill_dir_name):
                        return True

        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        # Post-mortem: scan accumulated output for skill reference.
        if not triggered and buffer:
            triggered = skill_dir_name in buffer
            # Also try parsing remaining lines.
            for line in buffer.split("\n"):
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if _event_triggers_skill(event, skill_dir_name):
                    triggered = True
                    break

        return triggered

    finally:
        if skill_dir.exists():
            shutil.rmtree(skill_dir)


def _event_triggers_skill(event: dict, skill_dir_name: str) -> bool:
    """Return True if *event* indicates the `skill` tool was called with *skill_dir_name*."""

    # Pattern A: OpenCode native tool_use event
    # {"type":"tool_use","part":{"type":"tool","tool":"skill","state":{"input":{"name":"target"}}}}
    if event.get("type") == "tool_use":
        part = event.get("part", {})
        if _part_is_skill_tool(part, skill_dir_name):
            return True

    # Pattern B: Anthropic-compatible streaming event
    # {"type":"content_block_start","content_block":{"type":"tool_use","name":"skill",...}}
    if event.get("type") == "content_block_start":
        cb = event.get("content_block", {})
        if cb.get("type") == "tool_use" and _is_skill_tool_call(cb, skill_dir_name):
            return True

    # Pattern C: nested stream_event wrapper (Anthropic API / opencode bridge)
    if event.get("type") == "stream_event":
        inner = event.get("event", {})
        return _event_triggers_skill(inner, skill_dir_name)

    # Pattern D: full assistant message
    if event.get("type") == "assistant":
        for item in event.get("message", {}).get("content", []):
            if item.get("type") == "tool_use" and _is_skill_tool_call(item, skill_dir_name):
                return True

    # Pattern E: result event that references the skill
    if event.get("type") == "result" and skill_dir_name in json.dumps(event):
        return True

    return False


def _part_is_skill_tool(part: dict, skill_dir_name: str) -> bool:
    """Check if *part* is an OpenCode native tool part for `skill`."""
    if part.get("type") != "tool":
        return False
    if part.get("tool", "").lower() != "skill":
        return False
    state_input = part.get("state", {}).get("input", {})
    if isinstance(state_input, dict) and state_input.get("name") == skill_dir_name:
        return True
    return False


def _is_skill_tool_call(item: dict, skill_dir_name: str) -> bool:
    """Check if *item* is a tool_use for the `skill` tool targeting our skill."""
    name = item.get("name", "")
    if name.lower() != "skill":
        return False
    return _skill_input_matches(item.get("input", {}), skill_dir_name)


def _skill_input_matches(input_obj: dict, skill_dir_name: str) -> bool:
    """Check if the tool input references our skill directory name."""
    skill_param = input_obj.get("name") or input_obj.get("skill") or input_obj.get("file_path")
    if isinstance(skill_param, str) and skill_dir_name in skill_param:
        return True
    # Also check raw stringify for edge cases.
    raw = json.dumps(input_obj)
    return skill_dir_name in raw


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model for opencode run, in provider/model format (default: user's configured model)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
