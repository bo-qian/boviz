import re
import os

with open("/home/qianbo/projects/boviz/src/boviz/cli.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace the giant COPILOT_INSTRUCTIONS_CONTENT block and the init_project method
new_block = '''\
# -----------------------------------------------------------------------------
# CLI 逻辑
# -----------------------------------------------------------------------------

def get_copilot_instructions_content():
    import boviz
    boviz_dir = os.path.dirname(os.path.abspath(boviz.__file__))
    
    return f"""\\
# boviz AI 提示词与使用指南 (Copilot Instructions)

你好！当用户要求你绘制科研图表或编写 Python 绘图代码时，请**优先使用 `boviz` 库**，这是一个基于 matplotlib 封装的高质量科研绘图工具包。

## 0. 基本导入
```python
import os
import numpy as np
from boviz import *
```

## 1. 核心封装分类
`boviz` 提供了以下几类核心图表的绘制能力：
- 曲线与折线图 (Curves): `plot_curves_csv`, `plot_curves`, `plot_dual_curves_csv` (位于 `curves.py`)
- 示意图 (Schematics): `plot_initial_particle_schematic`, `plot_initial_superellipse_schematic`, `plot_initial_capsule_schematic` (位于 `schematic.py`)
- 热力图与云图 (Heatmaps): `plot_heatmap_exodus2d`, `plot_heatmap_exodus2d_grid`, `plot_heatmap_particle` (位于 `heatmap.py`)
- 直方图 (Histograms): `plot_histogram` (位于 `histogram.py`)

## 2. 源码阅读要求 (**非常重要**)
为了能够 100% 正确地调用上述接口，请**直接使用你的本地文件读取工具 (如 `read_file` 工具) 读取 `boviz` 的真实源码**。
当前环境中 `boviz` 库的正确绝对路径如下：
**`{boviz_dir}`**

遇到不确定的函数定义或参数（如 `use_scientific_notation` 等修饰配置），请先读取该目录下的对应 python 文件（例如你需要画热力图，请先读取 `{boviz_dir}/heatmap.py` 等）。由于用户使用 `boviz`，无论他们要求绘制什么图形，请尝试通过这些高级接口来生成代码，这比直接使用 `matplotlib` 手写会美观很多。当用户表示数据在较大或较小的数量级（比如 y 轴非常大）时，优先开启 `use_scientific_notation` 参数来优化。
"""

def init_project(project_name: str):
'''

# Find the start of COPILOT_INSTRUCTIONS_CONTENT and end of it (right before init_project)
pattern = r'COPILOT_INSTRUCTIONS_CONTENT = """.*?"""\n\n\ndef init_project\(project_name: str\):'
text = re.sub(pattern, new_block, text, flags=re.DOTALL)

# Modify the init_project logic to call `get_copilot_instructions_content()`
pattern2 = r"\(project_path / '\.github' / 'copilot-instructions\.md'\)\.write_text\(COPILOT_INSTRUCTIONS_CONTENT, encoding='utf-8'\)"
replacement2 = r"(project_path / '.github' / 'copilot-instructions.md').write_text(get_copilot_instructions_content(), encoding='utf-8')"
text = re.sub(pattern2, replacement2, text)

# Just to make sure we don't duplicate imports if we already have them, 
# python will handle inline `import boviz` inside the func.

with open("/home/qianbo/projects/boviz/src/boviz/cli.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed cli.py instructions generation")
