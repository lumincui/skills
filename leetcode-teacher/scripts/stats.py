#!/usr/bin/env python3
"""
查看 LeetCode 刷题进度统计
用法: python3 stats.py [类型]
示例: python3 stats.py        # 显示总体统计
示例: python3 stats.py dp     # 显示 dp 类型的统计
"""

import sys
import os

README_PATH = "README.md"


def parse_readme():
    if not os.path.exists(README_PATH):
        return {}
    with open(README_PATH, "r") as f:
        content = f.read()
    result = {}
    lines = content.strip().split("\n")
    for line in lines[2:]:
        if line.strip().startswith("|") and "------" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 4 and parts[0].isdigit():
                result[parts[0]] = {
                    "name": parts[1],
                    "cat": parts[2],
                    "status": parts[3],
                    "date": parts[4] if len(parts) > 4 else "",
                }
    return result


def show_stats(category=None):
    progress = parse_readme()

    if not progress:
        print("📊 暂无进度记录")
        print("   使用 update_progress.py 添加题目")
        return

    total = len(progress)
    passed = sum(1 for p in progress.values() if "通过" in p["status"])
    review = sum(1 for p in progress.values() if "需复习" in p["status"])

    if category:
        filtered = {k: v for k, v in progress.items() if v["cat"] == category}
        cat_total = len(filtered)
        cat_passed = sum(1 for p in filtered.values() if "通过" in p["status"])
        cat_review = sum(1 for p in filtered.values() if "需复习" in p["status"])
        print(f"\n📊 {category} 类型统计")
        print(f"   总题目数: {cat_total}")
        if cat_total > 0:
            pct = cat_passed * 100 // cat_total
            print(f"   已通过: {cat_passed} ({pct}%)")
            print(f"   需复习: {cat_review}")
        if filtered:
            print("\n   题目列表:")
            for num, info in sorted(filtered.items(), key=lambda x: int(x[0])):
                emoji = "✅" if "通过" in info["status"] else "🔄"
                print(f"     {emoji} {num}. {info['name']}")
    else:
        print(f"\n📊 LeetCode 刷题进度")
        print(f"   总题目数: {total}")
        if total > 0:
            pct = passed * 100 // total
            print(f"   已通过: {passed} ({pct}%)  ✅")
            print(f"   需复习: {review}  🔄")
            print(f"   未开始: {total - passed - review}")

        by_cat = {}
        for info in progress.values():
            cat = info["cat"]
            if cat not in by_cat:
                by_cat[cat] = {"total": 0, "pass": 0, "review": 0}
            by_cat[cat]["total"] += 1
            if "通过" in info["status"]:
                by_cat[cat]["pass"] += 1
            if "需复习" in info["status"]:
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
