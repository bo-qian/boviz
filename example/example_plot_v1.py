import os
from boviz import *
import numpy as np

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "data/test_plotkit_multifeature_data.csv")


# 1. 绘制初始粒子分布示意图
# 绘制两个初始粒子的分布示意图
# plot_initial_particle_schematic(
#     coordinates=[[90, 90], [150, 90]],
#     radii=[30, 30],
#     domain=[240, 180],
#     title="Initial Particle Distribution",
#     show=True,
#     # save=True
# )

# plot_initial_particle_schematic(
#     coordinates=[[90, 150], [150, 150], [90, 90], [150, 90]],
#     radii=[30]*4,
#     domain=[240, 240],
#     title="Four Particles Distribution",
#     show=True,
#     save=True
# )

# plot_initial_particle_schematic(
#     coordinates=[[0.375, 0.625], [0.625, 0.625], [0.375, 0.375], [0.625, 0.375]],
#     radii=[0.125]*4,
#     domain=[1, 1],
#     title="Four Particles Distribution",
#     show=True,
#     save=True
# )

# plot_initial_particle_schematic(
#     coordinates=[[705, 1175], [1175, 1175], [705, 705], [1175, 705]],
#     radii=[235]*4,
#     domain=[1880, 1880],
#     title="Four Particles Distribution",
#     show=True,
#     save=True
# )

# # 绘制性能直方图
# plot_histogram(
#     x=[10, 20, 40, 60, 80, 100],
#     y=[21871, 10927, 9690, 5977, 4949, 4932],
#     title="Performance Histogram",
#     label="Histogram",
#     xy_label=("Number of Processor", "Runtime (h)"),
#     factor=[1/3600, 0],
#     show=True,
#     # save=True
# )

# # 绘制另一个初始粒子分布示意图
# plot_initial_particle_schematic(
#     coordinates=[[25, 25], [55, 25]],
#     radii=[15, 15],
#     domain=[80, 50],
#     title="Initial Particle Distribution",
#     show=False,
#     # save=True
# )

# 2. 多曲线对比：不同实验和模拟条件下的收缩率对比
# 从CSV文件读取多条曲线并绘制对比图
plot_curves_csv(
    path=[csv_path, csv_path, csv_path, csv_path],
    label=["Exp 800K", "Exp 900K", "Sim 800K", "Sim 900K"],
    x=[0, 0, 0, 0],
    y=[1, 2, 3, 4],
    xy_label=["Time (s)", "Shrinkage Ratio"], # type: ignore
    title_figure="Shrinkage Comparison at Two Temperatures",
    use_marker=[True, True, False, False],
    legend_ncol=2,
    # factor=[[(1.0, 0.0), (10.0, 0.0)], None, [(1.0, 0.0), (1.0, 0.0)], None],
    save=True,
    # show=True,
    # font_style='times',
    # font_style='sans',
    # font_weight='normal'
)

# # 3. 单曲线绘图：绘制单条模拟曲线
# # 从CSV文件读取单条曲线并绘制
# plot_curves_csv(
#     path=[csv_path],
#     label=["Sim 800K"],
#     x=[0],
#     y=[3],
#     title_figure="Shrinkage at 800K",
#     # save=True,
#     # show=True
# )

# # 4. 样式演示：展示不同颜色、marker、线型等样式
# # 展示不同实验条件下曲线的样式
# plot_curves_csv(
#     path=[csv_path, csv_path],
#     label=["Exp 800K", "Exp 900K"],
#     x=[0, 0],
#     y=[1, 2],
#     xy_label=["Time (s)", "Shrinkage Ratio"],
#     use_marker=[True, True],
#     title_figure="Style Demo",
#     # save=True,
#     show=False
# )

# # 5. 残差分析图：展示两条曲线的残差
# # 绘制两条模拟曲线及其残差分析
# plot_curves_csv(
#     path=[csv_path, csv_path],
#     label=["Sim 800K", "Sim 900K"],
#     x=[0, 0],
#     y=[3, 4],
#     xy_label=["Time (s)", "Shrinkage Ratio"],
#     title_figure="Residual Analysis",
#     show=False,
#     # save=True,
#     show_residual=True
# )

# # 6. 直接传入数据进行绘图
# # 直接传入numpy数组绘制正弦曲线
# x = np.linspace(0, 4*np.pi, 200)
# y = np.sin(x)
# plot_curves(
#     data=[(x, y)],
#     label=[r"$\sin(x)$"],
#     xy_label=(r"$x$", r"$\sin(x)$"),
#     title_figure="Sine Wave Example",
#     factor=[[(10.0, 0.0), (10.0, 0.0)]],
#     # save=True,
#     show_legend=False,
#     show=True
# )

# # radius = 30
# delta = 3
# omega = 0.05
# x = np.linspace(-10, 10, 200)
# y = 0.5 * (1 - np.tanh(x * 2 * np.arctanh(1 - 2 * omega) / delta))

# y_l = np.linspace(0, 1, 200)
# x_l = - 1.5 + y_l * 0

# y_r = np.linspace(0, 1, 200)
# x_r = 1.5 + y_r * 0
# # x_r = np.arctanh(1 - 2 * (1 - omega)) + y_r * 0

# x_up = np.linspace(-10, 10, 200)
# y_up = (1 - omega) + 0 * x_up

# plot_curves(
#     data=[(x, y), (x_l, y_l), (x_r, y_r), (x_up, y_up)],
#     label=[r"$C$", r"$x=-{\delta}/{2}$", r"$x={\delta}/{2}$", r"$y=1-\omega$"],
#     xy_label=(r"$x$", r"$y$"),
#     title_figure="Interface Scheme",
#     # factor=[[(10.0, 0.0), (10.0, 0.0)]],
#     # save=True,
#     # use_marker=[False, True, True, True],
#     use_scatter=[False, False, False, False],
#     line_style=['-', '--', '--', '--'],
#     # font_style='sans',
#     # font_weight='normal',
#     show_legend=True,
#     show=True,
#     save=True
# )

# # 7. 热力图示例：生成初始粒子分布的热力图
# # 绘制初始粒子的热力图分布
# plot_heatmap_particle(
#     particle_x_num=2,
#     particle_y_num=1,
#     particle_radius=30,
#     border=1,
#     cmap='coolwarm',
#     title_figure="Particle Heatmap Example",
#     # save=True,
#     show=False
# )