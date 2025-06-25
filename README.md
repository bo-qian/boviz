<!--
 * @Author: bo-qian bqian@shu.edu.cn
 * @Date: 2025-06-25 15:25:33
 * @LastEditors: bo-qian bqian@shu.edu.cn
 * @LastEditTime: 2025-06-25 19:39:38
 * @FilePath: /BoPlotKit/README.md
 * @Description: English introduction for BoPlotKit
 * Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
-->


# BoPlotKit

**BoPlotKit** is a modular and extensible scientific plotting toolkit designed for researchers and engineers. It streamlines common data visualization tasks and helps create high-quality, publication-ready figures with ease.

---

## ✨ Features

- **Modular Design**: Each functionality is self-contained and easy to maintain or extend.
- **Unified Visual Style**: Predefined colors, fonts, and line styles for visually consistent plots.
- **Essential Plotting Tools**: Supports curve plotting, schematic particle diagrams, residual visualization, and more.
- **Automatic File Naming**: Plot filenames are auto-generated using the format `boplot_<timestamp>_<title>.png`.
- **Easy Integration**: Usable as a standalone package or within existing Python-based projects.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bo-qian/BoPlotKit.git
cd BoPlotKit

# (Optional) Create and activate a virtual environment
# python -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install BoPlotKit as a local package
pip install .
```

---

### Example Usage

```python
from boplot import (
    plot_curves,
    plot_initial_particle_schematic,
    set_default_style,
    generate_plot_filename,
    GLOBAL_COLORS,
    DEFAULT_SAVE_DIR,
    DEFAULT_DPI,
    DEFAULT_FIGSIZE
)

# Apply consistent visual style
set_default_style()

# Plot curves from CSV file
plot_curves(
    path=["data/curve_data.csv"],
    x=[0], y=[1],
    label=["Simulation A"],
    xy_label=("Time (s)", "Stress (MPa)"),
    use_marker=[True],
    use_scatter=[False],
    title_figure="StressTimePlot"
)

# Plot schematic of initial particles
positions = [(90, 90), (150, 90)]
radii = [30, 30]
domain = [240, 180]
plot_initial_particle_schematic(positions, radii, domain)

# Save figure with auto-generated filename
filename = generate_plot_filename("my_figure")
plt.savefig(filename, dpi=DEFAULT_DPI)
```

---

## 📁 Project Structure

```
BoPlotKit/
├── boplot/
│   ├── __init__.py
│   ├── config.py                # Global config and constants
│   ├── curves.py                # Curve plotting functions
│   ├── schematic_particles.py   # Particle schematic drawing
│   ├── style.py                 # Style definitions
│   └── utils.py                 # Utilities like filename generation
├── tests/                       # Unit tests and usage examples
├── figures/                     # Output figures (optional)
├── requirements.txt             # Package dependencies
└── README.md
```

---

## 📦 Requirements

Dependencies are specified in `requirements.txt`. Main packages include:

```
matplotlib
numpy
pandas
pytest
```

Install all requirements with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing

Run unit tests using:

```bash
pytest tests/
```

This verifies the correctness of core functionalities such as curve plotting and schematic generation.

---

## 🤝 Contributing

Contributions are welcome! You may:

- Open an issue to report bugs or request features
- Submit a pull request with enhancements or new plotting modules
- Share your use cases and help improve usability

---

## 📄 License

MIT License © 2025 Bo Qian

---

For full documentation and detailed examples, see inline docstrings or browse the `tests/` directory.
