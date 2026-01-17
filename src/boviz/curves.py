import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator, NullFormatter

from boviz.config import GLOBAL_COLORS, set_default_dpi_figsize_savedir, set_residual_dpi_figsize_savedir
from boviz.style import set_default_style, set_cm_style, set_ax_style, apply_axis_scientific_format, apply_axis_limits_and_ticks, save_or_display_legend, plot_residual_curves, set_sans_style
from boviz.utils import generate_plot_filename, load_data_csv, save_figure

# -----------------------------------------------------------------------------
# 内部辅助函数 (Helper Functions)
# -----------------------------------------------------------------------------

def update_curve_plotting_with_styles(ax, x_data, y_data, label, index):
    """
    内部函数：使用循环的线型和标记样式绘制曲线。
    用于 use_marker=True 的情况。
    """
    line_styles = ['-', '--', '-.', ':']
    markers = ['o', 's', 'D', '^', 'v', '*']
    color = GLOBAL_COLORS[index % len(GLOBAL_COLORS)]

    ax.plot(x_data, y_data,
            label=label,
            linestyle=line_styles[index % len(line_styles)],
            marker=markers[index % len(markers)],
            markevery=slice(index * 2, None, max(1, len(x_data) // 20)),
            markersize=2,
            linewidth=1,
            color=color,
            alpha=0.9)


def plot_scatter_style(ax, x_data, y_data, label, index):
    """
    内部函数：绘制散点图样式。
    用于 use_scatter=True 的情况。
    """
    markers = ['o', 's', 'D', '^', 'v', '*']
    color = GLOBAL_COLORS[index % len(GLOBAL_COLORS)]

    ax.scatter(x_data, y_data,
               label=label,
               s=5,
               marker=markers[index % len(markers)],
               edgecolors=color,
               facecolors=color,
               linewidths=1,
               zorder=3)

def _apply_font_style(font_style, font_weight):
    """内部函数：统一应用字体设置"""
    if not font_style:
        if font_weight == 'bold':
            set_cm_style(bold=True)
        elif font_weight == 'normal':
            set_cm_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    elif font_style == 'sans':
        if font_weight == 'bold':
            set_sans_style(bold=True)
        elif font_weight == 'normal':
            set_sans_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    elif font_style == 'times':
        if font_weight == 'bold':
            set_default_style(bold=True)
        elif font_weight == 'normal':
            set_default_style(bold=False)
        else:
            raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    else:
        raise ValueError("Invalid font_style. Choose 'sans', 'times' or None.")

def _finalize_plot(
    fig, ax_main, ax_res, 
    save_dir, title_figure, label_suffix, 
    xy_label, curves, label,
    xlim, ylim, tick_interval_x, tick_interval_y,
    sci, ylog, 
    legend_location, split_legend, show_legend, legend_ncol, legend_fontsize,
    show_residual,
    font_weight, figure_format,
    save, show, dpi
):
    """
    内部核心函数：统一处理图形的后处理（标签、刻度、保存等）。
    提取此函数是为了避免 plot_curves_csv 和 plot_curves 代码大量重复。
    """
    # 设置轴标签
    ax_main.set_xlabel(xy_label[0], fontweight=font_weight, labelpad=2)
    ax_main.set_ylabel(xy_label[1], fontweight=font_weight, labelpad=3)

    # 科学计数法
    # 这里为了保持原代码逻辑，直接内嵌 FixedOrderFormatter 类
    class FixedOrderFormatter(ticker.ScalarFormatter):
        def __init__(self, order=0, useOffset=True, useMathText=True):
            super().__init__(useOffset=useOffset, useMathText=useMathText)
            self._force_order = order
        
        def _set_order_of_magnitude(self):
            self.orderOfMagnitude = self._force_order

    def apply_native_sci(ax, axis, scale):
        if scale is None: return
        order = int(np.floor(np.log10(abs(scale)))) if scale != 0 else 0
        formatter = FixedOrderFormatter(order=order, useOffset=True, useMathText=True)
        if axis == 'x': ax.xaxis.set_major_formatter(formatter)
        elif axis == 'y': ax.yaxis.set_major_formatter(formatter)

    apply_native_sci(ax_main, 'x', sci[0])
    apply_native_sci(ax_main, 'y', sci[1])

    # 刻度与范围
    apply_axis_limits_and_ticks(
        ax=ax_main, curves=curves, xlim=xlim, ylim=ylim,
        tick_interval_x=tick_interval_x, tick_interval_y=tick_interval_y
    )

    # 对数坐标
    if ylog:
        ax_main.set_yscale('log')
        if ylim:
            if ylim[0] <= 0 or ylim[1] <= 0:
                new_ylim = (max(ylim[0], 1e-6), max(ylim[1], 1e-6))
                ax_main.set_ylim(new_ylim)
                print(f"[Warning] 对数坐标轴 ylim 必须为正数，已自动调整为: {new_ylim}")
            else:
                ax_main.set_ylim(ylim)
        ax_main.yaxis.set_major_formatter(ticker.LogFormatterSciNotation())
        ax_main.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))

    # 图例字体
    if legend_fontsize is not None:
        plt.rcParams['legend.fontsize'] = legend_fontsize

    # 图例处理
    save_or_display_legend(
        ax=ax_main, save_dir=save_dir, figure_name_suffix=label_suffix,
        split_legend=split_legend, legend_location=legend_location,
        legend_ncol=legend_ncol or 1, dpi=dpi, xy_label=xy_label,
        show_legend=show_legend
    )

    # 残差绘制
    if show_residual and len(curves) >= 2 and ax_res is not None:
        plot_residual_curves(
            ax_res=ax_res, curves=curves, label=label,
            xy_label=xy_label, x_title_fallback=xy_label[0]
        )
    
    # 布局与保存
    plt.tight_layout(pad=0.1) 
    filename = generate_plot_filename(title=title_figure, file_format=figure_format, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path

# -----------------------------------------------------------------------------
# 公开绘图接口 (Public APIs)
# -----------------------------------------------------------------------------

def plot_curves_csv(
    path: list[str],
    label: list[str],
    x: list[int],
    y: list[int],
    information: str = None,
    factor: list[tuple[tuple, tuple]] = None,
    time_step: list[int | list | tuple] = None,
    xy_label: tuple[str, str] = None,
    use_marker: list[bool] = None,
    use_scatter: list[bool] = None,
    line_style: list[str] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None,
    legend_location: str = None,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    highlight_x: float = None,
    split_legend: bool = False,
    show_residual: bool = False,
    show_legend: bool = True,
    show_title: bool = True,
    title_figure: str = None,
    legend_ncol: int = None,
    legend_fontsize: int | float | str = None,
    ylog: bool = False,
    sci: tuple[float, float] = [None, None],
    color_group: list[int] = None,
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
    figure_format: str = 'png',
) -> str:
    """
    从 CSV 文件读取数据并绘制科学曲线。支持多曲线对比、样式定制及残差分析。

    Args:
        path (list[str]): CSV 文件路径列表。
        label (list[str]): 每条曲线的图例标签。
        x (list[int]): X 轴数据所在的列索引（从0开始）。
        y (list[int]): Y 轴数据所在的列索引（从0开始）。
        information (str, optional): 附加信息，用于生成文件名的后缀。默认为 None。
        factor (list[tuple[tuple, tuple]], optional): 数据缩放与平移因子。
            格式为 `[((x_scale, x_offset), (y_scale, y_offset)), ...]`。
            默认为 `(1.0, 0.0)`。
        time_step (list[int | list | tuple], optional): 数据截取设置。
            - 整数 N: 取前 N 行。
            - 列表 [start, end]: 取 start 到 end 行。
        xy_label (tuple[str, str], optional): (X轴名称, Y轴名称)。若不提供，将尝试使用 CSV 列名。
        use_marker (list[bool], optional): 是否为每条曲线启用标记点样式。默认为 False。
        use_scatter (list[bool], optional): 是否以散点图形式绘制。默认为 False。
        line_style (list[str], optional): 指定每条曲线的线型（如 '-', '--'）。默认为 '-'。
        tick_interval_x (float, optional): 强制 X 轴主刻度间隔。
        tick_interval_y (float, optional): 强制 Y 轴主刻度间隔。
        legend_location (str, optional): 图例位置，如 'upper right', 'best'。
        xlim (tuple[float, float], optional): X 轴显示范围 (min, max)。
        ylim (tuple[float, float], optional): Y 轴显示范围 (min, max)。
        split_legend (bool, optional): 是否将图例单独保存为一张图片。默认为 False。
        show_residual (bool, optional): 是否绘制残差子图（相对于第一条曲线）。默认为 False。
        show_legend (bool, optional): 是否显示图例。默认为 True。
        show_title (bool, optional): 是否显示标题。默认为 True。
        title_figure (str, optional): 图像标题，同时用于文件命名。
        legend_ncol (int, optional): 图例列数。
        ylog (bool, optional): Y 轴是否使用对数坐标。
        sci (tuple[float, float], optional): 科学计数法缩放因子 [x_scale, y_scale]。
        color_group (list[int], optional): 指定颜色分组索引，强制多条曲线使用相同颜色。
        show (bool, optional): 是否在窗口显示图像。默认为 False。
        save (bool, optional): 是否保存图像到文件。默认为 False。
        font_style (str, optional): 字体风格 ('times', 'sans' 或 None)。
        font_weight (str, optional): 字体粗细 ('bold' 或 'normal')。
        figure_format (str, optional): 保存格式 ('png', 'pdf', 'svg')。默认为 'png'。

    Returns:
        str: 保存的图像文件路径。
    """
    
    # 1. 字体设置
    _apply_font_style(font_style, font_weight)

    # 2. 画布初始化
    if show_residual:
        dpi, figuresize, savedir = set_residual_dpi_figsize_savedir()
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=figuresize, dpi=dpi,
                                              gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    else:
        dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
        fig, ax_main = plt.subplots(figsize=figuresize, dpi=dpi)
        ax_res = None
    save_dir = os.path.join(savedir, "Curves")

    # 3. 样式初始化
    for ax in [ax_main] + ([ax_res] if ax_res is not None else []):
        set_ax_style(ax)
        ax.tick_params(axis='both', length=2, direction='in', width=0.75, which='both', pad=4)

    # 4. 默认参数填充
    time_step = time_step or [0] * len(path)
    use_marker = use_marker or [False] * len(path)
    use_scatter = use_scatter or [False] * len(path)
    line_style = line_style or ['-'] * len(path)
    factor = factor or [[(1.0, 0.0), (1.0, 0.0)] for _ in range(len(path))]

    # 5. 数据读取与绘制循环
    curves = [] # 用于存储绘制后的数据 (x, y)，供范围计算和残差使用
    
    # 单曲线/多曲线逻辑统一处理
    # 如果只有一条曲线且未提供 xy_label，尝试从 CSV 读取列名
    need_auto_label = (len(path) == 1 and not xy_label)

    if show_title:
        default_title = f'Comparison' if len(path) > 1 else 'Curve'
        ax_main.set_title(title_figure or default_title, pad=7.5, fontweight=font_weight)

    for i in range(len(path)):
        x_d, y_d, x_colname, y_colname = load_data_csv(
            source=path[i],
            x_index=x[i] if isinstance(path[i], str) else None,
            y_index=y[i] if isinstance(path[i], str) else None,
            factor=factor[i],
            time_step=time_step[i]
        )
        curves.append((x_d, y_d))
        
        # 自动标签处理
        if need_auto_label:
            if not x_colname or not y_colname:
                 raise ValueError("CSV data missing column names. Please specify 'xy_label'.")
            xy_label = [x_colname, y_colname]

        # 颜色索引
        color_index = color_group[i] if color_group else (i if len(path) > 1 else 10)

        # 绘制
        if use_scatter[i]:
            plot_scatter_style(ax_main, x_d, y_d, label[i], color_index)
        elif use_marker[i]:
            update_curve_plotting_with_styles(ax_main, x_d, y_d, label[i], color_index)
        else:
            ax_main.plot(x_d, y_d, label=label[i], linewidth=1,
                         linestyle=line_style[i], 
                         color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])

    if not xy_label:
        raise ValueError("Please specify 'xy_label'.")

    # 6. 调用统一的后处理函数
    label_suffix = f"({information})" if information else None
    
    return _finalize_plot(
        fig, ax_main, ax_res, save_dir, title_figure, label_suffix,
        xy_label, curves, label,
        xlim, ylim, tick_interval_x, tick_interval_y,
        sci, ylog,
        legend_location, split_legend, show_legend, legend_ncol, legend_fontsize,
        show_residual, font_weight, figure_format,
        save, show, dpi
    )


