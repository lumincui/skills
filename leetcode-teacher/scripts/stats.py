#!/usr/bin/env python3
"""
查看 LeetCode 刷题进度统计
用法: python3 stats.py [类型]
示例: python3 stats.py        # 显示总体统计
示例: python3 stats.py dp     # 显示 dp 类型的统计
"""

import sys
import os
import json

LEETCODE_JSON = "leetcode.json"


def load_json():
    if not os.path.exists(LEETCODE_JSON):
        return {}
    with open(LEETCODE_JSON, "r") as f:
        return json.load(f)


def get_progress():
    data = load_json()
    return data.get("progress", {})


def get_problems():
    data = load_json()
    problems = data.get("problems", [])
    return {p["id"]: p for p in problems}


def show_stats(category=None):
    progress = get_progress()
    problems = get_problems()

    if not progress:
        print("📊 暂无进度记录")
        return

    total = len(problems)
    passed = sum(1 for p in progress.values() if p.get("status") == "pass")
    review = sum(1 for p in progress.values() if p.get("status") == "need_review")

    if category:
        filtered = {
            pid: info
            for pid, info in progress.items()
            if problems.get(pid, {}).get("category") == category
        }
        cat_total = len(filtered)
        cat_passed = sum(1 for p in filtered.values() if p.get("status") == "pass")
        cat_review = sum(
            1 for p in filtered.values() if p.get("status") == "need_review"
        )
        print(f"\n📊 {category} 类型统计")
        print(f"   总题目数: {cat_total}")
        if cat_total > 0:
            pct = cat_passed * 100 // cat_total
            print(f"   已通过: {cat_passed} ({pct}%)")
            print(f"   需复习: {cat_review}")
        if filtered:
            print("\n   题目列表:")
            for pid in sorted(filtered.keys(), key=lambda x: int(x)):
                info = filtered[pid]
                prob_info = problems.get(pid, {})
                emoji = "✅" if info.get("status") == "pass" else "🔄"
                print(f"     {emoji} {pid}. {prob_info.get('name', 'Unknown')}")
    else:
        print(f"\n📊 LeetCode 刷题进度")
        print(f"   总题目数: {len(problems)}")
        print(f"   已完成: {passed} ({passed * 100 // total if total > 0 else 0}%)  ✅")
        print(f"   需复习: {review}  🔄")
        print(f"   未开始: {total - passed - review}")

        by_cat = {}
        for pid, info in progress.items():
            prob_info = problems.get(pid, {})
            cat = prob_info.get("category", "unknown")
            if cat not in by_cat:
                by_cat[cat] = {"total": 0, "pass": 0, "review": 0}
            by_cat[cat]["total"] += 1
            if info.get("status") == "pass":
                by_cat[cat]["pass"] += 1
            if info.get("status") == "need_review":
                by_cat[cat]["review"] += 1

        print("\n   按类型统计:")
        for cat in sorted(by_cat.keys()):
            stats = by_cat[cat]
            pct = stats["pass"] * 100 // stats["total"] if stats["total"] else 0
            print(f"     {cat}: {stats['pass']}/{stats['total']} ({pct}%)")


def main():
    category = sys.argv[1] if len(sys.argv) > 1 else None
    show_stats(category)


if __name__ == "__main__":
    main()
