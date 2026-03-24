# Type: Side by Side

Two independent vertical flows placed left and right of a center divider for direct comparison. Each side has its own header, node sequence, and optional annotation box. The center divider makes structural differences immediately visible.

Use when: contrasting two approaches, architectures, or behaviors where the relationship between corresponding steps matters (e.g., Workflow vs Agent, Sync vs Async, Code vs LLM).

---

## Canvas

```
viewBox="0 0 680 [H]"
```

Height guide:
- Per node: 36px height + 18px gap = ~54px per step
- Left/right panels start at y=58
- Add 80–100 for annotation boxes and legends at the bottom
- Typical range: 400–500

---

## Structure

```
  ┌── Left header ──┐      ┌── Right header ──┐
  │  subtitle       │      │  subtitle        │
  │ ─ ─ ─ ─ ─ ─ ─ ─│─ ─ ─ │─ ─ ─ ─ ─ ─ ─ ─ ─│
  │  [node]         │      │  [node]          │
  │     ↓           │      │     ↓            │
  │  [node]         │      │  [diamond]       │
  │     ↓           │      │     ↓   ←─loop─  │
  │  [node]         │      │  [node]          │
  │     ↓           │      │     ↓            │
  │  [node]         │      │  [diamond]       │
  │  [annotation]   │      │  [node]          │
  │  [legend]       │      │  [annotation]    │
```

---

## Headers

Left panel: center x=160  
Right panel: center x=510

```svg
<!-- Main title (14px/500) -->
<text x="160" y="22" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Left Title
</text>
<!-- Subtitle (12px/400, opacity 0.45) -->
<text x="160" y="40" font-size="12" font-weight="400" opacity="0.45"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  subtitle text
</text>

<text x="510" y="22" …>Right Title</text>
<text x="510" y="40" …>subtitle text</text>
```

---

## Center Divider

```svg
<line x1="335" y1="52" x2="335" y2="[H - 10]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      stroke-dasharray="4 3"/>
```

No text-mask needed unless text crosses the divider.

---

## Panel Geometry

Left panel: x=70, width=180, center-x=160, right-edge=250  
Right panel: x=420, width=180, center-x=510, left-edge=420

---

## Nodes

Standard node rect (180×36 rx=7):

```svg
<rect x="[cx - 90]" y="[top]" width="180" height="36" rx="7"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[top + 18]" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Step Label
</text>
```

### Inter-node Arrow

Standard flow arrow between nodes (stroke-width 1.2, neutral):

```svg
<line x1="[cx]" y1="[node_bottom]" x2="[cx]" y2="[next_node_top]"
      stroke="rgba(31,30,29,0.3)" stroke-width="1.2"
      marker-end="url(#arrow)"/>
```

For arrows following a diamond or colored node, match the stroke color:

```svg
<line … stroke="#0F6E56" stroke-width="1.2" …/>
```

---

## Diamond (Decision Node)

Green diamond (LLM decides at runtime):

```svg
<!-- cx=510, cy = center of diamond; half-width=46, half-height=28 -->
<polygon points="510,[cy-28] 556,[cy] 510,[cy+28] 464,[cy]"
         fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.8"/>
<!-- Two-line text inside (10px and 9px) -->
<text x="510" y="[cy - 8]" font-size="10"
      fill="#085041" text-anchor="middle" dominant-baseline="central">
  question line 1
</text>
<text x="510" y="[cy + 8]" font-size="9"
      fill="#085041" text-anchor="middle" dominant-baseline="central">
  LLM decides
</text>
```

Diamond bounds: top = cy-28, bottom = cy+28, left = cx-46, right = cx+46.

---

## Loop Arrow (Right Side of Panel)

An L-shaped loop that exits the diamond's left point, travels left and up, then re-enters the earlier diamond's left point:

