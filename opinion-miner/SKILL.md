---
name: opinion-miner
description: >
  Community opinion mining skill. Use when 用户想分析 Bilibili、Reddit、GitHub Issues/PR、论坛或评论区里“大家怎么看”，需要抓取/整理评论、语义聚类、提取主要立场、争论轴、共识、少数派观点和情绪强度。触发词包括“分析评论/舆情分析/大家怎么说/社区共识/主要争议/观点聚类/总结 debate/what are people saying”。输出结构化报告，而不是普通摘要。
---

# Opinion Miner

## Overview

这个 skill 用于从社区评论中挖掘 **真实观点结构**。目标不是把评论压缩成摘要，而是回答：

```text
有哪些立场？各自的核心论据是什么？真正的分歧轴在哪里？哪些观点代表多数/少数但重要？
```

---

## Activation Triggers

使用本 skill 当用户说：

- “分析这个评论区 / 帖子 / issue 讨论”
- “大家对 X 怎么看？”
- “社区共识是什么？”
- “主要争议点是什么？”
- “把这些评论聚类一下”
- “分析 Reddit/B 站/GitHub 上的观点”
- “做一下舆情分析”

不要用于：

- 单篇文章摘要；
- 只有少量评论且用户只要简单总结；
- 需要严肃民调结论但数据来源并非代表性样本。此时必须强调样本偏差。

---

## Workflow

### Phase 1: Identify Platform and Scope

先识别：

| Platform | Input | Fetch strategy |
|---|---|---|
| Bilibili | `bilibili.com/video/BV...` | 解析 bvid → video info → comment API；失败则 browser |
| Reddit | `reddit.com/r/.../comments/...` | URL 后加 `.json?limit=500` |
| GitHub Issue | `/issues/<n>` | issue body + comments API |
| GitHub PR | `/pull/<n>` | PR body + review comments + issue comments |
| Generic forum | HTML page | browser/web extract，必要时分页 |

如果用户没有给 URL，先问要分析哪个来源；不要凭空分析“社区”。

### Phase 2: Collect Comments

将原始数据保存为 `comments_raw.json`（如任务需要落盘）：

```json
[
  {
    "id": "unique-id",
    "author": "username",
    "text": "comment body",
    "likes": 0,
    "replies": [],
    "timestamp": "2026-01-15T10:30:00Z",
    "url": "source url"
  }
]
```

平台细节：

- **Bilibili**：优先 API：`https://api.bilibili.com/x/v2/reply/main?type=1&oid={aid}&mode=3&ps=20&pn={page}`；需要先通过 bvid 获取 aid/oid。
- **Reddit**：使用 JSON：`https://www.reddit.com/r/sub/comments/postid.json?limit=500`；展平评论树，但保留 parent relation。
- **GitHub Issues**：同时读取 issue body 和 comments：`/repos/{owner}/{repo}/issues/{n}/comments?per_page=100&page=N`。
- **GitHub PR**：还要读取 review comments：`/pulls/{n}/comments`，因为技术争论常在代码 review 线程里。

### Phase 3: Clean and Sample

清理规则：

1. 去除 bot、重复、纯表情、`+1`、`bump` 等低信息内容；
2. 保留高赞/高回复评论；
3. 如果评论超过 500 条：
   - 高赞 top N；
   - 高回复线程；
   - 随机采样中低热度评论；
   - 明确保留少数派样本。
4. 保存或记录 `comments_cleaned.json`。

注意：不要把点赞数直接等同于真实民意。平台、排序和幸存者偏差都要说明。

### Phase 4: Semantic Clustering

按 **论点** 聚类，不按关键词聚类。

好聚类名：

```text
“该功能破坏向后兼容性，应该改为可选”
```

坏聚类名：

```text
“兼容性问题”
```

每个 cluster 记录：

```json
{
  "cluster_id": 1,
  "claim": "argument-style cluster name",
  "stance": "support / oppose / mixed / meta",
  "comment_count": 45,
  "support_ratio": 0.32,
  "representative_comments": ["..."],
  "evidence": ["facts/experiences people cite"],
  "counterarguments": ["..."],
  "confidence": "high/medium/low"
}
```

### Phase 5: Debate Analysis

提炼：

- **核心争论轴**：例如 “稳定性 vs 创新速度”、“成本 vs 体验”、“开发者偏好 vs 用户需求”。
- **共识点**：跨立场都承认的事实或问题。
- **分歧点**：直接冲突的观点。
- **少数派但强论据**：人数少但证据质量高。
- **情绪强度**：愤怒、焦虑、兴奋、讽刺、疲惫等。
- **群体差异**：用户、维护者、专业从业者、新手、重度用户。

---

## Report Template

```markdown
# [Topic] 社区观点分析

> 数据来源: [URL]
> 样本: 原始 N 条，清洗后 M 条
> 生成时间: YYYY-MM-DD
> 重要限制: [平台偏差/样本偏差/抓取限制]

## TL;DR
- [核心结论 1]
- [核心结论 2]
- [最大分歧轴]

## 核心争论轴

## 观点聚类
### 观点 1: [论点陈述]
- 占比: ~X%
- 代表人群:
- 核心论据:
- 典型评论:
- 反方回应:
- 置信度:

## 共识与分歧

## 少数派但值得关注的观点

## 情绪与语气

## 样本限制

## 可复用洞察 / 下一步建议
```

---

## Analysis Rules

- 不要只按数量排序；高质量少数派观点可能更重要。
- 引用原文时保留语气，但避免泄露敏感个人信息。
- 区分“用户真实痛点”和“发泄情绪”。
- 技术讨论要区分事实、偏好和维护成本。
- 多语言评论按论点合并，在 cluster 中标注语言分布。
- 结论必须带样本限制，尤其 Reddit/Bilibili 不能代表全体用户。

---

## Verification Checklist

- [ ] 是否明确数据来源、样本量、清洗规则？
- [ ] 是否按论点而不是关键词聚类？
- [ ] 是否识别核心争论轴和共识点？
- [ ] 是否保留少数派但强论据？
- [ ] 是否引用代表性评论？
- [ ] 是否说明平台/样本偏差？
- [ ] 报告是否是结构化观点分析，而不只是摘要？
