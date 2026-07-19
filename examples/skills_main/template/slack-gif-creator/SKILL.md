---
name: slack-gif-creator
description: 创建针对 Slack 优化的动画 GIF 的知识和工具。提供约束条件、验证工具和动画概念。当用户请求为 Slack 创建动画 GIF 时使用，如"给我做一个 X 做 Y 的 GIF，用于 Slack"。
license: Complete terms in LICENSE.txt
---

# Slack GIF 创建器

一个提供工具和知识，用于创建针对 Slack 优化的动画 GIF 的工具包。

## Slack 要求

**尺寸：**
- 表情 GIF：128x128（推荐）
- 消息 GIF：480x480

**参数：**
- FPS：10-30（越低文件越小）
- 颜色数：48-128（越少文件越小）
- 时长：表情 GIF 控制在 3 秒以内

## 核心工作流

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建构建器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成帧
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # 使用 PIL 图元绘制你的动画
    # （圆形、多边形、线条等）

    builder.add_frame(frame)

# 3. 保存并优化
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 处理用户上传的图片
如果用户上传了一张图片，考虑他们是否想：
- **直接使用**（例如，"把这个做成动画"、"把这个分割成帧"）
- **作为灵感**（例如，"做一个像这样的"）

使用 PIL 加载和处理图片：
```python
from PIL import Image

uploaded = Image.open('file.png')
# 直接使用，或仅作为颜色/风格的参考
```

### 从零开始绘制
从零开始绘制图形时，使用 PIL ImageDraw 图元：

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# 圆形/椭圆
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 星形、三角形、任意多边形
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 线条
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 矩形
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**不要使用：** Emoji 字体（跨平台不可靠）或假设此技能中包含预打包的图形。

### 让图形看起来美观

图形应该看起来精致而有创意，而不是基础简陋。以下方法：

**使用更粗的线条** - 始终为轮廓和线条设置 `width=2` 或更高。细线条（width=1）看起来粗糙而业余。

**增加视觉深度**：
- 使用渐变背景（`create_gradient_background`）
- 叠加多层形状以增加复杂度（例如，一个大星里面套一个小星）

**让形状更有趣**：
- 不要只画一个普通的圆——添加高光、环或图案
- 星形可以有发光效果（在后面画更大、半透明的版本）
- 组合多种形状（星星 + 闪光、圆形 + 环形）

**注意颜色**：
- 使用鲜艳、互补的颜色
- 增加对比度（浅色形状上的深色轮廓，深色形状上的浅色轮廓）
- 考虑整体构图

**对于复杂形状**（心形、雪花等）：
- 使用多边形和椭圆的组合
- 仔细计算对称点的位置
- 添加细节（心形可以有高光曲线，雪花有复杂的分支）

要有创意和细节！一个好的 Slack GIF 应该看起来精致，而不是像占位图形。

## 可用工具

### GIFBuilder（`core.gif_builder`）
组装帧并针对 Slack 优化：
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # 添加 PIL Image
builder.add_frames(frames)  # 添加帧列表
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### 验证器（`core.validators`）
检查 GIF 是否满足 Slack 要求：
```python
from core.validators import validate_gif, is_slack_ready

# 详细验证
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# 快速检查
if is_slack_ready('my.gif'):
    print("已就绪！")
```

### 缓动函数（`core.easing`）
平滑运动而非线性：
```python
from core.easing import interpolate

# 进度从 0.0 到 1.0
t = i / (num_frames - 1)

# 应用缓动
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# 可用：linear, ease_in, ease_out, ease_in_out,
#       bounce_out, elastic_out, back_out
```

### 帧辅助函数（`core.frame_composer`）
常见需求的便捷函数：
```python
from core.frame_composer import (
    create_blank_frame,         # 纯色背景
    create_gradient_background,  # 垂直渐变
    draw_circle,                # 圆形辅助函数
    draw_text,                  # 简单文本渲染
    draw_star                   # 五角星
)
```

## 动画概念

### 摇晃/振动
用振荡偏移对象位置：
- 使用 `math.sin()` 或 `math.cos()` 与帧索引结合
- 添加小幅随机变化以获得自然感
- 应用于 x 和/或 y 位置

### 脉冲/心跳
节奏性地缩放对象大小：
- 使用 `math.sin(t * frequency * 2 * math.pi)` 获得平滑脉动
- 心跳：两次快速脉冲后暂停（调整正弦波）
- 在基础大小的 0.8 到 1.2 之间缩放

### 弹跳
物体下落并弹起：
- 使用 `interpolate()` 并设置 `easing='bounce_out'` 表示着陆
- 使用 `easing='ease_in'` 表示下落（加速）
- 通过每帧增加 y 速度来应用重力

### 旋转/转动
围绕中心旋转对象：
- PIL：`image.rotate(angle, resample=Image.BICUBIC)`
- 摇摆：使用正弦波代替线性角度

### 淡入/淡出
逐渐出现或消失：
- 创建 RGBA 图像，调整 alpha 通道
- 或使用 `Image.blend(image1, image2, alpha)`
- 淡入：alpha 从 0 到 1
- 淡出：alpha 从 1 到 0

### 滑动
将对象从屏幕外移动到目标位置：
- 起始位置：帧边界外
- 结束位置：目标位置
- 使用 `interpolate()` 并设置 `easing='ease_out'` 获得平滑停止
- 过冲：使用 `easing='back_out'`

### 缩放
缩放和位置实现缩放效果：
- 放大：从 0.1 缩放到 2.0，裁剪中心
- 缩小：从 2.0 缩放到 1.0
- 可添加运动模糊增加戏剧性（PIL 滤镜）

### 爆炸/粒子爆发
创建向外辐射的粒子：
- 生成具有随机角度和速度的粒子
- 更新每个粒子：`x += vx`、`y += vy`
- 添加重力：`vy += gravity_constant`
- 随时间淡出粒子（减小 alpha）

## 优化策略

仅在需要减小文件大小时，实施以下方法中的几种：

1. **减少帧数** - 降低 FPS（10 而不是 20）或缩短时长
2. **减少颜色数** - `num_colors=48` 而不是 128
3. **缩小尺寸** - 128x128 而不是 480x480
4. **移除重复** - `remove_duplicates=True` 在 save() 中
5. **表情模式** - `optimize_for_emoji=True` 自动优化

```python
# 表情的最大优化
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 理念

此技能提供：
- **知识**：Slack 的要求和动画概念
- **工具**：GIFBuilder、验证器、缓动函数
- **灵活性**：使用 PIL 图元创建动画逻辑

不提供：
- 僵化的动画模板或预制函数
- Emoji 字体渲染（跨平台不可靠）
- 内置于技能中的预打包图形库

**关于用户上传的注意**：此技能不包含预构建的图形，但如果用户上传了图片，使用 PIL 加载和处理——根据他们的请求判断是直接使用还是仅作为灵感。

发挥创意！组合概念（弹跳 + 旋转，脉冲 + 滑动等），充分利用 PIL 的功能。

## 依赖

```bash
pip install pillow imageio numpy
```
