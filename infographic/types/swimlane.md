# Type: Swimlane

Horizontal rows (or vertical columns) that represent distinct actors, agents, or responsibility zones. Steps flow left-to-right within each lane; arrows cross lane boundaries to show handoffs. A center divider can split the canvas into two independent systems for comparison.

Use when: the diagram involves 2–5 named actors whose interactions must be traced step-by-step, or when comparing two operational modes side by side.

---

## Canvas

```
viewBox="0 0 680 [H]"
```

Height guide:
- Per lane (horizontal layout): ~60px each
- Per actor-row (vertical layout): ~52px per sub-agent + header
- Bottom planes section: add 80 if present
- Typical range: 300–420

---

## Variant A: Side-by-Side Comparison

Two independent swimlane systems rendered left and right, separated by a vertical center divider. Use when comparing two modes, approaches, or architectures.

```
┌─────── System A ────────┬─────── System B ────────┐
│  Lane 1 ── ── ── ──     │  Lane 1 ─────────────   │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  Lane 2                 │  Lane 2                 │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  output box             │  output box             │
└─────────────────────────┴─────────────────────────┘
```

### Center Divider

```svg
<line x1="340" y1="52" x2="340" y2="[H]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      stroke-dasharray="4 3" mask="url(#text-mask)"/>
```

### Column Headers (14px/500 + 12px/0.45 subtitle)

Left system: center x=170  
Right system: center x=510

```svg
<text x="170" y="22" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  System A Name
</text>
<text x="170" y="40" font-size="12" font-weight="400" opacity="0.45"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  subtitle / mode descriptor
</text>
```

### Lane Labels (left-aligned, opacity 0.4)

```svg
<text x="[section_left + 8]" y="[lane_cy]" font-size="12" font-weight="400"
      opacity="0.4" fill="[color.text-mid]"
      text-anchor="start" dominant-baseline="central">
  Lane Name
</text>
```

Lane positions (2-lane system, starting y=52):
- Lane 1 center y: ~72; lane divider at y=100
- Lane 2 center y: ~132; lane divider at y=160
- Lane 3 center y: ~192 (if 3 lanes); lane divider at y=220

### Lane Dividers

```svg
<line x1="[section_left]" y1="[y]" x2="[section_right]" y2="[y]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"/>
```

Left section: x1=50 x2=320. Right section: x1=350 x2=640.

### Cards Inside Lanes

Compact horizontal cards, 52×28 rx=6:

```svg
<rect x="[cx - 26]" y="[cy - 14]" width="52" height="28" rx="6"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[cy]" font-size="12" fill="[color.text-acc]"
      text-anchor="middle" dominant-baseline="central">label</text>
```

Wider cards for longer text: 68×28 or 80×28, adjust cx accordingly.

### Cross-Lane Arrows

Synchronous (solid, paired ↓↑):

```svg
<!-- down: human → agent -->
<line x1="[cx]" y1="[top_card_bottom]" x2="[cx]" y2="[bot_card_top]"
      stroke="[color.accent]" stroke-width="1" marker-end="url(#arrow)"/>
<!-- up: agent → human, offset +14px right -->
<line x1="[cx + 14]" y1="[bot_card_top]" x2="[cx + 14]" y2="[top_card_bottom]"
      stroke="[color.accent]" stroke-width="1" marker-end="url(#arrow)"/>
```

Async return (dashed, green `#1D9E75`):

```svg
<line x1="[agent_cx + 16]" y1="[agent_card_top]" x2="[human_cx + 16]" y2="[human_card_bottom]"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"
      marker-end="url(#arrow)" mask="url(#text-mask)"/>
```

### Gap / Ellipsis Label

Show time gap in the Human row:
```svg
<text x="[mid_x]" y="[lane1_cy]" font-size="12" opacity="0.3"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  · · · · · · · ·
</text>
```

### Marker / Event Annotation

Vertical colored line marking an event (e.g., session end):

```svg
<line x1="[x]" y1="[top_y]" x2="[x]" y2="[bot_y]"
      stroke="#E24B4A" stroke-width="1" stroke-dasharray="4 3"
      mask="url(#text-mask)"/>
<text x="[x + 4]" y="[top_y + 16]" font-size="11" fill="#A32D2D"
      text-anchor="start" dominant-baseline="central">event name</text>
<text x="[x + 4]" y="[top_y + 30]" font-size="11" fill="#A32D2D"
      text-anchor="start" dominant-baseline="central">detail</text>
```

