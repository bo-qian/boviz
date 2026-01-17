'''
Author: bo-qian bqian@shu.edu.cn
Description: boviz 安装脚本，集成 setuptools_scm 自动版本管理
Copyright (c) 2026 by Bo Qian, All Rights Reserved. 
'''
from setuptools import setup, find_packages

setup(
    name="boviz",
    use_scm_version=True,  # ✅ 开启：自动从 git tag 获取版本号
    setup_requires=['setuptools_scm'],  # ✅ 依赖：构建时需要这个包
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
        "argparse",
        "meshio>=4.0",
        "netCDF4>=1.5"
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