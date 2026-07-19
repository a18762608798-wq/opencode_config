# pandas agg 与 transform 的区别

**Date**: 2026-07-19 12:00
**Category**: Programming/Python
**Tags**: #pandas #groupby #agg #transform #z-score

## Background
用户在使用 groupby 聚合时，需要理解 `agg` 和 `transform` 两种操作的本质区别以及各自的典型使用场景。

## Content
`agg`（aggregate）和 `transform` 是 groupby 对象的两种不同的结果处理方式：

- **agg**：返回每组的聚合标量值，结果的行数等于分组数（即每个组一行）。使用场景是当你想把数据缩减为每个组的汇总信息时。

- **transform**：返回与原始 DataFrame 相同长度的结果，将聚合值广播回原始数据的每一行。使用场景是当你需要保留原始数据的行结构，但为每一行附加其所在组的统计信息时。

典型示例：计算组内 z-score。
```python
df['zscore'] = df.groupby('category')['amount'].transform(
    lambda x: (x - x.mean()) / x.std()
)
```
这里 `transform` 可以像普通列一样把结果直接赋值回原 DataFrame，不会改变行数。

## Key Points
- `agg` 返回每行代表一个组的聚合结果，行数 = 分组数
- `transform` 返回与原始数据等长的结果，将组统计值广播到每行
- `transform` 的结果可以直接作为新列添加回原 DataFrame
- 计算组内 z-score 或其他行级标准化操作用 `transform`
- 汇总报告、统计分析等场景用 `agg`
