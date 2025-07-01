'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-26 15:45:34
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-28 01:39:40
FilePath: /boviz/tests/test_plot_curves.py
Description: This module contains unit tests for the boviz plotting functions, ensuring they work correctly with sample data.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''
import os
import pytest
import pandas as pd
import matplotlib.pyplot as plt
from boviz import plot_curves_csv, plot_curves, plot_initial_particle_schematic, generate_plot_filename

# 测试数据路径（假设你提供了样例 csv）
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_CSV = os.path.join(DATA_DIR, "sample_curve.csv")

@pytest.fixture
def setup_sample_csv(tmp_path):
    # 创建一个简单的 csv 文件
    file_path = tmp_path / "sample_curve.csv"
    df = pd.DataFrame({
        "Time": [0, 1, 2, 3, 4, 5],
        "Value1": [0.0, 0.5, 0.9, 1.4, 1.6, 2.0],
        "Value2": [0.0, 0.4, 0.8, 1.3, 1.5, 1.9]
    })
    df.to_csv(file_path, index=False)
    return str(file_path)

def test_plot_single_curve(setup_sample_csv):
    save_path = plot_curves_csv(
        path=[setup_sample_csv],
        label=["Test Curve"],
        x=[0],
        y=[1],
        title_figure="Single Curve Plot",
        information="test_case_single",
        save=True,
        show=False
    )
    assert os.path.exists(save_path)

def test_particle_schematic():
    coordinates = [[10, 10], [20, 20]]
    radii = [2, 3]
    domain = [30, 30]
    save_path = plot_initial_particle_schematic(
        coordinates, radii, domain,
        title="InitialParticleDistribution",
        save=True,
        show=False
    )
    assert os.path.exists(save_path)

