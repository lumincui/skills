# Type: Pattern Grid

A comparison matrix where columns are pattern names and rows show each pattern's structure visually. Each cell contains one or more representative node shapes (rectangles, diamonds, circles, parallel boxes) connected by arrows. The grid communicates structural patterns at a glance rather than narrating a specific flow.

Use when: displaying a catalog of design patterns, architecture archetypes, or algorithm variants side by side.

---

## Canvas

```
viewBox="0 0 680 [H]"
```

Height guide:
- Header row: ~32px
- Main content zone: ~180–220px
- Footer note row: ~50px (optional)
- Typical total: 280–350

---

## Structure

```
│ Col A  │ Col B  │   Col C (wide)  │ Col D  │ Col E  │
│ header │ header │  sub-A │ sub-B  │ header │ header │
│──────────────────────────────────────────────────────│
│ nodes  │ nodes  │ nodes  │ nodes  │ nodes  │ nodes  │
│ arrows │ arrows │        │        │ arrows │        │
│──────────────────────────────────────────────────────│
│ note   │ note   │      note       │ note   │ note   │
```

---

## Column Layout

Five columns is the standard. Each column has a header label and an area for node shapes.

### Column Separators

Faint vertical lines between columns:

```svg
<line x1="[x]" y1="28" x2="[x]" y2="[H - 50]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      mask="url(#text-mask)"/>
```

Standard separator x positions: 118, 238, 418, 554.

### Column Centers (standard 5-column)

| Column         | separator-left | separator-right | center-x |
|---------------|---------------|----------------|---------|
| Prompt chain  | —             | 118            | 58      |
| Routing       | 118           | 238            | 178     |
| Parallelization | 238         | 418            | 328 (split: left 293, right 383) |
| Orchestrator  | 418           | 554            | 490     |
| Eval-Optimizer| 554           | —              | 610     |

### Column Headers

```svg
<text x="[cx]" y="[header_y]" font-size="11" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Column Name
</text>
```

### Sub-column (within a wide column)

A wide column can be split into two sub-columns with an interior dashed divider:

```svg
<line x1="[sub_divider_x]" y1="[header_bottom]" x2="[sub_divider_x]" y2="[content_bottom]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5" stroke-dasharray="4 3"/>
```

Sub-headers (one per sub-column, same font as column header):
```svg
<text x="[sub_cx]" y="[sub_header_y]" font-size="11" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Sub-column Name
</text>
```

---

## Node Shapes

The building blocks that populate each column. Mix types as needed.

### Standard Rect (process step)

```svg
<rect x="[cx - 42]" y="[cy - 14]" width="84" height="28" rx="6"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[cy]" font-size="12" font-weight="400"
      fill="[color.text-acc]" text-anchor="middle" dominant-baseline="central">
  Step
</text>
```

Smaller rect (sub-step, 64×24 rx=5):
```svg
<rect x="[cx - 32]" y="[cy - 12]" width="64" height="24" rx="5"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
```

### Diamond (decision / checkpoint / classifier)

```svg
<!-- cx,cy = center; half-width=36, half-height=22 -->
<polygon points="[cx],[cy-22] [cx+36],[cy] [cx],[cy+22] [cx-36],[cy]"
         fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[cy]" font-size="11" font-weight="400"
      fill="[color.text-acc]" text-anchor="middle" dominant-baseline="central">
  Route?
</text>
```

Color semantics:
- Amber diamond = checkpoint (approval, guard)
- Green diamond = classifier / decision

### Circle (hub / orchestrator node)

For central orchestrators only. Radius 28.

```svg
<circle cx="[cx]" cy="[cy]" r="28"
        fill="[color.fill]" stroke="[color.border]" stroke-width="0.8"/>
<text x="[cx]" y="[cy]" font-size="12" font-weight="400"
      fill="[color.text-acc]" text-anchor="middle" dominant-baseline="central">
  Hub
</text>
```

### Parallel Box (small, for fan-out)

Small rectangle indicating a parallel sub-task. 28×22 rx=4:

```svg
<rect x="[cx - 14]" y="[cy - 11]" width="28" height="22" rx="4"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
```

