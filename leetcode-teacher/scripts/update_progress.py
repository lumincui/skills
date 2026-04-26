#!/usr/bin/env python3
"""
更新 leetcode.json 进度
用法: python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]
示例: python3 update_progress.py 322 "Coin Change" dp pass
示例: python3 update_progress.py 322 "Coin Change" dp need_review

状态: pass / need_review
"""

import sys
import os
import json
from datetime import date

LEETCODE_JSON = "leetcode.json"


def load_json():
    if os.path.exists(LEETCODE_JSON):
        with open(LEETCODE_JSON, "r") as f:
            return json.load(f)
    return {"problems": [], "progress": {}, "study_plan": {}}


def save_json(data):
    with open(LEETCODE_JSON, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 5:
        print(
            "❌ 用法: python3 update_progress.py <题号> <题目名> <类型> <状态> [完成日期]"
        )
        print("   状态: pass (通过) / need_review (需复习)")
        sys.exit(1)

    num = sys.argv[1]
    name = sys.argv[2]
    category = sys.argv[3]
    status_input = sys.argv[4]
    completed_date = sys.argv[5] if len(sys.argv) > 5 else str(date.today())

    if status_input not in ["pass", "need_review"]:
        print(f"❌ 未知状态: {status_input}，使用 pass 或 need_review")
        sys.exit(1)

    data = load_json()
    progress = data.get("progress", {})

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
