'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 15:37:28
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-25 19:09:54
FilePath: /BoPlotKit/boplot/__init__.py
Description: This module initializes the BoPlotKit package, exposing its main functionalities.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''


from .config import GLOBAL_COLORS, DEFAULT_SAVE_DIR, DEFAULT_DPI, DEFAULT_FIGSIZE
from .style import set_default_style
from .utils import generate_plot_filename
from .curves import plot_curves
from .schematic_particles import plot_initial_particle_schematic
