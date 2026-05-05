---
name: infographic
description: |
  SVG 信息图、架构图、流程图生成器。Use when 用户想“画流程图/架构图/系统图/信息图/示意图”，需要把系统、流程、概念、对比方案可视化，或要求生成特定视觉风格的 SVG 图。即使用户没有明确说 SVG，只要目标是结构化可视化，都应使用此 skill。先选择图表类型，再选择视觉风格，读取对应 reference，最后产出可直接保存/渲染的完整 SVG。
---

# SVG Infographic Generator

## Overview

这个 skill 用于把文字描述转成 **可直接渲染的 SVG 信息图**。图的设计由两个独立维度组成：

```text
图表类型(type) = 布局结构 / 信息组织方式
视觉风格(style) = 颜色、字体、线条、箭头、质感
```

先选 type，再选 style。不要凭感觉随手画；必须先根据用户意图选择最合适的布局，再套用风格规范。

---

## Activation Triggers

使用本 skill 当用户说：

- “画个图说明……”、“生成架构图”、“画流程图/系统图/示意图”
- “把这个流程可视化”、“帮我做一张信息图”
- “用 SVG 画”、“输出 SVG”
- “做一个对比图”、“展示多个模式/方案”
- “Anthropic 风格 / 暗色风格 / 官方文档风格”

不要用于：

- 只需要文字总结、不需要图形的任务
- 需要真实图片/插画而非信息结构图的任务；这种应使用 image generation 或设计类 skill

---

## Workflow

### Phase 1: Clarify the Diagram Goal

快速判断用户到底想表达什么：

| 目标 | 关注点 | 常见图型 |
|---|---|---|
| 阶段推进 | 步骤、生命周期、流水线 | `layered-flow` |
| 系统架构 | 组件、层级、依赖 | `column-layer`, `nested-layer` |
| 多方交互 | actor、消息、协议 | `swimlane` |
| 方案对比 | A vs B、多模式权衡 | `side-by-side`, `pattern-grid` |
| 概念解释 | 核心概念和关系 | 选择最接近的信息结构 |

如果信息不足，问一个问题即可：

```text
你希望这张图主要表达：流程推进、系统架构、多方交互，还是方案对比？
```

### Phase 2: Select Chart Type

| Type | Use when | Reference |
|---|---|---|
| `layered-flow` | 垂直分层流程；单条主线、阶段递进 | `types/layered-flow.md` |
| `column-layer` | 水平多列架构；系统层/组件并排 | `types/column-layer.md` |
| `swimlane` | 多个参与者横向泳道，消息在泳道间流动 | `types/swimlane.md` |
| `pattern-grid` | 三个及以上方案/模式并列对比 | `types/pattern-grid.md` |
| `side-by-side` | 两个方案/状态左右对比 | `types/side-by-side.md` |
| `nested-layer` | 横向大层内嵌子模块，上下层数据流 | `types/nested-layer.md` |

选择规则：

- “流程 / 阶段 / pipeline / lifecycle” → `layered-flow`
- “系统 / 架构 / 组件 / 层” → `column-layer`
- “协议 / 多方 / 请求响应 / agent 协作” → `swimlane`
- “A vs B / 旧 vs 新” → `side-by-side`
- “多种方案 / 多模式 / pattern” → `pattern-grid`
- “分层架构 + 每层包含子模块” → `nested-layer`

### Phase 3: Select Visual Style

默认风格：

| Style | Description | Reference |
|---|---|---|
| `anthropic-flat` | Anthropic/Claude 文档风格；低饱和度色块、细边框、无阴影 | `styles/anthropic-flat.md` |

如果用户指定风格但 reference 不存在，先用最接近的现有风格，并说明可以新增 style reference。

### Phase 4: Read References Before Drawing

生成 SVG 前必须读取：

1. 选定 type 的 `types/<type>.md`
2. 选定 style 的 `styles/<style>.md`
3. 如有相近 example，读取 `examples/*.svg` 作为布局参考

不要在没读 reference 的情况下自由发挥坐标系统。

### Phase 5: Generate SVG

输出要求：

- 生成完整 `<svg ...>...</svg>`，不要省略 defs/style。
- 坐标、尺寸、颜色、箭头、字体必须自洽。
- 每个文本块要考虑换行和可读性，避免文字溢出。
- 优先使用 `<text>` + `<tspan>`，必要时用 `<foreignObject>` 但要注意兼容性。
- 箭头必须有 `marker-end`，并避免穿过节点主体。
- 信息密度要适中：图不是全文复制，而是结构化表达。

如果平台支持附件，写入 `.svg` 文件并在回复里给路径；否则直接输出 SVG 代码块。

---

## Output Format

默认回复：

```text
已生成 SVG：<path 或代码块>
类型：<type>
风格：<style>
```

如果用户只想复制代码，直接给：

```svg
<svg ...>
...
</svg>
```

---

## Quality Checklist

交付前检查：

- [ ] 是否选择了明确的 type 和 style？
- [ ] 是否读取了对应 `types/` 和 `styles/` reference？
- [ ] SVG 是否完整、可渲染、无未闭合标签？
- [ ] 文本是否不会明显溢出？
- [ ] 箭头是否表达正确方向且不遮挡主体？
- [ ] 图中信息是否经过筛选，而不是堆满原文？
- [ ] 是否按用户要求保存或直接输出？

---

## Extending This Skill

新增图表类型：

1. 在 `types/<new-type>.md` 写布局规范；
2. 增加至少一个 `examples/<new-type>-<style>.svg`；
3. 在本文件 type 表登记。

新增视觉风格：

1. 在 `styles/<new-style>.md` 写颜色、字体、边框、箭头规范；
2. 增加示例图；
3. 在 style 表登记。
