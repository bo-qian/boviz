<!--
 * @Author: bo-qian bqian@shu.edu.cn
 * @Date: 2025-06-25 15:25:33
 * @LastEditors: bo-qian bqian@shu.edu.cn
 * @LastEditTime: 2025-06-25 19:13:07
 * @FilePath: /BoPlotKit/README.md
 * @Description: 
 * Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
-->
# BoPlotKit

BoPlotKit is a modular and extensible scientific plotting toolkit designed for researchers and engineers. It streamlines common data visualization tasks and helps you create high-quality, publication-ready figures with ease.

## Features

- **Modular Design**: Each functionality is independent and easy to extend or maintain.
- **Unified Style**: Built-in color schemes and style settings for consistent, professional plots.
- **Essential Plotting Functions**: Includes curve plotting, schematic particle diagrams, and more for typical scientific needs.
- **Automatic File Naming & Saving**: Generate plot filenames automatically and customize save directories.
- **Easy Integration**: Import as a standalone package or integrate seamlessly into existing projects.

## Quick Start

### Installation

```bash
git clone https://github.com/bo-qian/BoPlotKit.git
cd BoPlotKit
# (Optional) Use a virtual environment
pip install .
```

### Basic Usage

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

# Set default style
set_default_style()

# Plot curves
plot_curves(x_data, y_data, label="Example Curve")

# Plot initial particle schematic
demo_positions = [(0,0), (1,1)]  # Example data
plot_initial_particle_schematic(demo_positions)

# Generate filename and save
filename = generate_plot_filename("my_figure")
plt.savefig(filename, dpi=DEFAULT_DPI)
```

## Project Structure

```
boplot/
    __init__.py
    config.py                # Global config and defaults
    curves.py                # Curve plotting functions
    schematic_particles.py   # Particle schematic plotting
    style.py                 # Style and color settings
    utils.py                 # Utility functions (e.g., filename generation)
figures/                     # Example figures or output directory
tests/                       # Unit tests
```

## Testing

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please open issues or pull requests to improve features or fix bugs.

## License

MIT License © 2025 Bo Qian

---

For detailed documentation and examples, see module docstrings or the `tests` directory.
