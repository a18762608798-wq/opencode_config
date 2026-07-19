# Skill Benchmark: knowledge-organizer

**Model**: deepseek/deepseek-v4-pro
**Date**: 2026-07-19T12:45:00Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 75% ± 13% | +0.25 |

## Per-Eval Breakdown

| Eval | With Skill | Without Skill |
|------|-----------|---------------|
| julia-broadcast-dispatch | 100% (8/8) | 75% (6/8) |
| quantum-basics-grover | 100% (8/8) | 62% (5/8) |
| pandas-agg-transform | 100% (8/8) | 88% (7/8) |

## Observations

- with_skill 在所有 eval 上达到完美 100%
- eval-1 (量子计算) without_skill 最低 (62%)：产生 5 个虚构知识点（VQE、表面码等）
- without_skill 普遍缺少：分类标记、时间戳文件命名、结构化段落
- 最大的 improvement delta 在 eval-1 (quantum): +38%
