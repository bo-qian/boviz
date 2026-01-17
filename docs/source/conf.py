import os
import sys
# 1. 引入自动版本管理工具 (如果没有安装，就用默认值)
try:
    from importlib.metadata import version as get_version
except ImportError:
    get_version = None
    
import sphinx_rtd_theme 

sys.path.insert(0, os.path.abspath('../../src'))

# =============================================================
#  🛑 之前缺失的关键部分 (Project Information)
# =============================================================
project = 'boviz'          # 👈 必须有这一行，左上角才会显示名字
copyright = '2026, Bo Qian'
author = 'Bo Qian'

# =============================================================
#  动态版本号逻辑 (让左上角显示 v0.3.1 而不是 v1.0.0)
# =============================================================
try:
    if get_version:
        release = get_version('boviz')
        version = release
    else:
        release = '1.0.0'
        version = '1.0.0'
except Exception:
    release = '1.0.0'
    version = '1.0.0'

# =============================================================
#  通用配置
# =============================================================
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_rtd_theme',
]

language = 'zh_CN'
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# =============================================================
#  主题设置
# =============================================================
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}