### Output Box

A dashed rect below the last lane summarizing output type:

```svg
<rect x="[left]" y="[y]" width="[w]" height="30" rx="6"
      fill="none" stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      stroke-dasharray="3 3"/>
<text x="[cx]" y="[y + 15]" font-size="12" opacity="0.5"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  output: description
</text>
```

For a "positive" output box (use green stroke):
```svg
<rect … stroke="#1D9E75" …/>
<text … fill="#0F6E56" …>output: branch · commit · PR · persisted</text>
```

---

## Variant B: Three-Column Actor Swimlane

Three named actors stacked as vertical columns (not time-series rows). Each actor column has a background container with cards inside. Flow runs left → middle → right.

```
┌────────────┐  ┌──────────────────┐  ┌────────────┐
│  Actor A   │  │   Protocol / Msg │  │  Actors    │
│  card      │→ │  inbox schema    │→ │  B / C     │
│  card      │  │  field list      │  │            │
│  card      │← │                  │← │            │
└────────────┘  └──────────────────┘  └────────────┘
     [bottom planes]
```

Column positions (3-column):
| Column       | x   | width | center-x |
|-------------|-----|-------|---------|
| Actor A     | 20  | 140   | 90      |
| Protocol    | 210 | 260   | 340     |
| Sub-agents  | 490 | 166   | 573     |

Column headers: `12px/500`, centered at column cx, y=16.

### Column Container

```svg
<rect x="[x]" y="[top]" width="[w]" height="[h]" rx="10"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[top + 20]" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Actor Name
</text>
<text x="[cx]" y="[top + 36]" font-size="12" font-weight="400"
      fill="[color.text-acc]" text-anchor="middle" dominant-baseline="central">
  subtitle
</text>
```

### Sub-agent Card (inside Sub-agents column)

Two-line card with worktree path below:

```svg
<!-- card -->
<rect x="[x]" y="[y]" width="166" height="52" rx="8"
      fill="[color.fill]" stroke="[color.border]" stroke-width="0.5"/>
<text x="[cx]" y="[y + 18]" font-size="14" font-weight="500"
      fill="[color.text-dark]" text-anchor="middle" dominant-baseline="central">
  Sub-agent Name
</text>
<text x="[cx]" y="[y + 34]" font-size="12"
      fill="[color.text-acc]" text-anchor="middle" dominant-baseline="central">
  own messages[]
</text>
<!-- worktree path (dashed, outside card) -->
<rect x="[x]" y="[y + 60]" width="166" height="24" rx="5"
      fill="none" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      stroke-dasharray="4 3"/>
<text x="[cx]" y="[y + 72]" font-size="12" opacity="0.45"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  .worktrees/agent-name
</text>
```

### Inter-Column Arrows (paired dispatch/summary)

Dispatch (solid, purple `#534AB7`): x offset -6 from center
Summary (dashed, green `#1D9E75`): x offset +6 from center

```svg
<!-- dispatch: Actor A → Protocol -->
<line x1="[left_col_right - 6]" y1="[mid_y]"
      x2="[middle_col_left - 6]" y2="[mid_y]"
      stroke="#534AB7" stroke-width="1.2" marker-end="url(#arrow)"
      mask="url(#text-mask)"/>
<!-- summary: Protocol → Actor A -->
<line x1="[middle_col_left + 6]" y1="[mid_y + 12]"
      x2="[left_col_right + 6]" y2="[mid_y + 12]"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"
      marker-end="url(#arrow)"/>
<!-- small arrow labels -->
<text x="[mid_x]" y="[mid_y - 8]" font-size="10" opacity="0.38"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  dispatch
</text>
<text x="[mid_x]" y="[mid_y + 22]" font-size="10" opacity="0.38"
      fill="#0F6E56" text-anchor="middle" dominant-baseline="central">
  summary
</text>
```

### L-bend Return Arrow (sub → protocol, from top of sub-agent)

