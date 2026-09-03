# boviz 中文文档

[![PyPI version](https://img.shields.io/pypi/v/boviz.svg)](https://pypi.org/project/boviz/)
[![Tests](https://github.com/bo-qian/boviz/actions/workflows/tests.yml/badge.svg)](https://github.com/bo-qian/boviz/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://pypi.org/project/boviz/)
[![Documentation Status](https://readthedocs.org/projects/boviz/badge/?version=latest)](https://boviz.readthedocs.io/zh-cn/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

`boviz` 是一个专为科研人员设计的高级 Python 绘图工具包。它基于 Matplotlib 构建，旨在用最少的代码生成符合学术发表标准（Publication-Ready）的高质量图表。无论是复杂的多曲线对比、双 Y 轴图表，还是热力图和示意图，`boviz` 都能轻松胜任，并自动应用专业的学术风格。

---

## ✨ 核心特性

* **学术级出版画质**：内置 Times New Roman 等学术字体支持，自动优化刻度、标签和图例，确保输出高分辨率、符合规范的图表。
* **高效工作流**：
    * **CSV 直读绘图**：`boviz.curves` 模块允许您直接从 CSV 文件读取数据并生成复杂对比图，无需繁琐的数据预处理。
    * **NumPy 支持**：同样支持直接绘制内存中的 NumPy 数组数据。
* **高级绘图功能**：
    * **残差分析 (Residual Analysis)**：一键自动计算并绘制实验数据与模拟数据之间的偏差。
    * **双 Y 轴 (Dual Y-Axis)**：轻松创建具有两个不同 Y 轴的图表。
    * **热力图与场数据**：使用 `boviz.heatmap` 可视化 2D 场数据（如有限元分析结果）。
    * **学术示意图**：使用 `boviz.schematic` 快速生成学术风格的示意图（如粒子分布图）。
* **自动化版本管理**：集成 `setuptools_scm`，基于 Git 标签自动管理项目版本号。

---

## 📦 安装指南

需要 Python 3.10 或更高版本。旧版安装元数据声称支持更早版本，但源码已使用 Python 3.10 语法，本版纠正该声明。

```bash
pip install boviz
```

或通过克隆仓库安装最新版（开发或获取最新特性）：

```bash
# 克隆仓库
git clone https://github.com/bo-qian/boviz.git
cd boviz

# （可选）创建虚拟环境
python -m venv venv && source venv/bin/activate

# 源码安装
pip install .
```

---

## 📖 使用方法

你可以通过内置的命令行工具快速搭建一个基于 boviz 的新项目：

```bash
boviz init my_project
```

该命令会创建一个名为 `my_project` 的新目录，包含推荐的项目结构、示例脚本和配置文件，帮助你以最佳实践组织绘图工作流。

**生成的目录结构：**
```
my_project/
├── data/
│   └── example.csv
└── plot.py
```

初始化后，你可以直接添加自己的数据和脚本，并像下方示例一样使用 boviz 的绘图函数。

---

## 🚀 快速示例

```python
from boviz import *

# 绘制初始粒子分布示意图
plot_initial_particle_schematic(
  coordinates=[[90, 90], [150, 90]],
  radii=[30, 30],
  domain=[240, 180],
  title="初始粒子分布",
  show=True,
  save=True
)

# 多曲线对比：不同实验和模拟条件下的收缩率对比
plot_curves_csv(
  path=["example/data/test_plotkit_multifeature_data.csv"] * 4,
  label=["Exp 800K", "Exp 900K", "Sim 800K", "Sim 900K"],
  x=[0, 0, 0, 0],
  y=[1, 2, 3, 4],
  xy_label=["Time (s)", "Shrinkage Ratio"],
  title_figure="Shrinkage Comparison at Two Temperatures",
  use_marker=[True, True, False, False],
  legend_ncol=2,
  save=True,
  show=True
)

# 直接传入数据进行绘图
x = np.linspace(0, 4*np.pi, 200)
y = np.sin(x)
plot_curves(
    data=[(x, y)],
    label=["$\sin(x)$"],
    xy_label=("$x$", "$\sin(x)$"),
    title_figure="Sine Wave Example",
    save=True,
    show=True
)

# 热力图示例：生成初始粒子分布的热力图
plot_heatmap_particle(
    particle_x_num=2,
    particle_y_num=1,
    particle_radius=30,
    border=1,
    cmap='coolwarm',
    title_figure="Particle Heatmap Example",
    save=True,
    show=False
)
```

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_InitialParticleDistribution.png" alt="初始粒子分布示意图" height="240"/><br/>
      <sub><b>初始粒子分布</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_ShrinkageComparisonatTwoTemperatures.png" alt="不同温度下的收缩率对比" height="240"/><br/>
      <sub><b>不同温度下的收缩率对比</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_SineWaveExample.png" alt="正弦波示例" height="240"/><br/>
      <sub><b>正弦波示例</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_ParticleHeatmapExample.png" alt="粒子热图示例" height="240"/><br/>
      <sub><b>粒子热图示例</b></sub>
    </td>
  </tr>
</table>

---

## 🧪 测试

运行全部测试：

```bash
python -m pip install -e ".[test]"
python -m pytest
```

> **注意：** Windows 用户如在 Conda 环境下安装，请在 Conda 终端（Anaconda Prompt 或已激活的 Conda shell）中运行上述命令。

当前回归测试覆盖 CSV 曲线导出、粒子示意图导出、自动 marker 错位、
间距与分组、双轴线型以及旧参数位置兼容性，尚未覆盖全部绘图 API。
测试使用无窗口后端，并将输出写入临时目录。本地测试读取仓库源码，
CI 在 Linux/Windows、Python 3.10–3.13 上验证安装后的包，并构建发布包与文档。

### Marker 控制

```python
import numpy as np
from boviz import plot_curves

x = np.linspace(0, 10, 501)
plot_curves(
    data=[(x, np.sin(x)), (x, np.sin(x))],
    label=["Experiment", "Simulation"],
    xy_label=("Time", "Response"),
    use_marker=[True, True],
    marker_spacing="auto",
    marker_group=[0, 1],
    save=True,
)
```

- `marker_spacing="auto"` 自动错开标记，名义间隔为坐标轴对角线的 0.12 倍；正数可调整该比例。
- `None` 在每个数据点绘制标记；两个数字的元组表示 `(offset_step, period)`，采用 Matplotlib 的距离模式。
- `marker_group` 独立于 `color_group` 控制标记形状。
- 双轴接口还支持 `marker_group_right`、`line_style`、`line_style_right`。

自动定位使用线性坐标映射近似，并选择已有采样点；对数坐标或稀疏曲线不保证严格等距。
详见 [更新日志](CHANGELOG.md) 和 [贡献指南](CONTRIBUTING.md)。

---

## 📁 项目结构

```
boviz/
├── src/
│   └── boviz/
│       ├── __init__.py
│       ├── cli.py               # 命令行绘图接口
│       ├── config.py            # 全局参数与配色
│       ├── curves.py            # 核心曲线绘图函数
│       ├── schematic.py         # 粒子示意图函数
│       ├── heatmap.py           # 粒子热力图绘制
│       ├── style.py             # 默认绘图样式
│       └── utils.py             # 文件名生成与辅助工具
├── tests/                       # 基于 Pytest 的测试用例
├── example/                     # 示例脚本与 CSV 数据
│   ├── data/
│   └── example_plot.py
├── figures/                     # 输出图片（自动生成）
│   └── ShowExample/             # 文档示例图片
├── requirements.txt             # 依赖包列表
├── pyproject.toml               # 构建配置
├── setup.py                     # 传统安装配置
├── LICENSE
├── README.md
└── README_zh.md                 # 中文版说明文档
```

---

## 📚 依赖说明

```txt
matplotlib>=3.0
numpy>=1.18
pandas>=1.0
meshio>=4.0
netCDF4>=1.5
```

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 🙌 贡献指南

欢迎通过以下方式参与贡献：
- 提交 issue 或 bug 报告
- 完善文档与示例
- 提交增强功能或新模块的 pull request

所有贡献都将被感谢和认可。

---

## 📜 许可证

GNU 通用公共许可证 v3 (GPLv3) © 2025 Bo Qian

---

更多高级用法和 API 说明，请参考 `tests/`、`example/` 目录或 `src/boviz/` 模块内的文档字符串。
