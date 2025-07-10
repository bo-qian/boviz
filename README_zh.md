# boviz 中文文档

**boviz** 是为研究人员、科学家和工程师设计的模块化、可扩展科学绘图工具包。它提供简洁一致的 API，可生成高质量、可用于发表的图形，包括曲线图、粒子示意图、热力图和残差分析。boviz 依赖极少，注重易用性，能够高效地帮助用户可视化复杂数据，无论是快速探索还是正式展示都得心应手。

---

## ✨ 主要特性

- **模块化设计**：曲线、示意图、样式、工具与配置等模块结构清晰。
- **统一美学风格**：预设配色、标记和线型，保证视觉风格一致。
- **灵活曲线绘制**：支持多曲线、残差对比、对数/科学坐标、截断、坐标轴自定义和多格式图例。
- **示意图绘制**：便捷生成粒子分布和区域示意图。
- **热力图可视化**：基于粒子的热力图，适用于空间数据分析。
- **批量绘图**：一次调用即可绘制多组数据或多张图，提升效率。
- **智能文件命名**：自动生成如 `boviz_<timestamp>_<title>.png` 格式的文件名。
- **极简依赖**：仅依赖 Matplotlib、NumPy 和 Pandas。
- **易于集成**：既可独立使用，也可嵌入更大 Python 工作流。
- **可定制样式**：支持自定义绘图风格、配色方案和图例布局。
- **发表级输出**：高分辨率图片，适用于学术论文和演示。
- **测试驱动开发**：内置丰富测试用例，保障稳定性与正确性。
- **丰富示例**：附带示例脚本和数据，便于快速上手和进阶使用。
- **项目脚手架 CLI**：通过命令行使用 `boviz init <project_name>` 快速搭建新的绘图项目结构。
- **命令行项目初始化**：通过 CLI 一键生成绘图项目结构、示例脚本和数据目录，快速上手。
- **残差分析功能**：支持多曲线残差对比与分析。
- **直接数据绘图**：不仅支持 CSV 文件，也可直接传入 numpy 数组或列表进行绘图。
- **粒子热力图与分布示意**：可视化初始粒子分布及基于粒子的热力图，适合材料、物理等空间分布分析。
- **智能输出管理**：自动生成带时间戳和标题的图片文件名，统一输出目录。
- **全局样式与配置**：全局配色、字体、分辨率、图像尺寸等参数可自定义，满足不同出版需求。

---

## 📦 安装方法

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
from boplot import *

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
python -m pytest
```

> **注意：** Windows 用户如在 Conda 环境下安装，请在 Conda 终端（Anaconda Prompt 或已激活的 Conda shell）中运行上述命令。

所有核心绘图函数均有 `tests/` 目录下的单元测试覆盖，包括：
- 曲线绘制（单曲线与多特征）
- 粒子分布示意图
- 残差对比
- 样式与图例配置

---

## 📁 项目结构

```
boviz/
├── src/
│   └── boviz/
│       ├── __init__.py
│       ├── __main__.py          # 包主入口
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
│   └── test_example_plot.py
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
pytest>=6.0
pathlib>=1.0
argparse>=1.4.0
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
