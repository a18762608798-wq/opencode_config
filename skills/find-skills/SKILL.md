---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill. Before installation, select the physical installation directory according to any hard-coded skill paths. If no specific directory is required, prefer OpenCode, then Claude Code.
---
# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

* Asks "how do I do X" where X might be a common task with an existing skill
* Says "find a skill for X" or "is there a skill for X"
* Asks "can you do X" where X is a specialized capability
* Expresses interest in extending agent capabilities
* Wants to search for tools, templates, or workflows
* Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

* `npx skills find [query] [--owner <owner>]` - Search for skills interactively or by keyword, optionally scoped to a GitHub owner
* `npx skills add <package>` - Install a skill from GitHub or other sources
* `npx skills update` - Update all installed skills

**Browse skills at:** <https://skills.sh/>

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check the Leaderboard First

Before running a CLI search, check the [skills.sh leaderboard](https://skills.sh/) to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development include:

* `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
* `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills find [query] [--owner <owner>]
```

For example:

* User asks "how do I make my React app faster?" → `npx skills find react performance`
* User asks "can you help me with PR reviews?" → `npx skills find pr review`
* User asks "I need to create a changelog" → `npx skills find changelog`

### Step 4: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.
4. **Installation paths** — Inspect `SKILL.md`, scripts, and configuration files for hard-coded agent-specific paths.

Look for paths such as:

```text
~/.config/opencode/skills/
~/.claude/skills/
```

Use the following rules:

* If operational commands or scripts hard-code `~/.config/opencode/skills/`, install for `opencode`.
* If operational commands or scripts hard-code `~/.claude/skills/`, install for `claude-code`.
* If the skill uses only relative or portable paths, install for `opencode`.
* If both directories are equally supported, prefer `opencode`, then `claude-code`.
* A path mentioned only as a README installation example does not count as an operational hard-code.
* If operational paths conflict, report the conflict instead of installing automatically.
* If the skill strongly depends on Codex-specific paths, commands, hooks, or behavior and cannot work through OpenCode or the Claude-compatible directory, do not install it. Report that the skill is incompatible with the intended setup.

The selected `--agent` value controls the physical installation directory. It does not necessarily determine which agent the user will use to load the skill.

### Step 5: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install count and source
3. The selected installation target and reason
4. The install command they can run
5. A link to learn more at skills.sh

Example response:

```text
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

No agent-specific installation path was found, so the OpenCode global
directory is preferred.

To install it:

npx skills add vercel-labs/agent-skills \
  --skill react-best-practices \
  --global \
  --agent opencode \
  --copy \
  --yes

Learn more:
https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

If a skill requires Codex and cannot be used through the supported directories, report it like this:

```text
This skill has a strong Codex-specific dependency and cannot be used reliably
through the current OpenCode setup.

Codex-specific requirement:
<describe the required path, command, hook, or behavior>

The skill was not installed.
```

### Step 6: Offer to Install

If the user wants to proceed, install the skill using the target selected during the path check.

**OpenCode** — default when no agent-specific path is required:

```bash
npx skills add <owner/repo> \
  --skill <skill-name> \
  --global \
  --agent opencode \
  --copy \
  --yes
```

**Claude Code** — when the skill operationally hard-codes `~/.claude/skills/`:

```bash
npx skills add <owner/repo> \
  --skill <skill-name> \
  --global \
  --agent claude-code \
  --copy \
  --yes
```

The `--global` flag installs at the user level, `--copy` places the files physically in the selected agent directory, and `--yes` skips confirmation prompts.

Do not use an ambiguous command such as:

```bash
npx skills add <owner/repo@skill> -g -y
```

Always specify the selected `--agent` and `--skill`.

Do not install a skill when it requires Codex-specific behavior that cannot work through OpenCode or the Claude-compatible directory.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`
4. **Check installation paths**: Prefer the directory required by operational hard-coded paths
5. **Use OpenCode by default**: When the skill is portable, prefer the OpenCode global directory
6. **Reject Codex-only skills**: If a skill cannot function without Codex-specific behavior, report the incompatibility instead of installing it

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```text
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:

npx skills init my-xyz-skill
```