```svg
<!-- exit left from sub-agent top edge, bend down to protocol entry level -->
<line x1="[sub_x]" y1="[sub_top_cy]"
      x2="[sub_x - 14]" y2="[sub_top_cy]"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="[sub_x - 14]" y1="[sub_top_cy]"
      x2="[sub_x - 14]" y2="[protocol_return_y]"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="[sub_x - 14]" y1="[protocol_return_y]"
      x2="[protocol_right]" y2="[protocol_return_y]"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"
      marker-end="url(#arrow)"/>
```

---

## Variant C: Orchestrator + Sub-agents (Hierarchical)

One orchestrator bar spans the full width at the top; sub-agents sit below as equal-width columns. A JSONL inbox line separates orchestrator from sub-agents.

```
┌──────────────────── Orchestrator ────────────────────┐
│ Main Agent · full context · decompose + aggregate    │
├─ ─ ─ ─ ─ ─ ─ ─ JSONL inbox ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
│  Sub A    │     Sub B     │     Sub C               │
│ messages[]│  messages[]   │  messages[]             │
│ .worktree │  .worktree    │  .worktree              │
└───────────┴───────────────┴─────────────────────────┘
     [warning bar if needed]
     [bottom planes]
```

### Orchestrator Bar

```svg
<rect x="118" y="28" width="548" height="52" rx="10"
      fill="[purple.fill]" stroke="[purple.border]" stroke-width="0.5"/>
<text x="392" y="46" font-size="14" font-weight="500"
      fill="[purple.text-dark]" text-anchor="middle" dominant-baseline="central">
  Orchestrator
</text>
<text x="392" y="66" font-size="12"
      fill="[purple.text-acc]" text-anchor="middle" dominant-baseline="central">
  Main Agent · full context · decompose + aggregate
</text>
```

### JSONL Inbox Divider

```svg
<text x="392" y="96" font-size="10" opacity="0.35"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  JSONL inbox · request_id / status · append-only
</text>
<line x1="122" y1="105" x2="662" y2="105"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      stroke-dasharray="3 3" mask="url(#text-mask)"/>
```

### Sub-agent Columns (equal width, N agents)

For 3 sub-agents: each w=162, gap=10. Total=506. Start x=139.  
Centers: 220, 392, 564.

Vertical dispatch (purple) and summary (dashed green) arrows between orchestrator (y=80) and sub-agents (y=138), offset ±6px:

```svg
<!-- dispatch down at x-6 -->
<line x1="[cx - 6]" y1="80" x2="[cx - 6]" y2="138"
      stroke="#534AB7" stroke-width="1" marker-end="url(#arrow)"
      mask="url(#text-mask)"/>
<!-- summary up at x+6 -->
<line x1="[cx + 6]" y1="138" x2="[cx + 6]" y2="80"
      stroke="#1D9E75" stroke-width="1" stroke-dasharray="4 3"
      marker-end="url(#arrow)" mask="url(#text-mask)"/>
```

Arrow labels flanking the gap:
```svg
<text x="[cx - 14]" y="112" font-size="10" opacity="0.35"
      text-anchor="end" dominant-baseline="central">task</text>
<text x="[cx + 14]" y="112" font-size="10" opacity="0.5" fill="#0F6E56"
      text-anchor="start" dominant-baseline="central">summary</text>
```

### Optional: Warning Bar

Full-width amber-bordered alert below sub-agents:

```svg
<rect x="118" y="[warn_y]" width="548" height="38" rx="8"
      fill="none" stroke="[amber.border]" stroke-width="0.5"/>
<text x="134" y="[warn_y + 14]" font-size="12" font-weight="500"
      fill="[amber.text-dark]" text-anchor="start" dominant-baseline="central">
  Warning title
</text>
<text x="134" y="[warn_y + 30]" font-size="12" opacity="0.55"
      fill="[color.text-mid]" text-anchor="start" dominant-baseline="central">
  Warning detail text.
</text>
```

---

## Bottom Planes Section

Shared infrastructure shown as two side-by-side rectangles below a separator line:

