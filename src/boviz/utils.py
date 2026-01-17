import os
import numpy as np
import pandas as pd
import meshio
from datetime import datetime
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from netCDF4 import chartostring

def generate_plot_filename(title: str, file_format='png', suffix=None) -> str:
    """
    生成统一命名格式的图片文件名，格式为：boviz_YYMMDDHHMM_title_suffix.png

    Args:
        title (str): 图像标题或描述性名称（可含空格，会被自动替换为下划线）。
        suffix (str, optional): 附加信息（如 "(test)"），默认空字符串。

    Returns:
        str: 构造后的图片文件名（不含路径）。
    """
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    title_clean = title.replace(" ", "") if title else "plot"
    if file_format not in ["png", "jpg", "jpeg", "tiff", "bmp", "pdf", "svg", "eps"]:
        raise ValueError(f"Unsupported file format: {file_format}. Supported formats are png, jpg, jpeg, tiff, bmp, pdf, svg.")
    if suffix is None:
        return f"boviz_{timestamp}_{title_clean}.{file_format}"
    else:
        return f"boviz_{timestamp}_{title_clean}{suffix}.{file_format}"


def save_figure(save_path: str, dpi: int = 300, verbose: bool = True):
    """
    保存当前图像到指定路径，并确保目录存在。

    Args:
        save_path (str): 图像保存完整路径（含文件名）。
        dpi (int): 图像分辨率，默认 300。
        verbose (bool): 是否打印保存信息，默认 True。
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.savefig(save_path, dpi=dpi)
    if verbose:
        print(f"[SAVE] 图像已保存到: {save_path}\n")


def load_data_csv(
    source: str,
    x_index: int,
    y_index: int,
    factor: tuple[tuple, tuple],
    time_step: int = 0
) -> tuple[np.ndarray, np.ndarray, str, str]:
    """
    从 CSV 文件中读取指定列的数据。

    Args:
        source (str): CSV 文件路径。
        x_index (int): X 轴数据的列索引。
        y_index (int): Y 轴数据的列索引。
        factor (tuple[touple, touple]): 用于缩放和平移 Y 轴数据的因子，格式为 [scale, offset]。
            - scale: 缩放因子，默认为 1.0。
            - offset: 平移量，默认为 0.0。
        time_step (int): 若不为 0，则只保留前 time_step 个时间步。

    Returns:
        x_data, y_data: 对应列的数据（NumPy 数组）
        x_colname, y_colname: 对应列名
    """

    if factor is None:
        factor = [(1.0, 0.0), (1.0, 0.0)]

    if not isinstance(source, str) or not source.endswith('.csv'):
        raise ValueError(f"Expected a .csv file path, got {source}")

    df = pd.read_csv(source)

    start_idx = 0
    end_idx = None
    if isinstance(time_step, int):
        if time_step != 0:
            end_idx = time_step
    elif isinstance(time_step, (list, tuple)):
        if len(time_step) >= 1:
            start_idx = time_step[0]
        if len(time_step) >= 2:
            end_idx = time_step[1] if time_step[1] != 0 else None

    x_data_raw = df.iloc[start_idx:end_idx, x_index]
    y_data_raw = df.iloc[start_idx:end_idx, y_index]
    
    x_colname = df.columns[x_index]
    y_colname = df.columns[y_index]

    x_data = x_data_raw * factor[0][0] + factor[0][1]
    y_data = y_data_raw * factor[1][0] + factor[1][1]

    return x_data.values, y_data.values, x_colname, y_colname

def generate_particle_layout(
        num_x: int, 
        num_y: int,
        radius: float,
        border: float = None,
    ) -> np.ndarray:
    """
    生成粒子布局的网格坐标。

    Args:
        num_x (int): X 方向的粒子数量。
        num_y (int): Y 方向的粒子数量。
        radius (float): 粒子的半径。
        border (float, optional): 边界的宽度，默认为2倍颗粒半径。

    Returns:
        tuple: 包含三个元素的元组：
            - centers_coordinate (list): 粒子中心坐标的列表，每个元素为 [x, y]。
            - radii (list): 每个粒子的半径列表。
            - domain_size (list): 网格的域大小 [domain_x, domain_y]。
    """
    if border is None:
        border = 2.0
    border = border * radius
    domain_x = 2 * radius * num_x + border * 2
    domain_y = 2 * radius * num_y + border * 2
    
    radii = [radius] * (num_x * num_y)
    centers_coordinate = []
    for j in range(num_y):
        for i in range(num_x):
            x_coordinate = int(domain_x / 2 + (i + (1 - num_x) / 2) * radius * 2)
            y_coordinate = int(domain_y / 2 + (j + (1 - num_y) / 2) * radius * 2)
            centers_coordinate.append([x_coordinate, y_coordinate])
    
    domain_size = [domain_x, domain_y]
    return centers_coordinate, radii, domain_size

def build_tanh_phase_field(
        centers_coordinate: list,
        radii: list,
        domain_size: list,
        tanh_width: float = 3.0,
        tanh_offset: float = 0.05
    ) -> np.ndarray:
    """
    构建基于双曲正切函数的相场。

    Args:
        centers_coordinate (list): 粒子中心坐标列表，每个元素为 [x, y]。
        radii (list): 每个粒子的半径列表。
        domain_size (list): 网格的域大小 [domain_x, domain_y]。
        tanh_width (float): 双曲正切函数的宽度，默认值为 3.0。
        tanh_offset (float): 双曲正切函数的偏移量，默认值为 0.05。

    Returns:
        np.ndarray: 生成的相场数组，大小为 [domain_x * 10, domain_y * 10]。
    """
    domain_x, domain_y = domain_size
    phase_field = 0
    x, y = np.meshgrid(np.arange(0, domain_x+0.1, 0.1), np.arange(0, domain_y+0.1, 0.1))
    for center, radius in zip(centers_coordinate, radii):
        distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
        phase_field += 0.5 * (1 - np.tanh((distance - radius) * (2 * np.arctanh(1 - 2 * tanh_offset)) / tanh_width))
    
    return phase_field


def load_exodus_data(
    source: str,
    variable_name: str,
    time_step: int = 0,
):
    """
    读取 Exodus 文件中的指定变量的指定时间步数据。
    
    args:
        source (str): Exodus 文件路径。
        variable_name (str): 要读取的变量名称。
        time_step (int): 时间步索引，默认为 0。
    returns:
        coordinates (np.ndarray): 网格节点坐标数组，形状为 (N, 2)，其中 N 是节点数量。
        variable_values (np.ndarray): 指定变量在指定时间步的值，形状为 (N,) 或 (N, M)，其中 M 是变量的维度（如标量或向量）。
    raises:
        ValueError: 如果指定的变量在 Exodus 文件中不存在。
    raises:
        FileNotFoundError: 如果指定的 Exodus 文件不存在。
    """

    print(meshio.__file__)   # 输出模块位置
    print(meshio.read)       # 输出 read 函数指针

    mesh = meshio.read(source, time_step=time_step)
    coordinates = mesh.points



    try:
        variable_values = mesh.point_data[variable_name]
        if variable_values.ndim == 2:
            variable_values = variable_values[time_step]
    except KeyError:
        raise ValueError(f"Variable '{variable_name}' not found in the Exodus file.")
    
    return coordinates, variable_values


def load_exodus_data_netcdf(source, variable_name, time_step=0):
    with Dataset(source, 'r') as f:
        # 获取节点坐标
        coords_x = f.variables["coordx"][:]
        coords_y = f.variables["coordy"][:]
        coordinates = np.stack([coords_x, coords_y], axis=1)

        # 获取变量名表
        raw_names = f.variables["name_nod_var"][:]
        var_names = chartostring(raw_names).tolist()
        var_names = [n.strip() for n in var_names]

        # 读取时间信息
        time_array = f.variables["time_whole"][:]
        num_steps = len(time_array)
        t = time_array[time_step]

        # 打印美观输出
        print("[INFO] Exodus 数据加载信息：")
        print(f"   ├─ 文件路径：{source}")
        print("   ├─ 可用变量：", var_names)
        print(f"   ├─ 当前变量：'{variable_name}'")
        print(f"   ├─ 当前时间步：第 {time_step} 步（时间 = {time_array[time_step]:.4f}）")
        print(f"   ├─ 总时间步数：{num_steps}")
        preview_steps = ", ".join([f"{t:.4f}" for t in time_array[:min(5, num_steps)]])
        tail = f", ..., {time_array[-1]:.4f}" if num_steps > 5 else ""
        print(f"   └─ 时间序列预览：[ {preview_steps}{tail} ]")

        if variable_name not in var_names:
            raise ValueError(f"变量 '{variable_name}' 不存在，可选项: {var_names}")

        print(f"[INFO] 正在绘制热图...请稍候...")
        idx = var_names.index(variable_name) + 1
        variable_values = f.variables[f"vals_nod_var{idx}"][time_step, :]
    
    # 自动生成图标题
    math_label = get_math_label(variable_name)
    title = f"{math_label} at {t:.4g}s"
    save_name = f"{variable_name}_{t:.4g}"

    return coordinates, variable_values, title, save_name


def get_math_label(var_name: str) -> str:
    """
    将变量名称映射为 LaTeX 数学表达式字符串。
    """
    mapping = {
        "F_density": r"$f$",
        "Real_Pressure": r"$P_\mathrm{real}$",
        "Stress_Magnitude": r"$|\boldsymbol{\sigma}|$",
        "Stress_xx": r"$\sigma_{xx}$",
        "Stress_xy": r"$\sigma_{xy}$",
        "Stress_yx": r"$\sigma_{yx}$",
        "Stress_yy": r"$\sigma_{yy}$",
        "V_Magnitude": r"$|\boldsymbol{v}|$",
        "c": r"$C$",
        "mu": r"$\mu$",
        "p": r"$p$",
        "u": r"$u_x$",
        "v": r"$u_y$",
    }
    return mapping.get(var_name, var_name)


def _broadcast(param, N):
    if isinstance(param, (list, tuple, np.ndarray)):
        if len(param) != N:
            raise ValueError(f"参数长度应为 {N}，但收到 {len(param)}")
        return list(param)
    return [param] * N

def _bbox_cols_from_gridspec(fig, gs, nx, ny):
    """取前 nx 列（跨 ny 行）的列槽位左右范围（figure 坐标）。"""
    fig.canvas.draw()
    # 用第一行的前 nx 列即可得到列左右边界
    bb_row0 = gs[0, :nx].get_position(fig)
    return bb_row0.x0, bb_row0.x1

def _bbox_rows_from_axes(fig, axes):
    """取实际 Axes（不含面板标题那段负偏移文本）的上下范围（figure 坐标）。"""
    fig.canvas.draw()
    y0 = min(ax.get_position().y0 for ax in axes)
    y1 = max(ax.get_position().y1 for ax in axes)
    return y0, y1
