#!/usr/bin/env python
import os

with open(os.path.join("loglab", "version.py"), "rt") as f:
    version = f.read().strip()
    version = version.split("=")[1].strip().strip('"')

__version__ = version

from setuptools import find_packages, setup

SCRIPTS = ["bin/loglab"]
if os.name == "nt":
    SCRIPTS += ["bin/loglab.bat"]

setup(
    name="loglab",
    version=__version__,
    author="JeongJu Kim",
    author_email="haje01@gmail.com",
    url="https://github.com/haje01/loglab",
    description="Tools that help you design and utilize log formats",
    platforms=["any"],
    python_requires=">=3.8",
    packages=find_packages(),
    scripts=SCRIPTS,
    license="MIT License",
    install_requires=[
        "click>=8.0.0",
        "jsonschema==3.2.0",
        "jinja2",
        "tabulate[widechars]",
        "requests",
    ],
    extras_require={
        "dev": ["pytest", "coverage", "pyinstaller", "tox"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
    ],
)
