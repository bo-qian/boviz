"""Headless tests with isolated output directories and Matplotlib state."""
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest


@pytest.fixture(autouse=True)
def isolated_plotting(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with matplotlib.rc_context():
        yield
    plt.close("all")


@pytest.fixture
def plotted_figures(monkeypatch):
    """Retain finished figures for assertions without bypassing rendering."""
    figures = []
    close = plt.close

    def capture(fig=None):
        if fig is None:
            figures.append(plt.gcf())
        close(fig)

    monkeypatch.setattr(plt, "close", capture)
    return figures
