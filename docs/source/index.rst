.. boviz documentation master file, created by
   sphinx-quickstart on Thu Sep  4 10:01:19 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

boviz documentation
===================

boviz 是面向科研绘图的 Python 工具包，提供 CSV/NumPy 曲线比较、双轴图、
热图及粒子示意图。需要 Python 3.10 或更新版本。

安装与测试
----------

.. code-block:: bash

   pip install boviz
   # 源码开发环境
   pip install -e ".[test,docs]"
   python -m pytest

曲线标记
--------

``plot_curves``、``plot_curves_csv`` 支持 ``marker_spacing`` 自动错位间隔，
以及独立于颜色的 ``marker_group`` 形状分组。
双轴接口另提供 ``marker_group_right``、``line_style_right``。
自动定位基于线性坐标近似；对数坐标和稀疏采样可能需要手动设置。

完整示例见 `项目 README <https://github.com/bo-qian/boviz#readme>`_。


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
