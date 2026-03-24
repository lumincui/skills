# Type: Nested Layer

水平分层架构图，每层内部有独立的子区块嵌套，层与层之间有纵向箭头流转。左侧可附加一个纵向管控面板（side panel）。

适用场景：系统具有清晰的水平分层（如"应用层 → 生产层 → 数据层"），每层内部有多个并列或嵌套的功能模块，需要同时展示层级关系与内部结构。

---

## Canvas

```
viewBox="0 0 [W] [H]"
```

- 有左侧面板时：`W = 900`，面板宽约 80px，主体从 x=100 开始
- 无左侧面板时：`W = 800`
- 层数 3：`H ≈ 560`；层数 4：`H ≈ 720`

---

## Structure

```
┌─────────┬──────────────────────────────────────────────────────┐
│         │  应用层（顶层）                                        │
│         │  ┌──────────────────┐  ┌───────────────────────────┐ │
│ 管控    │  │  区块 A          │  │  区块 B                   │ │
│ 面板    │  │  ┌──┐ ┌──┐ ┌──┐ │  │  ┌────┐  ┌────────────┐  │ │
│（可选）  │  │  └──┘ └──┘ └──┘ │  │  └────┘  └────────────┘  │ │
│         │  └──────────────────┘  └───────────────────────────┘ │
│         ├──────────────────────────────────────────────────────┤
│         │  生产层（中层）                                        │
│         │  ┌─────────────────────────┐  ┌───────────────────┐  │
│         │  │ 子区块（横向流程步骤） │  │ 子区块（列表型） │  │
│         │  └─────────────────────────┘  └───────────────────┘  │
│         ├──────────────────────────────────────────────────────┤
│         │  源数据层（底层）                                      │
│         │  ┌──────┐  ┌──────────┐  ┌──────────┐              │
│         │  └──────┘  └──────────┘  └──────────┘              │
└─────────┴──────────────────────────────────────────────────────┘
```

---

## Side Panel（左侧管控面板）

纵向矩形，宽 72px，与主体等高，圆角 12：

```svg
<rect x="24" y="24" width="72" height="[mainH]" rx="12"
      fill="[green.fill]" stroke="[green.border]" stroke-width="0.5"/>
<text x="60" y="44" font-size="14" font-weight="500"
      fill="[green.text]" text-anchor="middle" dominant-baseline="central">
  管数
</text>
<text x="60" y="62" font-size="11" font-weight="400"
      fill="[green.text]" opacity="0.6" text-anchor="middle" dominant-baseline="central">
  数据运维保障
</text>
```

面板内的图标/条目纵向堆叠，每项间距 60px，从 y=90 开始：

```svg
<!-- 图标区 + 文字，每组高约 48px -->
<circle cx="60" cy="[item_y]" r="14"
        fill="white" stroke="[green.border]" stroke-width="0.5" opacity="0.7"/>
<!-- icon placeholder -->
<text x="60" y="[item_y + 22]" font-size="10" font-weight="400"
      fill="[green.text]" text-anchor="middle" dominant-baseline="central" opacity="0.8">
  标签
</text>
```

---

## Layer Container（横向分层容器）

每层是一个大圆角矩形，左起 x=112（有面板）或 x=24（无面板），右至画布右边留 24px 边距：

```svg
<rect x="112" y="[layer_y]" width="[W - 136]" height="[layer_h]" rx="12"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<!-- 层标题，左上角 -->
<text x="136" y="[layer_y + 24]" font-size="16" font-weight="600"
      fill="[color.text]" dominant-baseline="central">
  层名称
</text>
<text x="136" y="[layer_y + 44]" font-size="11" font-weight="400"
      fill="[color.text]" opacity="0.55" dominant-baseline="central">
  副标题
</text>
```

层颜色按职责分配：
| 层职责 | 颜色 |
|--------|------|
| 应用/展示层 | 绿 |
| 生产/处理层 | 绿（稍浅）或沙 |
| 数据/基础层 | 紫 |
| 管控面板 | 绿 |

若多层使用同色系，用 opacity 差异（0.5 vs 1.0）或边框颜色深浅区分。

---

## Sub-Block（层内子区块）

子区块是层内的二级容器，白色或颜色底，实线边框：

```svg
<rect x="[bx]" y="[by]" width="[bw]" height="[bh]" rx="10"
      fill="white" stroke="[color.border]" stroke-width="0.5" opacity="0.85"/>
<text x="[bx + 16]" y="[by + 22]" font-size="13" font-weight="500"
      fill="[color.text]" dominant-baseline="central">
  子区块标题
</text>
```

子区块内再嵌套卡片（Mini Card）：

```svg
<!-- Mini Card：小圆角矩形，宽 80–120px，高 28–32px -->
<rect x="[mx]" y="[my]" width="[mw]" height="28" rx="6"
      fill="[accent.fill]" stroke="[accent.border]" stroke-width="0.5"/>
<text x="[mx + mw/2]" y="[my + 14]" font-size="11" font-weight="400"
      fill="[accent.text]" text-anchor="middle" dominant-baseline="central">
  卡片文字
</text>
```

---

## 流程箭头（子区块内横向）

子区块内部的横向流程步骤之间用实线箭头连接：

```svg
<line x1="[card_right + 4]" y1="[card_cy]" x2="[next_card_left - 4]" y2="[card_cy]"
      stroke="[color.border]" stroke-width="1"
      marker-end="url(#arrow)"/>
```

---

## 层间垂直箭头

层与层之间的数据流用垂直箭头，居中或沿主要数据流方向放置：

实线（主流向，向上/向下）：
```svg
<line x1="[ax]" y1="[upper_layer_bottom]" x2="[ax]" y2="[lower_layer_top]"
      stroke="rgba(31,30,29,0.4)" stroke-width="1"
      marker-end="url(#arrow)"/>
```

虚线（返回流/数据回流）：
```svg
<line x1="[ax + 10]" y1="[lower_layer_top]" x2="[ax + 10]" y2="[upper_layer_bottom]"
      stroke="rgba(31,30,29,0.25)" stroke-width="0.8" stroke-dasharray="4 3"
      marker-end="url(#arrow)"/>
```

---

## Layout Reference（三层 + 面板示例）

画布：`viewBox="0 0 900 560"`

| 元素 | x | y | width | height |
|------|---|---|-------|--------|
| Side panel | 24 | 24 | 72 | 512 |
| Layer 1（应用层） | 112 | 24 | 764 | 160 |
| Layer 2（生产层） | 112 | 204 | 764 | 224 |
| Layer 3（源数据层） | 112 | 448 | 764 | 88 |
| 层间间距 | — | — | — | 20 |

Layer 内 sub-block 横向并排，间距 16px，距层边距 16px（上）/ 12px（左右）。

---

## Generation Steps

1. 确定层数与每层内部的子区块数量 → 计算 `H`
2. 是否需要左侧 side panel → 决定主体起始 x
3. 从上到下绘制各层容器，分配颜色
4. 在每层内横向排列子区块，子区块内纵向或横向填充 mini card
5. 在层内子区块间绘制横向流程箭头（如有流程序列）
6. 在层与层之间绘制垂直连接箭头
7. 绘制 side panel，填入图标与标签条目
8. 应用 anthropic-flat 风格的颜色、字体、箭头 marker
