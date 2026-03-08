# LeetCode 中等难度高频面试题目列表

## High Priority

### 动态规划 (dp)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 322 | Coin Change | 完全背包 |
| 300 | Longest Increasing Subsequence | LIS |
| 1143 | Longest Common Subsequence | LCS |
| 416 | Partition Equal Subset Sum | 0/1背包 |
| 139 | Word Break | 完全背包 |
| 198 | House Robber | 线性DP |
| 213 | House Robber II | 环形DP |
| 152 | Maximum Product Subarray | 维护最大最小 |
| 62 | Unique Paths | 路径DP |
| 5 | Longest Palindromic Substring | 中心扩展/DP |
| 91 | Decode Ways | 线性DP |
| 309 | Best Time to Buy Stock with Cooldown | 状态机DP |

### 双指针 (array)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 11 | Container With Most Water | 左右收缩 |
| 15 | 3Sum | 排序+双指针 |
| 75 | Sort Colors | 三指针荷兰旗 |
| 238 | Product of Array Except Self | 前缀积 |
| 48 | Rotate Image | 转置+翻转 |
| 54 | Spiral Matrix | 边界模拟 |
| 73 | Set Matrix Zeroes | 原地标记 |

### 滑动窗口 (sliding_window)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 3 | Longest Substring Without Repeating Chars | 可变窗口 |
| 209 | Minimum Size Subarray Sum | 可变窗口 |
| 424 | Longest Repeating Character Replacement | 最大频率 |
| 567 | Permutation in String | 固定窗口 |
| 438 | Find All Anagrams in a String | 固定窗口 |

### 哈希表 (hashmap)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 49 | Group Anagrams | 排序key |
| 128 | Longest Consecutive Sequence | 集合+起点扩展 |
| 347 | Top K Frequent Elements | 频率+桶 |
| 560 | Subarray Sum Equals K | 前缀和+哈希 |
| 146 | LRU Cache | HashMap+双向链表 |

### 链表 (linkedlist)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 19 | Remove Nth Node From End | 快慢指针 |
| 143 | Reorder List | 找中点+翻转+合并 |
| 148 | Sort List | 归并排序 |
| 92 | Reverse Linked List II | 区间翻转 |
| 2 | Add Two Numbers | 模拟进位 |
| 328 | Odd Even Linked List | 奇偶分组 |

### 树 (tree)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 102 | Binary Tree Level Order Traversal | BFS层序 |
| 105 | Construct Binary Tree Preorder+Inorder | 递归分割 |
| 236 | Lowest Common Ancestor | 后序DFS |
| 437 | Path Sum III | 前缀和+DFS |
| 543 | Diameter of Binary Tree | 后序返回深度 |
| 199 | Binary Tree Right Side View | BFS取末尾 |
| 297 | Serialize and Deserialize Binary Tree | BFS序列化 |

### 图 (graph)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 200 | Number of Islands | DFS染色 |
| 207 | Course Schedule | 拓扑排序/环检测 |
| 210 | Course Schedule II | 拓扑排序 |
| 994 | Rotting Oranges | 多源BFS |
| 417 | Pacific Atlantic Water Flow | 反向双源BFS |

## Medium Priority

### 二分查找 (binary_search)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 33 | Search in Rotated Sorted Array | 判断有序侧 |
| 34 | Find First and Last Position | 两次二分 |
| 153 | Find Minimum in Rotated Array | 找转折点 |
| 875 | Koko Eating Bananas | 二分答案 |
| 1011 | Capacity to Ship Packages | 二分答案 |

### 栈/单调栈 (stack)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 739 | Daily Temperatures | 单调递减栈 |
| 394 | Decode String | 栈模拟嵌套 |
| 84 | Largest Rectangle in Histogram | 单调递增栈 |
| 503 | Next Greater Element II | 循环单调栈 |

### 堆 (heap)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 215 | Kth Largest Element | 小根堆K |
| 347 | Top K Frequent Elements | 频率堆 |
| 451 | Sort Characters By Frequency | 大根堆 |

### 回溯 (backtrack)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 39 | Combination Sum | 可重复组合 |
| 46 | Permutations | 全排列 |
| 78 | Subsets | 幂集 |
| 22 | Generate Parentheses | 剪枝回溯 |
| 131 | Palindrome Partitioning | 分割回文 |

### 区间 (interval)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 56 | Merge Intervals | 排序+贪心合并 |
| 435 | Non-overlapping Intervals | 贪心结束时间 |
| 253 | Meeting Rooms II | 堆/差分 |

## Low Priority

### 并查集/Trie (trie)
| 题号 | 题目 | 核心模式 |
|------|------|---------|
| 208 | Implement Trie | 前缀树 |
| 547 | Number of Provinces | 并查集 |
| 684 | Redundant Connection | 并查集找环 |
