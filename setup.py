'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 19:27:14
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-25 19:28:53
FilePath: /BoPlotKit/setup.py
Description: This script sets up the BoPlotKit package for distribution, including metadata and dependencies.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name='boplot',
    version='0.1.0',
    author='Bo Qian',
    author_email='bqian@shu.edu.cn',
    description='Bo Qian\'s advanced plotting toolkit',
    long_description='A toolkit for scientific plotting, supporting curve plots, schematic diagrams, custom styles, and more.',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/BoPlotKit',  # If not available, you can temporarily set to None
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
