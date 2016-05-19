#!/usr/bin/env python
import os
from setuptools import setup

setup(
    name='django_datetime_widget',
    version='0.1',
    packages=['datetime_widget'],
    description='Widget for selecting date and time',
    author='Henrik Heino',
    author_email='henrik.heino@gmail.com',
    url='https://github.com/henu/django_datetime_widget',
    license='MIT',
    install_requires=[
        'Django>=1.6',
    ],
)
