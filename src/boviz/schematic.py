import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from typing import Union, List, Tuple

from boviz.config import set_default_dpi_figsize_savedir
from boviz.style import set_default_style, set_cm_style, set_ax_style, set_sans_style, set_smart_xy_ticks
from boviz.utils import generate_plot_filename, save_figure

def plot_initial_particle_schematic(
    coordinates: list,
    radii: list,
    domain: list,
    title: str = "Initial Particle Distribution",
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    show_title: bool = True,
    font_weight: str = "bold",
    tick_interval: Union[float, List[float], Tuple[float, float]] = None,
    show_particle_labels: bool = True,
):
    """
    绘制初始粒子分布的示意图。

    Args:
        coordinates (list): 粒子中心坐标列表，格式为 [[x1, y1], [x2, y2], ...]。
        radii (list): 粒子半径列表，格式为 [r1, r2, ...]。
        domain (list): 绘图区域的空间大小，格式为 [width, height]。
        title (str): 图表标题。
        show (bool): 是否显示图像，默认不显示。
        save (bool): 是否保存图像，默认不保存。
        font_style (str): 字体样式，默认为 Times。可选值为 'sans' 或 None。
        show_title (bool, optional): 是否显示图片标题，默认显示。
        font_weight (str): 字体粗细，默认为 "bold"。可选值为 'bold' 或 'normal'。
        tick_interval (float | list | tuple, optional): 坐标轴刻度间隔。
            如果为单个数值（如 20），则XY轴间隔相同；
            如果为列表/元组（如 [50, 10]），则分别代表 [X轴间隔, Y轴间隔]。
            如果为 None，则自动使用 smart ticks。
        show_particle_labels (bool, optional): 是否在粒子中心显示编号，默认显示。
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

    save_dir = os.path.join(set_default_dpi_figsize_savedir()[2], "InitialSchematic")

    filename = generate_plot_filename(title=title)
    save_path = os.path.join(save_dir, filename)
    
    fig, ax = plt.subplots(figsize=set_default_dpi_figsize_savedir()[1], dpi=set_default_dpi_figsize_savedir()[0])
    
    ax.set_xlim(0, domain[0])
    ax.set_ylim(0, domain[1])
    
    if tick_interval is not None:
        # 判断输入类型
        if isinstance(tick_interval, (list, tuple)):
            # 如果是列表或元组，分别赋值
            if len(tick_interval) >= 2:
                dx, dy = tick_interval[0], tick_interval[1]
            else:
                # 如果列表长度为1，则默认xy相同
                dx = dy = tick_interval[0]
        else:
            # 如果是单个数值，则xy相同
            dx = dy = tick_interval

        # 设置刻度 (加微小量防止浮点数精度问题导致丢失最后一个刻度)
        if dx is not None and dx > 0:
            ax.set_xticks(np.arange(0, domain[0] + dx * 0.001, dx))
        if dy is not None and dy > 0:
            ax.set_yticks(np.arange(0, domain[1] + dy * 0.001, dy))
    else:
        # 如果未指定间隔，使用智能刻度
        set_smart_xy_ticks(ax, extent=(0, domain[0], 0, domain[1]))
    ax.set_aspect('equal', 'box')

    for i in range(len(coordinates)):
        circle = plt.Circle(
            (coordinates[i][0], coordinates[i][1]),
            radii[i],
            edgecolor='black',
            facecolor='white',
            linewidth=1,
            zorder=2
        )
        ax.add_artist(circle)
        if show_particle_labels:
            plt.text(
                coordinates[i][0],
                coordinates[i][1],
                rf"$\text{{P}}_{{{i + 1}}}$",
                fontsize=8,
                ha='center',
                va='center',
                zorder=3
            )

    ax.grid(True, linestyle='--', linewidth=0.75, zorder=1)
    ax.tick_params(axis="both", length=2.5, direction="in", width=0.75, which="both", pad=4)
    plt.xlabel('X-axis', fontweight=font_weight, labelpad=2)
    plt.ylabel('Y-axis', fontweight=font_weight, labelpad=3)
    if show_title:
        plt.title(title, pad=7.5, fontweight=font_weight)

    plt.tight_layout(pad=0.5)
    if save:
        save_figure(save_path, dpi=set_default_dpi_figsize_savedir()[0])
    if show:
        plt.show()
    plt.close()
    return save_path

def plot_initial_superellipse_schematic(
    coordinates: list,
    semi_axes: list,
    exponents: list,
    domain: list,
    title: str = "Initial Super-Ellipsoid Distribution",
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    show_title: bool = True,
    font_weight: str = "bold",
    tick_interval: Union[float, List[float], Tuple[float, float]] = None,
    show_particle_labels: bool = True,
    resolution: int = 200
):
    """
    绘制初始超椭圆(Super-ellipse)粒子分布的示意图。

    方程: ``|x/a|^n + |y/b|^n = 1``

    Args:
        coordinates (list): 粒子中心坐标 [[x1, y1], ...]
        semi_axes (list): 半轴长列表 [[a1, b1], [a2, b2], ...]
        exponents (list): 形状指数 n 列表 [n1, n2, ...]。n=2为椭圆，n>2趋向矩形。
        domain (list): [width, height]
        resolution (int): 绘制曲线的离散点数量
        ... (其他参数同 plot_initial_particle_schematic)
    """
    # --- 样式设置 (保持一致) ---
    if not font_style:
        if font_weight == 'bold': set_cm_style(bold=True)
        elif font_weight == 'normal': set_cm_style(bold=False)
        else: raise ValueError("Invalid font_weight.")
    elif font_style == 'sans':
        if font_weight == 'bold': set_sans_style(bold=True)
        elif font_weight == 'normal': set_sans_style(bold=False)
    elif font_style == 'times':
        if font_weight == 'bold': set_default_style(bold=True)
        elif font_weight == 'normal': set_default_style(bold=False)
    else:
        raise ValueError("Invalid font_style.")

    save_dir = os.path.join(set_default_dpi_figsize_savedir()[2], "InitialSchematic")
    filename = generate_plot_filename(title=title)
    save_path = os.path.join(save_dir, filename)
    
    fig, ax = plt.subplots(figsize=set_default_dpi_figsize_savedir()[1], dpi=set_default_dpi_figsize_savedir()[0])
    
    ax.set_xlim(0, domain[0])
    ax.set_ylim(0, domain[1])
    
    # --- 刻度设置 (保持一致) ---
    if tick_interval is not None:
        if isinstance(tick_interval, (list, tuple)):
            dx, dy = (tick_interval[0], tick_interval[1]) if len(tick_interval) >= 2 else (tick_interval[0], tick_interval[0])
        else:
            dx = dy = tick_interval
        if dx is not None and dx > 0: ax.set_xticks(np.arange(0, domain[0] + dx * 0.001, dx))
        if dy is not None and dy > 0: ax.set_yticks(np.arange(0, domain[1] + dy * 0.001, dy))
    else:
        set_smart_xy_ticks(ax, extent=(0, domain[0], 0, domain[1]))
    ax.set_aspect('equal', 'box')

    # --- 绘图逻辑: 超椭圆参数方程 ---
    # x = a * sgn(cos t) * |cos t|^(2/n)
    # y = b * sgn(sin t) * |sin t|^(2/n)
    t = np.linspace(0, 2 * np.pi, resolution)
    
    for i in range(len(coordinates)):
        xc, yc = coordinates[i]
        a, b = semi_axes[i]
        n = exponents[i]
        
        # 参数方程计算边界点
        x_pts = xc + a * np.sign(np.cos(t)) * (np.abs(np.cos(t))) ** (2 / n)
        y_pts = yc + b * np.sign(np.sin(t)) * (np.abs(np.sin(t))) ** (2 / n)
        
        # 绘制封闭曲线并填充
        ax.fill(x_pts, y_pts, facecolor='white', edgecolor='black', linewidth=1, zorder=2)
        
        if show_particle_labels:
            plt.text(xc, yc, rf"$\text{{SE}}_{{{i + 1}}}$", fontsize=8, ha='center', va='center', zorder=3)

    ax.grid(True, linestyle='--', linewidth=0.75, zorder=1)
    ax.tick_params(axis="both", length=2.5, direction="in", width=0.75, which="both", pad=4)
    plt.xlabel('X-axis', fontweight=font_weight, labelpad=2)
    plt.ylabel('Y-axis', fontweight=font_weight, labelpad=3)
    if show_title:
        plt.title(title, pad=7.5, fontweight=font_weight)

    plt.tight_layout(pad=0.5)
    if save: save_figure(save_path, dpi=set_default_dpi_figsize_savedir()[0])
    if show: plt.show()
    plt.close()
    return save_path


def plot_initial_capsule_schematic(
    coordinates: list,
    radii: list,
    lengths: list,
    angles: list,
    domain: list,
    title: str = "Initial Capsule Distribution",
    show: bool = False,
    save: bool = False,
    font_style: str = None,
    show_title: bool = True,
    font_weight: str = "bold",
    tick_interval: Union[float, List[float], Tuple[float, float]] = None,
    show_particle_labels: bool = True,
):
    """
    绘制初始胶囊/跑道形(Capsule)粒子分布的示意图
    胶囊由一个矩形和两个半圆组成。
    
    Args:
        coordinates (list): 粒子几何中心坐标 [[x1, y1], ...]
        radii (list): 胶囊两侧半圆的半径 [r1, r2, ...] (也即胶囊厚度的一半)
        lengths (list): 胶囊中间直线段的长度 [L1, L2, ...] (总长度 = L + 2r)
        angles (list): 旋转角度列表 [deg1, deg2, ...], 单位为度，逆时针为正。
        domain (list): [width, height]
        ... (其他参数同 plot_initial_particle_schematic)
    """

    # --- 样式设置 (保持一致) ---
    if not font_style:
        if font_weight == 'bold': set_cm_style(bold=True)
        elif font_weight == 'normal': set_cm_style(bold=False)
        else: raise ValueError("Invalid font_weight.")
    elif font_style == 'sans':
        if font_weight == 'bold': set_sans_style(bold=True)
        elif font_weight == 'normal': set_sans_style(bold=False)
    elif font_style == 'times':
        if font_weight == 'bold': set_default_style(bold=True)
        elif font_weight == 'normal': set_default_style(bold=False)
    else:
        raise ValueError("Invalid font_style.")

    save_dir = os.path.join(set_default_dpi_figsize_savedir()[2], "InitialSchematic")
    filename = generate_plot_filename(title=title)
    save_path = os.path.join(save_dir, filename)
    
    fig, ax = plt.subplots(figsize=set_default_dpi_figsize_savedir()[1], dpi=set_default_dpi_figsize_savedir()[0])
    
    ax.set_xlim(0, domain[0])
    ax.set_ylim(0, domain[1])
    
    # --- 刻度设置 (保持一致) ---
    if tick_interval is not None:
        if isinstance(tick_interval, (list, tuple)):
            dx, dy = (tick_interval[0], tick_interval[1]) if len(tick_interval) >= 2 else (tick_interval[0], tick_interval[0])
        else:
            dx = dy = tick_interval
        if dx is not None and dx > 0: ax.set_xticks(np.arange(0, domain[0] + dx * 0.001, dx))
        if dy is not None and dy > 0: ax.set_yticks(np.arange(0, domain[1] + dy * 0.001, dy))
    else:
        set_smart_xy_ticks(ax, extent=(0, domain[0], 0, domain[1]))
    ax.set_aspect('equal', 'box')

    # --- 绘图逻辑: 胶囊体 ---
    for i in range(len(coordinates)):
        cx, cy = coordinates[i]
        r = radii[i]
        L = lengths[i]
        deg = angles[i]
        rad = np.radians(deg)
        
        # 1. 构建未旋转的胶囊形状（以原点为中心）
        # 使用 matplotlib 的 FancyBboxPatch (BoxStyle='Round') 可以完美绘制胶囊
        # boxstyle="Round,pad=0,rounding_size=r" 
        # width = L, height = 2r. 
        # 注意: FancyBboxPatch 的 xy 是左下角，这里需要小心处理中心对齐和旋转
        
        # 替代方案：手动绘制 Rectangle + 2 Circles，便于精确控制旋转
        
        # 变换矩阵：先平移到中心，再旋转
        tr = transforms.Affine2D().rotate_deg_around(cx, cy, deg)
        
        # 矩形部分 (未旋转时的左下角坐标)
        # 矩形中心在 (cx, cy)，宽 L，高 2r
        rect_x = cx - L / 2
        rect_y = cy - r
        rect = patches.Rectangle((rect_x, rect_y), L, 2*r, 
                                 facecolor='white', edgecolor='black', linewidth=1, zorder=2)
        rect.set_transform(tr + ax.transData) # 应用旋转
        
        # 左侧半圆 (圆心在 cx - L/2)
        # 实际上直接画两个圆和矩形叠加即可，为了去掉内部线条，通常画完轮廓填充白色，再画一遍轮廓
        # 但最简单的方法是用 PathPatch 组合，或者 FancyBboxPatch
        
        # 使用 FancyBboxPatch 实现完整轮廓 (这是最干净的方法)
        # width=L (直线段长度), height=2r (总高度), boxstyle="Round, pad=0, rounding_size=r"
        # FancyBboxPatch 定义的是"内部矩形"的大小。
        # 如果我们希望总形状是胶囊，内部矩形应为 直线段部分。
        # 这里的 xy 是内部矩形的左下角。
        
        # 计算旋转前的左下角
        # 内部矩形宽 L, 高 0 (此时退化为线段) -> 不行，Round style 需要高度
        # 修正：定义内部矩形 宽=L, 高=0 是不行的。
        # 正确做法：使用 Capsular Path 或 简单组合
        
        # === 采用组合图形法 (视觉上融合) ===
        # 计算左右圆心 (旋转后)
        offset_x = (L / 2) * np.cos(rad)
        offset_y = (L / 2) * np.sin(rad)
        
        c1 = (cx - offset_x, cy - offset_y)
        c2 = (cx + offset_x, cy + offset_y)
        
        # 绘制
        # 技巧：为了不显示内部重叠线，先画一个更粗的白色线把内部盖住，或者使用 fill
        # 这里为了简单有效，我们构建一个多边形轮廓 + 两个圆弧
        
        # 生成胶囊轮廓点供 fill 使用
        theta = np.linspace(-np.pi/2, np.pi/2, 50)
        # 右半圆
        right_arc_x = c2[0] + r * np.cos(theta + rad)
        right_arc_y = c2[1] + r * np.sin(theta + rad)
        # 左半圆
        left_arc_x = c1[0] + r * np.cos(theta + np.pi + rad)
        left_arc_y = c1[1] + r * np.sin(theta + np.pi + rad)
        
        capsule_x = np.concatenate([right_arc_x, left_arc_x])
        capsule_y = np.concatenate([right_arc_y, left_arc_y])
        
        ax.fill(capsule_x, capsule_y, facecolor='white', edgecolor='black', linewidth=1, zorder=2)

        if show_particle_labels:
            plt.text(cx, cy, rf"$\text{{Cap}}_{{{i + 1}}}$", fontsize=8, ha='center', va='center', zorder=3)

    ax.grid(True, linestyle='--', linewidth=0.75, zorder=1)
    ax.tick_params(axis="both", length=2.5, direction="in", width=0.75, which="both", pad=4)
    plt.xlabel('X-axis', fontweight=font_weight, labelpad=2)
    plt.ylabel('Y-axis', fontweight=font_weight, labelpad=3)
    if show_title:
        plt.title(title, pad=7.5, fontweight=font_weight)

    plt.tight_layout(pad=0.5)
    if save: save_figure(save_path, dpi=set_default_dpi_figsize_savedir()[0])
    if show: plt.show()
    plt.close()
    return save_path