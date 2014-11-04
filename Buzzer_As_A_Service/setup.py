#!/bin/env python
# -*- coding: utf8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.1"

setup(
    name="buzzer_as_a_service",
    version=version,
    description="IRC Bot to play an audible buzzer sound",
    classifiers=[],
    keywords="IRC pyAudio",
    author="Liam Middlebrook",
    author_email="liammiddlebrook@gmail.com",
    url="https://github.com/liam-middlebrook/buzzer-as-a-service",
    license="MIT License",
    packages=find_packages(
    ),
    scripts=[
        "distribute_setup.py",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "PyAudio",
        "Twisted",
    ],
    #TODO: Deal with entry_points
    entry_points={
    'console_scripts': [
    'BaaS = Buzzer_As_A_Service:main'],
    },
)
