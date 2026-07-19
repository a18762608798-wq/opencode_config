# pandas groupby 多聚合与大数据分块读取

**Date**: 2026-07-19 12:00
**Category**: Programming/Python
**Tags**: #pandas #groupby #大数据 #聚合 #chunksize

## Background
用户需要处理 50 万行的 CSV 数据，要求按 category 列分组，对 amount 列同时计算均值和标准差。

## Content
使用 `df.groupby('category')['amount'].agg(['mean', 'std'])` 可以一次性按分组计算多个聚合函数。`agg` 方法接收函数名列表或函数对象列表，返回以这些函数名为列名的 DataFrame。

对于大数据量场景，如果内存不足以一次性加载全部数据，可以在 `pd.read_csv()` 中使用 `chunksize` 参数分块读取。例如 `pd.read_csv('data.csv', chunksize=50000)` 会返回一个可迭代的 `TextFileReader` 对象，每次返回指定行数的 chunk。随后在循环中对每个 chunk 分别进行 groupby 聚合，再将各 chunk 的结果合并。

此外，在只需要聚合结果而不需要完整原始数据的场景下，直接使用 `agg` 比先 `groupby` 再分别调用 `.mean()` 和 `.std()` 内存效率更高。

## Key Points
- `df.groupby(col)[col].agg(['mean', 'std'])` 可一次性完成多聚合
- `pd.read_csv(path, chunksize=N)` 按块读取大文件，避免内存溢出
- 分块处理后需自行合并各块结果（如累加求和后再除以总数计算均值）
- `agg` 内存效率优于分别调用多个聚合函数
