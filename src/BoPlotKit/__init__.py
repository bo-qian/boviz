'''
# BoPlotKit Package Initialization
Description: This module initializes the BoPlotKit package, exposing its main functionalities such as plotting curves and schematic particles.
Author: Bo Qian
Email: bqian@shu.edu.cn
'''

from .config import GLOBAL_COLORS, DEFAULT_SAVE_DIR, DEFAULT_DPI, DEFAULT_FIGSIZE
from .style import set_default_style
from .utils import generate_plot_filename
from .curves import plot_curves
from .schematic_particles import plot_initial_particle_schematic
