'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 19:27:14
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-06-28 01:31:49
FilePath: /BoPlotKit/setup.py
Description: This script sets up the BoPlotKit package for distribution, including metadata and dependencies.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name="BoPlotKit",
    version="0.1.6",
    author="Bo Qian",
    author_email="bqian@shu.edu.cn",
    description="Bo Qian's advanced scientific plotting toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/bo-qian/BoPlotKit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "pytest"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    include_package_data=True,
)