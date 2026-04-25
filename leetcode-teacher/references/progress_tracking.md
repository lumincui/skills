# 进度追踪参考

本文档定义 leetcode.json 中的进度追踪和学习计划格式。

## leetcode.json 结构

```json
{
  "problems": [...],
  "progress": {
    "题号": {
      "status": "pass",
      "date": "2024-01-15"
    }
  },
  "study_plan": {
    "to_review": [],
    "today": [],
    "knowledge_notes": []
  }
}
```

## progress 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `pass`（独立完成）或 `need_review`（需复习） |
| `date` | string | 完成日期 YYYY-MM-DD |

## study_plan 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `to_review` | array | 待复习题目列表 |
| `today` | array | 今日待做题目列表 |
| `knowledge_notes` | array | 知识点备忘 |

### to_review 元素格式

```json
{
  "id": "322",
  "name": "Coin Change",
  "reason": "思路不清晰",
  "plan": "明天复习"
}
```

### knowledge_notes 元素格式

```json
{
  "concept": "滑动窗口",
  "understanding": "适用于连续子数组问题，可变窗口需要收缩left指针"
}
```

## 自动序列触发条件

### 每日目标完成

当 progress 中完成日期为今天的题目达到每日目标时：

1. 告知用户"今日目标已完成！"
2. Git 提交推送（如果不是 git 仓库则跳过）
3. 更新 Todoist：搜索今日到期任务，添加评论，标记完成
4. 检查学习计划

### 收工序列

当用户说 `收工` / `完成` / `结束了` 时：

1. Git 提交推送
2. 更新 Todoist（如有匹配任务）
3. 检查学习计划，确认今日待做是否完成