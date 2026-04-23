#!/usr/bin/env python3
"""
获取 LeetCode 今日状态和建议下一步
用法: python3 count_today_problems.py
返回: JSON 格式状态和建议
"""

import os
import json
from datetime import datetime

README_PATH = "README.md"
CONFIG_PATH = ".leetcode.json"


def load_config():
    """从 .leetcode.json 读取配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {
        "daily_goal": 3,
        "todoist_enabled": False,
        "mode": "normal",
        "initialized": False,
    }


def count_today_problems():
    """统计今日完成的题目数量"""
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(README_PATH):
        return 0

    with open(README_PATH, "r") as f:
        content = f.read()

    count = 0
    lines = content.strip().split("\n")
    for line in lines[2:]:
        if line.strip().startswith("|") and "------" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 5 and parts[0].isdigit():
                date = parts[4]
                if date == today:
                    if "通过" in parts[3] or "需复习" in parts[3]:
                        count += 1

    return count


def get_status():
    """获取当前状态和建议下一步"""
    config = load_config()
    daily_goal = config.get("daily_goal", 3)
    completed = count_today_problems()
    remaining = max(0, daily_goal - completed)

    status = {
        "completed": completed,
        "daily_goal": daily_goal,
        "remaining": remaining,
        "goal_reached": completed >= daily_goal,
        "initialized": config.get("initialized", False),
        "mode": config.get("mode", "normal"),
        "todoist_enabled": config.get("todoist_enabled", False),
    }

    if completed == 0 and not config.get("initialized", False):
        status["next_step"] = "initialize"
    elif completed >= daily_goal:
        status["next_step"] = "done"
    elif completed > 0:
        status["next_step"] = "continue"
    else:
        status["next_step"] = "start"

    return status


def main():
    status = get_status()
    print(json.dumps(status, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
