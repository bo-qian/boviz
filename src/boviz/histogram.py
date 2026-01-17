import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator, NullFormatter

from boviz.config import GLOBAL_COLORS, set_default_dpi_figsize_savedir
from boviz.style import (
    set_default_style,
    set_sans_style,
    set_cm_style,
    set_ax_style,
    apply_axis_scientific_format,
    apply_axis_limits_and_ticks,
    save_or_display_legend,
)
from boviz.utils import generate_plot_filename, save_figure

def plot_histogram(
    label: str,
    x: list[float],
    y: list[float],
    xy_label: tuple[str, str],
    information: str = None,
    factor: list[(float, float)] = None,
    title: str = "Histogram",
    ylog: bool = False,
    sci: tuple[float, float] = [None, None],
    save: bool = False,
    show: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
    categorical_x: bool = True,
    show_values: bool = True,
) -> str:
    """
    绘制柱状图（直方图）

    Args:
        x (list[int]): 核数列表
        y (list[float]): 对应的运行时间列表
        label (str, optional): 图例标签. Defaults to "Runtime".
        xy_label (tuple[str, str], optional): x轴和y轴标签. Defaults to ("Number of Cores", "Runtime (s)").
        title (str, optional): 图表标题. Defaults to "Multi-core Performance".
        legend_location (str, optional): 图例位置. Defaults to "best".
        ylog (bool, optional): 是否使用对数y轴. Defaults to False.
        sci (tuple[float, float], optional): x轴和y轴的科学计数法阈值. Defaults to [None, None].
        save (bool, optional): 是否保存图表. Defaults to True.
        show (bool, optional): 是否显示图表. Defaults to True.
        font_style (str, optional): 字体风格，"sans"表示无衬线字体，None表示默认字体. Defaults to None.
        font_weight (str, optional): 字体粗细，"bold"表示粗体，"normal"表示正常字体. Defaults to "bold".
        categorical_x (bool, optional): 是否将x轴作为类别处理（等间距）. Defaults to True.
    
    Returns:
        str: 保存的图表路径
    """


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
        
    dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
    fig, ax = plt.subplots(figsize=figuresize, dpi=dpi)
    save_dir = os.path.join(savedir, "Histograms")

    set_ax_style(ax)
    ax.tick_params(axis="both", length=2.5, direction="in", width=0.75, which="both", pad=4)
    
    if factor:
        y = np.asarray(y, dtype=float)
        y = y * factor[0] + factor[1]

    # 绘制柱状图
    colors = plt.cm.Dark2.colors
    if categorical_x:
        width = 0.28
        x_pos = np.arange(len(x))
        bars = ax.bar(x_pos, y, color=colors, edgecolor="black", linewidth=0.5, width=width, label=label)
        ax.set_xticks(x_pos)
        ax.set_xticklabels([str(v) for v in x], fontweight=font_weight)

        # ✅ 两端空白 = 条间距的一半
        gap = 0.75
        ax.set_xlim(-gap, len(x) - 1 + gap)
    else:
        # 数值轴：按数值比例排布（你原来的画法）
        bars = ax.bar(x, y, color=colors, edgecolor="black", linewidth=0.5, width=0.6, label=label)
        ax.set_xlim(min(x) - 0.6, max(x) + 0.6)

    if show_values:
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax * 1.1)   # 上限增加 5%
        for bar, val in zip(bars, y):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{val:.2f}",    # 保留两位小数
                ha="center", va="bottom",
                fontweight=font_weight,
                fontsize=6
            )

    ax.set_title(title, pad=7.5, fontweight=font_weight)
    ax.set_xlabel(xy_label[0], fontweight=font_weight, labelpad=2)
    ax.set_ylabel(xy_label[1], fontweight=font_weight, labelpad=3)

    label_suffix = f"({information})" if information else None

    if sci[0]:
        apply_axis_scientific_format(ax, 'x', sci[0])
    if sci[1]:
        apply_axis_scientific_format(ax, 'y', sci[1])

    if ylog:
        ax.set_yscale('log')
        ax.set_ylim(0.0, 0.6)
        ax.yaxis.set_major_locator(FixedLocator([0.002, 0.01, 0.1, 0.6]))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
        ax.yaxis.set_minor_locator(NullLocator())
        ax.yaxis.set_minor_formatter(NullFormatter())

    plt.tight_layout(pad=0.1)
    filename = generate_plot_filename(title=title, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path


