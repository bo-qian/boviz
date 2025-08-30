'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 16:19:37
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-08-30 16:34:30
FilePath: /boviz/example/example_plot.py
Description: Test script for boviz, demonstrating how to use the plotting functions.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''


import os
from boviz import *
import numpy as np

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "data/test_plotkit_multifeature_data.csv")


# 1. 绘制初始粒子分布示意图
# 绘制两个初始粒子的分布示意图
plot_initial_particle_schematic(
    coordinates=[[90, 90], [150, 90]],
    radii=[30, 30],
    domain=[240, 180],
    title="Initial Particle Distribution",
    show=False,
    # save=True
)

# 绘制性能直方图
plot_histogram(
    x=[10, 20, 40, 60, 80, 100],
    y=[21871, 10927, 9690, 5977, 4949, 4932],
    title="Performance Histogram",
    label="Histogram",
    xy_label=("Number of Processor", "Runtime (h)"),
    factor=[1/3600, 0],
    # show=True,
    save=True
)

# 绘制另一个初始粒子分布示意图
plot_initial_particle_schematic(
    coordinates=[[25, 25], [55, 25]],
    radii=[15, 15],
    domain=[80, 50],
    title="Initial Particle Distribution",
    show=False,
    # save=True
)

# 2. 多曲线对比：不同实验和模拟条件下的收缩率对比
# 从CSV文件读取多条曲线并绘制对比图
plot_curves_csv(
    path=[csv_path, csv_path, csv_path, csv_path],
    label=["Exp 800K", "Exp 900K", "Sim 800K", "Sim 900K"],
    x=[0, 0, 0, 0],
    y=[1, 2, 3, 4],
    xy_label=["Time (s)", "Shrinkage Ratio"],
    title_figure="Shrinkage Comparison at Two Temperatures",
    use_marker=[True, True, False, False],
    legend_ncol=2,
    factor=[[(1.0, 0.0), (10.0, 0.0)], None, [(1.0, 0.0), (1.0, 0.0)], None],
    # save=True,
    # show=True
)

# 3. 单曲线绘图：绘制单条模拟曲线
# 从CSV文件读取单条曲线并绘制
plot_curves_csv(
    path=[csv_path],
    label=["Sim 800K"],
    x=[0],
    y=[3],
    title_figure="Shrinkage at 800K",
    # save=True,
    # show=True
)

# 4. 样式演示：展示不同颜色、marker、线型等样式
# 展示不同实验条件下曲线的样式
plot_curves_csv(
    path=[csv_path, csv_path],
    label=["Exp 800K", "Exp 900K"],
    x=[0, 0],
    y=[1, 2],
    xy_label=["Time (s)", "Shrinkage Ratio"],
    use_marker=[True, True],
    title_figure="Style Demo",
    # save=True,
    show=False
)

# 5. 残差分析图：展示两条曲线的残差
# 绘制两条模拟曲线及其残差分析
plot_curves_csv(
    path=[csv_path, csv_path],
    label=["Sim 800K", "Sim 900K"],
    x=[0, 0],
    y=[3, 4],
    xy_label=["Time (s)", "Shrinkage Ratio"],
    title_figure="Residual Analysis",
    show=False,
    # save=True,
    show_residual=True
)

# 6. 直接传入数据进行绘图
# 直接传入numpy数组绘制正弦曲线
x = np.linspace(0, 4*np.pi, 200)
y = np.sin(x)
plot_curves(
    data=[(x, y)],
    label=[r"$\sin(x)$"],
    xy_label=(r"$x$", r"$\sin(x)$"),
    title_figure="Sine Wave Example",
    factor=[[(10.0, 0.0), (10.0, 0.0)]],
    # save=True,
    show_legend=False,
    show=True
)

# 7. 热力图示例：生成初始粒子分布的热力图
# 绘制初始粒子的热力图分布
plot_heatmap_particle(
    particle_x_num=2,
    particle_y_num=1,
    particle_radius=30,
    border=1,
    cmap='coolwarm',
    title_figure="Particle Heatmap Example",
    # save=True,
    show=False
)