#!/usr/bin/env python

import io
import os
import re

from setuptools import find_packages, setup

with io.open("fins/version.py", "rt", encoding="utf-8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="fins-driver",
    version=version,
    description="Python FINS driver for Omron PLC",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    author="Indra Rudianto",
    author_email="indrarudianto.official@gmail.com",
    url="https://gitlab.com/smartoperator/fins-driver",
    zip_safe=False,
    packages=find_packages(exclude=["tests", "docs"]),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
