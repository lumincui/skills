# 视觉风格：anthropic-flat

Anthropic 技术文档的视觉语言。核心原则：**用结构说话，不用装饰**。

---

## 设计哲学

**克制即清晰。** 这套风格拒绝所有视觉噪声——无阴影、无渐变、无描边粗细变化炫技。每一个视觉决策都服务于信息层级，而非美观本身。

**颜色承载语义，不承载情绪。** 紫色表示调度方，绿色表示执行方，琥珀色表示消息/总线，红橙色表示外部系统或危险，沙色表示共享基础层。相同的角色在任何图中都用相同的颜色，不因布局变化。

**密度通过空间压缩实现，不通过字号缩小。** 主标题保持 14px，辅助信息用低 opacity（0.38–0.55）退入背景，而不是缩小字号直到不可读。

**边界即层级。** 容器的边框（`stroke-width 0.5`）远细于流程箭头线（`1–1.2`），因此视觉上容器是背景，流程才是主角。

---

## 颜色系统

每个语义角色对应一套三色组（浅底色 / 边框 / 深色文字），低饱和度，可叠加不冲突。

| 角色 | 语义 | fill | stroke | text |
|------|------|------|--------|------|
| 紫 | 调度方、Orchestrator、输入层 | `#EEEDFE` | `#534AB7` | `#3C3489` |
| 绿 | 执行方、Sub-agent、LLM 节点 | `#E1F5EE` | `#0F6E56` | `#085041` |
| 琥珀 | 消息队列、总线、警告 | `#FAEEDA` | `#BA7517` | `#633806` |
| 红橙 | 外部系统、工具层、危险 | `#FAECE7` | `#993C1D` | `#712B13` |
| 沙 | 共享平面、配置、注释框 | `#F1EFE8` | `#5F5E5A` | `#444441` |

连接线与辅助色：
- 普通连接 / 分隔线：`rgba(31,30,29, 0.3)`
- 轻量虚线框 / 次级分隔：`rgba(31,30,29, 0.15)`
- 注释文字：`rgb(61,61,58)` + `opacity 0.4–0.55`

---

## 箭头语义

箭头不只是连线，它携带方向含义。同一张图中，实线和虚线之间的对比就是"调用 vs 返回"的视觉编码。

| 样式 | 含义 | 写法 |
|------|------|------|
| 紫色实线 | 任务分发 / 调用 / 正向流 | `stroke="#534AB7"` |
| 绿色虚线（`#1D9E75`） | 子代理汇总返回 | `stroke="#1D9E75" stroke-dasharray="4 3"` |
| 绿色实线（`#0F6E56`） | Loop 回调 / 循环边 | `stroke="#0F6E56"`，无 dasharray |
| 半透明虚线 | 次要返回流 | + `opacity="0.45"` |
| 极细虚线 | 对角关联，无语义强调 | `stroke="rgba(31,30,29,0.15)" stroke-width="0.5" stroke-dasharray="3 3"` |

所有箭头使用同一 marker，`stroke="context-stroke"` 自动继承线色：

```xml
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

---

## 文字层级

文字不用大小来区分层级，用**粗细 + opacity** 的组合。14px 和 12px 是仅有的两档，两档内部再用 weight 和 opacity 细分。

| 用途 | size | weight | opacity |
|------|------|--------|---------|
| 区块标题 / 卡片主文字 | 14px | 500 | 1.0 |
| 卡片副文字 / 说明 | 12px | 400 | 1.0 |
| 列头 / 泳道标签 | 11–12px | 500 | 1.0 |
| 注释文字 | 12px | 400 | 0.4–0.55 |
| 层标注 / 小标签 | 10–12px | 400 | 0.38–0.45 |
| 时间空白占位 | 12px | 400 | 0.3，内容 `· · · · · ·` |

所有居中文字加 `text-anchor="middle" dominant-baseline="central"`。

---

## 节点形态

形状即类型。不同语义的节点用不同形态，不仅靠颜色区分：

| 形态 | 用途 | 规格 |
|------|------|------|
| 圆角矩形 | 普通步骤 / 服务 | rx=6–7；大容器 rx=10–12 |
| 菱形（polygon） | LLM 决策点 / 分支 | half-width=46, half-height=28；`stroke-width="0.8"` |
| 圆形（circle） | Orchestrator 专用（pattern-grid 中） | r=28，`stroke-width="0.8"` |
| 虚线矩形 | 注释框 / 非实体概念 | `fill="none"` + `stroke-dasharray` |

菱形和圆形使用略粗的 `stroke-width="0.8"`，与普通卡片 `0.5` 形成区分，强调其特殊角色。

---

## 边框与分隔

**容器边框极细（0.5）是刻意的**：它让容器作为视觉背景，不与内部的流程箭头争夺注意力。

分隔线只用于辅助，绝不能抢镜：
- 泳道分隔、列间分隔：`rgba(31,30,29,0.15) stroke-width="0.5"`
- 注释框轮廓：`rgba(31,30,29,0.15) stroke-dasharray="3 3"`

当分隔线穿过文字标签时，用 mask 在线上挖空，避免文字被压住：

```xml
<defs>
  <mask id="text-gap" maskUnits="userSpaceOnUse">
    <rect x="0" y="0" width="680" height="[H]" fill="white"/>
    <rect x="[tx]" y="[ty]" width="[tw]" height="[th]" fill="black" rx="2"/>
  </mask>
</defs>
<line ... mask="url(#text-gap)"/>
```

---

## 全局约定

- 画布：`viewBox="0 0 680 [HEIGHT]"`，`width="100%"`
- 字体：`"Anthropic Sans", -apple-system, "system-ui", "Segoe UI", sans-serif`
- 禁止：`style="..."` 内联样式、阴影、渐变、blur

---

## 快速颜色分配指引

新图时按角色分配颜色，不按视觉平衡分配：

- 谁发出调用 → **紫**
- 谁执行任务 → **绿**
- 什么是消息通道 → **琥珀**
- 什么是外部/工具 → **红橙**
- 什么是底层共享基础设施 → **沙**
- 次要概念、注释框、对比面板 → **沙** 或 `fill="none"`
