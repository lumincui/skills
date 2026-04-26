# 初始化配置参考

本文档描述首次使用 leetcode-teacher 时的初始化流程和配置格式。

## 配置文件

使用 `leetcode.json` 保存所有配置和进度：

```json
{
  "difficulty": "medium",
  "todoist_enabled": false,
  "daily_goal": 3,
  "mode": "normal",
  "initialized": true,
  "problems": [...],
  "progress": {},
  "study_plan": {}
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `difficulty` | string | `"medium"` | 难度偏好：`easy` / `medium` / `hard` |
| `todoist_enabled` | boolean | `false` | 是否启用 Todoist 集成 |
| `daily_goal` | number | `3` | 每日目标题目数 |
| `mode` | string | `"normal"` | 默认模式：`normal` 或 `fast` |
| `initialized` | boolean | `false` | 是否已完成初始化 |
| `problems` | array | `[]` | 题目列表 |
| `progress` | object | `{}` | 进度记录 |
| `study_plan` | object | `{}` | 学习计划 |

### problems 数组元素

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 题号 |
| `name` | string | 题目名称 |
| `category` | string | 题目类型 |
| `priority` | string | 优先级：high / medium / low |
| `core_pattern` | string | 核心模式 |

### progress 对象

key 为题号，value 包含：
| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 状态：`pass`（通过）或 `need_review`（需复习） |
| `date` | string | 完成日期 YYYY-MM-DD |

## 初始化流程

### 触发条件

当 `leetcode.json` 文件不存在时，触发初始化流程。

### 询问内容

通过 `question` 工具依次询问：

1. **difficulty**
   - 问题：想练习什么难度的题目？
   - 选项：简单 / 中等 / 困难
   - 默认：中等

2. **是否使用 Todoist**
   - 问题：是否启用 Todoist 集成？（用于自动更新任务状态）
   - 选项：是 / 否
   - 默认：否

3. **每日目标**
   - 问题：每日目标做几道题目？
   - 输入：数字（默认 3）

4. **默认模式**
   - 问题：默认使用哪种模式？
   - 选项：普通模式（生成脚手架）/ 快速模式（对话引导）
   - 默认：普通模式

### 配置保存

初始化完成后，将配置写入 `leetcode.json`。

## 配置读取

```python
import json

def load_json():
    with open('leetcode.json', 'r') as f:
        return json.load(f)

data = load_json()
difficulty = data.get('difficulty', 'medium')
daily_goal = data.get('daily_goal', 3)
todoist_enabled = data.get('todoist_enabled', False)
mode = data.get('mode', 'normal')
progress = data.get('progress', {})
problems = data.get('problems', [])
```

## 配置更新

用户可以通过说"修改配置"或"更新设置"来修改配置。

支持的修改项：
- `set difficulty <easy/medium/hard>` → 更新 leetcode.json 中的 difficulty
- `set todoist on/off` → 更新 leetcode.json 中的 todoist_enabled
- `set daily goal <N>` → 更新 leetcode.json 中的 daily_goal
- `set mode <normal/fast>` → 更新 leetcode.json 中的 mode

题目完成时，更新 `leetcode.json` 中的 `progress` 对象。