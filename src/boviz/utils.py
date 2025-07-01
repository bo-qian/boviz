'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 16:58:46
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-29 17:04:47
FilePath: /boviz/src/boviz/utils.py
Description: This module provides utility functions for boviz, including generating standardized plot filenames.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''


import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def generate_plot_filename(title: str, suffix=None) -> str:
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
    if suffix is None:
        return f"boviz_{timestamp}_{title_clean}.png"
    else:
        return f"boviz_{timestamp}_{title_clean}{suffix}.png"


def save_figure(save_path: str, dpi: int = 300, verbose: bool = True):
    """
    保存当前图像到指定路径，并确保目录存在。

    Args:
        save_path (str): 图像保存完整路径（含文件名）。
        dpi (int): 图像分辨率，默认 300。
        verbose (bool): 是否打印保存信息，默认 True。
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    if verbose:
        print(f"[Saved] {save_path}")


def load_data_csv(
    source: str,
    x_index: int,
    y_index: int,
    factor: tuple,
    time_step: int = 0
) -> tuple[np.ndarray, np.ndarray, str, str]:
    """
    从 CSV 文件中读取指定列的数据。

    Args:
        source (str): CSV 文件路径。
        x_index (int): X 轴数据的列索引。
        y_index (int): Y 轴数据的列索引。
        factor (tuple[float, float]): 用于缩放和平移 Y 轴数据的因子，格式为 [scale, offset]。
            - scale: 缩放因子，默认为 1.0。
            - offset: 平移量，默认为 0.0。
        time_step (int): 若不为 0，则只保留前 time_step 个时间步。

    Returns:
        x_data, y_data: 对应列的数据（NumPy 数组）
        x_colname, y_colname: 对应列名
    """
    if not isinstance(source, str) or not source.endswith('.csv'):
        raise ValueError(f"Expected a .csv file path, got {source}")

    df = pd.read_csv(source)
    x_data = df.iloc[:time_step, x_index] if time_step else df.iloc[:, x_index]
    y_data_raw = df.iloc[:time_step, y_index] if time_step else df.iloc[:, y_index]
    x_colname = df.columns[x_index]
    y_colname = df.columns[y_index]

    y_data = y_data_raw * factor[0] + factor[1]

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