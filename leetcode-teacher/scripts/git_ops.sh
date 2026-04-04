#!/bin/bash
# Git operations for LeetCode practice sessions
# Usage: source this script or call individual functions

git_add_commit_push() {
    local message="${1:-chore: complete LeetCode session ($(date +%Y-%m-%d))}"
    git add .
    git commit -m "$message"
    git push
}

git_check_status() {
    git status
}

# Auto-commit for daily 3 problems completion
git_daily_commit() {
    local message="chore: complete daily 3 LeetCode problems ($(date +%Y-%m-%d))"
    git_add_commit_push "$message"
}
