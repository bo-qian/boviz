'''
Author: bo-qian bqian@shu.edu.cn
Date: 2025-06-25 19:27:14
LastEditors: bo-qian bqian@shu.edu.cn
LastEditTime: 2025-07-01 16:54:10
FilePath: /boviz/setup.py
Description: This script sets up the boviz package for distribution, including metadata and dependencies.
Copyright (c) 2025 by Bo Qian, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name="boviz",
    version="0.1.8",
    author="Bo Qian",
    author_email="bqian@shu.edu.cn",
    description="Bo Qian's advanced scientific plotting toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/bo-qian/boviz",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
        "pytest",
        "pathlib",
        "argparse"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'boviz = boviz.cli:main',
        ],
    },
)