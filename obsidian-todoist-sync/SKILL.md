---
name: obsidian-todoist-sync
description: >
  Guide for setting up and using the Sync with Todoist Plugin for Obsidian (v2.6.0).
  Use this skill whenever the user asks about integrating Todoist with Obsidian, installing the Todoist plugin, creating query blocks to display tasks in Obsidian notes, adding tasks from Obsidian to Todoist, configuring API tokens, or any question related to the obsidian-todoist-plugin. Trigger even if the user just says "todoist obsidian", "show my tasks in obsidian", "obsidian task sync", or asks how to display/add/manage Todoist tasks inside Obsidian.
---

# Obsidian Todoist Plugin (Sync with Todoist, v2.6.0)

An **unofficial** plugin that integrates Todoist tasks into your Obsidian vault. Primarily one-way sync (Todoist → Obsidian), with limited ability to create tasks from Obsidian. Works on desktop and mobile.

---

## Reference files

Load these only when the user's question requires the detail:

| File | When to read |
|---|---|
| `references/query-blocks.md` | User asks about embedding tasks, query syntax, filter options, sorting, groupBy, show, autorefresh, view |
| `references/commands-and-config.md` | User asks about add task command, sync command, or any plugin configuration setting |

---

## 1. Installation

**Via Obsidian (recommended):**
Open this link in Obsidian: `obsidian://show-plugin?id=todoist-sync-plugin`
Or visit: https://obsidian.md/plugins?id=todoist-sync-plugin

**Manual:**
1. Settings → Community Plugins → enable community plugins
2. Browse → search "Todoist Sync" → Install → Enable

---

## 2. API Token Setup

After enabling the plugin:

1. A popup asks for your [Todoist API token](https://todoist.com/help/articles/find-your-api-token-Jpzx9IIlB)
2. Enter the token directly or use "Paste from clipboard"
3. A checkmark appears if the token is valid
4. Click **Save**

Token is stored in Obsidian's built-in secret storage by default. File-based storage (`.obsidian/todoist-token`) is available in configuration — avoid syncing that file if you share your vault.

---

## 3. Quick Start

**Embed tasks in a note:**

````
```todoist
filter: "today | overdue"
```
````

Only `filter` is required. All other options (`name`, `autorefresh`, `sorting`, `groupBy`, `show`, `view`) are optional.
→ For full query block reference, read `references/query-blocks.md`

**Add a task from Obsidian:**
Command Palette → "Add task" (pre-populates with any selected text)
→ For command variants and configuration, read `references/commands-and-config.md`

---

## Docs

https://jamiebrynes7.github.io/obsidian-todoist-plugin/docs/setup
