'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-29 13:54:52
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-29 17:06:19
FilePath: /boviz/src/boviz/heatmap.py
Description: Plotting module for generating heatmaps of particle distributions.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''


import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

from boviz.style import set_default_style, set_smart_xy_ticks, set_sans_style
from boviz.config import set_default_dpi_figsize_savedir
from boviz.utils import generate_plot_filename, generate_particle_layout, build_tanh_phase_field, save_figure


def plot_heatmap_particle(
    particle_x_num: int,
    particle_y_num: int,
    particle_radius: float,
    border: float = None,
    cmap: str = 'coolwarm',
    title_figure: str = "Initial Particle Schematic",
    show: bool = True,
    save: bool = True,
    information: str = None,
    surface_thickness: float = 3.0,
    tanh_offset: float = 0.05,
    font_style: str = None,
    font_weight: str = "bold",
    show_ticks: bool = True,
):
    """
    绘制初始粒子分布的热图。

    Args:
        particle_x_num (int): 粒子在x方向的数量。
        particle_y_num (int): 粒子在y方向的数量。
        particle_radius (float): 粒子的半径。
        border (float, optional): 粒子布局的边界宽度，默认为 None。
        cmap (str, optional): 热图使用的颜色映射，默认为 'coolwarm', 可选值包括 'viridis', 'plasma', 'inferno', 'magma', 'cividis' 等。
        title_figure (str, optional): 图像标题，默认为 "Initial Particle Schematic"。
        show (bool, optional): 是否显示图像，默认为 True。
        save (bool, optional): 是否保存图像，默认为 True。
        information (str, optional): 附加信息，用于生成文件名后缀。
        surface_thickness (float, optional): 表面厚度，用于生成相场，默认为 3.0。
        tanh_offset (float, optional): 相场的偏移量，默认为 0.05。
        font_style (str, optional): 字体样式，默认为 Times。可选值为 'sans' 或 None。
        font_weight (str, optional): 字体粗细，默认为 None。可选值为 'bold' 或 None。
        show_ticks (bool, optional): 是否显示坐标轴刻度以及标题，默认为 True。

    Returns:
        str: 保存的图像路径。
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

    dpi, figuresize, savedir = set_default_dpi_figsize_savedir()
    fig, ax = plt.subplots(figsize=figuresize, dpi=dpi)
    save_dir = os.path.join(savedir, "HeatMaps")
    label_suffix = f"({information})" if information else None

    particle_center_coordinate, radii, domain_size = generate_particle_layout(
        particle_x_num, particle_y_num, particle_radius, border=border
    )
    phase_field = build_tanh_phase_field(
        centers_coordinate=particle_center_coordinate,
        radii=radii,
        domain_size=domain_size,
        tanh_width=surface_thickness,
        tanh_offset=tanh_offset
    )

    heatmap = ax.imshow(
        phase_field,
        cmap=cmap,
        extent=[0, domain_size[0], 0, domain_size[1]],
        origin='lower',
        aspect='auto'
    )

    if show_ticks:
        set_smart_xy_ticks(ax)
        ax.set_xlabel('X Coordinate', fontweight=font_weight)
        ax.set_ylabel('Y Coordinate', fontweight=font_weight)
        ax.set_title(title_figure, pad=20, fontweight=font_weight)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    ax.set_aspect('equal', adjustable='box')
    divider = make_axes_locatable(plt.gca())
    width = axes_size.AxesY(ax, aspect=1. / 20)
    pad = axes_size.Fraction(0.5, width)
    cax = divider.append_axes("right", size=width, pad=pad)
    cbar = plt.colorbar(heatmap, cax=cax)

    plt.tight_layout()
    filename = generate_plot_filename(title=title_figure, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path
