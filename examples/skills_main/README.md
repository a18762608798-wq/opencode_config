# README

这是Anthropic 公开的 Agent Skills 示例与参考实现集合. 虽然我们使用的是opencode, 但这里依然提供了不少模板.

`skills/` 里主要是这些现成 Skill 示例：

* **文档处理**：`pdf`、`docx`、`pptx`、`xlsx`
* **开发工具**：`claude-api`、`mcp-builder`、`webapp-testing`、`frontend-design`、`web-artifacts-builder`
* **Skill 开发**：`skill-creator`
* **设计内容**：`algorithmic-art`、`canvas-design`、`brand-guidelines`、`theme-factory`、`slack-gif-creator`
* **办公写作**：`doc-coauthoring`、`internal-comms` 

## Useful cases:

1. **`skill-creator`**
   最重要。可用来创建你自己的科学计算 Skill，例如：

   * 数值计算流程
   * 数据清洗与统计分析
   * 仿真结果验证
   * Python/NumPy/SciPy 使用规范
   * 实验结果复现

2. **`mcp-builder`**
   如果要让 Agent 调用 Jupyter、Matlab、Wolfram、仿真软件或内部计算服务，可以参考它构建工具接口。

3. **`xlsx`**
   适合表格数据分析、公式、统计汇总和结果导出，但不适合大规模数值计算。

4. **`pdf`**
   适合读取论文、提取公式、表格和实验数据, 本质上是去编辑pdf。

5. **`docx` / `pptx`**
   用于生成实验报告、研究文档和汇报材料。

6. **`web-artifacts-builder`**
   可用于制作交互式数据图表或仿真结果展示页面。

**其实严格来说之哟第一, 二个相对有用**, 不过可以为我们提供范式.
