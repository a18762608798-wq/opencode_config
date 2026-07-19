# pandas apply 的使用时机与性能优化

**Date**: 2026-07-19 12:00
**Category**: Programming/Python
**Tags**: #pandas #apply #性能 #向量化 #优化

## Background
用户询问 pandas 的 `apply` 何时该用、何时该避免，需要理解其性能特性和替代方案。

## Content
`apply` 是 pandas 中非常灵活的操作，但它本质上是 Python 层面的逐行或逐组循环，**没有向量化**，因此性能较差。对于常见的数值操作，应优先使用以下替代方案：

1. **内置聚合方法**：`.sum()`, `.mean()`, `.count()`, `.std()` 等，它们底层使用 C 实现，速度远超 `apply`。
2. **`agg`**：同时执行多个聚合时比 apply 更高效。
3. **向量化运算**：如果 `apply` 的操作可以拆解为一系列向量化步骤的组合，就不要用 apply。

示例优化：将 `df.groupby('key').apply(lambda g: g['a'].sum() / g['b'].mean())` 改写为先分别用 `agg` 计算 `a.sum()` 和 `b.mean()`，再在结果上进行除法运算。这样避免了 Python 层面的逐组循环，性能提升显著。

`apply` 仅在操作逻辑非常特殊、无法用内置方法或向量化步骤表达时才应该使用。

## Key Points
- `apply` 是 Python 层面的循环，无向量化，性能差
- 优先用内置聚合方法（`.sum()`, `.mean()` 等）代替 apply
- 优先用 `agg` 做多聚合
- 能将 apply 拆成向量化步骤的就拆
- 仅在内置方法无法表达的特殊逻辑中使用 apply
- 分步聚合再组合比 apply 循环快很多
