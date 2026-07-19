---
name: pptx
description: "当 .pptx 或 .potx 文件以任何方式涉及时使用此技能——作为输入、输出或两者。包括：创建幻灯片组、路演文稿或演示文稿；读取、解析或提取任何 .pptx 或 .potx 文件的文本（即使提取的内容将用于其他地方，如电子邮件或摘要）；编辑、修改或更新现有演示文稿；合并或拆分幻灯片文件；使用模板（.potx）、布局、演讲者备注或批注。当用户提到\"幻灯片\"、\"演示\"、\"演示文稿\"或引用 .pptx 或 .potx 文件名时触发，无论他们计划对内容做什么后续操作。如果需要打开、创建或涉及 .pptx 或 .potx 文件，使用此技能。"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX 创建、编辑和分析

`.pptx` 是 XML 文件的 ZIP 压缩包。按任务选择方法：

| 任务 | 方法 |
|---|---|
| **创建**新演示文稿 | 编写 `pptxgenjs` 脚本 — 见下方注意事项 |
| **编辑**现有演示文稿，或从模板构建 | unzip → 编辑 `ppt/slides/slideN.xml` → zip |
| **读取**内容 | `markitdown deck.pptx`（每个幻灯片以 `<!-- Slide number: N -->` 标记分隔）；可视化网格：`python scripts/thumbnail.py deck.pptx` |

## 脚本

路径相对于此技能的目录。其他一切使用纯 Python、`node` 或 shell。

| 脚本 | 功能 |
|---|---|
| `scripts/thumbnail.py deck.pptx [prefix]` | 每个幻灯片的带标签网格，用于选择模板布局。仅 .pptx。传入 `prefix`——默认为 `thumbnails`，会覆盖同一目录中其他演示文稿的网格 |
| `scripts/add_slide.py unpacked/ slide2.xml [--after slideN.xml]` | 复制幻灯片（或 `slideLayoutN.xml`），包含所有包相关操作。也可直接接受 `.pptx` 文件：`-o out.pptx` |
| `scripts/clean.py unpacked/` | 删除不再引用的幻灯片、媒体和关系。在 `<p:sldIdLst>` 定稿后运行 |
| `scripts/office/validate.py deck.pptx [--original src.pptx]` | Schema、关系、内容类型、图表和幻灯片检查；每个失败项会指明修复方法。对任何模板衍生的演示文稿传入 `--original`——它会基于模板进行基准校验，因此模板本身的 XSD 错误不会显示为你的错误 |
| `scripts/office/soffice.py --headless --convert-to pdf deck.pptx` | LibreOffice 包装器——原始 `soffice` 在沙盒中会挂起 |

## 使用 pptxgenjs 创建 — 注意事项

`pptxgenjs` 已预装——不要先运行 `npm install`；直接编写脚本并 `require('pptxgenjs')`。仅当 require 失败时：`npm install pptxgenjs`。模型了解该 API；以下是易错点：

