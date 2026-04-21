# -*- coding: utf-8 -*-
"""
主入口 - 商品零售购物篮分析
"""

import os
import logging
from data_loader import load_order_data, load_types_data, transform_to_transactions, get_total_records
from eda import (descriptive_stats, analyze_top_products, analyze_category,
                 analyze_subcategory, analyze_top6_categories)
from apriori import apriori
from rule_miner import generate_rules, rules_to_dataframe, print_top_rules, save_rules

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    # 确保输出目录存在
    os.makedirs('outputs', exist_ok=True)

    # -------------------- 1. 数据加载与探索 --------------------
    logger.info("开始加载数据...")
    order_data = load_order_data('data/GoodsOrder.csv')
    types_data = load_types_data('data/GoodsTypes.csv')

    logger.info("进行描述性统计...")
    descriptive_stats(order_data)

    logger.info("热销商品分析...")
    sorted_goods = analyze_top_products(order_data, top_n=10)

    logger.info("商品品类分析...")
    merged_data, category_stats = analyze_category(order_data, sorted_goods, types_data)

    logger.info("非酒精饮料内部分析...")
    analyze_subcategory(merged_data, '非酒精饮料')

    logger.info("前六热销品类内部TOP10分析...")
    analyze_top6_categories(merged_data, category_stats)

    # -------------------- 2. 数据预处理 --------------------
    logger.info("转换数据格式用于关联规则挖掘...")
    transactions = transform_to_transactions(order_data)
    logger.info(f"转换完成，总订单数：{len(transactions)}")

    # -------------------- 3. Apriori建模 --------------------
    min_support = 0.02
    min_confidence = 0.35

    logger.info(f"开始Apriori关联规则挖掘（min_support={min_support}, min_confidence={min_confidence})...")
    freq_itemsets, support_data = apriori(transactions, min_support)

    # -------------------- 4. 规则生成与输出 --------------------
    rules = generate_rules(freq_itemsets, support_data, min_confidence)
    rules_df = rules_to_dataframe(rules)
    print_top_rules(rules_df, top_n=10)
    save_rules(rules_df)

    logger.info("分析完成！所有图表和规则已保存至 outputs/ 目录。")


if __name__ == '__main__':
    main()