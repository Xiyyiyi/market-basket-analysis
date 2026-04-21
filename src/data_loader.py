# -*- coding: utf-8 -*-
"""
数据读取与预处理模块
"""

import pandas as pd

import os

# 获取当前文件所在目录 (src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_order_data(filepath='data/GoodsOrder.csv', encoding='gbk'):
    full_path = os.path.join(BASE_DIR, filepath)
    return pd.read_csv(full_path, encoding=encoding)

def load_types_data(filepath='data/GoodsTypes.csv', encoding='gbk'):
    full_path = os.path.join(BASE_DIR, filepath)
    return pd.read_csv(full_path, encoding=encoding)


def transform_to_transactions(data):
    """
    将订单明细数据转换为嵌套列表格式，用于Apriori算法输入
    Args:
        data: DataFrame，包含 'id' 和 'Goods' 列
    Returns:
        list of lists: 每个子列表为一个订单包含的商品
    """
    transactions = data.groupby('id')['Goods'].apply(list).tolist()
    return transactions


def get_total_orders(data):
    """获取总订单数"""
    return data['id'].nunique()


def get_total_records(data):
    """获取总记录数"""
    return data.shape[0]