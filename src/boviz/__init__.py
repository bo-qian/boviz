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
from .style import set_default_style, set_ax_style, apply_axis_scientific_format, apply_axis_limits_and_ticks, save_or_display_legend, plot_residual_curves, set_sans_style, set_smart_xy_ticks, set_cm_style
from .utils import generate_plot_filename, load_data_csv, save_figure, generate_particle_layout, build_tanh_phase_field, load_exodus_data, get_math_label, _broadcast, _bbox_cols_from_gridspec, _bbox_rows_from_axes
from .curves import plot_curves_csv, plot_curves, plot_dual_curves_csv
from .histogram import plot_histogram
from .heatmap import plot_heatmap_particle, plot_heatmap_exodus2d, plot_heatmap_exodus2d_grid
from .schematic import plot_initial_particle_schematic, plot_initial_superellipse_schematic, plot_initial_capsule_schematic