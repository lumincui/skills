#!/usr/bin/env python3
"""
统计今日完成的 LeetCode 题目数量
用法: python3 count_today_problems.py
返回: 今日完成题目数量
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


def check_daily_goal():
    """检查是否达到每日目标"""
    config = load_config()
    daily_goal = config.get("daily_goal", 3)
    completed = count_today_problems()
    return completed >= daily_goal, completed, daily_goal


def main():
    count = count_today_problems()
    print(count)


if __name__ == "__main__":
    main()
