# -*- coding: utf-8 -*-
"""
探索性数据分析与可视化模块
"""

import os
import platform
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 项目根目录定位 ====================
# 当前文件路径: .../src/eda.py
# 项目根目录: 上一级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 跨平台中文字体设置 ====================
if platform.system() == 'Windows':
    plt.rcParams['font.sans-serif'] = 'SimHei'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
else:  # Linux
    plt.rcParams['font.sans-serif'] = 'WenQuanYi Micro Hei'
plt.rcParams['axes.unicode_minus'] = False


def descriptive_stats(data):
    """对交易编号进行描述统计"""
    data_id = data['id']
    stats = {
        '总记录数': data_id.count(),
        '最小订单ID': data_id.min(),
        '最大订单ID': data_id.max(),
        '订单总数': data['id'].nunique()
    }
    stats_df = pd.DataFrame([stats])
    print('描述性统计结果：\n', stats_df)
    return stats_df


def analyze_top_products(data, top_n=10):
    """
    热销商品分析
    Returns:
        sorted_goods: 按销量排序的商品DataFrame
    """
    total_records = data.shape[0]
    group_goods = data.groupby(['Goods']).count().reset_index()
    sorted_goods = group_goods.sort_values('id', ascending=False).reset_index(drop=True)
    sorted_goods.rename(columns={'id': 'sales'}, inplace=True)
    sorted_goods['sales_pct'] = sorted_goods['sales'] / total_records

    print(f'\n销量排行前{top_n}商品的销量：')
    print(sorted_goods.head(top_n)[['Goods', 'sales', 'sales_pct']])

    # 绘制条形图
    plt.figure(figsize=(8, 4))
    top_data = sorted_goods.head(top_n)
    plt.barh(top_data['Goods'], top_data['sales'])
    plt.xlabel('销量')
    plt.ylabel('商品')
    plt.title(f'商品销量TOP{top_n}')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'top10.png'), dpi=150)
    plt.show()

    return sorted_goods


def analyze_category(data, sorted_goods, types_df):
    """
    商品品类分析
    """
    total_records = data.shape[0]
    # 合并商品与品类信息
    merged = pd.merge(sorted_goods, types_df, on='Goods')
    category_stats = merged.groupby('Types')['sales'].sum().reset_index()
    category_stats = category_stats.sort_values('sales', ascending=False).reset_index(drop=True)
    category_stats['sales_pct'] = category_stats['sales'] / total_records

    print('\n各类别商品的销量及其占比：')
    print(category_stats)

    # 饼图
    plt.figure(figsize=(8, 6))
    plt.pie(category_stats['sales_pct'], labels=category_stats['Types'], autopct='%1.2f%%')
    plt.title('每类商品销量占比')
    plt.savefig(os.path.join(OUTPUT_DIR, 'percent.png'), dpi=150)
    plt.show()

    return merged, category_stats


def analyze_subcategory(merged, category_name='非酒精饮料'):
    """分析特定品类内部商品结构"""
    selected = merged[merged['Types'] == category_name].copy()
    total_sales = selected['sales'].sum()
    selected['sub_pct'] = selected['sales'] / total_sales
    selected = selected.sort_values('sales', ascending=False).reset_index(drop=True)

    print(f'\n{category_name}内部商品的销量及其占比：')
    print(selected[['Goods', 'sales', 'sub_pct']])

    # 饼图
    plt.figure(figsize=(8, 6))
    plt.pie(selected['sub_pct'], labels=selected['Goods'], autopct='%1.2f%%')
    plt.title(f'{category_name}内部各商品销量占比')
    plt.savefig(os.path.join(OUTPUT_DIR, 'non_alcohol_percent.png'), dpi=150)
    plt.show()

    return selected


def analyze_top6_categories(merged, category_stats):
    """分析前六热销品类内部商品TOP10"""
    top6_types = category_stats.head(6)['Types'].tolist()
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, tp in enumerate(top6_types):
        tp_data = merged[merged['Types'] == tp].copy()
        tp_top10 = tp_data.sort_values('sales', ascending=False).head(10)
        axes[idx].barh(tp_top10['Goods'], tp_top10['sales'])
        axes[idx].set_title(f'{tp} 内部热销商品TOP10', fontsize=12)
        axes[idx].invert_yaxis()
        axes[idx].set_xlabel('销量')

    plt.suptitle('前六热销品类内部商品销量TOP10', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, 'top6_categories_top10.png'), dpi=150)
    plt.show()