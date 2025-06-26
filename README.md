# BoPlotKit

**BoPlotKit** is a modular, extensible scientific plotting toolkit developed for researchers, scientists, and engineers. It provides clean and consistent APIs to generate high-quality, publication-ready figures such as curve plots, particle schematics, and residual analysis.

---

## ✨ Features

- **Modular Design**: Well-organized modules for curves, schematics, styles, utilities, and configuration.
- **Unified Aesthetics**: Consistent visual themes with predefined colors, markers, and line styles.
- **Flexible Curve Plotting**: Support for multiple curves, residual comparison, log/scientific scale, truncation, axis customization, and multi-format legends.
- **Schematic Plotting**: Easily create particle distributions and domain diagrams.
- **Smart File Naming**: Auto-generated filenames in the format `boplot_<timestamp>_<title>.png`.
- **Minimal Dependencies**: Built on top of Matplotlib, NumPy, and Pandas.
- **Easy Integration**: Can be used as a standalone package or imported into larger Python-based workflows.
- **Test-Driven Development**: Comes with robust test cases to ensure stability and correctness.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/bo-qian/BoPlotKit.git
cd BoPlotKit

# (Optional) Create a virtual environment
python -m venv venv && source venv/bin/activate

# Install the package
pip install .
```

---

## 🚀 Quick Example

```python
from boplot import *

# Plot initial schematic of particles
plot_initial_particle_schematic(
    coordinates=[[90, 90], [150, 90]],
    radii=[30, 30],
    domain=[240, 180],
    title="Initial Particle Distribution",
    show=True,
    save=True
)

# Plot multiple curves with residual analysis
plot_curves(
    path=["example/data/test_plotkit_multifeature_data.csv"] * 2,
    label=["Sim 800K", "Sim 900K"],
    x=[0, 0],
    y=[3, 4],
    xy_label=["Time (s)", "Shrinkage Ratio"],
    title_figure="Residual Analysis",
    show_residual=True,
    save=True,
    show=True
)
```

---

## 🧪 Testing

To run all tests:

```bash
python -m pytest
```

All core plotting functions are covered by unit tests under the `tests/` directory, including:

- Curve plotting (single and multi-feature)
- Schematic particle distribution
- Residual comparison
- Style and legend configurations

---

## 📁 Project Structure

```
BoPlotKit/
├── src/
│   └── boplot/
│       ├── __init__.py
│       ├── config.py            # Global parameters and color sets
│       ├── curves.py            # Core curve plotting functions
│       ├── schematic.py         # Particle schematic functions
│       ├── style.py             # Default plot styling
│       └── utils.py             # Filename generator and helpers
├── tests/                       # Pytest-based test cases
├── example/                     # Example scripts and CSV data
│   ├── data/
│   └── test_example_plot.py
├── figures/                     # Output figures (auto-generated)
├── pyproject.toml               # Build configuration
├── setup.py                     # Legacy install config
├── LICENSE
└── README.md
```

---

## 📚 Dependencies

```txt
matplotlib>=3.0
numpy>=1.18
pandas>=1.0
pytest>=6.0
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

For advanced examples and API documentation, please refer to the `tests/` and `example/` directories, or explore the docstrings inside the `src/boplot/` module.
