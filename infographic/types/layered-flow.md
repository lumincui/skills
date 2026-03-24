# 图表类型：layered-flow（垂直分层流程）

垂直堆叠的分层流程图。每一层代表一个阶段/角色，层内可有多个横向排列的卡片，层间用箭头连接。适合表达"初始化 → 执行循环 → 结果"这类有明确阶段递进的流程。

---

## 画布

```
viewBox="0 0 680 [HEIGHT]"
HEIGHT 估算：顶部留白 30px + 各层高度之和 + 层间距（约 30px/间隔）+ 底部留白 30px
单行卡片层约 110px，多步骤层约 160–220px
```

---

## 结构组成

```
[可选：层标注小字]   "Session 1 · runs once"   opacity:0.4, 12px
[层容器]             大圆角矩形，宽约 600px，左右各留 40px 边距
  [卡片 1] [卡片 2] [卡片 3] …   横向排列，等宽或按内容比例
[↓ 连接箭头]
[可选：filesystem / 说明虚线框]
[↓ 连接箭头]
[层标注] + [下一层容器]
  [步骤 1 → 步骤 2 → 步骤 3 → …]  水平流程
[循环箭头（右侧折线）]
[↓ 连接箭头]
[底部结果框]
```

---

## 元素规范

### 层容器
```xml
<rect x="40" y="[Y]" width="600" height="[H]" rx="10"
      fill="[accent.fill]" stroke="[accent.stroke]" stroke-width="0.5"/>
```
- 宽固定 600（左右各留 40px margin）
- 高由内容决定；单行卡片约 110px，多步骤约 160–220px

### 层标题（容器内顶部）
```xml
<text x="340" y="[Y+18]" text-anchor="middle" dominant-baseline="central"
      fill="[accent.text-dark]" font-size="14" font-weight="500">
  层名称
</text>
```

### 内部卡片（横向排列）
```xml
<rect x="[X]" y="[Y]" width="[W]" height="[H]" rx="6"
      fill="[accent.fill]" stroke="[accent.stroke]" stroke-width="0.5"/>
<!-- 主标题行 -->
<text x="[cx]" y="[ty1]" text-anchor="middle" dominant-baseline="central"
      fill="[accent.text-dark]" font-size="11" font-weight="500">标题</text>
<!-- 副标题行 -->
<text x="[cx]" y="[ty2]" text-anchor="middle" dominant-baseline="central"
      fill="[accent.text-light]" font-size="12">说明</text>
```
- 卡片间距 ≥ 10px
- 单行卡片高约 28–36px；双行卡片高约 52–60px

### 层间垂直连接箭头
```xml
<line x1="340" y1="[层底Y]" x2="340" y2="[下层顶Y]"
      stroke="[accent.stroke]" stroke-width="1.5"
      marker-end="url(#arrow)" fill="none"/>
```

### 层内水平步骤箭头
```xml
<line x1="[卡片右边X]" y1="[中心Y]" x2="[下一卡片左边X]" y2="[中心Y]"
      stroke="[accent.stroke]" stroke-width="1"
      marker-end="url(#arrow)" fill="none"/>
```

### 虚线说明框（filesystem / 补充说明）
```xml
<!-- 较重（secondary） -->
<rect x="200" y="[Y]" width="280" height="28" rx="6"
      fill="none" stroke="rgba(31,30,29,0.3)"
      stroke-width="0.5" stroke-dasharray="4 3"/>
<!-- 较轻（tertiary） -->
<rect x="56" y="[Y]" width="568" height="28" rx="6"
      fill="none" stroke="rgba(31,30,29,0.15)"
      stroke-width="0.5" stroke-dasharray="3 3"/>
```

### 循环回路箭头（右侧折线）
从当前层底部右侧引出 → 向右偏移 → 向上 → 折回进入目标层右侧：
```xml
<line x1="640" y1="[底部Y]" x2="660" y2="[底部Y]"
      stroke="[loop-arrow色]" stroke-width="1" fill="none"/>
<line x1="660" y1="[底部Y]" x2="660" y2="[顶部Y]"
      stroke="[loop-arrow色]" stroke-width="1" fill="none"/>
<line x1="660" y1="[顶部Y]" x2="640" y2="[顶部Y]"
      stroke="[loop-arrow色]" stroke-width="1"
      marker-end="url(#arrow)" fill="none"/>
<text x="670" y="[中间Y]" text-anchor="start" dominant-baseline="central"
      fill="[accent.stroke]" font-size="10">next</text>
```

### 层标注小字（层容器外左上角）
```xml
<text x="60" y="[层顶Y - 10]" text-anchor="start" dominant-baseline="central"
      fill="rgb(61,61,58)" font-size="12" opacity="0.4">
  Session 1 · runs once
</text>
```

### 底部结果框
```xml
<rect x="40" y="[Y]" width="600" height="36" rx="8"
      fill="[accent.fill]" stroke="[accent.stroke]" stroke-width="0.5"/>
<text x="340" y="[Y+18]" text-anchor="middle" dominant-baseline="central"
      fill="[accent.text-dark]" font-size="14" font-weight="500">
  完成状态
</text>
```

---

## 颜色分配建议

- **初始化/输入层** → 紫色
- **执行循环层** → 绿色（循环箭头用 `loop-arrow: #1D9E75`）
- **结果/输出层** → 紫色或中性沙色
- **filesystem/连接层** → 中性连接线色（`rgba(31,30,29,0.3)`）

---

## 布局节奏参考

```
y=0   顶部
y=12  层标注小字
y=28  第一层容器顶部
      层容器高度 ≈ 上下各 14px padding + 内容高度
      层间距 ≈ 30px（含连接层/箭头）
      底部结果框高 36px
y=[H-30] 底部留白
```

---

## 生成步骤

1. 拆解层数与每层节点数
2. 估算各层高度 → 计算 viewBox HEIGHT
3. 从上到下：层标注 → 容器矩形 → 内部卡片/步骤 → 层间箭头
4. 最后加循环箭头和底部结果框
