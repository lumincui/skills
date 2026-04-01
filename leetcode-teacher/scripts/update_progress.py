#!/usr/bin/env python3
"""
更新 README.md 进度表格
用法: python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]
示例: python3 update_progress.py 322 "Coin Change" dp pass
示例: python3 update_progress.py 322 "Coin Change" dp review

状态: pass/review
"""

import sys
import os
from datetime import date

README_PATH = "README.md"

TABLE_HEADER = """| 题号 | 题目名 | 类型 | 状态 | 完成日期 |
|------|--------|------|------|----------|
"""

STATUS_MAP = {
    "pass": "✅ 通过",
    "review": "🔄 需复习",
    "✅ 通过": "✅ 通过",
    "🔄 需复习": "🔄 需复习",
}


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


def find_problem(problems, num):
    for i, p in enumerate(problems):
        if p[0] == num:
            return i
    return -1


def main():
    if len(sys.argv) < 5:
        print(
            "❌ 用法: python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]"
        )
        print("   状态: pass (通过) / review (需复习)")
        sys.exit(1)

    num = sys.argv[1]
    name = sys.argv[2]
    category = sys.argv[3]
    status_input = sys.argv[4]
    status = STATUS_MAP.get(status_input, status_input)
    completed_date = sys.argv[5] if len(sys.argv) > 5 else str(date.today())

    if status_input not in STATUS_MAP:
        print(f"❌ 未知状态: {status_input}，使用 pass 或 review")
        sys.exit(1)

    if os.path.exists(README_PATH):
        with open(README_PATH, "r") as f:
            content = f.read()
        problems = parse_table(content) if "题号" in content else []
    else:
        content = ""
        problems = []

    idx = find_problem(problems, num)
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

    print(f"✅ {action}: {num} {name} [{status}]")
    print(f"   目录: {category}/")
    print(f"   日期: {completed_date}")


if __name__ == "__main__":
    main()
