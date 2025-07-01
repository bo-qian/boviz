"""
boviz: A Python plotting toolkit for scientific visualization.

This package exports:
    - plot_curves: Plotting of scientific curves with customizable styles.
    - plot_initial_particle_schematic: Visualization of initial particle schematics.
    - set_default_style: Set global matplotlib style for consistent appearance.
    - generate_plot_filename: Utility for generating plot filenames.
    - GLOBAL_COLORS, DEFAULT_SAVE_DIR, DEFAULT_DPI, DEFAULT_FIGSIZE: Global configuration constants.

Programs that import and use 'boviz' can easily create publication-quality plots
with consistent styles and convenient utilities.

Author: Bo Qian
Email: bqian@shu.edu.cn
"""

from .config import GLOBAL_COLORS, set_default_dpi_figsize_savedir, set_residual_dpi_figsize_savedir
from .style import set_default_style, set_ax_style, apply_axis_scientific_format, apply_axis_limits_and_ticks, save_or_display_legend, plot_residual_curves, set_sans_style, set_smart_xy_ticks
from .utils import generate_plot_filename, load_data_csv, save_figure, generate_particle_layout, build_tanh_phase_field
from .curves import plot_curves_csv, plot_curves
from .heatmap import plot_heatmap_particle
from .schematic import plot_initial_particle_schematic