import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from matplotlib import gridspec
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from boviz.style import set_default_style, set_smart_xy_ticks, set_sans_style
from boviz.config import set_default_dpi_figsize_savedir
from boviz.utils import generate_plot_filename, generate_particle_layout, build_tanh_phase_field, save_figure, load_exodus_data_netcdf, _broadcast, _bbox_cols_from_gridspec, _bbox_rows_from_axes


def plot_heatmap_particle(
    particle_x_num: int,
    particle_y_num: int,
    particle_radius: float,
    border: float = None,
    cmap: str = 'coolwarm',
    title_figure: str = "Initial Particle Schematic",
    show: bool = False,
    save: bool = False,
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

    plt.tight_layout(pad=0.1)
    filename = generate_plot_filename(title=title_figure, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path


def plot_heatmap_exodus2d(
    path: str,
    variable: str,
    colorbar_range: tuple = None,
    time_step: int = 0,
    cmap: str = 'coolwarm',
    title_figure: str = None,
    show: bool = False,
    save: bool = False,
    information: str = None,
    font_style: str = None,
    font_weight: str = "bold",
    show_ticks: bool = True,
):
    """
    绘制 Exodus 2D 数据的热图。

    Args:
        path (str): Exodus 2D NetCDF 文件路径。
        variable (str): 需要绘制的变量名。
        colorbar_range (tuple, optional): 色条的取值范围 (vmin, vmax)。若为 None，则自动根据数据计算。
        time_step (int, optional): 变量的时间步索引，默认为 0。
        cmap (str, optional): 热图使用的颜色映射，默认为 'coolwarm', 可选值包括 'viridis', 'plasma', 'inferno', 'magma', 'cividis' 等。
        title_figure (str, optional): 图像标题，默认为文件内自带标题。
        show (bool, optional): 是否显示图像，默认为 False。
        save (bool, optional): 是否保存图像，默认为 False。
        information (str, optional): 附加信息，用于生成文件名后缀。
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
    
    coordinates, variable_values, title, save_name = load_exodus_data_netcdf(
        source=path, 
        variable_name=variable, 
        time_step=time_step
    )

    x = coordinates[:, 0]
    y = coordinates[:, 1]

    if colorbar_range is None:
        heatmap = ax.tricontourf(x, y, variable_values, cmap=cmap, levels=256, origin='lower')
        vmin, vmax = heatmap.get_clim()
    else:
        vmin, vmax = colorbar_range
        levels = np.linspace(vmin, vmax, 256)
        heatmap = ax.tricontourf(x, y, variable_values, cmap=cmap, levels=levels, origin='lower')

    print(f"[INFO] 热图绘制完成。")

    if show_ticks:
        set_smart_xy_ticks(ax)
        ax.set_xlabel('X Coordinate', fontweight=font_weight)
        ax.set_ylabel('Y Coordinate', fontweight=font_weight)
    else:
        ax.set_xticks([])
        ax.set_yticks([])
    
    if title_figure is None:
        title_figure = title
    ax.set_title(title_figure, pad=20, fontweight=font_weight)
    ax.set_aspect('equal', adjustable='box')
    divider = make_axes_locatable(plt.gca())
    width = axes_size.AxesY(ax, aspect=1. / 20)
    pad = axes_size.Fraction(0.5, width)
    cax = divider.append_axes("right", size=width, pad=pad)
    cbar = plt.colorbar(heatmap, cax=cax)
    
    tick_locs = np.linspace(vmin, vmax, 6)
    cbar.set_ticks(tick_locs)
    cbar.set_ticklabels([f"{v:.1f}".replace("-0.0", "0.0") for v in tick_locs])


    plt.tight_layout(pad=0.1)
    filename = generate_plot_filename(title=save_name, suffix=label_suffix)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close()
    return save_path


def plot_heatmap_exodus2d_grid(
    nx: int,
    ny: int,
    paths,
    variables,
    time_steps=0,
    cmap='coolwarm',
    colorbar_range: tuple | None = None,   # (vmin, vmax)；None 自动
    titles: list | None = None,            # 每个子图标题；None 用文件内标题
    suptitle: str | None = None,           # 总标题
    panel_title_size: int = 20,            # 小图标题字号（更小）
    suptitle_size: int = 24,               # 总标题字号
    cbar_width: float = 0.025,     # ← 色条宽度（相对图像坐标）
    cbar_pad: float = 0.025,      # ← 色条与右侧子图之间的间距
    information: str | None = None,
    font_style: str | None = None,
    font_weight: str = 'bold',
    show: bool = False,
    save: bool = False,
):
    """
    绘制 Exodus2D 网格数据的热力图（支持多子图排版）。

    Args:
        nx (int): 水平子图数量。
        ny (int): 垂直子图数量。
        paths (list[str] | str): Exodus2D NetCDF 文件路径列表或单一路径（会广播）。
        variables (list[str] | str): 变量名列表或单一变量名（会广播）。
        time_steps (list[int] | int, optional): 时间步索引列表或单一索引（会广播），默认为 0。
        cmap (str | list[str], optional): 颜色映射名称或列表，默认为 'coolwarm'（会广播）。
        colorbar_range (tuple, optional): 色条取值范围 (vmin, vmax)，默认为 None（自动计算）。
        titles (list[str], optional): 每个子图的标题列表，默认为 None（使用文件内标题）。
        suptitle (str, optional): 总标题，默认为 None。
        panel_title_size (int, optional): 小图标题字号，默认为 20。
        suptitle_size (int, optional): 总标题字号，默认为 24。
        cbar_width (float, optional): 色条宽度（相对图像坐标），默认为 0.025。
        cbar_pad (float, optional): 色条与右侧子图间距（相对图像坐标），默认为 0.025。
        information (str, optional): 附加信息，用于生成文件名后缀。
        font_style (str, optional): 字体样式，默认为 None。可选值为 'sans' 或 None。
        font_weight (str, optional): 字体粗细，默认为 'bold'。可选值为 'bold' 或 'normal'.
        show (bool, optional): 是否显示图像，默认为 False。
        save (bool, optional): 是否保存图像，默认为 False。

    Returns:
        str: 保存的图像路径。
    """
    # 字体与风格
    if not font_style:
        if font_weight == 'bold': set_default_style(bold=True)
        elif font_weight == 'normal': set_default_style(bold=False)
        else: raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    elif font_style == 'sans':
        if font_weight == 'bold': set_sans_style(bold=True)
        elif font_weight == 'normal': set_sans_style(bold=False)
        else: raise ValueError("Invalid font_weight. Choose 'bold' or 'normal'.")
    else:
        raise ValueError("Invalid font_style. Choose 'sans' or None.")

    N = nx * ny
    paths      = _broadcast(paths, N)
    variables  = _broadcast(variables, N)
    time_steps = _broadcast(time_steps, N)
    cmaps      = _broadcast(cmap, N)

    dpi, figuresize, savedir = set_default_dpi_figsize_savedir()

    fig = plt.figure(figsize=figuresize, dpi=dpi)
    gs = gridspec.GridSpec(
        nrows=ny, ncols=nx + 1,
        width_ratios=[1] * nx + [nx/(22-nx)],   # 右侧留出 colorbar 列
        height_ratios=[1] * ny,
        figure=fig
    )

    # 载入数据，计算全局色标范围
    recs = []  # (x, y, vals, default_title, save_name)
    gmin, gmax = np.inf, -np.inf
    for i in range(N):
        print(f"\n获取第 {i+1} 张图的数据...")
        coords, vals, dtitle, sname = load_exodus_data_netcdf(
            source=paths[i], variable_name=variables[i], time_step=time_steps[i]
        )
        x, y = coords[:, 0], coords[:, 1]
        recs.append((x, y, vals, dtitle, sname))
        if colorbar_range is None and np.size(vals):
            vmin_i, vmax_i = np.nanmin(vals), np.nanmax(vals)
            print(f"第 {i+1} 张图的色标范围: ({vmin_i}, {vmax_i})")
            gmin = min(gmin, vmin_i); gmax = max(gmax, vmax_i)

    if colorbar_range is None:
        vmin, vmax = gmin, gmax
    else:
        vmin, vmax = colorbar_range
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        raise ValueError("无法确定 colorbar 范围（数据为空或全为 NaN）。")

    # 统一色标
    norm = Normalize(vmin=vmin, vmax=vmax)
    cmap_common = cmaps[0]   # 共享色条需单一 cmap；如需每图不同色表，就不能共享色条
    sm = ScalarMappable(norm=norm, cmap=cmap_common)
    sm.set_array([])

    print("\n正在排版...")
    axes = []
    for k in range(N):
        r, c = divmod(k, nx)
        ax = fig.add_subplot(gs[r, c])
        x, y, vals, dtitle, sname = recs[k]

        levels = np.linspace(vmin, vmax, 256)
        m = ax.tricontourf(x, y, vals, levels=levels, cmap=cmaps[k], origin='lower')
        ax.set_xticks([]); ax.set_yticks([])

        # 小图标题放在图下方居中
        t = dtitle if titles is None else _broadcast(titles, N)[k]
        ax.text(0.5, -0.04, t, ha='center', va='top', transform=ax.transAxes,
                fontsize=panel_title_size, fontweight=font_weight, clip_on=False)

        ax.set_aspect('equal', adjustable='box')
        axes.append(ax)

    # x 边界：用 GridSpec 列槽位；y 边界：用实际 Axes
    fig.subplots_adjust(
        wspace=nx/(22-nx),   # 子图之间的水平间距（默认大约0.2）
        hspace=ny/(22-ny)    # 子图之间的垂直间距（默认大约0.2）
    )   
    left, right = _bbox_cols_from_gridspec(fig, gs, nx, ny)
    bottom, top = _bbox_rows_from_axes(fig, axes)
    host = fig.add_axes([left, bottom, right - left, top - bottom], frameon=False)
    host.set(xticks=[], yticks=[])
    for sp in host.spines.values():
        sp.set_visible(False)
    # 仿单图：用 divider 在右侧追加色条轴
    pad_fig = cbar_pad   # 右侧留白（占 figure 宽度），可微调
    w_fig   = cbar_width  # 色条宽度（占 figure 宽度），对应你原 cbar_width

    cax = fig.add_axes([right + pad_fig, bottom, w_fig, top - bottom])

    cbar  = fig.colorbar(sm, cax=cax)
    ticks = np.linspace(vmin, vmax, 6)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f"{v:.1f}".replace("-0.0", "0.0") for v in ticks])
    cbar.ax.tick_params(labelsize=24)
    cbar.outline.set_visible(True)

    # 总标题置顶居中
    if suptitle:  
        host.set_title(suptitle, fontsize=suptitle_size, fontweight=font_weight, pad=20)

    # 保存/显示
    label_suffix = f"({information})" if information else None
    filename = generate_plot_filename(title="Exodus2D_Grid", suffix=label_suffix)
    save_dir = os.path.join(savedir, "HeatMaps"); os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    if save:
        save_figure(save_path, dpi=dpi)
    if show:
        plt.show()
    plt.close(fig)
    return save_path