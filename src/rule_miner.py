# -*- coding: utf-8 -*-
"""
关联规则生成与评估模块
"""

import os
from itertools import combinations
import pandas as pd

# ==================== 项目根目录定位 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_rules(freq_itemsets, support_data, min_confidence=0.7):
    """
    从频繁项集生成强关联规则
    Args:
        freq_itemsets: 频繁项集列表（由apriori返回的L）
        support_data: 支持度字典
        min_confidence: 最小置信度阈值
    Returns:
        rules: 规则列表，每个元素为字典
    """
    rules = []

    for i in range(1, len(freq_itemsets)):  # 从2-项集开始
        for freq_set in freq_itemsets[i]:
            items = list(freq_set)
            for r in range(1, len(items)):
                for conseq in combinations(items, r):
                    conseq = frozenset(conseq)
                    ant = freq_set - conseq
                    if len(ant) == 0:
                        continue

                    conf = support_data[freq_set] / support_data[ant]
                    lift = support_data[freq_set] / (support_data[conseq] * support_data[ant])

                    if conf >= min_confidence and lift > 1.0:
                        rules.append({
                            'antecedent': ant,
                            'consequent': conseq,
                            'support': support_data[freq_set],
                            'confidence': conf,
                            'lift': lift
                        })

    return rules


def rules_to_dataframe(rules):
    """将规则列表转换为DataFrame"""
    df = pd.DataFrame(rules)
    if df.empty:
        return df
    # 转换frozenset为可读字符串
    df['antecedent'] = df['antecedent'].apply(lambda x: ', '.join(sorted(list(x))))
    df['consequent'] = df['consequent'].apply(lambda x: ', '.join(sorted(list(x))))
    df = df.sort_values('lift', ascending=False).reset_index(drop=True)
    return df


def print_top_rules(rules_df, top_n=10):
    """打印Top N规则"""
    if rules_df.empty:
        print("未生成任何规则，请尝试降低支持度或置信度阈值。")
        return
    print(f"\n========== 强关联规则TOP{top_n}（按提升度降序） ==========")
    print(rules_df.head(top_n).to_string(index=False))


def save_rules(rules_df, filepath=None):
    """保存规则到CSV"""
    if filepath is None:
        filepath = os.path.join(OUTPUT_DIR, 'association_rules.csv')
    if not rules_df.empty:
        rules_df.to_csv(filepath, index=False, encoding='gbk')
        print(f"\n关联规则已保存至 {filepath}")