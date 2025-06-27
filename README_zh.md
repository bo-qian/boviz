# BoPlotKit 中文文档

**BoPlotKit** 是为科研人员、科学家和工程师开发的模块化、可扩展的科学绘图工具包。它提供简洁一致的 API，帮助用户高效生成高质量、可用于发表的曲线图、粒子示意图和残差分析等科学可视化图像。

---

## ✨ 主要特性

- **模块化设计**：曲线、示意图、样式、工具和配置等功能分区明确，便于维护和扩展。
- **统一美学风格**：内置配色、标记和线型，保证图像风格统一、专业。
- **灵活的曲线绘制**：支持多曲线、残差对比、对数/科学坐标、截断、坐标轴自定义、多格式图例等。
- **示意图绘制**：轻松绘制粒子分布、区域示意等科学图形。
- **智能文件命名**：自动生成如 `boplot_<timestamp>_<title>.png` 格式的图片文件名。
- **极简依赖**：仅依赖 Matplotlib、NumPy 和 Pandas。
- **易于集成**：既可独立使用，也可集成到大型 Python 工作流中。
- **测试驱动开发**：内置丰富测试用例，保证功能稳定可靠。

---

## 📦 安装方法

```bash
pip install BoPlotKit
```

或通过克隆仓库安装最新版（开发或获取最新特性）：

```bash
# 克隆仓库
git clone https://github.com/bo-qian/BoPlotKit.git
cd BoPlotKit

# （可选）创建虚拟环境
python -m venv venv && source venv/bin/activate

# 源码安装
pip install .
```

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
plot_curves(
  path=["example/data/test_plotkit_multifeature_data.csv"] * 4,
  label=["Exp 800K", "Exp 900K", "Sim 800K", "Sim 900K"],
  x=[0, 0, 0, 0],
  y=[1, 2, 3, 4],
  xy_label=["Time (s)", "Shrinkage Ratio"],
  title_figure="Shrinkage Comparison at Two Temperatures",
  use_marker=[True, True, False, False],
  legend_ncol=2,
  save=True,
  show=False,
  information="shrinkage_comparison"
)
```

<div align="center">

<img src="https://github.com/bo-qian/BoPlotKit/figures/initial_schematic/boplot_InitialParticleDistribution.png" alt="初始粒子分布示意图" width="400"/>
&nbsp;
<img src="https://github.com/bo-qian/BoPlotKit/figures/plot_curves/boplot_ShrinkageComparisonatTwoTemperatures.png" alt="不同温度下的收缩率对比" width="400"/>

</div>

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
BoPlotKit/
├── src/
│   └── boplot/
│       ├── __init__.py
│       ├── config.py            # 全局参数与配色
│       ├── curves.py            # 曲线绘图核心
│       ├── schematic.py         # 粒子示意图
│       ├── style.py             # 默认绘图样式
│       └── utils.py             # 文件名生成与辅助函数
├── tests/                       # 基于 pytest 的测试用例
├── example/                     # 示例脚本与 CSV 数据
│   ├── data/
│   └── test_example_plot.py
├── figures/                     # 输出图片（自动生成）
├── pyproject.toml               # 构建配置
├── setup.py                     # 传统安装配置
├── LICENSE
└── README.md
```

---

## 📚 依赖说明

```txt
matplotlib>=3.0
numpy>=1.18
pandas>=1.0
pytest>=6.0
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

更多高级用法和 API 说明，请参考 `tests/`、`example/` 目录或 `src/BoPlotKit/` 模块内的文档字符串。
