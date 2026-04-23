#!/bin/bash
# Todoist operations for LeetCode practice
# Requires: td CLI tool (Todoist CLI)

CONFIG_PATH=".leetcode.json"

get_todoist_enabled() {
    if [ -f "$CONFIG_PATH" ]; then
        python3 -c "import json; print(json.load(open('$CONFIG_PATH')).get('todoist_enabled', False))" 2>/dev/null || echo "false"
    else
        echo "false"
    fi
}

find_leetcode_tasks() {
    td task list --all --json 2>/dev/null | python3 -c "
import sys, json, re
from datetime import datetime, timedelta

keywords = ['leetcode', '刷题']
pattern = '|'.join(keywords)
case_insensitive = re.compile(pattern, re.IGNORECASE)

tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    if not results:
        print('No tasks found')
        sys.exit(0)
    
    found = False
    for task in results:
        content = task.get('content', '')
        if case_insensitive.search(content):
            due = task.get('due')
            due_str = due.get('date', '') if due else ''
            due_date = due_str.split('T')[0] if due_str else ''
            
            if due_date and due_date >= tomorrow:
                continue
            
            is_recurring = '🔄' if due and due.get('isRecurring') else ''
            status = '⚠️ OVERDUE' if due_date and due_date < tomorrow else ''
            print(f\"{task['id']} | {due_date} {is_recurring} {status} | {content}\")
            found = True
    
    if not found:
        print('No matching tasks found')
except json.JSONDecodeError:
    print('Error: Failed to parse Todoist response')
    sys.exit(1)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"
}

# Add comment to task and mark complete
# Usage: complete_leetcode_task <task_id> <commit_url>
complete_leetcode_task() {
    local task_id="$1"
    local commit_url="$2"
    
    enabled=$(get_todoist_enabled)
    if [ "$enabled" != "True" ] && [ "$enabled" != "true" ]; then
        return 0
    fi
    
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
