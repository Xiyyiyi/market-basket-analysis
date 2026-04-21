# -*- coding: utf-8 -*-
"""
Apriori算法核心实现（优化版）
"""

from itertools import combinations


def create_candidates_1(data_set):
    """生成候选1-项集"""
    candidates = []
    for transaction in data_set:
        for item in transaction:
            if [item] not in candidates:
                candidates.append([item])
    candidates.sort()
    return list(map(frozenset, candidates))


def scan_transactions(transactions, candidates, min_support):
    """
    扫描事务数据库，计算支持度，返回频繁项集和支持度字典
    """
    support_counts = {}
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                support_counts[candidate] = support_counts.get(candidate, 0) + 1

    num_transactions = float(len(transactions))
    freq_itemsets = []
    support_data = {}

    for itemset, count in support_counts.items():
        support = count / num_transactions
        if support >= min_support:
            freq_itemsets.insert(0, itemset)
            support_data[itemset] = support

    return freq_itemsets, support_data


def generate_candidates(prev_freq_itemsets, k):
    """
    由频繁(k-1)-项集生成候选k-项集，并利用先验原理剪枝
    """
    candidates = set()
    # 将所有项集转为排序后的元组，便于比较
    sorted_items = [tuple(sorted(list(itemset))) for itemset in prev_freq_itemsets]

    n = len(sorted_items)
    for i in range(n):
        for j in range(i + 1, n):
            # 前 k-2 项相同才合并
            if sorted_items[i][:k-2] == sorted_items[j][:k-2]:
                candidate = frozenset(set(sorted_items[i]) | set(sorted_items[j]))
                if len(candidate) == k:
                    candidates.add(candidate)

    # 剪枝：检查所有 (k-1)-子集是否都在 prev_freq_itemsets 中
    valid_candidates = []
    for candidate in candidates:
        subsets = list(combinations(candidate, k-1))
        if all(frozenset(sub) in prev_freq_itemsets for sub in subsets):
            valid_candidates.append(candidate)

    return valid_candidates


def apriori(transactions, min_support=0.2):
    """
    Apriori算法主函数
    Args:
        transactions: 嵌套列表格式的事务数据
        min_support: 最小支持度阈值
    Returns:
        L: 所有频繁项集的列表，L[k] 为频繁(k+1)-项集
        support_data: 支持度字典
    """
    # 转换为集合列表，便于子集判断
    transaction_sets = list(map(set, transactions))

    # 生成频繁1-项集
    c1 = create_candidates_1(transactions)
    l1, support_data = scan_transactions(transaction_sets, c1, min_support)

    all_freq_itemsets = [l1]
    k = 2

    while len(all_freq_itemsets[k-2]) > 0:
        candidates = generate_candidates(all_freq_itemsets[k-2], k)
        freq_k, sup_k = scan_transactions(transaction_sets, candidates, min_support)
        support_data.update(sup_k)
        all_freq_itemsets.append(freq_k)
        k += 1

    # 删除最后一个空列表
    if len(all_freq_itemsets[-1]) == 0:
        del all_freq_itemsets[-1]

    return all_freq_itemsets, support_data