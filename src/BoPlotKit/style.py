'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:29:33
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-26 18:29:38
FilePath: /BoPlotKit/src/BoPlotKit/style.py
Description: This module provides functions to set default styles for plots in BoPlotKit.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import matplotlib.pyplot as plt

def set_default_style():
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman'],
        'font.weight': 'bold',
        'font.size': 32,
        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Times New Roman',
        'mathtext.it': 'Times New Roman:italic',
        'mathtext.bf': 'Times New Roman:bold',
        'axes.unicode_minus': False,
        'axes.linewidth': 3,
        'xtick.major.width': 3,
        'ytick.major.width': 3,
        'legend.fontsize': 28
    })
