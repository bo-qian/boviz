<p align="center">
  <b>English</b> | <a href="README_zh.md"><b>中文</b></a>
</p>

[![PyPI version](https://img.shields.io/pypi/v/boviz.svg)](https://pypi.org/project/boviz/)
[![Tests](https://github.com/bo-qian/boviz/actions/workflows/tests.yml/badge.svg)](https://github.com/bo-qian/boviz/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://pypi.org/project/boviz/)
[![Documentation Status](https://readthedocs.org/projects/boviz/badge/?version=latest)](https://boviz.readthedocs.io/zh-cn/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

# boviz

`boviz` is an advanced Python toolkit designed for generating publication-quality scientific figures with minimal code. Built on top of Matplotlib, it simplifies the creation of complex plots like multi-curve comparisons, dual-axis charts, heatmaps, and schematic diagrams, all while automatically applying academic styling conventions.

---

## ✨ Key Features

* **Publication-Ready Aesthetics**: Automatically applies academic font styles (e.g., Times New Roman) and optimizes tick marks, labels, and legends for high-resolution output.
* **Streamlined Workflow**:
    * **CSV to Plot**: The `boviz.curves` module allows you to generate complex comparison plots directly from CSV files with a single function call.
    * **NumPy Support**: Easily plot data directly from NumPy arrays.
* **Advanced Plotting Capabilities**:
    * **Residual Analysis**: Automatically calculate and visualize the difference between experimental and simulation data.
    * **Dual Y-Axis**: Effortlessly create plots with two different Y-axes.
    * **Heatmaps & Fields**: Visualize 2D fields (e.g., from finite element analysis) with `boviz.heatmap`.
    * **Schematics**: Generate academic-style schematic diagrams (e.g., particle distributions) with `boviz.schematic`.
* **Automated Versioning**: Uses `setuptools_scm` for seamless version management based on Git tags.

---

## 📦 Installation

Requires Python 3.10 or newer. Earlier metadata incorrectly advertised older Python versions despite the source using Python 3.10 syntax.

```bash
pip install boviz
```

Or, to install the development or latest version from source:

```bash
# Clone the repository
git clone https://github.com/bo-qian/boviz.git
cd boviz

# (Optional) Create a virtual environment
python -m venv venv && source venv/bin/activate

# Install the package from source
pip install .
```

---

## 📖 Usage

For detailed API documentation, tutorials, and more examples, please visit the official documentation:
👉 https://boviz.readthedocs.io/zh-cn/latest/

You can quickly scaffold a new boviz-based project using the built-in CLI:

```bash
boviz init my_project
```

This command creates a new directory `my_project` with a recommended structure, including example scripts and configuration files. It helps you get started with best practices for organizing your plotting workflow.

**Generated structure:**
```
my_project/
├── data/
│   └── example.csv
└── plot.py
```

After initialization, you can immediately start adding your data and scripts, and use boviz's plotting functions as shown below.

---

## 🚀 Quick Example

```python
from boviz import *
import numpy as np

# Plot initial particle distribution schematic
plot_initial_particle_schematic(
  coordinates=[[90, 90], [150, 90]],
  radii=[30, 30],
  domain=[240, 180],
  title="Initial Particle Distribution",
  show=True,
  save=True
)

# Multiple feature curve plotting
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
  show=False
)

# Single curve plotting: Plot a single simulation curve
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

# Particle heatmap example
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
      <sub><b>Initial Particle Distribution</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_ShrinkageComparisonatTwoTemperatures.png" alt="不同温度下的收缩率对比" height="240"/><br/>
      <sub><b>Shrinkage Comparison</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_SineWaveExample.png" alt="正弦波示例" height="240"/><br/>
      <sub><b>Sine Wave Example</b></sub>
    </td>
    <td align="center">
      <img src="https://github.com/bo-qian/boviz/blob/main/figures/ShowExample/boviz_ParticleHeatmapExample.png" alt="粒子热图示例" height="240"/><br/>
      <sub><b>Particle Heatmap Example</b></sub>
    </td>
  </tr>
</table>

---

## 🧪 Testing

To run all tests, use:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

> **Note:** On Windows, if you installed boviz in a Conda environment, make sure to run this command from the Conda terminal (Anaconda Prompt or your activated Conda shell), not from the default system terminal.

The tests cover CSV curve export, particle schematic export, automatic marker
placement, spacing and grouping, dual-axis styles, and legacy parameter order.
This is targeted regression coverage, not exhaustive coverage of all plotting APIs.
Tests run headlessly and write figures to temporary directories. Local pytest uses
the source tree; CI tests the installed package on Linux and Windows with Python
3.10–3.13, and builds the distribution and documentation.

### Marker controls

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

- `marker_spacing="auto"` uses phased marker placement with a nominal period of
  0.12 of the axes diagonal; a positive number changes that fraction.
- `marker_spacing=None` marks every data point. A two-number tuple specifies
  `(offset_step, period)` for Matplotlib's distance-based `markevery` mode.
- `marker_group` selects marker shapes independently of `color_group`.
- `plot_dual_curves_csv` also supports `marker_group_right`, `line_style`, and
  `line_style_right`.

Automatic placement uses a linear data-to-display approximation and selects
existing samples; it does not guarantee uniform spacing on logarithmic axes or
very sparsely sampled curves. See [release notes](CHANGELOG.md).

---

## 📁 Project Structure

```
boviz/
├── src/
│   └── boviz/
│       ├── __init__.py
│       ├── cli.py               # Command-line interface for plotting
│       ├── config.py            # Global parameters and color sets
│       ├── curves.py            # Core curve plotting functions
│       ├── schematic.py         # Particle schematic functions
│       ├── heatmap.py           # Particle heatmap plotting
│       ├── style.py             # Default plot styling
│       └── utils.py             # Filename generator and helpers
├── tests/                       # Pytest-based test cases
├── example/                     # Example scripts and CSV data
│   ├── data/
│   └── example_plot.py
├── figures/                     # Output figures (auto-generated)
│   └── ShowExample/             # Example figures for documentation
├── requirements.txt             # Required dependencies
├── pyproject.toml               # Build configuration
├── setup.py                     # Legacy install config
├── LICENSE
├── README.md
└── README_zh.md                 # Chinese version of the README
```

---

## 📚 Dependencies

```txt
matplotlib>=3.0
numpy>=1.18
pandas>=1.0
meshio>=4.0
netCDF4>=1.5
```

Install via:

```bash
pip install -r requirements.txt
```

---

## 🙌 Contributing

Feel free to contribute by:

- Reporting issues and bugs
- Improving documentation and examples
- Submitting pull requests with enhancements or new plotting modules

All contributions are welcome and appreciated.

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, testing, and release checks.

---

## 📜 License

GNU General Public License v3 (GPLv3) License © 2025 Bo Qian

---

For advanced examples and API documentation, please refer to the `tests/` and `example/` directories, or explore the docstrings inside the `src/boviz/` module.
