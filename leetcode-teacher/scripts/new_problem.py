#!/usr/bin/env python3
"""
快速生成 LeetCode 题目脚手架
用法: python3 new_problem.py <题号> <题目slug> <类型>
示例: python3 new_problem.py 322 coin_change dp
"""

import sys
import os

TEMPLATES = {
    "default": '''"""
{num}. {title}
难度: Medium | 类型: {category}
链接: https://leetcode.com/problems/{slug}/

题目描述:
    TODO

示例:
    TODO

约束:
    TODO

思路提示:
    TODO
"""

from typing import List


def solution(params) -> None:
    # TODO: 在这里写你的解法
    pass


import sys

def run_tests():
    test_cases = [
        # (input, expected, note)
    ]
    passed = failed = 0
    for i, (inp, expected, note) in enumerate(test_cases, 1):
        result = solution(inp)
        ok = result == expected
        status = "PASS" if ok else "FAIL"
        if ok: passed += 1
        else: failed += 1
        print(f"[{{status}}] Test {{i}}: {{note}}")
        if not ok:
            print(f"       expected={{expected}}, got={{result}}")
        else:
            print(f"       result={{result}}")
    print(f"\\n{'='*40}")
    print(f"结果: {{passed}}/{{passed+failed}} 通过")
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
''',

    "linkedlist": '''"""
{num}. {title}
难度: Medium | 类型: 链表
链接: https://leetcode.com/problems/{slug}/

题目描述:
    TODO

思路提示:
    TODO
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def solution(head: Optional[ListNode]) -> Optional[ListNode]:
    # TODO: 在这里写你的解法
    pass


def make_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


import sys

def run_tests():
    test_cases = [
        # (vals, expected_vals, note)
    ]
    passed = failed = 0
    for i, (vals, expected, note) in enumerate(test_cases, 1):
        head = make_list(vals)
        result = to_list(solution(head))
        ok = result == expected
        status = "PASS" if ok else "FAIL"
        if ok: passed += 1
        else: failed += 1
        print(f"[{{status}}] Test {{i}}: {{note}}")
        if not ok:
            print(f"       expected={{expected}}, got={{result}}")
        else:
            print(f"       result={{result}}")
    print(f"\\n{'='*40}")
    print(f"结果: {{passed}}/{{passed+failed}} 通过")
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
''',

    "tree": '''"""
{num}. {title}
难度: Medium | 类型: 树
链接: https://leetcode.com/problems/{slug}/

题目描述:
    TODO

思路提示:
    TODO
"""

from typing import Optional, List
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def solution(root: Optional[TreeNode]):
    # TODO: 在这里写你的解法
    pass


def make_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


import sys

def run_tests():
    test_cases = [
        # (tree_vals, expected, note)
    ]
    passed = failed = 0
    for i, (vals, expected, note) in enumerate(test_cases, 1):
        root = make_tree(vals)
        result = solution(root)
        ok = result == expected
        status = "PASS" if ok else "FAIL"
        if ok: passed += 1
        else: failed += 1
        print(f"[{{status}}] Test {{i}}: {{note}}")
        if not ok:
            print(f"       expected={{expected}}, got={{result}}")
        else:
            print(f"       result={{result}}")
    print(f"\\n{'='*40}")
    print(f"结果: {{passed}}/{{passed+failed}} 通过")
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
'''
}

def main():
    if len(sys.argv) < 4:
        print("用法: python3 new_problem.py <题号> <slug> <类型>")
        print("类型: dp/array/hashmap/linkedlist/tree/graph/binary_search/stack/heap/backtrack/interval/string/trie")
        sys.exit(1)

    num, slug, category = sys.argv[1], sys.argv[2], sys.argv[3]
    title = slug.replace("_", " ").title()

    tpl_key = "linkedlist" if "linked" in category else \
              "tree" if category == "tree" else "default"
    template = TEMPLATES[tpl_key]

    content = template.format(num=num, title=title, slug=slug, category=category)

    dir_path = os.path.expanduser(f"~/leetcode/{category}")
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f"{num}_{slug}.py")

    with open(file_path, "w") as f:
        f.write(content)

    print(f"已生成: {file_path}")

if __name__ == "__main__":
    main()
