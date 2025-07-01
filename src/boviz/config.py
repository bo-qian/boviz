'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:28:18
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-07-01 16:41:21
FilePath: /boviz/src/boviz/config.py
Description: This module defines global configuration settings for boviz, including default colors, save directory, DPI, and figure size.
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

def set_default_dpi_figsize_savedir():
    """
    Set default DPI, figure size, and save directory for plots.

    Args:
        None

    Returns:
        tuple: A tuple containing default DPI, figure size, and save directory.
    """
    savedir = os.path.join(os.getcwd(), "figures")
    os.makedirs(savedir, exist_ok=True)
    default_dpi = 100
    default_figsize = (12, 9)
    return default_dpi, default_figsize, savedir

def set_residual_dpi_figsize_savedir():
    """
    Set default DPI, figure size, and save directory for residual plots.

    Args:
        None

    Returns:
        tuple: A tuple containing default DPI, figure size, and save directory.
    """
    savedir = os.path.join(os.getcwd(), "figures")
    os.makedirs(savedir, exist_ok=True)
    default_dpi = 100
    default_figsize = (12, 9)
    return default_dpi, default_figsize, savedir