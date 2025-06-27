'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 17:14:02
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-27 17:05:56
FilePath: /BoPlotKit/src/BoPlotKit/schematic_particles.py
Description: This module provides a function to plot the initial distribution of particles in a schematic format, including their positions and radii.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



import os
import numpy as np
import matplotlib.pyplot as plt

from BoPlotKit.config import set_default_dpi_figsize_savedir
from BoPlotKit.style import set_default_style, set_ax_style
from BoPlotKit.utils import generate_plot_filename

def plot_initial_particle_schematic(
    coordinates: list,
    radii: list,
    domain: list,
    title: str = "Initial Particle Distribution",
    show: bool = False,
    save: bool = False
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
    """
    set_default_style()  # 设置默认样式
    # 创建保存目录
    save_dir = os.path.join(set_default_dpi_figsize_savedir()[2], "initial_schematic")

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
    plt.xlabel('X-axis', fontweight='bold')
    plt.ylabel('Y-axis', fontweight='bold')
    plt.title(title, pad=20, fontweight='bold')

    plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=set_default_dpi_figsize_savedir()[0], bbox_inches='tight')
        print(f"[Saved] {save_path}")
    if show:
        plt.show()
    plt.close()
    return save_path
