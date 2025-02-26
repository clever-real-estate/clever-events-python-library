#!/usr/bin/env python
"""
pip setup file
"""
from setuptools import find_packages, setup

from clever_events_library import __version__

__library__ = "clever-events-python-library"
__user__ = "https://github.com/clever-real-estate"


with open("README.md") as readme:
    LONG_DESCRIPTION = readme.read()


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    author="Clever Real Estate",
    author_email="automation@movewithclever.com",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description=("Clever Real Estate Events Library"),
    download_url=f"{__user__}/{__library__}.git",
    install_requires=required,
    license="LICENSE",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    name="clever_events_python_library",
    packages=find_packages(),
    url=f"{__user__}/{__library__}.git",
    version=__version__,
    zip_safe=False,
    py_modules=["clever_events_library", "boto3"],
)
