#!/usr/bin/env python3
"""
更新 leetcode.json 进度
用法:
  python3 update_progress.py <题号> <状态> [完成日期]
  python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]

示例:
  python3 update_progress.py 322 pass
  python3 update_progress.py 322 need_review
  python3 update_progress.py 322 "Coin Change" dp pass

状态: pass / need_review
"""

import sys
import os
import json
import re
from datetime import date
from pathlib import Path

LEETCODE_JSON = "leetcode.json"
VALID_STATUSES = {"pass", "need_review"}
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROBLEM_LIST = SKILL_DIR / "references" / "problem_list.md"


def load_json():
    if os.path.exists(LEETCODE_JSON):
        with open(LEETCODE_JSON, "r") as f:
            return json.load(f)
    return {"problems": [], "progress": {}, "study_plan": {}}


def save_json(data):
    with open(LEETCODE_JSON, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_name(text):
    return " ".join(part.capitalize() for part in re.split(r"[_\-\s]+", text) if part)


def infer_from_problem_list(num):
    if not PROBLEM_LIST.exists():
        return None

    category = None
    category_pattern = re.compile(r"^###\s+.+\(([^)]+)\)")
    row_pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")

    with PROBLEM_LIST.open("r", encoding="utf-8") as f:
        for line in f:
            category_match = category_pattern.match(line.strip())
            if category_match:
                category = category_match.group(1).strip()
                continue

            row_match = row_pattern.match(line.strip())
            if row_match and row_match.group(1) == num:
                return {
                    "name": row_match.group(2).strip(),
                    "category": category or "uncategorized",
                }
    return None


def infer_from_solution_files(num):
    cwd = Path.cwd()
    patterns = (f"{num}_*.py", f"{int(num):03d}_*.py") if num.isdigit() else (f"{num}_*.py",)

    for pattern in patterns:
        for path in sorted(cwd.glob(f"*/{pattern}")):
            stem = re.sub(rf"^{int(num):03d}_|^{re.escape(num)}_", "", path.stem)
            return {"name": normalize_name(stem), "category": path.parent.name}

    return None


def infer_problem(data, num):
    progress = data.get("progress", {})
    if num in progress:
        current = progress[num]
        if current.get("name") or current.get("category"):
            return {
                "name": current.get("name") or f"LeetCode {num}",
                "category": current.get("category") or "uncategorized",
            }

    for source in (infer_from_solution_files, infer_from_problem_list):
        inferred = source(num)
        if inferred:
            return inferred

    return {"name": f"LeetCode {num}", "category": "uncategorized"}


def usage():
    print("❌ 用法:")
    print("   python3 update_progress.py <题号> <状态> [完成日期]")
    print("   python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]")
    print("   状态: pass (通过) / need_review (需复习)")


def parse_args(argv):
    if len(argv) < 3:
        usage()
        sys.exit(1)

    num = argv[1]
    args = argv[2:]

    if args[0] in VALID_STATUSES:
        status_input = args[0]
        completed_date = args[1] if len(args) > 1 else str(date.today())
        return num, None, None, status_input, completed_date

    if len(args) >= 3 and args[2] in VALID_STATUSES:
        name, category, status_input = args[:3]
        completed_date = args[3] if len(args) > 3 else str(date.today())
        return num, name, category, status_input, completed_date

    usage()
    sys.exit(1)


def main():
    num, name, category, status_input, completed_date = parse_args(sys.argv)

    if status_input not in VALID_STATUSES:
        print(f"❌ 未知状态: {status_input}，使用 pass 或 need_review")
        sys.exit(1)

    data = load_json()
    progress = data.get("progress", {})

    if not name or not category:
        inferred = infer_problem(data, num)
        name = name or inferred["name"]
        category = category or inferred["category"]

    if num in progress:
        action = "更新"
    else:
        action = "添加"

    progress[num] = {
        "status": status_input,
        "date": completed_date,
        "name": name,
        "category": category,
    }

    data["progress"] = progress
    save_json(data)

    print(f"✅ {action}: {num} {name} [{status_input}]")
    print(f"   目录: {category}/")
    print(f"   日期: {completed_date}")


if __name__ == "__main__":
    main()
