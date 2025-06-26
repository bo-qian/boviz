'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:38:39
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-26 18:29:12
FilePath: /BoPlotKit/src/BoPlotKit/curves.py
Description: This module provides functions to plot curves with various styles and options, including support for multiple curves, residual analysis, and custom styling.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator, NullFormatter

from BoPlotKit.config import GLOBAL_COLORS, DEFAULT_SAVE_DIR, DEFAULT_DPI, DEFAULT_FIGSIZE
from BoPlotKit.style import set_default_style
from BoPlotKit.utils import generate_plot_filename

def update_curve_plotting_with_styles(ax, x_data, y_data, label, index):
    line_styles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', '^', 'v', '*']
    color = GLOBAL_COLORS[index % len(GLOBAL_COLORS)]

    ax.plot(x_data, y_data,
            label=label,
            linestyle=line_styles[index % len(line_styles)],
            marker=markers[index % len(markers)],
            markevery=slice(index * 2, None, max(1, len(x_data) // 20)),
            markersize=6,
            linewidth=3 if index == 0 else 2,
            color=color,
            alpha=0.9)


def plot_scatter_style(ax, x_data, y_data, label, index):
    markers = ['o', 's', 'D', '^', 'v', '*']
    color = GLOBAL_COLORS[index % len(GLOBAL_COLORS)]

    ax.scatter(x_data, y_data,
               label=label,
               s=60,
               marker=markers[index % len(markers)],
               edgecolors=color,
               facecolors=color,
               linewidths=1.5,
               zorder=5)


def plot_curves(
    path, label, x, y,
    information=None,
    factor=None,
    time_step=None,
    xy_label=None,
    use_marker=None,
    use_scatter=None,
    tick_interval_x=None,
    tick_interval_y=None,
    legend_location=None,
    xlim=None,
    ylim=None,
    highlight_x=None,
    split_legend=False,
    show_residual=False,
    title_figure=None,
    legend_ncol=None,
    ylog=False,
    y_sci=None,
    color_group=None,
    show: bool = False,
    save: bool = False
):
    """
    绘制一条或多条曲线，支持多种样式控制与残差分析的通用函数。

    Args:
        path (List[str]): 每条曲线对应的 CSV 文件路径。
        label (List[str]): 每条曲线的图例标签。
        x (List[int]): 每条曲线 X 数据所在列的索引。
        y (List[int]): 每条曲线 Y 数据所在列的索引。
        information (str, optional): 文件名后缀信息，用于区分保存图像。
        factor (List[float], optional): Y 轴缩放因子，例如用于单位换算。默认均为 1。
        time_step (List[int], optional): 用于截断数据的步数，若为 0 表示不截断。
        xy_label (Tuple[str, str], optional): X 和 Y 轴标签，例如 ("Time (s)", "Stress (MPa)")。
        use_marker (List[bool], optional): 是否为每条曲线使用线+标记风格。
        use_scatter (List[bool], optional): 是否将每条曲线绘制为散点图。
        tick_interval_x (float, optional): X 轴主刻度间隔。
        tick_interval_y (float, optional): Y 轴主刻度间隔。
        legend_location (str, optional): 图例位置（如 'best'、'upper right' 等）。
        xlim (Tuple[float, float], optional): X 轴显示范围。
        ylim (Tuple[float, float], optional): Y 轴显示范围。
        highlight_x (float, optional): 保留接口，尚未启用，用于高亮指定 X 点。
        split_legend (bool, optional): 是否将图例单独绘制成图像保存。
        show_residual (bool, optional): 是否绘制与参考曲线（第 1 条）相比的残差图。
        title_figure (str, optional): 图像标题，也作为保存文件名的前缀。
        legend_ncol (int, optional): 图例列数，默认自动调整。
        ylog (bool, optional): 是否对 Y 轴使用对数坐标。
        y_sci (float, optional): 若设置则以科学计数格式显示 Y 轴（如设置为 1e6 会在坐标轴显示 ×10⁶）。
        color_group (List[int], optional): 每条曲线的颜色索引（用于自定义颜色组）。
        show (bool, optional): 是否在绘制完成后显示图像，默认不显示。
        save (bool, optional): 是否保存图像，默认不保存。

    Returns:
        None. 图像将自动保存至默认目录，并在终端打印保存路径。
    """
    
    set_default_style()

    save_dir = os.path.join(DEFAULT_SAVE_DIR, "plot_curves")
    os.makedirs(save_dir, exist_ok=True)

    if show_residual:
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=(10, 10), dpi=DEFAULT_DPI,
                                            gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    else:
        fig, ax_main = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=DEFAULT_DPI)
        ax_res = None

    for ax in [ax_main] + ([ax_res] if ax_res is not None else []):
        ax.spines['top'].set_linewidth(3)
        ax.spines['bottom'].set_linewidth(3)
        ax.spines['left'].set_linewidth(3)
        ax.spines['right'].set_linewidth(3)
        ax.tick_params(axis='both', direction='in', width=3, which='both', pad=10)

    factor = factor or [1] * len(path)
    time_step = time_step or [0] * len(path)
    use_marker = use_marker or [False] * len(path)
    use_scatter = use_scatter or [False] * len(path)

    curves = []

    for i in range(len(path)):
        df = pd.read_csv(path[i])
        title = df.columns

        x_data = df.iloc[:time_step[i], x[i]] if time_step[i] else df.iloc[:, x[i]]
        if title[y[i]] == 'shrinkage_length':
            y_data = np.abs(df.iloc[:time_step[i], y[i]] / df.iloc[0, y[i]] - 1)
        else:
            y_data = df.iloc[:time_step[i], y[i]] * factor[i] if time_step[i] else df.iloc[:, y[i]] * factor[i]

        curves.append((x_data.values, y_data.values))

        color_index = color_group[i] if color_group else i

        if use_scatter[i]:
            plot_scatter_style(ax_main, x_data, y_data, label[i], color_index)
        elif use_marker[i]:
            update_curve_plotting_with_styles(ax_main, x_data, y_data, label[i], color_index)
        else:
            ax_main.plot(x_data, y_data, label=label[i], linewidth=3,
                         color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])

    if y_sci:
        ax_main.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y / y_sci:.1f}"))
        sci_power = int(np.log10(y_sci))
        ax_main.text(0.01, 1.01, rf'$\times10^{{{sci_power}}}$',
                     transform=ax_main.transAxes, fontsize=22,
                     fontweight='bold', verticalalignment='bottom',
                     horizontalalignment='left')

    if tick_interval_x:
        x_min = min(min(c[0]) for c in curves)
        x_max = max(max(c[0]) for c in curves)
        ax_main.set_xticks(np.arange(x_min, x_max + tick_interval_x, tick_interval_x))

    if tick_interval_y:
        y_min = min(min(c[1]) for c in curves)
        y_max = max(max(c[1]) for c in curves)
        ax_main.set_yticks(np.arange(y_min, y_max + tick_interval_y, tick_interval_y))

    label_suffix = f"({information})" if information else ""

    num_curves = len(path)
    if num_curves > 1:
        if not xy_label or not xy_label[0] or not xy_label[1]:
            raise ValueError("When plotting multiple curves, please specify 'xy_label' explicitly.")
        ax_main.set_title(title_figure or f'Comparison of {xy_label[1]}', pad=20, fontweight='bold')
        ax_main.set_xlabel(xy_label[0], fontweight='bold')
        ax_main.set_ylabel(xy_label[1], fontweight='bold')
    else:
        # 单条曲线时，从 DataFrame 自动读取列标题
        x_label = df.columns[x[0]] if hasattr(df, "columns") else "X"
        y_label = df.columns[y[0]] if hasattr(df, "columns") else "Y"
        ax_main.set_title(title_figure or f'Curve of {y_label}', pad=20, fontweight='bold')
        ax_main.set_xlabel(x_label, fontweight='bold')
        ax_main.set_ylabel(y_label, fontweight='bold')

    if xlim:
        ax_main.set_xlim(*xlim)
    if ylim:
        ax_main.set_ylim(*ylim)
        if tick_interval_y:
            ax_main.set_yticks(np.arange(ylim[0], ylim[1] + 0.1 * tick_interval_y, tick_interval_y))
    else:
        if tick_interval_y:
            y_min = min([min(c[1]) for c in curves])
            y_max = max([max(c[1]) for c in curves])
            ax_main.set_yticks(np.arange(y_min, y_max + tick_interval_y, tick_interval_y))

    if ylog:
        ax_main.set_yscale('log')
        ax_main.set_ylim(0.0, 0.6)
        ax_main.yaxis.set_major_locator(FixedLocator([0.002, 0.01, 0.1, 0.6]))
        ax_main.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
        ax_main.yaxis.set_minor_locator(NullLocator())
        ax_main.yaxis.set_minor_formatter(NullFormatter())

    if split_legend:
        legend = ax_main.legend(fontsize='small', loc=legend_location or 'best')
        fig_leg = plt.figure(figsize=(4, 2))
        fig_leg.legend(*ax_main.get_legend_handles_labels(), loc='center')
        fig_leg.tight_layout()
        legend_path = os.path.join(save_dir, f'Legend of {title[y[1]]}{label_suffix}.png')
        fig_leg.savefig(legend_path, dpi=DEFAULT_DPI, bbox_inches='tight')
        plt.close(fig_leg)
        legend.remove()
    else:
        ax_main.legend(fontsize='small', loc=legend_location or 'best', ncol=legend_ncol or 1)

    if show_residual and len(curves) >= 2:
        x_ref, y_ref = curves[0]
        for i in range(1, len(curves)):
            x_i, y_i = curves[i]
            y_interp = np.interp(x_ref, x_i, y_i)
            ax_res.plot(x_ref, y_interp - y_ref,
                        label=f'{label[i]} - {label[0]}', linewidth=2)
        ax_res.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x * 1e2:.1f}'))
        ax_res.text(0.01, 1.02, r'$\times10^{-2}$', transform=ax_res.transAxes, fontsize=20,
                    verticalalignment='bottom', horizontalalignment='left')
        ax_res.axhline(0, color='gray', linestyle='--', linewidth=1)
        ax_res.set_ylabel("Residual", fontweight='bold')
        ax_res.set_xlabel(xy_label[0] if xy_label and xy_label[0] else title[x[1]], fontweight='bold')
        ax_res.legend(fontsize=20)

    plt.tight_layout() 
    filename = generate_plot_filename(title=title_figure, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches='tight')
        print(f"[Saved] {save_path}")
    if show:
        plt.show()
    plt.close()
    return save_path