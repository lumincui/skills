---
name: opinion-miner
description: Analyze community opinions from forums and comment sections. Scrapes comments from Bilibili, Reddit, or GitHub Issues, clusters them by semantic similarity, and extracts the core arguments, debates, and viewpoints. Produces a structured report showing what the community actually thinks — not just a summary of comments, but the underlying positions people hold and where the real disagreements are. Use this skill when the user wants to understand public opinion on a topic, find the main points of contention in a discussion, or do competitive/event research from community sources. Triggers include requests to "analyze comments", "what are people saying about X", "summarize the debate", "find the key arguments", "what's the community consensus", or any task involving opinion extraction from forum or comment data.
---

# 舆情分析工具 (Opinion Miner)

分析社区评论，挖掘用户真正的核心观点和立场。

## 何时使用此技能

当用户想要了解社区对某个话题的看法时使用此技能——不仅仅是"他们说了什么"，而是"他们持有什么样的立场以及在哪里存在分歧"。目标是将原始评论转化为结构化的洞察。

典型触发场景：
- "大家对 X 在 Reddit/Bilibili/GitHub 上怎么说？"
- "分析一下这个帖子的评论"
- "这里主要的分歧点是什么？"
- "帮我了解一下社区对这个问题的态度"
- "做一下这个话题的舆情分析"

## 支持的数据来源

| 数据来源 | 爬取方式 |
|---------|---------|
| Bilibili 视频评论 | `agent-browser`（需要 JS 渲染）或通过 `webfetch` 调用 Bilibili API |
| Reddit 帖子 | 通过 `webfetch` 访问 `old.reddit.com` 或 Reddit JSON API (`/.json`) |
| GitHub Issues 评论 | 通过 `webfetch` 调用 GitHub API (`/repos/owner/repo/issues/N/comments`) |

如果用户提供了 URL，先识别平台类型，然后使用相应的方法进行爬取。

## 工作流程

### 步骤 1: 爬取评论

从给定的 URL 收集所有评论。将原始数据保存到 `comments_raw.json`，使用以下结构：

```json
[
  {
    "id": "unique-id",
    "author": "username",
    "text": "comment body",
    "likes": 0,
    "replies": [],
    "timestamp": "2026-01-15T10:30:00Z"
  }
]
```

**平台特定的爬取方式：**

**Bilibili：** 先尝试评论 API — `https://api.bilibili.com/x/v2/reply/main?type=1&oid={video_id}&mode=3&ps=20&pn={page}`。分页爬取直到评论耗尽。如果 API 失败，回退到 `agent-browser`：
```
agent-browser open "https://www.bilibili.com/video/BVxxxxx" && agent-browser wait --load networkidle
agent-browser snapshot -i
```
然后滚动页面并通过 DOM 快照提取评论。

**Reddit：** 使用 JSON API — 在任意 Reddit URL 末尾添加 `.json`：
```
webfetch "https://www.reddit.com/r/subreddit/comments/postid.json?limit=500"
```
解析嵌套的树状结构。将回复作为嵌套评论包含在内，但在聚类时将其展平（回复通常会重复父评论的观点）。

**GitHub Issues：** 使用 GitHub API：
```
webfetch "https://api.github.com/repos/owner/repo/issues/issue_number/comments?per_page=100"
```
使用 `&page=N` 进行分页。同时获取 issue 正文——它定义了讨论的背景。

### 步骤 2: 预处理

在分析之前清理原始评论：
1. 移除机器人评论、垃圾信息以及无意义评论（如 "+1"、"bump"、单个表情）
2. 如果评论超过 500 条，战略性采样——选取高赞评论 + 随机抽取中热度评论，以捕捉少数派观点
3. 保留元数据（点赞数、作者）——有助于判断哪些观点更受欢迎

将清理后的数据保存到 `comments_cleaned.json`。

### 步骤 3: 语义聚类

阅读所有清理后的评论，按语义相似性进行分组——表达相同底层论点的评论归为一组，即使措辞完全不同。

**高效聚类的方法：**
- 批量阅读评论（每次 50-100 条）并进行第一轮分组
- 通过对比各批次之间的聚类结果进行合并——相同论点 = 同一聚类
- 每个聚类应该代表一个独特的**立场**或**论点**，而不仅仅是主题
- 用简洁的论点陈述来命名每个聚类（而不是主题标签）

**聚类命名规范：** 每个聚类名称应该是一个论点，而不是主题。
- 好的例子："此功能破坏向后兼容性，应该改为可选"
- 不好的例子："向后兼容性担忧"

将聚类结果保存到 `clusters.json`：

```json
[
  {
    "cluster_id": 1,
    "name": "Concise argument statement",
    "comment_count": 45,
    "representative_comments": ["full text of 2-3 best examples"],
    "support_ratio": 0.7,
    "sample_comment_ids": ["id1", "id2", "id3"]
  }
]
```

### 步骤 4: 辩论分析

针对每个聚类，确定以下内容：
1. **立场**：这个群体到底在争论什么？
2. **论据**：他们引用了什么事实、经验或逻辑？
3. **信念强度**：他们是肯定的还是犹豫的？利用语言线索和点赞数进行判断
4. **与其他聚类的关系**：这是对另一个聚类的反对观点吗？还是补充或延伸？

然后综合所有聚类进行识别：
- **核心争论轴**：根本性的分歧（如"安全 vs. 便利"、"创新 vs. 稳定"）
- **共识点**：大多数聚类都同意的点
- **分歧点**：社区存在明显对立的点
- **少数派观点**：持有者少但论据有力的观点

### 步骤 5: 生成报告

使用以下模板输出 Markdown 报告：

```markdown
# [Topic] 社区观点分析

> 数据来源: [URL]
> 评论总数: N (分析了 M 条有效评论)
> 生成时间: YYYY-MM-DD

## 摘要

[2-3 句话概括社区的整体态度和主要分歧]

## 核心争论点

[描述最核心的 1-2 个分歧轴，解释为什么这是争论的焦点]

## 观点聚类

### 观点 1: [论点陈述]
- **占比**: ~X% (约 N 条评论)
- **核心论据**: [支持这个观点的主要理由]
- **典型评论**: [1-2 条代表性原文]
- **热度**: [点赞/支持度]

### 观点 2: [论点陈述]
...

## 共识与分歧

### 共识
- [大多数人都同意的点]

### 分歧
- [主要对立点，哪些观点之间存在直接冲突]

## 少数派观点
- [持有者少但论据有力的观点，值得关注]

## 情绪分析
- **整体情绪**: [正面/负面/中立/混合]
- **情绪强度**: [激烈/温和]
- **情绪变化趋势**: [如有时间线数据]
```

如果用户也请求 JSON 输出，请同时保存结构化数据。

## 分析技巧

- 不要只数投票数——高赞的少数派观点可能比低参与度的多数派立场更重要
- 注意人们**如何**争论，而不仅仅是他们说了什么。讽刺、情绪化语言和防御性表态都表明强烈的立场
- 寻找**隐含的**论点——有时真正的分歧并未明确说出（例如，人们争论实现细节实际上可能是在争论优先级）
- 与回复交叉参考——一个强烈反对父评论的回复揭示了辩论结构
- 如果评论涉及多种语言，按论点进行聚类（不考虑语言），然后在每个聚类中注明语言分布