```svg
<!-- separator -->
<line x1="14" y1="[sep_y]" x2="666" y2="[sep_y]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"/>

<!-- control plane (sand) -->
<rect x="14" y="[sep_y + 10]" width="318" height="42" rx="8"
      fill="[sand.fill]" stroke="[sand.border]" stroke-width="0.5"/>
<text x="173" y="[sep_y + 24]" font-size="14" font-weight="500"
      fill="[sand.text-dark]" text-anchor="middle" dominant-baseline="central">
  .tasks/  control plane
</text>
<text x="173" y="[sep_y + 40]" font-size="12"
      fill="[sand.text-acc]" text-anchor="middle" dominant-baseline="central">
  task graph · owner · blockedBy · status
</text>

<!-- execution plane (green) -->
<rect x="344" y="[sep_y + 10]" width="322" height="42" rx="8"
      fill="[green.fill]" stroke="[green.border]" stroke-width="0.5"/>
<text x="505" y="[sep_y + 24]" font-size="14" font-weight="500"
      fill="[green.text-dark]" text-anchor="middle" dominant-baseline="central">
  .worktrees/  execution plane
</text>
<text x="505" y="[sep_y + 40]" font-size="12"
      fill="[green.text-acc]" text-anchor="middle" dominant-baseline="central">
  file isolation · no cross-agent write
</text>
```

Faint dashed connectors from sub-agents down to the execution plane:
```svg
<line x1="[sub_cx]" y1="[sub_bottom + 2]" x2="[sub_cx]" y2="[sep_y + 10]"
      stroke="rgba(31,30,29,0.15)" stroke-width="0.5"
      stroke-dasharray="3 3" mask="url(#text-mask)"/>
```

---

## Optional: Left-Side Task Graph Panel

A small dashed panel left of the main area showing a task dependency tree:

```svg
<rect x="14" y="28" width="86" height="188" rx="8"
      fill="none" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      stroke-dasharray="5 3"/>
<text x="57" y="44" font-size="11" opacity="0.45"
      fill="[color.text-mid]" text-anchor="middle" dominant-baseline="central">
  Task graph
</text>
```

Task nodes inside (sand color, 70×28 rx=5 for root; 38×34 rx=5 for child nodes):
```svg
<rect x="22" y="56" width="70" height="28" rx="5"
      fill="[sand.fill]" stroke="[sand.border]" stroke-width="0.5"/>
<text x="57" y="70" font-size="11" font-weight="500"
      fill="[sand.text-dark]" text-anchor="middle" dominant-baseline="central">
  T-001
</text>
```

Branch connector (T-junction → two child nodes):
```svg
<line x1="57" y1="84" x2="57" y2="92" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"/>
<line x1="36" y1="92" x2="78" y2="92" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"/>
<line x1="36" y1="92" x2="36" y2="108" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      marker-end="url(#arrow)"/>
<line x1="78" y1="92" x2="78" y2="108" stroke="rgba(31,30,29,0.3)" stroke-width="0.5"
      marker-end="url(#arrow)"/>
```

Faint metadata labels below children (opacity 0.38, 10px):
```svg
<text x="57" y="162" font-size="10" opacity="0.38" fill="[color.text-mid]"
      text-anchor="middle" dominant-baseline="central">owner</text>
<text x="57" y="176" font-size="10" opacity="0.38" …>blockedBy</text>
<text x="57" y="190" font-size="10" opacity="0.38" …>status</text>
```

---

## Color Assignment

| Actor type          | Color  |
|---------------------|--------|
| Human / Initiator   | green  |
| Orchestrator / Main | purple |
| Sub-agent / Worker  | green  |
| Protocol / Infra    | blue (approximate with: fill `#E6F1FB`, stroke `#185FA5`, text `#0C447C`) |
| Shared planes       | sand   |
| Warning / Alert     | amber  |
| Error / Session end | red-orange |

---

## Generation Steps

1. Choose variant: A (side-by-side comparison), B (column actors), or C (hierarchical orchestrator)
2. Count lanes/actors and estimate canvas height
3. Draw dividers, headers, and lane labels first
4. Place actor nodes (cards) in chronological/logical order
5. Draw cross-lane arrows: solid for dispatch/call, dashed for return/summary
6. Add event markers (colored vertical lines) or gap ellipsis as needed
7. Add output box or bottom planes if applicable
8. Apply style from selected style document (colors, fonts, marker defs)
