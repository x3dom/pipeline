#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


deps = [
    'Flask>=0.9',
    'Flask-Script>=0.5.1,<0.6.0',
    'redis>=2.7.0,<2.8.0',
    'celery>=3.0.13,<3.1.0'
]


setup(
    name='modelconvert',
    version='0.1',
    description='3D model conversion service',
    long_description=__doc__,
    packages=['modelconvert'],
    include_package_data=True,
    zip_safe=False,
    install_requires=deps
)