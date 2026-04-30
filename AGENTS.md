# Agents 工作规范

## Skill 更新流程

更新、优化 skills 的时候在 `$pwd`（当前工作目录）执行，而不是 skills 实际加载的目录。

### 更新步骤

1. 加载 skill-creator
2. 在 `$pwd` 执行 skill 更新
3. 更新后提交并推送
