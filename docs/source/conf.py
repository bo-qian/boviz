# boviz/docs/source/conf.py

import os
import sys
# 引入主题包 (如果安装了的话，有些版本需要import)
import sphinx_rtd_theme 

sys.path.insert(0, os.path.abspath('../../src'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # ✅ 支持 Google 风格注释
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_rtd_theme',     # ✅ 建议把主题也加到扩展里
]

# 确保支持中文
language = 'zh_CN'
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -----------------------------------------------------------------------------
# 主题设置 (Theme Setup) - 这里就是你要的蓝色主题
# -----------------------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'

# 可选：配置主题的细节（比如左上角的logo，导航栏层级等）
html_theme_options = {
    'navigation_depth': 4,           # 导航栏显示的层级深度
    'collapse_navigation': False,    # 是否折叠导航
    'sticky_navigation': True,       # 导航栏是否固定
}