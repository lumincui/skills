#!/usr/bin/env python3
"""
完成一道 LeetCode 题目：更新进度、关闭 Todoist 任务、提交 git
用法: python3 finish_problem.py <题号> <题目名> <类型> <状态>
示例: python3 finish_problem.py 322 "Coin Change" dp pass
示例: python3 finish_problem.py 322 "Coin Change" dp need_review

状态: pass (通过) / need_review (需复习)
"""

import sys
import os
import subprocess
import json
from datetime import date

LEETCODE_JSON = "leetcode.json"
TODOIST_PROJECT = "Inbox"

STATUS_MAP = {
    "pass": "✅ 通过",
    "need_review": "🔄 需复习",
}


def load_json():
    """从 leetcode.json 读取全部数据"""
    if os.path.exists(LEETCODE_JSON):
        with open(LEETCODE_JSON, "r") as f:
            return json.load(f)
    return {
        "difficulty": "medium",
        "todoist_enabled": False,
        "daily_goal": 3,
        "mode": "normal",
        "initialized": False,
        "problems": [],
        "progress": {},
        "study_plan": {},
    }


def save_json(data):
    """保存到 leetcode.json"""
    with open(LEETCODE_JSON, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_progress_json(num, name, category, status_input, completed_date):
    """更新 leetcode.json 中的 progress"""
    data = load_json()
    progress = data.get("progress", {})

    status = "pass" if status_input == "pass" else "need_review"

    progress[num] = {
        "status": status,
        "date": completed_date,
        "name": name,
        "category": category,
    }

    data["progress"] = progress
    save_json(data)

    print(f"✅ leetcode.json: 更新 {num} {name} [{status}]")


def complete_todoist_task():
    data = load_json()
    if not data.get("todoist_enabled", False):
        return False

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

        result_data = json.loads(result.stdout)
        tasks = result_data.get("results", [])
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
        print("   状态: pass (通过) / need_review (需复习)")
        sys.exit(1)

    num = sys.argv[1]
    name = sys.argv[2]
    category = sys.argv[3]
    status_input = sys.argv[4]
    status = STATUS_MAP.get(status_input, status_input)
    completed_date = str(date.today())

    if status_input not in STATUS_MAP:
        print(f"❌ 未知状态: {status_input}，使用 pass 或 need_review")
        sys.exit(1)

    print(f"\n🎉 完成题目: {num}. {name}")
    print(f"   类型: {category} | 状态: {status}")
    print()

    update_progress_json(num, name, category, status_input, completed_date)
    complete_todoist_task()
    git_commit(num, name, category, status)

    print(f"\n✨ 完成!")


if __name__ == "__main__":
    main()
