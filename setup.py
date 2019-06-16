#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["ruamel.yaml>0.15"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Christophe Furmaniak",
    author_email="christophe.furmaniak@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Split multidoc yaml formatted kubernetes descriptors to a set \
        of single resource files",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords=(
        "kubesplit",
        "kubernetes",
        "yaml",
        "yamkix",
        "resource",
        "single file",
    ),
    name="kubesplit",
    packages=find_packages(include=["kubesplit"]),
    python_requires=">=3.6",
    entry_points={"console_scripts": ["kubesplit = kubesplit.__main__:main"]},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/looztra/kubesplit",
    version="0.1.0",
    zip_safe=False,
)