Use 2–3 of these side by side to show parallelism:
```
 ┌──┐ ┌──┐ ┌──┐
 │  │ │  │ │  │
 └──┘ └──┘ └──┘
```

---

## Arrows

### Standard Flow Arrow (↓)

```svg
<line x1="[cx]" y1="[from_y]" x2="[cx]" y2="[to_y]"
      stroke="context-stroke" stroke-width="0.5"
      marker-end="url(#arrow)"/>
```

### Fan-out (one → many)

From one node to multiple parallel boxes: draw a vertical stem, then a horizontal bar, then vertical drops to each box.

```svg
<!-- stem -->
<line x1="[cx]" y1="[from_y]" x2="[cx]" y2="[bar_y]"
      stroke="context-stroke" stroke-width="0.5"/>
<!-- bar -->
<line x1="[left_cx]" y1="[bar_y]" x2="[right_cx]" y2="[bar_y]"
      stroke="context-stroke" stroke-width="0.5"/>
<!-- drops -->
<line x1="[sub_cx]" y1="[bar_y]" x2="[sub_cx]" y2="[box_top]"
      stroke="context-stroke" stroke-width="0.5" marker-end="url(#arrow)"/>
```

### Feedback / Loop Arrow (red `#E24B4A`)

An L-shaped arrow going upward on the left edge of the column, indicating an iteration loop:

```svg
<!-- down leg -->
<line x1="[cx - col_w/2 + 8]" y1="[bottom_node_y]"
      x2="[cx - col_w/2 + 8]" y2="[bottom_node_y + 20]"
      stroke="#E24B4A" stroke-width="0.5"/>
<!-- left leg -->
<line x1="[cx - col_w/2 + 8]" y1="[bottom_node_y + 20]"
      x2="[cx - col_w/2]" y2="[bottom_node_y + 20]"
      stroke="#E24B4A" stroke-width="0.5"/>
<!-- up leg -->
<line x1="[cx - col_w/2]" y1="[bottom_node_y + 20]"
      x2="[cx - col_w/2]" y2="[top_node_y]"
      stroke="#E24B4A" stroke-width="0.5"/>
<!-- right leg with arrow -->
<line x1="[cx - col_w/2]" y1="[top_node_y]"
      x2="[cx - col_w/2 + 8]" y2="[top_node_y]"
      stroke="#E24B4A" stroke-width="0.5" marker-end="url(#arrow)"/>
```

---

## Footer Note Row

Two lines of supplementary text per column, shown below a separator line. Use for caveats, use-cases, or constraints.

```svg
<!-- separator -->
<line x1="20" y1="[note_y]" x2="660" y2="[note_y]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"/>

<!-- note lines (two per column) -->
<text x="[cx]" y="[note_y + 14]" font-size="11" opacity="0.4"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  first note line
</text>
<text x="[cx]" y="[note_y + 28]" font-size="11" opacity="0.4"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  second note line
</text>
```

---

## Color Assignment

| Pattern role       | Color  |
|--------------------|--------|
| Primary node       | purple |
| Secondary / worker | sand or green (smaller size) |
| Checkpoint / guard | amber diamond |
| Classifier / route | green diamond |
| Hub / orchestrator | purple circle |
| Feedback arrow     | red-orange (#E24B4A) |

Keep the palette minimal per column: typically 1 primary color + feedback arrow.

---

## Layout Reference (5-column, 680×300)

- Header y: ~24
- Sub-header y: ~46 (for split columns)
- Content zone: y=56–240
- Note separator y: ~248
- Note lines: y=260, y=275

Typical node vertical rhythm: 44px between centers within a column.

For the Orchestrator column (wide circle node + hub-and-spoke):
- Circle at cy=130, r=28
- Spoke nodes (small rects) fanning out at y=80 and y=180, offset ±30px left/right

---

## Generation Steps

1. Count pattern columns and identify which need sub-columns
2. Compute separator x positions and column center-x values
3. Draw column separators and headers
4. For each column, lay out representative nodes top to bottom
5. Add arrows (flow, fan-out, feedback)
6. Draw footer separator and note lines
7. Apply style from selected style document (colors, fonts, marker defs)
