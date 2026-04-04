# LeetCode 脚手架模板参考

本文档包含各类题型的脚手架模板和测试用例生成原则。当需要生成脚手架时，读取对应章节。

## 目录

- [普通题模板](#普通题模板)
- [链表题额外工具](#链表题额外工具)
- [树题额外工具](#树题额外工具)
- [测试用例生成原则](#测试用例生成原则)
  - [生成测试用例前的分析](#生成测试用例前的分析)
  - [测试用例生成步骤](#测试用例生成步骤)
  - [测试用例结构](#测试用例结构)
  - [不同题型的测试用例重点](#不同题型的测试用例重点)

---

## 普通题模板

```python
"""
<题号>. <题目名> - <中文名>
难度: Medium | 类型: <类型>
链接: https://leetcode.com/problems/<slug>/

题目描述:
    <描述>

示例:
    <示例>

约束:
    <约束>
"""

from typing import List


def solution_func(params) -> ReturnType:
    # TODO: 在这里写你的解法
    pass
```

---

## 链表题额外工具

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def make_list(vals):
    """从列表构建链表，返回头节点"""
    if not vals:
        return None
    head = ListNode(vals[0])
    curr = head
    for val in vals[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def to_list(head):
    """将链表转换为列表"""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result
```

---

## 树题额外工具

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def make_tree(vals):
    """从层序列表构建二叉树，None表示空节点"""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root

def to_list(root):
    """层序遍历二叉树为列表"""
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        result.append(node.val if node else None)
        if node:
            queue.append(node.left)
            queue.append(node.right)
    return result
```

---

## 测试用例生成原则

**核心原则：根据题目约束和示例生成针对性测试用例，而非泛化边界值。**

### 生成测试用例前的分析

在生成测试用例之前，先深入思考以下三个维度：

#### 1. 题目考核重点

思考这道题在考核什么核心能力：
- 是考察某种特定算法思想（双指针、滑动窗口、DP等）？
- 是考察对特定数据结构的理解（二叉树、图、链表等）？
- 是考察数学推导或逻辑推理能力？
- 是考察边界条件处理？

#### 2. 实现过程可能出现的错误

根据题目类型，预判常见的实现陷阱：
- 滑动窗口：窗口大小是否正确更新、是否遗漏左边界收缩条件
- 链表：是否有空指针、是否正确处理环、删除节点是否断链
- 二叉树：是否正确处理空树、递归终止条件是否正确
- DP：状态转移是否完整、是否有遗漏的状态组合
- 二分查找：边界条件是否正确（left <= right 或 left < right）
- 回溯：是否正确恢复状态、剪枝是否充分

#### 3. 题目所有可能的执行分支

列举题目可能的所有分支路径：
- 输入的边界情况（空、单个元素、全相同、全负数等）
- 不同约束组合下的分支（如：括号生成中 n=0, n=1, n>1 的处理）
- 特殊返回值分支（如：不存在时返回 -1、0、null 等）
- 题目未明确说明但实际存在的情况（如：数组中可能有重复元素）

**完成分析后，再根据分析结果生成针对性的测试用例。**

### 测试用例生成步骤

1. **分析题目约束**：从约束条件中提取数值范围、长度限制等
2. **覆盖示例场景**：确保包含题目给出的所有示例
3. **补充相关场景**：根据问题类型补充常见场景
4. **包含边界情况**：与问题相关的边界值

### 测试用例结构

```python
def run_tests():
    test_cases = [
        # (input_params, expected, description),
        ...
    ]
    
    passed = 0
    for args, expected, desc in test_cases:
        if isinstance(args, tuple):
            result = solution_func(*args)
        else:
            result = solution_func(args)
        if result == expected:
            print(f"PASS: {desc}")
            passed += 1
        else:
            print(f"FAIL: {desc} - Expected {expected}, got {result}")
    
    print(f"\n{passed}/{len(test_cases)} tests passed")
```

### 不同题型的测试用例重点

| 题型 | 重点测试场景 |
|------|-------------|
| 数组/滑动窗口 | 窗口大小边界、负数处理、全正/全负、递增/递减序列 |
| 链表 | 空链表、单节点、循环链表、相交、删除节点 |
| 树 | 满二叉、平衡、单支、只有左/右子、深度限制 |
| DP | 基础情况、转移方程验证、空间优化对比 |
| 图 | 连通分量、环检测、拓扑排序 |
| 字符串 | 空串、特殊字符、大小写、数字字母混合 |
| 数学 | 0、1、负数、大数、溢出边界 |

### 示例：两数之和

```python
def run_tests():
    test_cases = [
        # 示例（题目自带的示例，测试用例中必须覆盖）
        ([2, 7, 11, 15], 9, "官方示例1"),
        ([3, 2, 4], 6, "官方示例2"),
        ([3, 3], 6, "官方示例3"),
        
        # 自身就是答案的情况
        ([0, 4, 3, 0], 0, "自身为答案"),
        
        # 不同位置对应相同值
        ([1, 5, 2, 8], 9, "后面两个数和为9"),
        
        # 负数处理
        ([-1, -2, -3, -4, -5], -8, "全负数"),
        ([-1, 2, 3, 4], 3, "一负一正"),
        
        # 边界值
        ([0], 0, "单元素需要自身相加"),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 19, "长数组"),
    ]
    # ...测试逻辑
```

### 示例：括号生成

```python
def run_tests():
    test_cases = [
        # 示例
        (3, ["((()))","(()())","(())()","()(())","()()()"], "n=3"),
        (1, ["()"], "n=1"),
        
        # 边界
        (0, [""], "n=0空字符串"),
        (2, ["(())","()()"], "n=2"),
        
        # 长度验证
        (4, None, "n=4生成2n长度"),
    ]
    # ...测试逻辑（结果验证用回溯检查合法性）
```
