# Commands Reference

## Add Task

Opens a modal to create tasks in Todoist from Obsidian. Any selected text is pre-populated as the task content.

**Variants:**
- **Add task** — basic version
- **Add task with current page in task content** — appends an Obsidian backlink to the task content
- **Add task with current page in task description** — appends an Obsidian backlink to the task description

### Copy Markdown Link After Creating

The "Add task" button is a **split button** with a dropdown:

| Action | Description |
|---|---|
| Add task | Creates the task only |
| Add task and copy link (app) | Copies `task content [Todoist](todoist://task?id=...)` |
| Add task and copy link (web) | Copies `task content [Todoist](https://todoist.com/app/project/...)` |

If "append link to content" is enabled, the Obsidian backlink is also included in the copied text.

Set a default action via: **Settings → Task creation → Default add task action**

---

## Sync with Todoist

Manually triggers a refresh of all query blocks in the current note.

---

# Configuration Reference

## General

| Setting | Options | Description |
|---|---|---|
| Token storage | Obsidian secrets *(recommended)*, File-based | Where the API token is stored. File path: `.obsidian/todoist-token`. Changing this setting migrates your token automatically. |

> If using file-based storage and syncing your vault, exclude `.obsidian/todoist-token` from sync for security.

---

## Auto-refresh

| Setting | Description |
|---|---|
| Auto-refresh enabled | Enables global auto-refresh for all queries |
| Auto-refresh interval | Interval in seconds (used when a query has no explicit `autorefresh`) |

---

## Rendering

| Setting | Description |
|---|---|
| Task fade animation | Tasks fade in/out when added or removed |
| Render date icon | Show icon next to due dates |
| Render project & section icon | Show icon next to project/section |
| Render labels icon | Show icon next to labels |

---

## Task Creation

| Setting | Description |
|---|---|
| Add parenthesis to page links | Wraps Obsidian page links in parentheses (useful for mobile) |
| Add task button adds page link | Embedded add-task button in query blocks also links back to the current page |
| Default due date | `none`, `today`, or `tomorrow` |
| Default project | Any project or Inbox |
| Default labels | Zero or more labels auto-applied to new tasks |
| Default add task action | Default action for the split button in the task creation modal |

> If a default project or label no longer exists in Todoist, you'll get a warning when opening the task creation modal and the Inbox / no label will be used instead.

---

## Advanced

| Setting | Description |
|---|---|
| Debug logging | Prints extra info to Developer Tools console (rarely needed) |
