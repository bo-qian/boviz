'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:28:18
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-26 18:28:43
FilePath: /BoPlotKit/src/BoPlotKit/config.py
Description: This module defines global configuration settings for BoPlotKit, including default colors, save directory, DPI, and figure size.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import os

# 全局颜色列表（可自定义扩展）
GLOBAL_COLORS = [
    'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
    'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan',
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

# 默认保存路径（可被函数覆盖）
DEFAULT_SAVE_DIR = os.path.join(os.getcwd(), "figures")

# DPI 与图像尺寸默认设置
DEFAULT_DPI = 100
DEFAULT_FIGSIZE = (12, 9)