#!/usr/bin/env python3
"""
完成一道 LeetCode 题目：更新进度、关闭 Todoist 任务、提交 git
用法: python3 finish_problem.py <题号> <题目名> <类型> <状态>
示例: python3 finish_problem.py 322 "Coin Change" dp pass
示例: python3 finish_problem.py 322 "Coin Change" dp review

状态: pass (通过) / review (需复习)
"""

import sys
import os
import subprocess
import json
from datetime import date

README_PATH = "README.md"
TODOIST_PROJECT = "Inbox"  # 固定的 Todoist 项目名

STATUS_MAP = {
    "pass": "✅ 通过",
    "review": "🔄 需复习",
}

TABLE_HEADER = """| 题号 | 题目名 | 类型 | 状态 | 完成日期 |
|------|--------|------|------|----------|
"""


def parse_table(content):
    lines = content.strip().split("\n")
    problems = []
    for line in lines[2:]:
        if line.strip().startswith("|") and "------" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4 and parts[0].isdigit():
                problems.append(parts)
    return problems


def format_table(problems):
    lines = [TABLE_HEADER.strip()]
    for p in problems:
        lines.append(f"| {p[0]} | {p[1]} | {p[2]} | {p[3]} | {p[4]} |")
    return "\n".join(lines)


def update_readme(num, name, category, status, completed_date):
    if os.path.exists(README_PATH):
        with open(README_PATH, "r") as f:
            content = f.read()
        problems = parse_table(content) if "题号" in content else []
    else:
        content = ""
        problems = []

    idx = -1
    for i, p in enumerate(problems):
        if p[0] == num:
            idx = i
            break

    if idx >= 0:
        problems[idx] = [num, name, category, status, completed_date]
        action = "更新"
    else:
        problems.append([num, name, category, status, completed_date])
        problems.sort(key=lambda x: int(x[0]))
        action = "添加"

    new_content = format_table(problems)

    if content:
        header_end = content.find("| 题号 |")
        if header_end > 0:
            new_content = content[:header_end] + new_content
        else:
            new_content = f"# LeetCode 刷题进度\n\n{new_content}\n"
    else:
        new_content = f"# LeetCode 刷题进度\n\n{new_content}\n"

    with open(README_PATH, "w") as f:
        f.write(new_content)

    print(f"✅ README: {action} {num} {name} [{status}]")
    return True


def complete_todoist_task():
    try:
        result = subprocess.run(
            ["td", "task", "list", "--project", TODOIST_PROJECT, "--json"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            print(f"⚠️ Todoist: 无法获取项目列表")
            return False

        data = json.loads(result.stdout)
        tasks = data.get("results", [])
        for task in tasks:
            content = task.get("content", "")
            if "leetcode" in content.lower():
                task_id = task.get("id")
                subprocess.run(["td", "task", "complete", task_id], timeout=10)
                print(f"✅ Todoist: 已完成 '{content}'")
                return True

        print(f"⚠️ Todoist: 未找到 LeetCode 任务")
        return False
    except Exception as e:
        print(f"⚠️ Todoist: 执行失败 - {e}")
        return False


def git_commit(num, name, category, status):
    status_emoji = "✅" if "通过" in status else "🔄"
    commit_msg = f"{status_emoji} LeetCode {num}: {name} [{category}]"

    try:
        subprocess.run(["git", "add", "-A"], capture_output=True, timeout=10)
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print(f"✅ Git: 提交成功 '{commit_msg}'")
            return True
        elif (
            "nothing to commit" in result.stdout or "nothing to commit" in result.stderr
        ):
            print(f"⚠️ Git: 没有变更需要提交")
            return True
        else:
            print(f"⚠️ Git: 提交失败 - {result.stderr or result.stdout}")
            return False
    except Exception as e:
        print(f"⚠️ Git: 执行失败 - {e}")
        return False


def main():
    if len(sys.argv) < 5:
        print("❌ 用法: python3 finish_problem.py <题号> <题目名> <类型> <状态>")
        print("   状态: pass (通过) / review (需复习)")
        sys.exit(1)

    num = sys.argv[1]
    name = sys.argv[2]
    category = sys.argv[3]
    status_input = sys.argv[4]
    status = STATUS_MAP.get(status_input, status_input)
    completed_date = str(date.today())

    if status_input not in STATUS_MAP:
        print(f"❌ 未知状态: {status_input}，使用 pass 或 review")
        sys.exit(1)

    print(f"\n🎉 完成题目: {num}. {name}")
    print(f"   类型: {category} | 状态: {status}")
    print()

    update_readme(num, name, category, status, completed_date)
    complete_todoist_task()
    git_commit(num, name, category, status)

    print(f"\n✨ 完成!")


if __name__ == "__main__":
    main()
