---
name: obsidian-todoist-sync
description: >
  Obsidian 与 Todoist 集成指南。Use when 用户询问 Todoist + Obsidian、安装/配置 Sync with Todoist 插件、API token、在笔记中显示任务、todoist 代码块查询、从 Obsidian 创建 Todoist 任务、同步/刷新/过滤/排序/分组，或说“todoist obsidian / show tasks in obsidian / obsidian task sync”。覆盖 Sync with Todoist Plugin v2.6.0 的安装、查询块和命令配置。
---

# Obsidian Todoist Sync

## Overview

这个 skill 用于指导用户设置和使用 Obsidian 社区插件 **Sync with Todoist**。它主要解决三个问题：

1. 在 Obsidian 笔记里显示 Todoist 任务；
2. 从 Obsidian 创建 Todoist 任务；
3. 配置 token、刷新、过滤、排序、分组和视图。

注意：这是 **非官方插件**。默认能力更偏向 Todoist → Obsidian 展示，同步语义不要夸大成完整双向同步。

---

## Activation Triggers

使用本 skill 当用户说：

- “Todoist 和 Obsidian 怎么同步？”
- “在 Obsidian 里显示 Todoist 任务”
- “todoist query block / todoist 代码块”
- “Obsidian 添加 Todoist 任务”
- “Todoist API token 配置”
- “Sync with Todoist plugin”
- “任务过滤、排序、groupBy、autorefresh、view”

---

## Reference Files

按需读取：

| File | When to read |
|---|---|
| `references/query-blocks.md` | 查询块语法：filter、name、sorting、groupBy、show、view、autorefresh |
| `references/commands-and-config.md` | Add task 命令、sync 命令、插件设置、token 存储 |

不要把所有 reference 一次性塞给用户；根据问题读取相关部分。

---

## Quick Decision Tree

| User wants | Answer path |
|---|---|
| 安装插件 | Installation + token setup |
| 显示今天/逾期任务 | Query block quick start |
| 复杂筛选/排序/分组 | Read `query-blocks.md` |
| 从 Obsidian 添加任务 | Read `commands-and-config.md` |
| 同步失败/任务不显示 | Troubleshooting |
| 安全/Token | Token storage and vault sync warning |

---

## Installation

推荐安装：

1. 打开 Obsidian 插件页：
   ```text
   obsidian://show-plugin?id=todoist-sync-plugin
   ```
2. 或访问：
   ```text
   https://obsidian.md/plugins?id=todoist-sync-plugin
   ```
3. Settings → Community Plugins → Browse → 搜索 “Todoist Sync” → Install → Enable。

如果用户不能打开链接，指导其在 Obsidian 插件市场手动搜索。

---

## API Token Setup

启用插件后：

1. 插件弹窗会要求 Todoist API token；
2. 到 Todoist 获取 token：
   ```text
   https://todoist.com/help/articles/find-your-api-token-Jpzx9IIlB
   ```
3. 粘贴 token；
4. 出现 checkmark 表示有效；
5. 点击 Save。

安全提醒：

- 默认 token 存在 Obsidian secret storage。
- 如果启用文件存储 `.obsidian/todoist-token`，不要把它同步到公开仓库或共享 vault。
- 不要让用户把 token 发到聊天里；如果已泄漏，建议去 Todoist 轮换 token。

---

## Query Block Quick Start

显示今天和逾期任务：

````markdown
```todoist
filter: "today | overdue"
```
````

显示某项目任务：

````markdown
```todoist
filter: "#Work & !subtask"
sorting: "date"
groupBy: "project"
```
````

常用字段：

| Field | Meaning |
|---|---|
| `filter` | Todoist filter 查询，唯一必需字段 |
| `name` | 块标题 |
| `autorefresh` | 自动刷新间隔/开关 |
| `sorting` | 排序方式 |
| `groupBy` | 分组维度 |
| `show` | 显示哪些字段 |
| `view` | 展示视图 |

复杂查询前读取 `references/query-blocks.md`。

---

## Add Tasks from Obsidian

基本方式：

1. Command Palette；
2. 运行 “Add task”；
3. 如果选中了文字，插件会预填任务内容；
4. 选择项目、日期、标签等；
5. 保存到 Todoist。

命令变体、配置项、快捷键建议：读取 `references/commands-and-config.md`。

---

## Troubleshooting

| Symptom | Checks |
|---|---|
| 任务不显示 | token 是否有效；filter 是否能在 Todoist 原生搜索中工作；网络是否可访问 Todoist |
| 查询块无刷新 | 检查 `autorefresh` 和手动 sync 命令 |
| 过滤结果不对 | 先在 Todoist App 中验证 filter 语法 |
| 移动端不同步 | 确认插件已在移动端启用，token 已配置 |
| token 泄漏 | 轮换 Todoist token，删除 `.obsidian/todoist-token` 历史 |

---

## Response Style

- 用户问“怎么做”时，给最短可执行步骤。
- 用户问“配置项”时，给表格和示例代码块。
- 用户排错时，先让其在 Todoist 原生 filter 中验证查询，再看插件设置。
- 不要承诺完整双向同步；明确插件能力边界。

---

## Verification Checklist

- [ ] 是否说明这是非官方插件？
- [ ] 是否避免泄露/索要 token？
- [ ] 查询块是否包含必需的 `filter`？
- [ ] 是否建议先在 Todoist 原生搜索中验证 filter？
- [ ] 是否按需读取了 query/config reference？
