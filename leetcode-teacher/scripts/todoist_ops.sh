#!/bin/bash
# Todoist operations for LeetCode practice
# Requires: td CLI tool (Todoist CLI)

# Find today's LeetCode tasks (keywords: leetcode, lc, 算法, 刷题)
find_today_leetcode_tasks() {
    td today | grep -E "leetcode|lc|算法|刷题" || echo "No matching tasks found"
}

# Add comment to task and mark complete
# Usage: complete_leetcode_task <task_id> <commit_url>
complete_leetcode_task() {
    local task_id="$1"
    local commit_url="$2"
    
    if [ -n "$task_id" ]; then
        td comment add "$task_id" "LeetCode练习完成！$commit_url"
        td done "$task_id"
    fi
}

# Get commit URL for commenting
get_commit_url() {
    git remote get-url origin 2>/dev/null | sed 's/\.git$//' | tr -d '\n'
    echo "/commit/$(git rev-parse HEAD)"
}
