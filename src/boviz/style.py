'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:29:33
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-29 16:46:15
FilePath: /boviz/src/boviz/style.py
Description: This module provides functions to set default styles for plots in boviz.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import ticker

def set_default_style(bold: bool = True):
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman'],
        'font.weight': 'bold' if bold else 'normal',
        'font.size': 32,
        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Times New Roman',
        'mathtext.it': 'Times New Roman:italic',
        'mathtext.bf': 'Times New Roman:bold' if bold else 'Times New Roman',
        'axes.unicode_minus': False,
        'legend.fontsize': 28
    })


def set_sans_style(bold: bool = True):
    """
    Set the default style for plots using sans-serif fonts.
    """
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial'],
        'font.weight': 'bold' if bold else 'normal',
        'font.size': 32,
        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Arial',
        'mathtext.it': 'Arial:italic',
        'mathtext.bf': 'Arial:bold' if bold else 'Arial',
        'axes.unicode_minus': False,
        'legend.fontsize': 28
    })


def set_ax_style(ax, linewidth=3):
    """
    Set the style for a given Axes object.

    Args:
        ax (matplotlib.axes.Axes): The Axes object to style.
    Returns:
        None
    """
    ax.spines['top'].set_linewidth(linewidth)
    ax.spines['bottom'].set_linewidth(linewidth)
    ax.spines['left'].set_linewidth(linewidth)
    ax.spines['right'].set_linewidth(linewidth)


def apply_axis_scientific_format(ax, axis: str, scale: float, fontsize: int = 22):
    """
    将某个轴设置为科学计数格式。

    Args:
        ax: matplotlib 坐标轴对象。
        axis (str): 'x' 或 'y'。
        scale (float): 缩放因子。
        fontsize (int): 标注字号。
    Returns:
        None
    """
    if not scale or scale == 1.0:
        return
    sci_power = int(np.log10(scale))
    formatter = FuncFormatter(lambda val, _: f"{val / scale:.1f}")

    if axis == 'y':
        ax.yaxis.set_major_formatter(formatter)
        ax.text(0.01, 1.01, rf'$\times10^{{{sci_power}}}$',
                transform=ax.transAxes,
                fontsize=fontsize,
                fontweight='bold',
                verticalalignment='bottom',
                horizontalalignment='left')
    elif axis == 'x':
        ax.xaxis.set_major_formatter(formatter)
        ax.text(1.01, -0.13, rf'$\times10^{{{sci_power}}}$',
                transform=ax.transAxes,
                fontsize=fontsize,
                fontweight='bold',
                verticalalignment='top',
                horizontalalignment='right')
        

def apply_axis_limits_and_ticks(
    ax: plt.Axes,
    curves: list[tuple[np.ndarray, np.ndarray]],
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None
):
    """
    设置 x/y 轴的显示范围与主刻度间隔。

    Args:
        ax: matplotlib Axes 对象。
        curves: 曲线数据列表，每项为 (x_data, y_data)。
        xlim: x 轴范围，如 (0, 10)。若为 None，则自动判断。
        ylim: y 轴范围，如 (-1, 1)。若为 None，则自动判断。
        tick_interval_x: x 轴主刻度间隔。
        tick_interval_y: y 轴主刻度间隔。
    Returns:
        None
    """
    # ----- X 轴主刻度 -----
    if tick_interval_x:
        x_min = min(min(c[0]) for c in curves)
        x_max = max(max(c[0]) for c in curves)
        ax.set_xticks(np.arange(x_min, x_max + tick_interval_x, tick_interval_x))

    # ----- Y 轴主刻度（先粗设）-----
    if tick_interval_y:
        y_min = min(min(c[1]) for c in curves)
        y_max = max(max(c[1]) for c in curves)
        ax.set_yticks(np.arange(y_min, y_max + tick_interval_y, tick_interval_y))

    # ----- X/Y 轴显示范围 -----
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
        # 若设定了 ylim 且 tick_interval_y 也存在，则精确地重新设定 y ticks
        if tick_interval_y:
            ax.set_yticks(np.arange(ylim[0], ylim[1] + 0.1 * tick_interval_y, tick_interval_y))


