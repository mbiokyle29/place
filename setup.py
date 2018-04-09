#!/usr/bin/env python
# file: setup.py
# author: mbiokyled29
import sys
from setuptools import setup

try:
    with open("requirements.txt") as reqs:
        lines = reqs.read().split("\n")
        requirements = list(filter(lambda l: not l.startswith("#"), lines))
except IOError:
    requirements = []

try:
    with open("requirements_dev.txt") as test_reqs:
        lines = test_reqs.read().split("\n")
        test_requirements = list(filter(lambda l: not l.startswith("#"), lines))
except IOError:
    test_requirements = []


setup(
    name="place",
    version="0.1.0",
    description="Emulate mv while updating config files",
    author="Kyle McChesney",
    author_email="mbiokyle29@gmail.com",
    url="https://github.com/mbiokyle29/place",
    packages=["place", "place.lib"],
    package_dir={
        "place": "place",
        "place.lib": "place/lib"
    },
    include_package_data=True,
    package_data={
        "place": ["data/.placerc"]
    },
    entry_points="""
        [console_scripts]
        place=place.main:cli
    """,
    install_requires=requirements,
    zip_safe=False,
    keywords="place",
    classifiers=[],
    test_suite="tests",
    tests_require=test_requirements
)
