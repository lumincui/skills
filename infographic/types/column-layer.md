# Type: Column Layer

Vertical columns, each representing a logical role or phase, rendered side by side. Items inside each column stack vertically. Arrows in the gaps between columns show dependencies or data flow across boundaries.

Use when: the system has 3–6 distinct roles/phases that operate in parallel with cross-column communication.

---

## Canvas

```
viewBox="0 0 680 [H]"
```

Height guide:
- Base (no banner, no footer): `H = topPad + maxRows × 44 + 60`
- With banner: add 36
- With shared footer row: add 80

Typical range: 300–500. Start at 430 for a 5-row, 4-column layout.

---

## Structure

```
[optional banner]
[optional layer label]
  ┌────────┐  ┌──────┐  ┌──────────────┐  ┌────────┐
  │ Col A  │→ │ Col B│→ │    Col C     │→ │ Col D  │
  │ card   │  │ card │  │ card │ card  │  │ card   │
  │ card   │← │      │  │ card │ card  │  │ card   │
  └────────┘  └──────┘  └──────────────┘  └────────┘
         [shared footer items]
```

---

## Column Container

Each column is a tall background rectangle:

```svg
<rect x="[cx - w/2]" y="[top]" width="[w]" height="[innerH]" rx="12"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
```

Column title (inside, near top):
```svg
<text x="[cx]" y="[top + 20]" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Column Name
</text>
```

Optional sub-label (below title, opacity 0.38):
```svg
<text x="[cx]" y="[top + 34]" font-size="12" font-weight="400"
      fill="[color.text-dark]" opacity="0.38"
      text-anchor="middle" dominant-baseline="central">Layer 1</text>
```

---

## Cards (Inside Columns)

Single-line card:
```svg
<rect x="[cx - 45]" y="[cy - 14]" width="90" height="28" rx="6"
      fill="white" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[cy]" font-size="12" font-weight="400"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Label
</text>
```

Two-line card (title + subtitle):
```svg
<rect x="[cx - 45]" y="[cy - 27]" width="90" height="54" rx="6"
      fill="white" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[cy - 10]" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Title
</text>
<text x="[cx]" y="[cy + 10]" font-size="12" font-weight="400"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  subtitle
</text>
```

---

## Inter-Column Arrows

Arrows sit in the gap between adjacent columns, at the midpoint height of the relevant cards.

Forward (→), solid:
```svg
<line x1="[col_right]" y1="[mid_y]" x2="[next_col_left]" y2="[mid_y]"
      stroke="context-stroke" stroke-width="0.5"
      marker-end="url(#arrow)"/>
```

Return (←), dashed, reduced opacity:
```svg
<line x1="[next_col_left]" y1="[mid_y + 10]" x2="[col_right]" y2="[mid_y + 10]"
      stroke="context-stroke" stroke-width="0.5" opacity="0.45"
      stroke-dasharray="4 3"
      marker-end="url(#arrow)"/>
```

---

## Optional: Sub-Group Frame

A dashed border inside one column to visually group related cards:

```svg
<rect x="[fx]" y="[fy]" width="[fw]" height="[fh]" rx="6"
      fill="none" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      stroke-dasharray="4 3"/>
<text x="[fx + fw/2]" y="[fy - 8]" font-size="11" opacity="0.45"
      text-anchor="middle" dominant-baseline="central">group label</text>
```

---

## Optional: Banner

A full-width header spanning all columns, typically representing a shared context or orchestrating layer:

```svg
<rect x="30" y="16" width="620" height="28" rx="6"
      fill="none" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      stroke-dasharray="4 3"/>
<text x="340" y="30" font-size="12" opacity="0.45"
      text-anchor="middle" dominant-baseline="central">Banner Label</text>
```

---

## Optional: Shared Footer Row

3 or more neutral-colored rectangles at the bottom, representing shared infrastructure or common output:

```svg
<!-- Footer item 1 of 3 -->
<rect x="[fx1]" y="[footer_y]" width="192" height="40" rx="8"
      fill="[sand.fill]" stroke="[sand.border]" stroke-width="0.5"/>
<text x="[fx1 + 96]" y="[footer_y + 20]" font-size="12"
      fill="[sand.text-dark]" text-anchor="middle" dominant-baseline="central">
  Shared Component
</text>
```

Connect footer items to the column above using a faint dashed diagonal:
```svg
<line x1="[col_cx]" y1="[col_bottom]" x2="[footer_cx]" y2="[footer_y]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5" stroke-dasharray="4 3"/>
```

Footer y: typically `column_bottom + 20`. Space footer items evenly across x=30–650.

---

## Color Assignment

Assign one color per column based on logical role:

| Role type         | Color  |
|-------------------|--------|
| Input / Interface | purple |
| Configuration     | amber  |
| Processing / Core | green  |
| Output / Review   | red-orange |
| Shared / Infra    | sand   |

A single diagram typically uses 2–4 colors. Keep adjacent columns in different color families.

---

## Layout Reference

Typical 4-column layout (based on SVG source 599dc523):

| Column | x    | width | center-x |
|--------|------|-------|----------|
| 1      | 30   | 118   | 89       |
| 2      | 168  | 104   | 220      |
| 3      | 292  | 216   | 400      |
| 4      | 528  | 122   | 589      |

Column gaps for arrows: col1→col2 at x≈148–168, col2→col3 at x≈272–292, col3→col4 at x≈508–528.

For 3 columns: widths approximately 180 / 180 / 180, x at 30 / 230 / 430.  
For 5 columns: compress to widths ~100 each, or drop the footer.

Cards inside a column: horizontally centered at `cx`, vertically spaced 44px apart starting at `top + 48`.

---

## Generation Steps

1. Count columns (roles/phases) and max card rows → compute `H`
2. Decide if banner and/or footer are needed
3. Draw columns left to right, assign colors per role type
4. Fill cards top to bottom inside each column
5. Draw inter-column arrows at the vertical midpoint of the related cards
6. Add sub-group frames if cards in a column form 2 logical clusters
7. Draw footer rectangles and dashed connection lines if needed
8. Apply style from the selected style document (colors, fonts, marker defs)
