'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 17:14:02
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-29 17:06:32
FilePath: /boviz/src/boviz/schematic_particles.py
Description: This module provides a function to plot the initial distribution of particles in a schematic format, including their positions and radii.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import os
import numpy as np
import matplotlib.pyplot as plt

from boviz.config import set_default_dpi_figsize_savedir
from boviz.style import set_default_style, set_ax_style, set_sans_style
from boviz.utils import generate_plot_filename

def plot_initial_particle_schematic(
    coordinates: list,
    radii: list,
    domain: list,
    title: str = "Initial Particle Distribution",
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    font_weight: str = "bold",
):
    """
    绘制初始粒子分布的示意图
    Args:
        coordinates (list): 粒子中心坐标列表，格式为 [[x1, y1], [x2, y2], ...]。
        radii (list): 粒子半径列表，格式为 [r1, r2, ...]。
        domain (list): 绘图区域的空间大小，格式为 [width, height]。
        title (str): 图表标题。
        show (bool): 是否显示图像，默认不显示。
        save (bool): 是否保存图像，默认不保存。
        font_style (str): 字体样式，默认为 Times。可选值为 'sans' 或 None。
        font_weight (str): 字体粗细，默认为 "bold"。可选值为 'bold' 或 'normal'.
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

    save_dir = os.path.join(set_default_dpi_figsize_savedir()[2], "InitialSchematic")

    filename = generate_plot_filename(title=title)
    save_path = os.path.join(save_dir, filename)
    
    fig, ax = plt.subplots(figsize=set_default_dpi_figsize_savedir()[1], dpi=set_default_dpi_figsize_savedir()[0])
    set_ax_style(ax)

    ax.set_xlim(0, domain[0])
    ax.set_ylim(0, domain[1])
    ax.set_xticks(np.arange(0, domain[0] + 1, 30))
    ax.set_yticks(np.arange(0, domain[1] + 1, 30))
    ax.set_aspect('equal', 'box')

    for i in range(len(coordinates)):
        circle = plt.Circle(
            (coordinates[i][0], coordinates[i][1]),
            radii[i],
            edgecolor='black',
            facecolor='white',
            linewidth=3,
            zorder=2
        )
        ax.add_artist(circle)
        plt.text(
            coordinates[i][0],
            coordinates[i][1],
            rf"$\text{{Particle}}_{{{i + 1}}}$",
            fontsize=32,
            ha='center',
            va='center',
            zorder=3
        )

    ax.grid(True, linestyle='--', linewidth=3, zorder=1)
    plt.tick_params(axis='both', direction='in', width=3, which='both', pad=10)
    plt.xlabel('X-axis', fontweight=font_weight)
    plt.ylabel('Y-axis', fontweight=font_weight)
    plt.title(title, pad=20, fontweight=font_weight)

    plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=set_default_dpi_figsize_savedir()[0], bbox_inches='tight')
        print(f"[Saved] {save_path}")
    if show:
        plt.show()
    plt.close()
    return save_path
