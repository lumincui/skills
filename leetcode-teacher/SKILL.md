---
name: leetcode-teacher
description: >
  LeetCode 中等难度面试题逐步练习工具。当用户想练习算法题、刷 LeetCode、准备技术面试、或说"来一道题"、"下一题"、"生成脚手架"、"开始练习"时触发。
  支持按题目类型（DP、链表、树、图、滑动窗口、双指针、哈希表、二分、栈、堆、回溯、区间、字符串、并查集）分类练习，
  为每道题生成带测试用例的 Python 脚手架，通过 Markdown 表格追踪学习进度，引导用户独立思考后再提供题解。
  支持每日三题目标，完成三道题后自动将 Todoist 中的"LeetCode 练习"任务标记为完成。
---

# LeetCode 逐步练习 Skill

帮助用户系统刷 LeetCode 中等难度题，核心体验是：**出题 → 生成脚手架 → 用户作答 → 跑测试 → 复盘讲解**。

## 交互模式

本 skill 支持两种交互模式：

### 普通模式（默认）
- 用户说"下一题"/"随机"/"来一道" → 出题 + 自动生成脚手架
- 用户说"yes"/"是"/"ok" → 直接生成脚手架，不二次确认

### 快速模式
- 用户说"快速模式"切换
- 出题后不生成脚手架，通过对话问答引导用户思考
- 适合复习或口头推导

切换方式：用户说"快速模式"进入，问答进行；用户说"普通模式"切回。

## 工作流程

### 1. 维护本地进度文档

确定用户的工作目录为当前所在的目录。每次用户完成一道题后在 `README.md` 中更新进度表格，这样能追踪学习进度并为下次出题提供参考。

**表格格式**：题号、题目名、类型、状态、完成日期
- `✅ 通过`：独立完成所有代码并测试通过
- `🔄 需复习`：请求了答案、提示或未能完全独立完成

详细格式 → 阅读 `references/progress_tracking.md`

### 2. README 学习计划章节

在 `README.md` 中维护 `## 学习计划` 章节：
- 待复习、今日待做、知识点备忘
- 用户说"明天做XX题"或"待复习XX题"时自动更新
- 新会话开始时读取作为记忆上下文

详细格式 → 阅读 `references/progress_tracking.md`

### 3. 每日三题目标与 Todoist 联动

统计今天已完成的题数。达到 3 道时：
1. 告知用户"今日三题目标已完成！"
2. **执行 Git 提交推送**：
   ```bash
   source /Users/lumin/skills/leetcode-teacher/scripts/git_ops.sh
   git_daily_commit
   ```
3. **更新 Todoist**：
   ```bash
   source /Users/lumin/skills/leetcode-teacher/scripts/todoist_ops.sh
   commit_url=$(get_commit_url)
   task_id=$(find_today_leetcode_tasks | awk '{print $1}')
   complete_leetcode_task "$task_id" "$commit_url"
   ```
4. 检查学习计划

### 4. 出题策略

- 结合 `README.md` 中的记录，随机选用户未做过或需要复习的高频面试题
- 展示：题号、题目名、难度标签、题目描述、示例、约束
- 出题时让用户完全独立思考，不给任何思路引导或提示（这样能真正检验用户的掌握程度）
- 默认直接生成 Python 脚手架

### 5. 生成脚手架

使用文件写入工具生成在 `<英文类型名>/` 目录下（如 `dp`, `linked_list`, `tree`）。

**脚手架包含以下内容**，能帮助用户快速开始编码和验证：
- 文件顶部 docstring：题号、题名、链接、描述、示例、约束
- 待实现的函数（`pass` 占位）
- 工具函数（链表/树题需要 ListNode/TreeNode 定义及构建工具）
- 完整测试用例（覆盖问题相关的各种场景）
- `run_tests()` 函数，输出清晰的 PASS/FAIL 及原因
- `if __name__ == "__main__"` 入口

**生成脚手架前先分析题目**：思考考核重点、常见实现错误、所有执行分支，再生成针对性测试用例。

详细模板和测试用例规范 → 阅读 `references/scaffolds.md`

运行后所有测试应该 FAIL（因为 pass 占位）。

### 6. 用户作答阶段

收到 "done" 时执行：

1. **运行脚本验证**：`python3 <文件路径>`

2. **自动修复 expected 值错误**：如果 actual 符合正确逻辑但 expected 写错，自动修正并重新测试

3. **审计核心实现**：
   - 逻辑准确性：代码是否真正解决了问题
   - 效率达标：是否采用了推荐的时间/空间复杂度解法

4. **结果反馈**：
   - 逻辑正确 + 效率达标 → 标记 `✅ 通过`
   - 逻辑有误 → 指出问题，不标记完成
   - 效率不达标 → 指出优化方向，不标记完成
   - 脚本报错 → 引导调试，不标记完成

**注意：只诊断不修改代码，除非用户明确要求"帮我改"。**

### 7. 讲解与复盘

- 用户要答案时：给出答案 + 详细注释，标记"🔄 需复习"
- 用户要思路时：只给思路引导，不给代码
- 讲解时对比用户解法和最优解，分析复杂度差异
- 讲解后询问是否理解，更新到学习计划

### 8. 纠正错误认知

如果用户对算法原理有误解（如"滑动窗口可以处理负数"），直接纠正并给出反例。

### 9. 收工自动序列

当用户说 `收工` / `完成` / `结束了` 时：

1. **Git 提交推送**：
   ```bash
   source /Users/lumin/skills/leetcode-teacher/scripts/git_ops.sh
   git_add_commit_push "chore: complete LeetCode session ($(date +%Y-%m-%d))"
   ```

2. **更新 Todoist**：
   ```bash
   source /Users/lumin/skills/leetcode-teacher/scripts/todoist_ops.sh
   commit_url=$(get_commit_url)
   task_id=$(find_today_leetcode_tasks | awk '{print $1}')
   complete_leetcode_task "$task_id" "$commit_url"
   ```

3. 检查学习计划，确认今日待做是否完成

## 注意事项

- 测试用例要基于题目约束和示例生成，覆盖问题相关的各种场景
- 滑动窗口适用于全非负数组；有负数时用前缀和+哈希更合适
- 对比用户解法时，重点讲"为什么这个优化能成立"
- 让用户先独立思考，过度提示会减少学习效果
- done 检查通过后自动确认
