import os
import matplotlib.pyplot as plt

# 全局颜色列表（可自定义扩展）
GLOBAL_COLORS = [
    'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
    'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', 'black',
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
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