---
name: opinion-miner
description: Analyze community opinions from forums and comment sections. Scrapes comments from Bilibili, Reddit, or GitHub Issues, clusters them by semantic similarity, and extracts the core arguments, debates, and viewpoints. Produces a structured report showing what the community actually thinks — not just a summary of comments, but the underlying positions people hold and where the real disagreements are. Use this skill when the user wants to understand public opinion on a topic, find the main points of contention in a discussion, or do competitive/event research from community sources. Triggers include requests to "analyze comments", "what are people saying about X", "summarize the debate", "find the key arguments", "what's the community consensus", or any task involving opinion extraction from forum or comment data.
---

# Opinion Miner

Analyze community comments to surface the core arguments and viewpoints people actually hold.

## When to use this skill

Use this skill when the user wants to understand what a community thinks about a topic — not just "what they said" but "what positions they hold and where they disagree." The goal is to move from raw comments to structured insight.

Typical triggers:
- "What are people saying about X on Reddit/Bilibili/GitHub?"
- "Analyze the comments on this post"
- "What's the main point of disagreement here?"
- "Help me understand the community's stance on this issue"
- "做一下这个话题的舆情分析"

## Supported sources

| Source | Scraping method |
|--------|----------------|
| Bilibili video comments | `agent-browser` (requires JS rendering) or Bilibili API via `webfetch` |
| Reddit threads | `webfetch` on `old.reddit.com` or Reddit JSON API (`/.json`) |
| GitHub Issues (comments) | GitHub API via `webfetch` (`/repos/owner/repo/issues/N/comments`) |

If the user provides a URL, identify the source platform and use the appropriate method.

## Workflow

### Step 1: Scrape comments

Collect all comments from the given URL. Save raw data to `comments_raw.json` with this structure:

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

**Platform-specific scraping:**

**Bilibili:** Try the comment API first — `https://api.bilibili.com/x/v2/reply/main?type=1&oid={video_id}&mode=3&ps=20&pn={page}`. Paginate until comments are exhausted. If API fails, fall back to `agent-browser`:
```
agent-browser open "https://www.bilibili.com/video/BVxxxxx" && agent-browser wait --load networkidle
agent-browser snapshot -i
```
Then scroll and extract comments via DOM snapshots.

**Reddit:** Use JSON API — append `.json` to any Reddit URL:
```
webfetch "https://www.reddit.com/r/subreddit/comments/postid.json?limit=500"
```
Parse the nested tree structure. Include replies as nested comments but flatten for clustering (replies often restate the parent argument).

**GitHub Issues:** Use the GitHub API:
```
webfetch "https://api.github.com/repos/owner/repo/issues/issue_number/comments?per_page=100"
```
Paginate with `&page=N`. Also fetch the issue body — it frames the debate.

### Step 2: Preprocess

Clean the raw comments before analysis:
1. Remove bot comments, spam, and empty/meaningless comments (e.g. "+1", "bump", single emoji)
2. If over 500 comments, sample strategically — take top-voted comments + a random sample of mid-tier to capture minority viewpoints
3. Keep metadata (likes, author) — it helps gauge which viewpoints are popular

Save cleaned data to `comments_cleaned.json`.

### Step 3: Semantic clustering

Read all cleaned comments and group them by semantic similarity — comments that express the same underlying argument go in the same cluster, even if they use very different wording.

**How to cluster effectively:**
- Read comments in batches (50-100 at a time) and do a first-pass grouping
- Merge batches by comparing clusters across passes — same argument = same cluster
- Each cluster should represent a distinct **position** or **argument**, not just a topic
- Name each cluster with a concise statement of its core argument (not a topic label)

**Cluster naming convention:** Each cluster name should be a claim, not a topic.
- Good: "This feature breaks backward compatibility and should be opt-in"
- Bad: "Backward compatibility concerns"

Save clustering results to `clusters.json`:

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

### Step 4: Debate analysis

For each cluster, determine:
1. **Position**: What exactly is this group arguing?
2. **Evidence**: What facts, experiences, or logic do they cite?
3. **Strength of conviction**: Are they assertive or tentative? Use language cues and like counts.
4. **Relationship to other clusters**: Is this an opposing view to another cluster? A nuance or extension?

Then synthesize across clusters to identify:
- **Core debate axis**: The fundamental disagreement (e.g., "security vs. convenience", "innovation vs. stability")
- **Consensus points**: Things most clusters agree on
- **Polarizing points**: Where the community is sharply divided
- **Minority viewpoints**: Positions held by few but with strong reasoning

### Step 5: Generate report

Output a Markdown report using this template:

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

If the user requests JSON output as well, also save the structured data.

## Tips for better analysis

- Don't just count votes — a highly-upvoted minority opinion may matter more than a low-engagement majority position
- Pay attention to **how** people argue, not just what they say. Sarcasm, emotional language, and defensiveness signal strong positions
- Look for **implicit** arguments — sometimes the real disagreement is unstated (e.g., people arguing about implementation details may actually disagree about priorities)
- Cross-reference with replies — a reply that heavily disagrees with a parent comment reveals the debate structure
- If comments are in multiple languages, cluster by argument regardless of language, then note language distribution in each cluster
