#!/usr/bin/env python3
"""
从 README.md 迁移题目数据到 .leetcode.json
用法: python3 migrate_from_markdown.py
"""

import os
import json
import re
from datetime import datetime

README_PATH = "README.md"
CONFIG_PATH = ".leetcode.json"


def parse_readme_problems():
    """解析 README.md 中的题目表格"""
    if not os.path.exists(README_PATH):
        return []

    with open(README_PATH, "r") as f:
        content = f.read()

    problems = []
    lines = content.strip().split("\n")
    in_table = False

    for line in lines:
        line = line.strip()
        if line.startswith("| 题号 |") or line.startswith("|题号|"):
            in_table = True
            continue
        if in_table and "------" in line:
            continue
        if in_table and line.startswith("|") and "------" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 5 and parts[0].isdigit():
                num = parts[0]
                name = parts[1]
                category = parts[2].lower().replace("_", "").replace(" ", "")
                status_raw = parts[3]
                date_str = parts[4]

                status = "pass" if "通过" in status_raw else "review"

                if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                    problems.append(
                        {
                            "id": num,
                            "name": name,
                            "category": category,
                            "status": status,
                            "date": date_str,
                        }
                    )

    return problems


def load_config():
    """读取现有配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {
        "todoist_enabled": False,
        "daily_goal": 3,
        "mode": "normal",
        "initialized": False,
        "problems": [],
    }


def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def migrate():
    """执行迁移"""
    problems = parse_readme_problems()

    if not problems:
        print("No problems found in README.md")
        return 0

    config = load_config()

    existing_ids = {p["id"] for p in config.get("problems", [])}
    new_problems = [p for p in problems if p["id"] not in existing_ids]

    if "problems" not in config:
        config["problems"] = []

    config["problems"].extend(new_problems)
    save_config(config)

    print(f"Migrated {len(new_problems)} problems from README.md")
    return len(new_problems)


if __name__ == "__main__":
    migrate()
