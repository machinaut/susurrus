#!/usr/bin/env python
from distutils.core import setup

setup(
    name="susurrus",
    version="0.0.1",
    scripts=["scripts/susurrus"],
    install_requires=["openai"],
)