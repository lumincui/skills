---
name: infographic
description: |
  绘制 Anthropic/Claude 官方文档风格的 SVG 信息图与架构流程图。

  当用户提到以下任何场景时，务必使用此 skill：
  - 画流程图、架构图、系统图、信息图
  - 用 SVG 绘制图表、可视化某个流程或概念
  - "帮我画一张图说明……"、"生成一张架构图"、"画个示意图"
  - 想要 Anthropic / Claude 文档风格的插图
  - 将文字描述的系统或流程可视化为图表

  即使用户没有明确说"SVG"或"Anthropic 风格"，只要涉及流程/架构/信息的可视化，都应使用此 skill。
---

# Anthropic 风格 SVG 信息图

## 风格定义

参照 Anthropic / Claude 官方技术文档插图的视觉语言，特征如下：

| 属性 | 规范 |
|------|------|
| 字体 | `"Anthropic Sans", -apple-system, "system-ui", "Segoe UI", sans-serif` |
| 风格 | Flat，无阴影，无渐变 |
| 边框 | `stroke-width: 0.5`，细而克制 |
| 填充 | 低饱和度色块，透明度分层 |
| 箭头 | 自定义 marker，`stroke-linecap: round` |

---

## 配色系统

每个主题区块用一套色调统一内部所有元素：

### 紫色区块（Session 1 / 初始化 / 输入层）
```
背景填充:  rgb(238, 237, 254)   #EEEDFE
边框:      rgb(83, 74, 183)     #534AB7
标题文字:  rgb(60, 52, 137)     #3C3489
正文文字:  rgb(83, 74, 183)     #534AB7
箭头:      #534AB7
```

### 绿色区块（Session 2…N / 执行循环 / 处理层）
```
背景填充:  rgb(225, 245, 238)   #E1F5EE
边框:      rgb(15, 110, 86)     #0F6E56
标题文字:  rgb(8, 80, 65)       #085041
正文文字:  rgb(15, 110, 86)     #0F6E56
循环箭头:  rgb(29, 158, 117)    #1D9E75
```

### 中性辅助（连接线、注释、虚线框）
```
连接箭头:  rgba(31, 30, 29, 0.3)
虚线框边:  rgba(31, 30, 29, 0.15–0.3)
注释文字:  opacity: 0.4–0.55, fill: rgb(61, 61, 58)
正文深色:  rgb(20, 20, 19)
```

---

## SVG 结构模板

```xml
<svg width="100%" viewBox="0 0 720 [HEIGHT]" xmlns="http://www.w3.org/2000/svg">
<defs>
  <!-- 箭头 marker，context-stroke 自动继承线条颜色 -->
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>

<!-- 每个逻辑层：标签 + 大矩形容器 + 内部卡片 + 连接箭头 -->
</svg>
```

**viewBox 高度建议**：按层数 × 约 120–160px 估算，留顶部 30px + 底部 60px 边距。

---

## 元素规范

### 容器矩形（区块）
```xml
<rect x="40" y="34" width="600" height="110" rx="10"
      stroke-width="0.5"
      style="fill:rgb(238,237,254); stroke:rgb(83,74,183)"/>
```
- 外层容器：`rx="10"`，`width="600"`，左右各留 40px 边距
- 内部卡片：`rx="6"`，按内容自适应宽高

### 区块标题
```xml
<text x="340" y="56" text-anchor="middle" dominant-baseline="central"
      style="fill:rgb(60,52,137); font-size:14px; font-weight:500">
  区块名称
</text>
```

### 内部卡片文字（双行）
```xml
<!-- 第一行：文件名/标题，font-size:11px font-weight:500 -->
<text x="125" y="86" text-anchor="middle" dominant-baseline="central"
      style="font-size:11px; fill:rgb(60,52,137); font-weight:500">
  filename.json
</text>
<!-- 第二行起：说明，font-size:12px font-weight:400 -->
<text x="125" y="102" text-anchor="middle" dominant-baseline="central"
      style="fill:rgb(83,74,183); font-size:12px">
  描述文字
</text>
```

### 区块间连接箭头（垂直）
```xml
<line x1="340" y1="[底部Y]" x2="340" y2="[顶部Y+偏移]"
      stroke="#534AB7" stroke-width="1.5"
      marker-end="url(#arrow)" fill="none"/>
```

### 步骤间水平箭头
```xml
<line x1="[box右边]" y1="[中心Y]" x2="[下一box左边]" y2="[中心Y]"
      stroke="#0F6E56" stroke-width="1"
      marker-end="url(#arrow)" fill="none"/>
```

### 虚线注释框
```xml
<!-- 较重虚线（filesystem 层） -->
<rect x="200" y="168" width="280" height="28" rx="6"
      fill="none" stroke="rgba(31,30,29,0.3)"
      stroke-width="0.5" stroke-dasharray="4 3"/>

<!-- 较轻虚线（内部说明） -->
<rect x="56" y="322" width="568" height="28" rx="6"
      fill="none" stroke="rgba(31,30,29,0.15)"
      stroke-width="0.5" stroke-dasharray="3 3"/>
```

### 循环回路箭头（右侧折线）
```xml
<!-- 从底部引出 → 右转 → 向上 → 左转回到顶部 -->
<line x1="640" y1="302" x2="660" y2="302" stroke="#1D9E75" stroke-width="1" fill="none"/>
<line x1="660" y1="302" x2="660" y2="214" stroke="#1D9E75" stroke-width="1" fill="none"/>
<line x1="660" y1="214" x2="640" y2="214" stroke="#1D9E75" stroke-width="1"
      marker-end="url(#arrow)" fill="none"/>
<!-- 旁边配小标签 -->
<text x="670" y="258" text-anchor="start" dominant-baseline="central"
      style="fill:#0F6E56; font-size:10px">next</text>
```

### 区块标注（左上角小字）
```xml
<text x="60" y="22" text-anchor="start" dominant-baseline="central"
      style="opacity:0.4; fill:rgb(61,61,58); font-size:12px">
  Session 1 · runs once
</text>
```

---

## 布局节奏

```
顶部留白      30px
区块标注文字  约 12px 高
区块容器      高度由内容决定（单行卡片约 110px，多步骤约 200px）
区块间距      约 24–30px（含中间的 filesystem/连接层）
底部结果框    36px 高
底部留白      24px
```

内部卡片横向排列时，建议等宽或按内容比例分配，卡片间距 ≥ 10px。

---

## 完整示例参考

以下是一个双层（初始化 → 执行循环）架构图的典型骨架：

```
[区块标注] Session 1 · runs once
[紫色容器]
  [卡片1] feature-list.json   [卡片2] init.sh   [卡片3] git commit   [卡片4] progress.txt
[↓ 箭头]
[虚线框] filesystem persisted · git committed
[↓ 箭头]
[区块标注] Session 2…N · restartable
[绿色容器]
  [步骤1→步骤2→步骤3→步骤4→步骤5] 水平流程
  [虚线框] 崩溃恢复说明
  [信息框] 状态传递机制说明
[循环箭头（右侧）]
[↓ 箭头]
[底部结果框] 完成状态
```

---

## 生成流程

1. **理解内容**：拆解用户描述的系统/流程，识别层次结构（几层、每层几个节点）
2. **规划布局**：确定 viewBox 高度，分配各层 Y 坐标
3. **选择配色**：按语义角色分配紫色/绿色/中性色
4. **编写 SVG**：从上到下逐层输出，先容器后内容后箭头
5. **检查对齐**：文字 `text-anchor="middle"` + `dominant-baseline="central"` 确保居中

输出时直接给出完整可用的 SVG 代码，不需要额外说明。
