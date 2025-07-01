'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:38:39
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-29 18:48:29
FilePath: /boviz/src/boviz/curves.py
Description: This module provides functions to plot curves with various styles and options, including support for multiple curves, residual analysis, and custom styling.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator, NullFormatter

from boviz.config import GLOBAL_COLORS, set_default_dpi_figsize_savedir, set_residual_dpi_figsize_savedir
from boviz.style import set_default_style, set_ax_style, apply_axis_scientific_format, apply_axis_limits_and_ticks, save_or_display_legend, plot_residual_curves, set_sans_style
from boviz.utils import generate_plot_filename, load_data_csv, save_figure

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


def plot_curves_csv(
    path: list[str],
    label: list[str],
    x: list[int],
    y: list[int],
    information: str = None,
    factor: list[(float, float)] = None,
    time_step: list[int] = None,
    xy_label: tuple[str, str] = None,
    use_marker: list[bool] = None,
    use_scatter: list[bool] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None,
    legend_location: str = None,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    highlight_x: float = None,
    split_legend: bool = False,
    show_residual: bool = False,
    title_figure: str = None,
    legend_ncol: int = None,
    ylog: bool = False,
    sci: tuple[float, float] = [None, None],
    color_group: list[int] = None,
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
) -> str:
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
        sci (Tuple[float, float], optional): 用于设置x轴或y轴的科学计数法格式，格式为 (x轴缩放因子，y轴缩放因子)。
        color_group (List[int], optional): 每条曲线的颜色索引（用于自定义颜色组）。
        show (bool, optional): 是否在绘制完成后显示图像，默认不显示。
        save (bool, optional): 是否保存图像，默认不保存。
        font_style (str, optional): 字体样式，默认为 Times。可选值为 'sans' 或 None。
        font_weight (str, optional): 字体粗细，默认为 "bold"。可选值为 'bold' 或 'normal'。

    Returns:
        None. 图像将自动保存至默认目录，并在终端打印保存路径。
    """
    
    if not font_style:
        if font_weight == 'bold':
            set_default_style(bold=True)
        elif font_weight == 'normal':
            set_default_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    elif font_style == 'sans':
        if font_weight == 'bold':
            set_sans_style(bold=True)
        elif font_weight == 'normal':
            set_sans_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    else:
        raise ValueError("Invalid font_style. Choose 'sans' or None.")

    if show_residual:
        dpi, figuresize, savedir = set_residual_dpi_figsize_savedir()
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=figuresize, dpi=dpi,
                                            gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    else:
        dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
        fig, ax_main = plt.subplots(figsize=figuresize, dpi=dpi)
        ax_res = None
    save_dir = os.path.join(savedir, "Curves")

    # Set the main axis style
    for ax in [ax_main] + ([ax_res] if ax_res is not None else []):
        set_ax_style(ax)
        ax.tick_params(axis='both', direction='in', width=3, which='both', pad=10)

    time_step = time_step or [0] * len(path)
    use_marker = use_marker or [False] * len(path)
    use_scatter = use_scatter or [False] * len(path)

    curves = []
    if len(path) > 1:
        if not xy_label or not xy_label[0] or not xy_label[1]:
            raise ValueError("When plotting multiple curves, please specify 'xy_label' explicitly.")
        ax_main.set_title(title_figure or f'Comparison of {xy_label[1]}', pad=20, fontweight=font_weight)
        
        for i in range(len(path)):
            x_data, y_data, x_colname, y_colname = load_data_csv(
                source=path[i],
                x_index=x[i] if isinstance(path[i], str) else None,
                y_index=y[i] if isinstance(path[i], str) else None,
                factor=factor[i] if factor else (1.0, 0.0),
                time_step=time_step[i]
            )
            curves.append((x_data, y_data))

            color_index = color_group[i] if color_group else i

            if use_scatter[i]:
                plot_scatter_style(ax_main, x_data, y_data, label[i], color_index)
            elif use_marker[i]:
                update_curve_plotting_with_styles(ax_main, x_data, y_data, label[i], color_index)
            else:
                ax_main.plot(x_data, y_data, label=label[i], linewidth=3,
                            color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])
    else:
        x_data, y_data, x_colname, y_colname = load_data_csv(
            source=path[0],
            x_index=x[0] if isinstance(path[0], str) else None,
            y_index=y[0] if isinstance(path[0], str) else None,
            factor=factor[i] if factor else (1.0, 0.0),
            time_step=time_step[0]
        )
        curves.append((x_data, y_data))

        color_index = color_group[0] if color_group else 0

        if use_scatter[0]:
            plot_scatter_style(ax_main, x_data, y_data, label[i], color_index)
        elif use_marker[0]:
            update_curve_plotting_with_styles(ax_main, x_data, y_data, label[i], color_index)
        else:
            ax_main.plot(x_data, y_data, label=label[0], linewidth=3, 
                         color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])
        
        if not x_colname or not y_colname:
            raise ValueError("The current CSV data does not have column names. Please specify the 'xy_label' parameter.")
        if not xy_label:
            xy_label = [x_colname, y_colname]
        ax_main.set_title(title_figure or f'Curve of {xy_label[1]}', pad=20, fontweight=font_weight)

    ax_main.set_xlabel(xy_label[0], fontweight=font_weight)
    ax_main.set_ylabel(xy_label[1], fontweight=font_weight)

    label_suffix = f"({information})" if information else None

    if sci[0]:
        apply_axis_scientific_format(ax_main, 'x', sci[0])
    if sci[1]:
        apply_axis_scientific_format(ax_main, 'y', sci[1])

    apply_axis_limits_and_ticks(
        ax=ax_main,
        curves=curves,
        xlim=xlim,
        ylim=ylim,
        tick_interval_x=tick_interval_x,
        tick_interval_y=tick_interval_y
    )

    if ylog:
        ax_main.set_yscale('log')
        ax_main.set_ylim(1e-3, 0.6)
        ax_main.yaxis.set_major_locator(FixedLocator([0.002, 0.01, 0.1, 0.6]))
        ax_main.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
        ax_main.yaxis.set_minor_locator(NullLocator())
        ax_main.yaxis.set_minor_formatter(NullFormatter())

    save_or_display_legend(
        ax=ax_main,
        save_dir=save_dir,
        figure_name_suffix=label_suffix,
        split_legend=split_legend,
        legend_location=legend_location,
        legend_ncol=legend_ncol or 1,
        dpi=dpi,
        xy_label=xy_label
    )

    if show_residual and len(curves) >= 2:
        plot_residual_curves(
            ax_res=ax_res,
            curves=curves,
            label=label,
            xy_label=xy_label,
            x_title_fallback=xy_label[0]
        )

    plt.tight_layout() 
    filename = generate_plot_filename(title=title_figure, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path


def plot_curves(
    data: list[tuple[np.ndarray, np.ndarray]],
    label: list[str],
    information: str = None,
    factor: list[tuple[float, float]] = None,
    time_step: list[int] = None,
    xy_label: tuple[str, str] = None,
    use_marker: list[bool] = None,
    use_scatter: list[bool] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None,
    legend_location: str = None,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    highlight_x: float = None,
    split_legend: bool = False,
    show_residual: bool = False,
    title_figure: str = None,
    legend_ncol: int = None,
    ylog: bool = False,
    sci: tuple[float, float] = (None, None),
    color_group: list[int] = None,
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
) -> str:
    """
    绘制一条或多条曲线，支持多种样式控制与残差分析的通用函数。

    Args:
        data (List[Tuple[np.ndarray, np.ndarray]]): 每条曲线的数据，格式为 [(x_data, y_data), ...]。
        label (List[str]): 每条曲线的图例标签。
        information (str, optional): 文件名后缀信息，用于区分保存图像。
        factor (List[Tuple[float, float]], optional): Y 轴缩放因子，例如用于单位换算。默认均为 (1.0, 0.0)。
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
        sci (Tuple[float, float], optional): 用于设置x轴或y轴的科学计数法格式，格式为 (x轴缩放因子，y轴缩放因子)。
        color_group (List[int], optional): 每条曲线的颜色索引（用于自定义颜色组）。
        show (bool, optional): 是否在绘制完成后显示图像，默认不显示。
        save (bool, optional): 是否保存图像，默认不保存。
        font_style (str, optional): 字体样式，默认为 Times。可选值为 'sans' 或 None。
        font_weight (str, optional): 字体粗细，默认为 "bold"。可选值为 'bold' 或 'normal'.

    Returns:
        str: 保存的图像路径。

    Raises:
        ValueError: 如果数据格式不正确或缺少必要参数。
        ValueError: 如果 xy_label 在多条曲线绘制时未指定。
        ValueError: 如果 xy_label 在单条曲线绘制时未指定且数据没有列名。
    """
    
    if not font_style:
        if font_weight == 'bold':
            set_default_style(bold=True)
        elif font_weight == 'normal':
            set_default_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    elif font_style == 'sans':
        if font_weight == 'bold':
            set_sans_style(bold=True)
        elif font_weight == 'normal':
            set_sans_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    else:
        raise ValueError("Invalid font_style. Choose 'sans' or None.")

    if show_residual:
        dpi, figuresize, savedir = set_residual_dpi_figsize_savedir()
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=figuresize, dpi=dpi,
                                              gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    else:
        dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
        fig, ax_main = plt.subplots(figsize=figuresize, dpi=dpi)
        ax_res = None
    save_dir = os.path.join(savedir, "Curves")

    for ax in [ax_main] + ([ax_res] if ax_res is not None else []):
        set_ax_style(ax)
        ax.tick_params(axis='both', direction='in', width=3, which='both', pad=10)

    time_step = time_step or [0] * len(data)
    use_marker = use_marker or [False] * len(data)
    use_scatter = use_scatter or [False] * len(data)
    factor = factor or [(1.0, 0.0)] * len(data)

    curves = []
    for i in range(len(data)):
        x_data, y_data = data[i]
        scale, offset = factor[i]
        if time_step[i]:
            x_data = x_data[:time_step[i]]
            y_data = y_data[:time_step[i]]
        y_data = y_data * scale + offset
        curves.append((x_data, y_data))

        color_index = color_group[i] if color_group else i

        if use_scatter[i]:
            plot_scatter_style(ax_main, x_data, y_data, label[i], color_index)
        elif use_marker[i]:
            update_curve_plotting_with_styles(ax_main, x_data, y_data, label[i], color_index)
        else:
            ax_main.plot(x_data, y_data, label=label[i], linewidth=3,
                         color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])

    label_suffix = f"({information})" if information else None

    if len(data) > 1:
        if not xy_label or not xy_label[0] or not xy_label[1]:
            raise ValueError("When plotting multiple curves, please specify 'xy_label' explicitly.")
        ax_main.set_title(title_figure or f'Comparison of {xy_label[1]}', pad=20, fontweight=font_weight)
    else:
        if not xy_label:
            raise ValueError("For single curve, 'xy_label' is required when no column name is provided.")
        ax_main.set_title(title_figure or f'Curve of {xy_label[1]}', pad=20, fontweight=font_weight)

    ax_main.set_xlabel(xy_label[0], fontweight=font_weight)
    ax_main.set_ylabel(xy_label[1], fontweight=font_weight)

    if sci[0]:
        apply_axis_scientific_format(ax_main, 'x', sci[0])
    if sci[1]:
        apply_axis_scientific_format(ax_main, 'y', sci[1])

    apply_axis_limits_and_ticks(
        ax=ax_main,
        curves=curves,
        xlim=xlim,
        ylim=ylim,
        tick_interval_x=tick_interval_x,
        tick_interval_y=tick_interval_y
    )

    if ylog:
        ax_main.set_yscale('log')
        ax_main.set_ylim(0.0, 0.6)
        ax_main.yaxis.set_major_locator(FixedLocator([0.002, 0.01, 0.1, 0.6]))
        ax_main.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
        ax_main.yaxis.set_minor_locator(NullLocator())
        ax_main.yaxis.set_minor_formatter(NullFormatter())

    save_or_display_legend(
        ax=ax_main,
        save_dir=save_dir,
        figure_name_suffix=label_suffix,
        split_legend=split_legend,
        legend_location=legend_location,
        legend_ncol=legend_ncol or 1,
        dpi=dpi,
        xy_label=xy_label
    )

    if show_residual and len(curves) >= 2:
        plot_residual_curves(
            ax_res=ax_res,
            curves=curves,
            label=label,
            xy_label=xy_label,
            x_title_fallback=xy_label[0]
        )

    plt.tight_layout()
    filename = generate_plot_filename(title=title_figure, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path