```svg
<!-- exit left from bottom diamond: from (464, cy2) leftward to x=406 -->
<line x1="464" y1="[cy2]" x2="406" y2="[cy2]"
      stroke="#0F6E56" stroke-width="1"/>
<!-- travel up to level of top diamond -->
<line x1="406" y1="[cy2]" x2="406" y2="[cy1]"
      stroke="#0F6E56" stroke-width="1"/>
<!-- enter top diamond's left point rightward -->
<line x1="406" y1="[cy1]" x2="464" y2="[cy1]"
      stroke="#0F6E56" stroke-width="1" marker-end="url(#arrow)"/>
<!-- "loop" label to the left of the vertical segment -->
<text x="398" y="[mid_y]" font-size="12" opacity="0.45"
      fill="[color.text-mid]" text-anchor="end" dominant-baseline="central">
  loop
</text>
```

Typical coordinates (based on source 03905781):
- Top diamond cy=140; bottom diamond cy=322
- Loop track x=406 (28px left of diamond's left edge at x=464)
- Label at x=398, y=232

---

## Annotation Box

A faint dashed rect below the last node, containing multi-line italic-style notes:

```svg
<rect x="[cx - 90]" y="[ann_y]" width="180" height="[ann_h]" rx="7"
      fill="none" stroke="rgba(31,30,29,0.15)" stroke-width="0.5"/>
<text x="[cx]" y="[ann_y + 16]" font-size="12" opacity="0.55"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  Note line 1.
</text>
<text x="[cx]" y="[ann_y + 32]" font-size="12" opacity="0.55"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  Note line 2.
</text>
```

Annotation height: 20px per line + 8px padding. For 3 lines: height=68.

---

## Legend

Small color swatches with labels, placed in the bottom of the left panel:

```svg
<rect x="[cx - 90]" y="[legend_y]" width="12" height="12" rx="2"
      fill="[color1.fill]" stroke="[color1.border]" stroke-width="0.5"/>
<text x="[cx - 90 + 18]" y="[legend_y + 6]" font-size="12"
      fill="[color.text-mid]" text-anchor="start" dominant-baseline="central">
  label 1
</text>
<!-- second swatch, offset 100px right -->
<rect x="[cx - 90 + 100]" y="[legend_y]" width="12" height="12" rx="2"
      fill="[color2.fill]" stroke="[color2.border]" stroke-width="0.5"/>
<text x="[cx - 90 + 118]" y="[legend_y + 6]" …>label 2</text>
```

---

## Color Assignment

| Node type          | Color  |
|--------------------|--------|
| Code / deterministic step | purple |
| LLM step / generation     | green  |
| Diamond (LLM decision)    | green  |
| Diamond (code guard)      | amber  |
| Annotation box             | none (faint border) |
| Loop arrow                 | green (#0F6E56) |
| Inter-node arrows (default)| neutral rgba(0.3) |

Each panel typically uses 1–2 colors. If comparing "code vs LLM", use purple for code nodes and green for LLM nodes uniformly across both panels.

---

## Layout Reference (680×470)

Based on source 03905781:

| y range      | content                        |
|-------------|-------------------------------|
| y=22–40     | column headers                |
| y=52        | divider starts                |
| y=58–94     | node 1 (36px + 18px gap)      |
| y=112–148   | node 2 / diamond 1            |
| y=166–202   | node 3                        |
| y=220–256   | node 4                        |
| y=274–310   | node 5 / diamond 2            |
| y=328–392   | annotation box (left: 64px)   |
| y=418–430   | legend / second annotation    |

Right panel uses same y positions. Diamond 1 cy=140, diamond 2 cy=322.

---

## Generation Steps

1. Identify two systems/approaches to compare; assign left and right
2. List the steps for each side; note which steps involve LLM decisions (use diamonds)
3. Determine if the right side needs a loop arrow between two diamonds
4. Calculate canvas height: max nodes × 54px + 160px for annotations
5. Draw left panel top to bottom (headers → nodes → arrows → annotation → legend)
6. Draw right panel top to bottom (headers → nodes with diamonds → loop arrow → annotation)
7. Draw center divider
8. Apply style from selected style document (colors, fonts, marker defs)
