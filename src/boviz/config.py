import os
import matplotlib.pyplot as plt

# 全局颜色列表（可自定义扩展），这里替换为了学术期刊（如JMPS）常用的高对比度/色盲友好深色系配色
GLOBAL_COLORS = [
    '#4589C8', # 顶刊 NO.05 蓝 (Non-SMK)
    '#EE7C7A', # 顶刊 NO.05 红 (SMK)
    '#008F91', # 顶刊 NO.05 蓝绿 (Non-SMK +abx)
    '#E67300', # 深橙 (Deep Orange)
    '#8B5A8C',  # 深紫 (Deep Purple - Morandi Style)
    '#008080', # 深青 (Teal)
    '#800000', # 绛紫/褐 (Maroon)
    '#555555', # 深灰 (Dark Gray)
    'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
    'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', 'black',
]

def set_default_dpi_figsize_savedir(bold: bool = True):
    """
    Set default DPI, figure size, and save directory for plots.

    Args:
        None

    Returns:
        tuple: A tuple containing default DPI, figure size, and save directory.
    """
    savedir = os.path.join(os.getcwd(), "figures")
    os.makedirs(savedir, exist_ok=True)
    default_dpi = 300
    default_figsize = (3.1496, 2.3622)
    # default_figsize = (3.1496, 3.1496)
    plt.rcParams.update({
        'axes.unicode_minus': False, # 配合 mathtext，正确显示负号
        'axes.titlesize': 10,     # 设置标题字体大小
        'font.size': 10,          # 设置xy轴标题字体大小
        'xtick.labelsize': 9,     # 设置x轴数字字体大小
        'ytick.labelsize': 9,     # 设置y轴数字字体大小
        'legend.fontsize': 9,     # 设置图例字体大小
    })
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
    default_dpi = 1000
    default_figsize = (3.5, 2.5)
    return default_dpi, default_figsize, savedir