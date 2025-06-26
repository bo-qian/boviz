'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 16:58:46
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-26 18:29:45
FilePath: /BoPlotKit/src/BoPlotKit/utils.py
Description: This module provides utility functions for BoPlotKit, including generating standardized plot filenames.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''



from datetime import datetime

def generate_plot_filename(title: str, suffix=None) -> str:
    """
    生成统一命名格式的图片文件名，格式为：boplot_YYMMDDHHMM_title_suffix.png

    Args:
        title (str): 图像标题或描述性名称（可含空格，会被自动替换为下划线）。
        suffix (str, optional): 附加信息（如 "(test)"），默认空字符串。

    Returns:
        str: 构造后的图片文件名（不含路径）。
    """
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    title_clean = title.replace(" ", "") if title else "plot"
    if suffix is None:
        return f"boplot_{timestamp}_{title_clean}.png"
    else:
        return f"boplot_{timestamp}_{title_clean}{suffix}.png"