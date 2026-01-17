import os
import sys
# 1. 引入自动版本管理工具
from importlib.metadata import version as get_version
import sphinx_rtd_theme 

sys.path.insert(0, os.path.abspath('../../src'))

# =============================================================
#  项目基本信息 (Project Information) - 之前可能缺了这部分
# =============================================================
project = 'boviz'
copyright = '2026, Bo Qian'
author = 'Bo Qian'

# 动态获取版本号 (配合 pyproject.toml 的设置)
try:
    release = get_version('boviz')
    version = release
except Exception:
    release = 'latest'
    version = release

# =============================================================
#  通用配置 (General Configuration)
# =============================================================
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # 支持 Google/NumPy 风格注释
    'sphinx.ext.viewcode',
    'myst_parser',          # 支持 Markdown
    'sphinx_rtd_theme',     # 注册主题
]

# 语言设置
language = 'zh_CN'

# Napoleon 设置
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# =============================================================
#  主题设置 (HTML Output)
# =============================================================
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    # 'logo_only': True,  # 如果你有logo图片，可以开启这个
}