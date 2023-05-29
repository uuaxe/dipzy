#!/usr/bin/env python3

import setuptools


with open("README.md") as f:
    README = f.read()

setuptools.setup(
    author="Wei Xin Chan",
    author_email="weixin.1990@gmail.com",
    name="dipzy",
    license="MIT",
    description="Dipzy is a Python package for interacting with different data and notification APIs.",
    version="v0.0.1",
    long_description=README,
    url="https://github.com/uuaxe/dipzy",
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    install_requires=["numpy", "pandas", "requests", "telegram"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
