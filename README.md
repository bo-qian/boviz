<p align="center">
  <b>English</b> | <a href="README_zh.md"><b>中文</b></a>
</p>

# boviz

**boviz** is a modular and extensible scientific plotting toolkit designed for researchers, scientists, and engineers. It offers a clean, consistent API for generating high-quality, publication-ready figures—including curve plots, particle schematics, heatmaps, and residual analysis. With minimal dependencies and a focus on usability, boviz streamlines the process of visualizing complex data for both quick exploration and formal presentation.

---

## ✨ Features

- **Modular Design**: Well-organized modules for curves, schematics, styles, utilities, and configuration.
- **Unified Aesthetics**: Consistent visual themes with predefined colors, markers, and line styles.
- **Flexible Curve Plotting**: Support for multiple curves, residual comparison, log/scientific scale, truncation, axis customization, and multi-format legends.
- **Schematic Plotting**: Easily create particle distributions and domain diagrams.
- **Heatmap Visualization**: Generate particle-based heatmaps for spatial data analysis.
- **Batch Plotting**: Plot multiple datasets or figures in a single call for efficient workflow.
- **Smart File Naming**: Auto-generated filenames in the format `boviz_<timestamp>_<title>.png`.
- **Minimal Dependencies**: Built on top of Matplotlib, NumPy, and Pandas.
- **Easy Integration**: Can be used as a standalone package or imported into larger Python-based workflows.
- **Customizable Styles**: Easily adjust plot styles, color palettes, and legend layouts.
- **Publication-Ready Output**: High-resolution figures suitable for academic papers and presentations.
- **Test-Driven Development**: Comes with robust test cases to ensure stability and correctness.
- **Comprehensive Examples**: Includes example scripts and data for quick start and advanced usage.
- **Project Scaffolding CLI**: Instantly scaffold a new plotting project structure using `boviz init <project_name>` from the command line.

---

## 📦 Installation

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
from boplot import *

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
python -m pytest
```

> **Note:** On Windows, if you installed boviz in a Conda environment, make sure to run this command from the Conda terminal (Anaconda Prompt or your activated Conda shell), not from the default system terminal.

All core plotting functions are covered by unit tests under the `tests/` directory, including:

- Curve plotting (single and multi-feature)
- Schematic particle distribution
- Residual comparison
- Style and legend configurations

---

## 📁 Project Structure

```
boviz/
├── src/
│   └── boviz/
│       ├── __init__.py
│       ├── __main__.py          # Main entry point for the package
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
│   └── test_example_plot.py
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
pytest>=6.0
pathlib>=1.0
argparse>=1.4.0
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

---

## 📜 License

GNU General Public License v3 (GPLv3) License © 2025 Bo Qian

---

For advanced examples and API documentation, please refer to the `tests/` and `example/` directories, or explore the docstrings inside the `src/boviz/` module.