- **在添加幻灯片之前设置 `pres.layout`。** 默认画布是 `LAYOUT_16x9` = **10" × 5.625"**，不是 13.3" 宽。超出边缘的坐标被写入而非裁剪——形状只是不在幻灯片上。（`LAYOUT_WIDE` 是 13.3" × 7.5"。）
- **十六进制颜色：绝不用 `#`，绝不用 8 位数。** `color: "FF0000"`。`"#FF0000"` 和带有 alpha 的十六进制（`"00000020"`）都会**损坏文件**。半透明：填充和图片使用 `transparency: 0-100`，阴影使用 `opacity: 0.0-1.0`——两者在对方上会被静默忽略。
- **pptxgenjs 会就地修改选项对象**（首次使用时将值转换为 EMU）。永远不要在两个 `add*` 调用之间共享同一个 `shadow`/options 对象——每次构建新对象。
- **阴影 `offset` 必须 ≥ 0**——负偏移会损坏文件。要使阴影向上投射，使用 `angle: 270` 配合正偏移。
- **`letterSpacing` 被静默忽略**——真正的选项是 `charSpacing`。
- **列表：** 每个项目设置 `bullet: true`，绝不用字面 `•`（会渲染双重点符号）。除最后一项外，每个数组元素设置 `breakLine: true`。使用 `paraSpaceAfter` 而非 `lineSpacing` 来间隔带项目符号的段落（否则间隙巨大）。
- **每个输出文件一个新 `new pptxgen()`**——绝不重复使用实例。
- **`rectRadius` 仅在 `ROUNDED_RECTANGLE` 上生效**，不在 `RECTANGLE` 上。
- **不支持渐变填充**——使用渐变图片作为背景替代。
- **文本框有内置内边距**——每当文本需要与同一 x 坐标处的形状、线条或图标对齐时，设置 `margin: 0`。
- **演讲者备注放在 `slide.addNotes("...")` 中**（纯文本，每张幻灯片一次），绝不在幻灯片上的文本框中。
- **保持图表为原生格式。** 使用 `addChart()` 处理 PowerPoint 能绘制的所有图表类型（传入 `{type, data, options}` 数组用于组合图表）。对于库未暴露的 PowerPoint 原生功能（趋势线、误差线），自行计算额外的系列或后处理生成的 OOXML——不要回退到渲染图片。仅 PowerPoint 没有原生形式的图表类型（桑基图、网络图、和弦图）才使用图片。
- **默认图表渲染得光秃秃的**——无标题、无数据标签、过时的调色板。设置 `showTitle` + `title`、`showValue: true` + `dataLabelPosition`、来自你调色板的 `chartColors: [...]`，并调低框架（`catAxisLabelColor`/`valAxisLabelColor`、`valGridLine: { color, size }`、`catGridLine: { style: "none" }`、单个系列时 `showLegend: false`）。
- **在堆叠柱状图或条形图上，`dataLabelPosition` 必须是 `ctr`、`inEnd` 或 `inBase`。** `outEnd` **会损坏文件**。
- **使用 `secondaryValAxis`/`secondaryCatAxis` 的组合图表系列需要在图表选项中同时设置 `valAxes` 和 `catAxes`，各两个条目。** 如果没有，pptxgenjs 写入了 PowerPoint 未声明的轴 *id*，PowerPoint 会**丢弃该图表**并报告文件损坏。只提供 `valAxes` 是不够的。
- **在 `writeFile()` 之后，运行 `python scripts/office/validate.py deck.pptx`。** 它会报告上述两种图表错误以及 PowerPoint 拒绝的幻灯片 XML 缺陷，并指明每个的修复方法。在生成器中修复，而非手动编辑打包的 XML。
- **绝不重新排序 `<p:presentation>` 的子元素。** pptxgenjs 在 `<p:sldIdLst>` 之后立即写入 `<p:notesMasterIdLst>`，并将两个母版指向同一个主题部分。PowerPoint 可以正常打开——移动元素位置后，同一个演示文稿变得无法打开。
- **图标：** 将 `react-icons` 渲染为 SVG（`ReactDOMServer.renderToStaticMarkup`），使用 `sharp` 以 ≥256px 栅格化，并通过 `addImage({ data: "image/png;base64," + buf.toString("base64") })` 插入——`image/png;base64,` 前缀是必需的（`react-icons`、`react`、`react-dom` 和 `sharp` 已预装——仅在 require 失败时 `npm install react-icons react react-dom sharp`）。

## 编辑现有演示文稿和模板

