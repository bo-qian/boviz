'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 16:19:37
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-25 19:06:21
FilePath: /BoPlotKit/tests/test_plot.py
Description: Test plotting functions in BoPlotKit, including curve plotting and initial particle schematic.
Copyright (c) 2025 by Bo Qian, All Rights Reserved.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from boplot.curves import plot_curves
from boplot.schematic_particles import plot_initial_particle_schematic

base_dir = os.path.dirname(__file__)
csv_paths = [os.path.join(base_dir, "data/不同排列方式的应变变化.csv")]

base_path = "/home/qianbo/projects/viscosity_sintering"
base_path_wsl = "/mnt/d/OneDrive/Science_Research/2.Secondstage_CodeAndData_Python/Viscosity Sintering/viscosity_sintering"
base_path_local = "/mnt/d/OneDrive/Science_Research/2.Secondstage_CodeAndData_Python"
base_path_local_main = "/mnt/d/OneDrive/Science_Research"
base_path_taizhou_conference = "/mnt/d/OneDrive/Science_Research/Research Activities/2506 - 第六届相场法及集成计算材料工程论坛/模拟数据_csv版本"


plot_curves(
    path=csv_paths,
    label=["Result A", "Result B"],
    x=[0, 0],     # 假设两条曲线都用第 0 列作为 X
    y=[1, 2],     # 假设两条曲线都用第 1 列作为 Y
    factor=[1.0, 1.0],
    time_step=[0, 0],       # 不截断数据
    xy_label=("Time (s)", "Shrinkage"),
    ylog=False,
    split_legend=False,
    show_residual=False,
    title_figure="Shrinkage Curve Comparison",
    information="test",
    legend_ncol=2,
    y_sci=None,
    save=True,
)

plot_initial_particle_schematic(
    coordinates=[[90, 90], [150, 90]],
    radii=[30, 30],
    domain=[240, 180],
    title="Initial Particle Distribution",
    show=True,
    save=True
)

plot_curves(
    path=[
        base_path_taizhou_conference + "/网格无关性验证.csv",
        base_path_taizhou_conference + "/网格无关性验证.csv",
        base_path_taizhou_conference + "/网格无关性验证.csv"
    ],
    label=["M1", "M2", "M3"],
    x=[0, 0, 0],
    y=[1, 2, 3],
    information="mesh_independence",
    xy_label=["Dimensionless Time", "Dimensionless Contact Radius"],
    use_marker=[True, True, True],
    tick_interval_x=1,
    title_figure="Mesh Independence Validation",
    save=True
)

plot_curves(
    path=[
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv",
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv",
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv",
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv",
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv",
        base_path_taizhou_conference + "/不同尺寸下的颈部长度变化.csv"
    ],
    label=["b = 1", "b = 2", "b = 3", "b = 4", "b = 5", "b = 6"],
    x=[0, 0, 0, 0, 0, 0],
    y=[1, 2, 3, 4, 5, 6],
    information="different_size_particle_contact_radius",
    xy_label=["Dimensionless Time", "Dimensionless Contact Radius"],
    tick_interval_x=1.0,
    tick_interval_y=0.25,
    xlim=[0, 8.0],
    ylim=[0, 2.0],
    title_figure="Evolution of Contact Radius",
    legend_ncol=2,
    show=True,
    save=True
)