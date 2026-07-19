---
name: docx
description: "当用户想要创建、读取、编辑或操作 Word 文档（.docx 文件）或 Word 模板（.dotx 文件）时使用此技能。触发条件包括：任何提及 'Word doc'、'word document'、'.docx'、'.dotx' 或请求生成带格式的专业文档（如目录、标题、页码或信头）。也用于从 .docx 或 .dotx 文件中提取或重组内容、在文档中插入或替换图片、在 Word 文件中执行查找替换、处理修订或批注，或将内容转换为精美的 Word 文档。如果用户要求生成 Word 或 .docx 文件的\"报告\"、\"备忘录\"、\"信函\"、\"模板\"或类似交付物，使用此技能。不要用于 PDF、电子表格、Google Docs 或与文档生成无关的通用编码任务。"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX 创建、编辑和分析

`.docx` 是 XML 文件的 ZIP 压缩包。按任务选择方法：

| 任务 | 方法 |
|---|---|
| **创建**新文档 | 编写 `docx`（npm）脚本 — 见下方注意事项 |
| **编辑**现有文档 | `unzip` → 编辑 `word/document.xml` → `zip`（docx-js 无法打开现有文件） |
| **读取**内容 | `pandoc -t markdown file.docx` |

> 以下脚本路径相对于此技能的目录。

## 使用 docx-js 创建 — 注意事项

`docx` 已预装——不要先运行 `npm install`；直接编写脚本并 `require('docx')`。仅当 require 失败时：`npm install docx`。模型了解该 API；以下是易错点：

- **页面大小默认为 A4。** 使用 US Letter 时设置 `page: { size: { width: 12240, height: 15840 } }`（DXA 单位；1440 = 1 英寸）。
- **横向：** 传入纵向尺寸和 `orientation: PageOrientation.LANDSCAPE` — docx-js 内部交换宽高。
- **表格需要双重宽度：** 在表格上设置 `columnWidths`，并在每个单元格上设置 `width`，两者都使用 `WidthType.DXA`（PERCENTAGE 在 Google Docs 中会损坏）。列宽必须等于表格宽度之和。
- **表格底纹：** 使用 `ShadingType.CLEAR`，绝不用 `SOLID`（渲染为黑色）。
- **列表：** 绝不要直接插入 `•` 字面字符；使用带 `LevelFormat.BULLET` 的 `numbering` 配置。
- **`ImageRun` 需要 `type:`**（`"png"`、`"jpg"` 等）。
- **`PageBreak` 必须在 `Paragraph` 内部。**
- **绝不要使用 `\n`** — 使用单独的 `Paragraph` 元素。
- **目录：** 标题必须使用内置的 `HeadingLevel.*`；自定义标题样式需要设置 `outlineLevel`，否则不会出现在目录中。
- **不要用表格作为水平分隔线** — 改用段落底边框。
- **点引导符/同一行右对齐：** 在 `TextRun` 中使用 `PositionalTab`（`alignment: PositionalTabAlignment.RIGHT`，`leader: PositionalTabLeader.DOT`），而非字面的 `.` 或空格填充。

## 验证输出

编写 `.docx` 后，渲染并查看：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg   # 然后使用 Read 工具查看图片
```

`pdftoppm` 对页码进行零填充，宽度与总页数位宽一致（`page-01.jpg`…`page-12.jpg`）。

## 编辑现有文档

旧的 `.doc` 文件必须先转换：`python scripts/office/soffice.py --headless --convert-to docx file.doc`。

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # 删除符号链接条目 — 来自外部的 docx 不可信任
python scripts/merge_runs.py unpacked/   # 合并碎片化的 run，使文本可查找
# 就地编辑 unpacked/word/document.xml — 不要重新格式化或美化
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD 检查；--auto-repair 修复常见问题
# 修订？添加 --author "<你用于修订的名称>" 来检查每个编辑是否已标记
```

Word 将文本分散在许多 `<w:r>` run 中（修订 ID、拼写检查标记），因此你在文档中能看到的短语通常在 XML 中不是连续的字符串。`merge_runs.py` 合并 `word/document.xml` 中相邻且格式相同的 run，不改变内容或渲染；它也接受直接传入 `.docx` 文件（`python scripts/merge_runs.py doc.docx -o merged.docx`）。

**修订（Tracked changes）：** 进行修订时，使用 `--author "<你用于修订的名称>"` 验证（需要 `--original`）— 它报告任何你更改了但未用 `<w:ins>`/`<w:del>` 包裹的文本，这种情况容易意外发生，且在接受视图下不可见。用带有 `w:id`、`w:author`、`w:date` 属性的 `<w:ins>`/`<w:del>` 包裹 run。在 `<w:del>` 内部，文本元素是 `<w:delText>`，而非 `<w:t>`。一个已删除的段落标记（`<w:pPr><w:rPr><w:del w:id=".." w:author=".." w:date=".."/></w:rPr></w:pPr>`）意味着"将此段落合并到下一个段落" — 因此彻底删除段落需要加上在每个 run 周围包裹 `<w:del>`。`<w:del/>` 必须位于 rPr 其他子元素之前；它们的顺序受 schema 约束。

生成一个接受所有修订的干净副本：`python scripts/accept_changes.py in.docx out.docx`。

接受已删除的段落标记应将该段落合并到其下的段落，因此所有 run 都已被删除的段落会消失。Word 会这样做；但 `accept_changes.py` 和 `pandoc --track-changes=accept` 不总是如此。两者以相同的方式失败 — 它们删除已删除的文本，但保留空段落，当它是自动编号时会显示为杂散的空项目符号：

- `pandoc --track-changes=accept` 从不合并段落。
- `accept_changes.py`（LibreOffice）正确合并，除非被删除段落后跟着一个空的分隔段。

任一视图中的空项目符号是该视图的产物，而非文档缺陷。在 XML 中检查段落删除。

## 批注（Comments）

批注需要六个交叉链接的文件。使用辅助脚本——当你还需要编辑 `document.xml` 时使用目录模式（省去解压/重新压缩的循环），否则使用 `.docx` 直接模式：

```bash
# 针对已解压的目录（同时放置标记时推荐）
python scripts/comment.py unpacked/ "费用和开支上限太低"
python scripts/comment.py unpacked/ "同意" --parent 0

# 直接针对 .docx
python scripts/comment.py contract.docx "这个上限太低" -o annotated.docx
```

该脚本写入 `comments.xml`、`commentsExtended.xml`、`commentsIds.xml`、`commentsExtensible.xml`、关系文件及内容类型覆盖。批注 ID 自动分配。然后打印 `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>` 片段，添加到 `word/document.xml` 中以将批注锚定到特定文本——在放置这些标记之前，批注存在但不可见。

## 依赖

`docx`（npm，已预装 — 仅当 `require('docx')` 失败时才安装）· `pandoc` · LibreOffice（`soffice`）· `pdftoppm`（Poppler）
