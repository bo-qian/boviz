import inspect

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from boviz import plot_curves, plot_curves_csv, plot_dual_curves_csv
from boviz.curves import _auto_marker_markevery, _resolve_marker_frame


@pytest.mark.parametrize("orientation", ["horizontal", "vertical", "diagonal"])
def test_overlapping_curves_have_distinct_phases(orientation):
    values = np.linspace(0, 10, 1001)
    x = np.ones_like(values) if orientation == "vertical" else values
    y = np.ones_like(values) if orientation == "horizontal" else values
    frame = _resolve_marker_frame([(x, y)])
    phases = [_auto_marker_markevery(x, y, i, 3, marker_frame=frame) for i in range(3)]
    for indices in phases:
        assert len(indices) > 2
        assert indices == sorted(set(indices))
        assert all(0 <= i < len(x) for i in indices)
    for i in range(3):
        for j in range(i):
            assert set(phases[i]).isdisjoint(phases[j])


def test_spacing_controls_density():
    x = np.linspace(0, 10, 1001)
    dense = _auto_marker_markevery(x, x, 0, marker_spacing=0.05)
    sparse = _auto_marker_markevery(x, x, 0, marker_spacing=0.2)
    assert len(dense) > len(sparse) > 1


@pytest.mark.parametrize("spacing, expected", [(None, None), ([], None), ((0.05, 0.2), (0.1, 0.2)), ([2, 4, 6], 6)])
def test_explicit_markevery_modes(spacing, expected):
    assert _auto_marker_markevery([0, 1], [0, 1], 2, marker_spacing=spacing) == expected


@pytest.mark.parametrize("x,y,expected", [([], [], None), ([np.nan], [1], None), ([1], [1], [0]), ([1, 1], [1, 1], [0])])
def test_degenerate_data(x, y, expected):
    assert _auto_marker_markevery(x, y, 0) == expected


def test_frame_ignores_nonfinite_values_and_handles_partial_limits():
    frame = _resolve_marker_frame([([0, 1, np.nan], [2, 3, 100])], xlim=(None, 2))
    assert frame[:2] == (0, 2)
    assert frame[2:4] == pytest.approx((1.95, 3.05))


def test_markers_use_only_finite_visible_x_positions():
    x = np.linspace(0, 10, 1001)
    y = x.copy()
    y[300] = np.nan
    frame = _resolve_marker_frame([(x, y)], xlim=(2, 8))
    indices = _auto_marker_markevery(x, y, 0, marker_frame=frame)
    assert indices
    assert np.isfinite(y[indices]).all()
    assert ((x[indices] >= 2) & (x[indices] <= 8)).all()


@pytest.mark.parametrize("source", ["arrays", "csv"])
def test_marker_groups_are_independent_of_color(source, tmp_path, plotted_figures):
    x = np.linspace(0, 10, 501)
    options = dict(label=["A", "B"], xy_label=("x", "y"), use_marker=[True, True],
                   marker_group=[2, 2], color_group=[0, 1], marker_spacing=0.1,
                   line_style=["--", ":"], save=True)
    if source == "arrays":
        path = plot_curves(data=[(x, x), (x, x)], **options)
    else:
        csv = tmp_path / "curves.csv"
        pd.DataFrame({"x": x, "y": x}).to_csv(csv, index=False)
        path = plot_curves_csv(path=[str(csv)] * 2, x=[0, 0], y=[1, 1], **options)
    from pathlib import Path
    assert Path(path).is_file()
    first, second = plotted_figures[-1].axes[0].lines
    assert first.get_marker() == second.get_marker() == "^"
    assert first.get_color() != second.get_color()
    assert first.get_linestyle() == "--"
    assert second.get_linestyle() == ":"
    assert set(first.get_markevery()).isdisjoint(second.get_markevery())


@pytest.mark.parametrize("markers", [False, True])
def test_dual_axis_styles(tmp_path, plotted_figures, markers):
    x = np.linspace(0, 10, 501)
    csv = tmp_path / "dual.csv"
    pd.DataFrame({"x": x, "y": x}).to_csv(csv, index=False)
    plot_dual_curves_csv(
        path=[str(csv)], label=["left"], x=[0], y=[1],
        path_right=[str(csv)], label_right=["right"], x_right=[0], y_right=[1],
        xy_label=("x", "left"), y_label_right="right", use_marker=[markers],
        use_marker_right=[markers], line_style=["--"], line_style_right=[":"],
        marker_group=[3], marker_group_right=[3], show_legend=True, save=True,
    )
    left, right = plotted_figures[-1].axes
    assert left.lines[0].get_linestyle() == "--"
    assert right.lines[0].get_linestyle() == ":"
    if markers:
        assert left.lines[0].get_marker() == right.lines[0].get_marker() == "v"
        assert left.lines[0].get_markevery() != right.lines[0].get_markevery()


@pytest.mark.parametrize("function", [plot_curves, plot_curves_csv, plot_dual_curves_csv])
def test_new_options_follow_legacy_parameters(function):
    names = list(inspect.signature(function).parameters)
    assert names.index("marker_spacing") > names.index("show_grid")
    assert names.index("marker_group") > names.index("show_grid")
