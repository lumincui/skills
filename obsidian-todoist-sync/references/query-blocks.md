# Query Blocks — Full Reference

Embed Todoist task lists in any Obsidian note using a `todoist` code block written in YAML.

````
```todoist
filter: "today | overdue"
```
````

---

## Options

### `filter` *(required)*

A valid [Todoist filter expression](https://todoist.com/help/articles/introduction-to-filters-V98wIH).

- Must be the filter content — **not** a saved filter name from your account
- Supports `{{filename}}` placeholder (replaced with current note's name, without `.md`)
- **Known limitations:**
  - Wildcard filters don't work as expected (e.g., `@*ball`)
  - Cannot combine multiple filters with commas (e.g., `today | overdue, p1`)

---

### `name`

Renders an `<h4>` header above the task list.

```yaml
name: "Today & Overdue"
filter: "today | overdue"
```

---

### `autorefresh`

Seconds between automatic refreshes. Overrides the plugin-level setting.

```yaml
filter: "today | overdue"
autorefresh: 120
```

---

### `sorting`

Ordered list of sort criteria applied in sequence:

| Value | Description |
|---|---|
| `alphabetical` / `alphabeticalAscending` | A→Z by name |
| `alphabeticalDescending` | Z→A by name |
| `date` / `dateAscending` | Ascending due date |
| `dateDescending` | Descending due date |
| `priority` / `priorityAscending` | Ascending priority |
| `priorityDescending` | Descending priority |
| `order` | Todoist native order |
| `dateAdded` / `dateAddedAscending` | Ascending date added |
| `dateAddedDescending` | Descending date added |

```yaml
filter: "today | overdue"
sorting:
  - date
  - priority
```

---

### `groupBy`

Groups tasks when rendered. If omitted, no grouping is applied.

| Value | Description |
|---|---|
| `project` | Group by project |
| `section` | Group by project and section |
| `due` / `date` | Group by due date (overdue tasks grouped together) |
| `labels` | Group by labels (unlabelled tasks grouped together) |
| `priority` | Group by priority (high→low) |

---

### `show`

Controls which task metadata fields are rendered. Omit to show all.

| Value | Description |
|---|---|
| `due` / `date` | Due date |
| `time` | Only the time component of due date |
| `deadline` | Deadline |
| `description` | Task description |
| `project` | Project (and section if applicable) |
| `section` | Only the section name |
| `labels` | Labels |

> If both `project` and `section` are specified, only `project` is shown to avoid redundancy.

Set to `none` to hide all metadata:

```yaml
filter: "today | overdue"
show: none
```

---

### `view`

Customize display when no tasks are found.

| Property | Description |
|---|---|
| `noTasksMessage` | Custom message shown when query returns no tasks |
| `hideNoTasks` | Set `true` to hide the block entirely when no tasks exist |

```yaml
filter: "#work & today"
view:
  noTasksMessage: "Nothing due today! Take a break."
  hideNoTasks: true
```

---

## Full Example

```yaml
name: "Work Tasks"
filter: "#work & today"
autorefresh: 60
sorting:
  - priority
  - date
groupBy: section
show:
  - due
  - labels
view:
  noTasksMessage: "All clear!"
```
