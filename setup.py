# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:50:15 2023

@author: IAmYodea
"""

from setuptools import setup, find_packages

setup(
    name='salary_extractor',
    version='0.1',
    author='Udechukwu Nonso',
    description='A package for extracting salaries from unstructured strings',
    packages=find_packages(),
    install_requires=['datetime', 're', 'statistics', 'string', 'numpy', 'ccxt'],
)