def plot_curves(
    data: list[tuple[np.ndarray, np.ndarray]],
    label: list[str],
    information: str = None,
    factor: list[tuple[tuple, tuple]] = None,
    time_step: list[int | list | tuple] = None,
    xy_label: tuple[str, str] = None,
    use_marker: list[bool] = None,
    use_scatter: list[bool] = None,
    line_style: list[str] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None,
    legend_location: str = None,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    highlight_x: float = None,
    split_legend: bool = False,
    show_legend: bool = True,
    show_residual: bool = False,
    show_title: bool = True,
    title_figure: str = None,
    legend_ncol: int = None,
    ylog: bool = False,
    sci: tuple[float, float] = (None, None),
    color_group: list[int] = None,
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
    figure_format: str = 'png',
) -> str:
    """
    直接绘制内存中的数据（NumPy 数组）。参数含义同 plot_curves_csv。
    """
    
    # 1. 字体
    _apply_font_style(font_style, font_weight)

    # 2. 画布
    if show_residual:
        dpi, figuresize, savedir = set_residual_dpi_figsize_savedir()
        fig, (ax_main, ax_res) = plt.subplots(2, 1, figsize=figuresize, dpi=dpi,
                                              gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    else:
        dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
        fig, ax_main = plt.subplots(figsize=figuresize, dpi=dpi)
        ax_res = None
    save_dir = os.path.join(savedir, "Curves")

    # 3. 样式
    for ax in [ax_main] + ([ax_res] if ax_res is not None else []):
        set_ax_style(ax)
        ax.tick_params(axis='both', length=2, direction='in', width=0.75, which='both', pad=4)

    # 4. 默认值
    time_step = time_step or [0] * len(data)
    use_marker = use_marker or [False] * len(data)
    use_scatter = use_scatter or [False] * len(data)
    line_style = line_style or ['-'] * len(data)
    factor = factor or [[(1.0, 0.0), (1.0, 0.0)] for _ in range(len(data))]

    # 5. 绘制循环
    curves = []
    if not xy_label:
         raise ValueError("For plot_curves, 'xy_label' is required.")

    if show_title:
        default_title = f'Comparison of {xy_label[1]}' if len(data) > 1 else f'Curve of {xy_label[1]}'
        ax_main.set_title(title_figure or default_title, pad=7.5, fontweight=font_weight)

    for i in range(len(data)):
        x_data, y_data = data[i]
        
        # 截断处理
        current_ts = time_step[i]
        start_idx, end_idx = 0, None
        if isinstance(current_ts, int) and current_ts != 0:
            end_idx = current_ts
        elif isinstance(current_ts, (list, tuple)):
            if len(current_ts) >= 1: start_idx = current_ts[0]
            if len(current_ts) >= 2: end_idx = current_ts[1] if current_ts[1] != 0 else None
        
        if start_idx != 0 or end_idx is not None:
            x_data = x_data[start_idx:end_idx]
            y_data = y_data[start_idx:end_idx]

        # 缩放处理
        x_scale, x_offset = factor[i][0]
        y_scale, y_offset = factor[i][1]
        x_data = x_data * x_scale + x_offset
        y_data = y_data * y_scale + y_offset

        curves.append((x_data, y_data))

        # 颜色
        color_index = color_group[i] if color_group else (i if len(data) > 1 else 10)

        # 绘图
        if use_scatter[i]:
            plot_scatter_style(ax_main, x_data, y_data, label[i], color_index)
        elif use_marker[i]:
            update_curve_plotting_with_styles(ax_main, x_data, y_data, label[i], color_index)
        else:
            ax_main.plot(x_data, y_data, label=label[i], linewidth=1, linestyle=line_style[i],
                        color=GLOBAL_COLORS[color_index % len(GLOBAL_COLORS)])

    # 6. 后处理
    label_suffix = f"({information})" if information else None

    return _finalize_plot(
        fig, ax_main, ax_res, save_dir, title_figure, label_suffix,
        xy_label, curves, label,
        xlim, ylim, tick_interval_x, tick_interval_y,
        sci, ylog,
        legend_location, split_legend, show_legend, legend_ncol, None,
        show_residual, font_weight, figure_format,
        save, show, dpi
    )


def plot_dual_curves_csv(
    path: list[str],
    label: list[str],
    x: list[int],
    y: list[int],
    path_right: list[str],
    label_right: list[str],
    x_right: list[int],
    y_right: list[int],
    information: str = None,
    factor: list[tuple[tuple, tuple]] = None,
    factor_right: list[tuple[tuple, tuple]] = None,
    time_step: list[int | list | tuple] = None,
    time_step_right: list[int | list | tuple] = None,
    xy_label: tuple[str, str] = None,
    y_label_right: str = None,
    use_marker: list[bool] = None,
    use_marker_right: list[bool] = None,
    use_scatter: list[bool] = None,
    use_scatter_right: list[bool] = None,
    tick_interval_x: float = None,
    tick_interval_y: float = None,
    tick_interval_y_right: float = None,
    legend_location: str = None,
    xlim: tuple[float, float] = None,
    ylim: tuple[float, float] = None,
    ylim_right: tuple[float, float] = None,
    split_legend: bool = False,
    show_legend: bool = False,
    match_axis_color: bool = True,
    add_axis_arrow: bool = False,
    show_title: bool = True,
    title_figure: str = None,
    legend_ncol: int = None,
    
    # --- 科学计数法设置 [X轴, 左Y轴, 右Y轴] ---
    auto_sci: bool = True,
    sci: list[float] = [None, None, None],
    # ----------------------------------------
    
    color_group: list[int] = None,
    color_group_right: list[int] = None,
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
    figure_format: str = 'png',
) -> str:
    """
    双轴绘图（风格统一版）：线宽为1，实线，完美复刻 plot_curves_csv 风格。
    """
    # ... (字体设置保持不变) ...
    if not font_style:
        if font_weight == 'bold':
            set_cm_style(bold=True)
        elif font_weight == 'normal':
            set_cm_style(bold=False)
    elif font_style == 'sans':
        if font_weight == 'bold':
            set_sans_style(bold=True)
        elif font_weight == 'normal':
            set_sans_style(bold=False)
    elif font_style == 'times':
        if font_weight == 'bold':
            set_default_style(bold=True)
        elif font_weight == 'normal':
            set_default_style(bold=False)

    dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
    fig, ax_main = plt.subplots(figsize=figuresize, dpi=dpi)
    ax_right = ax_main.twinx()
    
    save_dir = os.path.join(savedir, "Curves")

    # 样式基础设置
    for ax in [ax_main, ax_right]:
        set_ax_style(ax)
        ax.tick_params(axis='both', length=2, direction='in', width=0.75, which='both', pad=4)

    # ... (数据加载逻辑保持不变) ...
    time_step = time_step or [0] * len(path)
    time_step_right = time_step_right or [0] * len(path_right)
    use_marker = use_marker or [False] * len(path)
    use_marker_right = use_marker_right or [False] * len(path_right)
    use_scatter = use_scatter or [False] * len(path)
    use_scatter_right = use_scatter_right or [False] * len(path_right)

    curves_left = []
    if not xy_label: raise ValueError("需要 xy_label")
    for i in range(len(path)):
        x_d, y_d, _, _ = load_data_csv(path[i], x[i], y[i], factor[i] if factor else [(1,0),(1,0)], time_step[i])
        curves_left.append((x_d, y_d))
        color_idx = color_group[i] if color_group else i
        if use_scatter[i]: plot_scatter_style(ax_main, x_d, y_d, label[i], color_idx)
        elif use_marker[i]: update_curve_plotting_with_styles(ax_main, x_d, y_d, label[i], color_idx)
        else: 
            # 【修改】显式指定 linewidth=1
            ax_main.plot(x_d, y_d, label=label[i], linewidth=1, 
                         color=GLOBAL_COLORS[color_idx%len(GLOBAL_COLORS)])

    curves_right = []
    color_offset = len(path) if not color_group_right else 0
    for i in range(len(path_right)):
        x_d, y_d, _, _ = load_data_csv(path_right[i], x_right[i], y_right[i], factor_right[i] if factor_right else [(1,0),(1,0)], time_step_right[i])
        curves_right.append((x_d, y_d))
        color_idx = color_group_right[i] if color_group_right else (i+color_offset)
        if use_scatter_right[i]: plot_scatter_style(ax_right, x_d, y_d, label_right[i], color_idx)
        elif use_marker_right[i]: update_curve_plotting_with_styles(ax_right, x_d, y_d, label_right[i], color_idx)
        else: 
            # 【修改】显式指定 linewidth=1，去除 linestyle='--'
            ax_right.plot(x_d, y_d, label=label_right[i], linewidth=1, 
                          color=GLOBAL_COLORS[color_idx%len(GLOBAL_COLORS)])

    # =========================================================================
    # 科学计数法参数解析 & Formatter (之前讨论的完美方案)
    # =========================================================================
    sci_list = list(sci) if sci else []
    while len(sci_list) < 3: sci_list.append(None)
    scale_x, scale_y_left, scale_y_right = sci_list[0], sci_list[1], sci_list[2]

    class FixedOrderFormatter(ticker.ScalarFormatter):
        def __init__(self, order=0, useOffset=True, useMathText=True):
            super().__init__(useOffset=useOffset, useMathText=useMathText)
            self._force_order = order
        def _set_order_of_magnitude(self):
            self.orderOfMagnitude = self._force_order

    def apply_sci_format(ax, axis, scale=None):
        ax_obj = ax.yaxis if axis == 'y' else ax.xaxis
        if scale is not None:
            order = int(np.floor(np.log10(abs(scale)))) if scale != 0 else 0
            formatter = FixedOrderFormatter(order=order, useOffset=True, useMathText=True)
            ax_obj.set_major_formatter(formatter)
        elif auto_sci:
            formatter = ticker.ScalarFormatter(useOffset=True, useMathText=True)
            formatter.set_powerlimits((-2, 3))
            ax_obj.set_major_formatter(formatter)

    apply_sci_format(ax_main, 'x', scale_x)
    apply_sci_format(ax_main, 'y', scale_y_left)
    apply_sci_format(ax_right, 'y', scale_y_right)
    # =========================================================================

    if show_title:
        ax_main.set_title(title_figure or f'Comparison', pad=10, fontweight=font_weight)
    ax_main.set_xlabel(xy_label[0], fontweight=font_weight, labelpad=2)
    
    c_left = GLOBAL_COLORS[color_group[0]%len(GLOBAL_COLORS)] if color_group else GLOBAL_COLORS[0]
    idx_right = color_group_right[0] if color_group_right else (0 + color_offset)
    c_right = GLOBAL_COLORS[idx_right%len(GLOBAL_COLORS)]

    label_color_left = c_left if match_axis_color else 'black'
    label_color_right = c_right if match_axis_color else 'black'

    ax_main.set_ylabel(xy_label[1], color=label_color_left, fontweight=font_weight, labelpad=3)
    ax_right.set_ylabel(y_label_right, color=label_color_right, fontweight=font_weight, labelpad=3)

    if match_axis_color:
        ax_main.tick_params(axis='y', colors=c_left, which='both')
        ax_main.yaxis.get_offset_text().set_color(c_left)
        ax_main.spines['left'].set_color(c_left)
        ax_main.spines['left'].set_linewidth(0.75) 
        ax_main.spines['right'].set_visible(False) 

        ax_right.tick_params(axis='y', colors=c_right, which='both')
        ax_right.yaxis.get_offset_text().set_color(c_right)
        ax_right.spines['right'].set_color(c_right)
        ax_right.spines['right'].set_linewidth(0.75)
        ax_right.spines['left'].set_visible(False) 

    if add_axis_arrow:
        ax_main.plot(0, 1, "^", transform=ax_main.transAxes, color=label_color_left, clip_on=False, markersize=4, zorder=10)
        ax_main.plot(1, 1, "^", transform=ax_main.transAxes, color=label_color_right, clip_on=False, markersize=4, zorder=10)
        ax_main.plot(1, 0, ">", transform=ax_main.transAxes, color='black', clip_on=False, markersize=4, zorder=10)

    apply_axis_limits_and_ticks(ax_main, curves_left, xlim, ylim, tick_interval_x, tick_interval_y)
    
    if tick_interval_y_right:
        y_min = min(min(c[1]) for c in curves_right)
        y_max = max(max(c[1]) for c in curves_right)
        start = ylim_right[0] if ylim_right else y_min
        end = ylim_right[1] if ylim_right else y_max
        ax_right.set_yticks(np.arange(start, end + 0.1 * tick_interval_y_right, tick_interval_y_right))
    if ylim_right: ax_right.set_ylim(*ylim_right)

    h1, l1 = ax_main.get_legend_handles_labels()
    h2, l2 = ax_right.get_legend_handles_labels()
    label_suffix = f"({information})" if information else None

    if split_legend:
        fig_leg = plt.figure(figsize=(4, 2))
        fig_leg.legend(h1 + h2, l1 + l2, loc='center', ncol=legend_ncol or 1)
        fig_leg.tight_layout()
        legend_path = os.path.join(save_dir, f'Legend_Dual_{xy_label[1]}_{y_label_right}{label_suffix or ""}.png')
        fig_leg.savefig(legend_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig_leg)
    elif show_legend:
        ax_main.legend(h1 + h2, l1 + l2, loc=legend_location or 'best', ncol=legend_ncol or 1, frameon=True).get_frame().set_linewidth(0.5)

    plt.tight_layout(pad=0.1)
    filename = generate_plot_filename(title=title_figure, file_format=figure_format, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # 【关键】这里直接调用 savefig 并开启 bbox_inches='tight'
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0.1)
        print(f"[SAVE] 图像已保存到: {save_path}\n")
    if show:
        plt.show()
    plt.close()
    return save_path