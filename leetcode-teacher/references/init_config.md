# 初始化配置参考

本 skill 会在当前目录创建 `leetcode.json` 保存用户配置和题目状态。

## leetcode.json 配置格式

```json
{
  "todoist_enabled": false,
  "daily_goal": 3,
  "mode": "normal",
  "initialized": true,
  "problems": [
    {"id": "322", "name": "Coin Change", "category": "dp", "status": "pass", "date": "2024-01-15"},
    {"id": "300", "name": "Longest Increasing Subsequence", "category": "dp", "status": "review", "date": "2024-01-14"}
  ]
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `todoist_enabled` | boolean | `false` | 是否启用 Todoist 集成 |
| `daily_goal` | number | `3` | 每日目标题目数 |
| `mode` | string | `"normal"` | 默认模式：`normal` 或 `fast` |
| `initialized` | boolean | `false` | 是否已完成初始化 |
| `problems` | array | `[]` | 已完成的题目列表 |

### problems 数组元素

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 题号 |
| `name` | string | 题目名称 |
| `category` | string | 题目类型 |
| `status` | string | 状态：`pass`（通过）或 `review`（需复习） |
| `date` | string | 完成日期 YYYY-MM-DD |

## 初始化流程

### 触发条件

当 `leetcode.json` 文件不存在时，触发初始化流程。

### 询问内容

通过 `question` 工具依次询问：

1. **是否使用 Todoist**
   - 问题：是否启用 Todoist 集成？（用于自动更新任务状态）
   - 选项：是 / 否
   - 默认：否

2. **每日目标**
   - 问题：每日目标做几道题目？
   - 输入：数字（默认 3）

3. **默认模式**
   - 问题：默认使用哪种模式？
   - 选项：普通模式（生成脚手架）/ 快速模式（对话引导）
   - 默认：普通模式

### Markdown 迁移

若存在 `README.md` 且包含进度表格（格式参考 `references/progress_tracking.md`），解析表格内容并将题目数据迁移到 `leetcode.json` 的 `problems` 数组。

迁移规则：
- 读取 `| 题号 | 题目名 | 类型 | 状态 | 完成日期 |` 格式的表格
- 状态转换：`✅ 通过` → `pass`，`🔄 需复习` → `review`
- 日期格式统一为 `YYYY-MM-DD`

### 配置保存

初始化完成后，将配置写入 `leetcode.json`，格式见上方。

## 配置读取

所有脚本和决策点应从 `leetcode.json` 读取配置：

```python
import json

def load_config():
    with open('leetcode.json', 'r') as f:
        return json.load(f)

config = load_config()
daily_goal = config.get('daily_goal', 3)
todoist_enabled = config.get('todoist_enabled', False)
mode = config.get('mode', 'normal')
problems = config.get('problems', [])
```

## 配置更新

用户可以通过说"修改配置"或"更新设置"来修改配置。

支持的修改项：
- `set todoist on/off` → 更新 todoist_enabled
- `set daily goal <N>` → 更新 daily_goal
- `set mode <normal/fast>` → 更新 mode

题目完成时，将题目信息追加到 `problems` 数组。