先选择布局：`python scripts/thumbnail.py template.pptx template-thumbs` 写入每个幻灯片的带标签网格并打印创建的文件——`template-thumbs.jpg`，超过 12 页时分割为 `template-thumbs-N.jpg`。**始终传入第二个参数，以演示文稿命名。** 默认为 `thumbnails`，因此同一目录中两个演示文稿的缩略图会静默地互相覆盖网格——第一个演示文稿的网格直接消失（仅用于模板分析——可视化 QA 需要 [转换为图片](#converting-to-images) 的全分辨率渲染；它只接受 `.pptx`，因此先将 `.potx` 复制为 `.pptx` 名称）。配合 `markitdown` 使用，将每个内容部分映射到模板幻灯片上，并变化布局——不要将所有部分放在同一个标题加项目符号的幻灯片上。

```bash
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" deck.pptx
python scripts/add_slide.py unpacked/ slide2.xml --after slide2.xml   # 复制幻灯片（或 slideLayoutN.xml）；打印新幻灯片的路径
# 重新排序 / 删除幻灯片 = 编辑 ppt/presentation.xml 中的 <p:sldIdLst>
python scripts/clean.py unpacked/                                     # 删除后：移除孤立的幻灯片、媒体和关系
# 在 ppt/slides/slideN.xml 中编辑幻灯片内容
(cd unpacked && rm -f ../out.pptx && zip -Xr ../out.pptx .)           # 从目录内部 zip；先 rm，否则已删除的部分会残留
python scripts/office/validate.py out.pptx --original deck.pptx
```

- **在编辑任何幻灯片内容之前完成所有结构性工作——添加、删除、重新排序。** `add_slide.py` 逐字复制幻灯片文件，因此在编辑后复制会克隆已编辑的内容；而 `clean.py` 会删除 `<p:sldIdLst>` 中缺失的任何幻灯片，包括你刚刚编写的。
- **绝不用手动方式复制幻灯片文件**——`add_slide.py` 处理新幻灯片所需的所有注册，并报告它创建了什么（`Created ppt/slides/slide17.xml from slide2.xml`）。它也可直接处理文件：`add_slide.py deck.pptx slide2.xml -o out.pptx`——**传入 `-o`，否则它会原地重写输入文件。** 复制的幻灯片仍然*引用*其源的图表/SmartArt/嵌入对象部分，而非克隆它们，因此编辑一张幻灯片上的图表会改变另一张上的。
- **如果使用 `python-pptx`**，它不能做的三件事：复制幻灯片（其唯一入口点是 `add_slide(layout)`）、通过 `text_frame.text = "..."` 保持格式（会折叠段落为单个无样式 run——应分配 `run.text`）、或读取大多数模板艺术使用的 SVG/EMF（`add_picture` 引发 `UnidentifiedImageError`）。
- 旧的 `.ppt` 必须先转换：`python scripts/office/soffice.py --headless --convert-to pptx file.ppt`。`.potx` 模板以相同方式解包和重新打包——输出时保留 `.potx` 扩展名。
- 重用模板图标或图片：复制已经包含它的幻灯片或布局。

填充模板时：

- 如果编写 XML 转换脚本，使用 `defusedxml.minidom` 解析——通过 `xml.etree.ElementTree` 往返 OOXML 会重写命名空间前缀并损坏演示文稿。
- **模板槽位 ≠ 源条目。** 如果模板显示 4 个团队成员而你只有 3 个，删除第 4 个成员的整个组（图片 + 文本框），而不仅仅是其文本——然后在 QA 中检查孤立的视觉元素。
- 每个列表项一个 `<a:p>`——绝不将多个项目连接到一个段落中。复制兄弟 `<a:pPr>` 以保持间距，并在标题、节标题和内联标签（`Status:`、`Owner:`）的 `<a:rPr>` 上放置 `b="1"`。
- 让项目符号从布局继承；仅在覆盖时添加 `<a:buChar>`、`<a:buAutoNum>`（编号）或 `<a:buNone>`——绝不在文本中使用字面 `•`。
- 带有前导或尾随空格的文本需要在其 `<a:t>` 上设置 `xml:space="preserve"`。

## 设计理念

**不要创建无聊的幻灯片。** 白色背景上的纯项目符号不会给任何人留下深刻印象。为每张幻灯片考虑以下想法。

### 开始之前

- **选择大胆的、以内容为依据的调色板**：调色板应该感觉是为这个主题设计的。如果将你的颜色换到完全不同的演示文稿中仍然"适用"，则说明你还没有做出足够具体的选择。
- **主次分明**：一种颜色应占主导地位（60-70% 的视觉权重），配合 1-2 种辅助色调和一种鲜明的强调色。绝不要让所有颜色权重相同。
- **深/浅对比**：标题和总结幻灯片使用深色背景，内容使用浅色（"三明治"结构）。或者全程深色以获得高级感。
- **确定一个视觉主题**：选择一个独特的元素并重复使用——圆角图片框、彩色圆圈中的图标。贯穿每张幻灯片。**不要使用色条或强调条纹作为主题**（见避免列表）。

### 调色板

选择与主题匹配的颜色——不要默认使用通用蓝色。以下调色板作为灵感：

| 主题 | 主色 | 辅色 | 强调色 |
|-------|---------|-----------|--------|
| **午夜行政** | `1E2761`（海军蓝） | `CADCFC`（冰蓝） | `FFFFFF`（白色） |
| **森林苔藓** | `2C5F2D`（森林绿） | `97BC62`（苔藓） | `F5F5F5`（奶油） |
| **珊瑚能量** | `F96167`（珊瑚红） | `F9E795`（金色） | `2F3C7E`（海军蓝） |
| **暖赤陶** | `B85042`（赤陶） | `E7E8D1`（沙色） | `A7BEAE`（鼠尾草） |
| **海洋渐变** | `065A82`（深海蓝） | `1C7293`（蓝绿） | `21295C`（午夜蓝） |
| **炭灰极简** | `36454F`（炭灰） | `F2F2F2`（灰白） | `212121`（黑色） |
| **蓝绿信任** | `028090`（蓝绿） | `00A896`（海沫） | `02C39A`（薄荷） |
| **浆果奶油** | `6D2E46`（浆果） | `A26769`（暗玫瑰） | `ECE2D0`（奶油） |
| **鼠尾草宁静** | `84B59F`（鼠尾草） | `69A297`（尤加利） | `50808E`（石板） |
| **樱桃大胆** | `990011`（樱桃红） | `FCF6F5`（灰白） | `2F3C7E`（海军蓝） |

### 每张幻灯片

**每张幻灯片都需要一个视觉元素**——图片、图表、图标或形状。纯文本幻灯片很容易被遗忘。

**布局选项：**
- 两栏（左侧文字，右侧插图）
- 图标 + 文字行（彩色圆圈中的图标，粗体标题，下方描述）
- 2x2 或 2x3 网格（一侧图片，另一侧内容块网格）
- 半出血图片（全左或全右）配合内容叠加

**数据展示：**
- 大号统计数字（60-72pt 的大数字，下方有小标签）
- 对比栏（前/后、优/缺、并排选项）
- 时间线或流程图（编号步骤、箭头）

**视觉润色：**
- 节标题旁边放在小彩色圆圈中的图标
- 关键统计或标语使用斜体强调文字

### 排版

**写入 .pptx 的字体名称由用户的 PowerPoint 渲染，而非此环境。** 你的可视化 QA 通过 LibreOffice 渲染，它会替换没有的字体——对于某些字体，替换字体有不同宽度，因此你的 QA 预览可能显示真实演示文稿中没有的文本溢出（或适配）。为了使 QA 可信：

- **安全字体**（在 QA 中渲染宽度可信 *且* 随 Office 一起提供）：**Arial、Calibri、Cambria、Times New Roman、Courier New、Bookman Old Style、Century Schoolbook**。正文和任何适配很重要的地方使用这些字体。
- **零 QA 风险的有个性标题**：将安全列表中的衬线标题（Cambria、Bookman Old Style、Century Schoolbook）与安全列表中的无衬线正文（Calibri 或 Arial）配对。在获得可靠的溢出检查的同时，也能获得视觉对比。
- **如果用户要求安全列表外的字体**（如 Georgia 或 Trebuchet MS）：在用户要求的地方使用，但为这些容器留出额外宽松空间（~10%），不要信任这些元素的 QA 文本适配——该字体的预览是近似的。如果用户未指定，优先使用安全列表字体作为正文。
- **QA 不可靠字体**（替换字体宽度不同——溢出检查可能出错）：Georgia、Trebuchet MS、Impact、Arial Black、Garamond、Consolas、Palatino Linotype。Calibri Light 的替换因环境而异；视为 QA 不可靠。适合具有宽松空间的标题/强调；不要信任这些字体上的 QA 文本适配。
- **绝不默认为 Aptos**——Office 2023 年后的默认字体在此环境中没有度量兼容的替代字体 *且* 在旧版 Office 安装中缺失，因此两端都不可靠。

| 元素 | 大小 |
|---------|------|
| 幻灯片标题 | 36-44pt 粗体 |
| 节标题 | 20-24pt 粗体 |
| 正文 | 14-16pt |
| 说明文字 | 10-12pt 柔和颜色 |

### 间距

- 最小 0.5 英寸边距
- 内容块之间 0.3-0.5 英寸
- 留出呼吸空间——不要填满每一寸

### 避免（常见错误）

- **不要重复相同布局**——在各幻灯片间变化栏、卡片和标注
- **正文不要居中**——段落和列表左对齐；仅标题居中
- **不要吝啬大小对比**——标题需要 36pt+ 才能与 14-16pt 正文区分
- **不要默认蓝色**——选择反映具体主题的颜色
- **不要随意混合间距**——选择 0.3 英寸或 0.5 英寸间距并一致使用
- **不要只美化一张幻灯片而让其他保持简陋**——要么全力以赴，要么全程保持简单
- **不要创建纯文本幻灯片**——添加图片、图标、图表或视觉元素；避免纯标题+项目符号
- **不要忘记文本框内边距**——当将线条或形状与文本边缘对齐时，在文本框上设置 `margin: 0` 或偏移形状以考虑内边距
- **不要使用低对比度元素**——图标和文本都需要与背景有强烈对比；避免浅色文本在浅色背景上或深色文本在深色背景上
- **绝不在标题下使用强调线**——这是 AI 生成幻灯片的标志；改用留白或背景色
- **绝不添加装饰性色条或强调条纹**——包括：跨幻灯片宽度的页眉/页脚条、幻灯片一侧边缘的垂直侧边栏条纹、卡片或内容块边缘的细强调条纹以及矩形上的"单侧边框"。这些读起来像是 AI 生成的填充内容。如果想突出卡片，使用微妙的背景色、投影或图标——而非边缘条纹。
- **不要默认奶油/米色背景**——当没有指定背景时，使用白色（`FFFFFF`）或用户的品牌调色板；避免暖中性默认值如 `F5F5DC`、`FAF0E6`、`FAEBD7`、`FFF8E1`
- **不要提交超出其形状的文本**——如果文本放不下，减小字号、拆分到多张幻灯片或扩大容器；绝不要让内容被裁切或溢出边界

## QA（必需）

第一次渲染通常会有一些真实问题——重叠、溢出、未对齐。找出并修复这些问题，仅重新渲染更改过的幻灯片，然后停止。

### 内容 QA

```bash
markitdown output.pptx
```

检查缺失内容、拼写错误、顺序错误。

**使用模板时，检查残留占位文本：**

```bash
markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

如果 grep 返回结果，在声明成功之前修复它们。

### 文件 QA（必需）

```bash
python scripts/office/validate.py output.pptx                      # 从零构建
python scripts/office/validate.py output.pptx --original src.pptx  # 从模板构建
```

**如果演示文稿来自模板，始终传入 `--original`。** 模板本身可能包含 XSD 拒绝的部分，因此单独运行时可能报告你从未造成的失败——而真正的回归可能隐藏其中。`--original` 基于模板对 schema 和幻灯片检查进行基准校验，抑制其已有的错误。结构性检查——关系、内容类型、图表——忽略 `--original`，无论哪种方式都会报告模板继承的问题，因此根据其自身情况阅读这些。

pptxgenjs 发出的图表 XML PowerPoint 拒绝打开，而其他所有工具都接受：python-pptx 能打开这些演示文稿，LibreOffice 能渲染它们，XSD 也能通过。每个失败都指明其修复方法。在生成器中修复并重新构建。

### 可视化 QA

将幻灯片转换为图片（见 [转换为图片](#converting-to-images)）并检查每一张。长时间盯着生成代码后，你倾向于看到预期的内容而非实际渲染的内容，因此以全新的视角查看图片（如果有子代理，这很有效）。需要注意的用户可见缺陷：

- **文本溢出或文本在框或幻灯片边界处被截断——首先检查此项。** 这是最常见的缺陷，且始终用户可见。（对于预览器渲染不可靠的字体，根据排版说明，预览是近似的：信任你留下的 ~10% 宽松空间，而非其表面上的适配情况。）
- 重叠元素（文本穿过形状、线条穿过文字、堆叠的元素）
- 来源引用或页脚与上方内容冲突
- 元素过近（< 0.3 英寸间距）或卡片/部分几乎接触
- 不均匀的间距（一处大面积空白，另一处拥挤）
- 距幻灯片边缘边距不足（< 0.5 英寸）
- 列或类似元素未一致对齐
- 低对比度文本（例如，奶油色背景上的浅灰色文本）
- 模板装饰在文本替换后位置错误——例如，标题下划线定位为一行，但替换后的标题换行成了两行
- 低对比度图标（例如，深色图标在深色背景上缺少对比圆圈）
- 文本框过窄导致过度换行
- 残留的占位内容

## 转换为图片

将演示文稿转换为单页幻灯片图片以进行视觉检查：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

**将上面打印的绝对路径直接传入查看工具。** `rm` 清除先前运行的过时图片。`pdftoppm` 根据总页数进行零填充：10 页以下为 `slide-1.jpg`，10-99 页为 `slide-01.jpg`，100 页以上为 `slide-001.jpg`。

**修复后，重新运行以上四个命令**——PDF 必须从编辑后的 `.pptx` 重新生成，`pdftoppm` 才能反映更改。

## 依赖

`pptxgenjs`（npm，已预装——仅当 `require('pptxgenjs')` 失败时才安装）· `markitdown[pptx]`、`Pillow`、`defusedxml`、`lxml`（pip——文本转储、缩略图、清理、验证）· LibreOffice（`soffice`，通过 `scripts/office/soffice.py` 自动配置为沙盒环境）· `pdftoppm`（Poppler）