def save_or_display_legend(
    ax,
    save_dir: str,
    figure_name_suffix: str,
    split_legend: bool = False,
    legend_location: str = 'best',
    legend_ncol: int = 1,
    dpi: int = 300,
    xy_label: list[str, str] = None
):
    """
    处理图例显示或保存为单独图像的逻辑。

    Args:
        ax: 主图坐标轴。
        save_dir: 图像保存目录。
        figure_name_suffix: 用于生成图例文件名的后缀。
        split_legend: 是否将图例单独绘制保存。
        legend_location: 图例位置（默认 'best'）。
        legend_ncol: 图例列数。
        dpi: 图像保存分辨率。
        y_label: 用于命名的 y 轴标签。
    """
    if split_legend:
        legend = ax.legend(fontsize='small', loc=legend_location or 'best')
        fig_leg = plt.figure(figsize=(4, 2))
        fig_leg.legend(*ax.get_legend_handles_labels(), loc='center')
        fig_leg.tight_layout()

        if xy_label:
            y_label = xy_label[1]
        else:
            ValueError("xy_label must be provided.")
        legend_path = os.path.join(save_dir, f'Legend of {y_label}{figure_name_suffix}.png')
        fig_leg.savefig(legend_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig_leg)
        legend.remove()
    else:
        ax.legend(fontsize='small', loc=legend_location or 'best', ncol=legend_ncol or 1)


def plot_residual_curves(
    ax_res,
    curves: list[tuple[np.ndarray, np.ndarray]],
    label: list[str],
    xy_label: tuple[str, str] = None,
    x_title_fallback: str = None
):
    """
    绘制残差图：将第 1 条曲线作为参考，绘制其与其他曲线之间的差值。

    Args:
        ax_res: matplotlib 的残差子图坐标轴。
        curves: 所有曲线的 (x, y) 数据对。
        label: 每条曲线的标签。
        xy_label: 坐标轴标签元组，用于设置 x 轴名。
        x_title_fallback: 如果 xy_label 不存在时使用的 x 轴名。
    """
    if len(curves) < 2:
        return

    x_ref, y_ref = curves[0]
    for i in range(1, len(curves)):
        x_i, y_i = curves[i]
        y_interp = np.interp(x_ref, x_i, y_i)
        residual = y_interp - y_ref
        ax_res.plot(x_ref, residual,
                    label=f'{label[i]} - {label[0]}', linewidth=2)

    # 设置 y 轴以 ×10⁻² 显示
    ax_res.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x * 1e2:.1f}'))
    ax_res.text(0.01, 1.02, r'$\times10^{-2}$', transform=ax_res.transAxes,
                fontsize=20, verticalalignment='bottom', horizontalalignment='left')

    ax_res.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax_res.set_ylabel("Residual", fontweight='bold')
    ax_res.set_xlabel(xy_label[0] if xy_label and xy_label[0] else x_title_fallback, fontweight='bold')
    ax_res.legend(fontsize=20)


def set_smart_xy_ticks(ax, extent=None):
    """
    为 ax 自动设置 x 和 y 轴的主刻度，使其间隔为 (5,10,20,25,30,50,100) 中的一个，
    且总刻度数在 5 到 9 之间。
    
    参数：
        ax : matplotlib.axes.Axes
            目标坐标轴对象
        extent : tuple or None
            可选的 (x0, x1, y0, y1)，若为 None 则自动从 ax 获取当前坐标范围
    """
    step_candidates = (5, 10, 20, 25, 30, 40, 50, 100)

    def compute_ticks(start, end):
        range_ = end - start
        for step in step_candidates:
            ticks_count = range_ / step
            if ticks_count.is_integer() and 4 <= ticks_count <= 7:
                break
        else:
            # fallback：选一个最接近7个刻度的
            step = min(step_candidates, key=lambda s: abs((range_ / s) - 6))

        ticks = np.arange(start, end + 0.5 * step, step)
        return np.round(ticks, 8)

    if extent is not None:
        x0, x1, y0, y1 = extent
    else:
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()

    ax.set_xticks(compute_ticks(x0, x1))
    ax.set_yticks(compute_ticks(y0, y1))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
