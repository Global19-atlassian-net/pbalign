#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pbalign',
    version='0.3.1',
    author='Pacific Biosciences',
    author_email='devnet@pacificbiosciences.com',
    license='BSD-3-Clause-Clear',
    packages=find_packages(),
    install_requires=[
        'pbcore >= 0.8.5',
        'pbcommand >= 0.2.0',
        'pysam >= 0.15.1',
    ],
    test_requires=[
        'nose',
        'pbtestdata',
    ],
    test_suite='nose.collector',
    entry_points={'console_scripts': [
        'pbalign = pbalign.pbalignrunner:main',
        'maskAlignedReads.py = pbalign.tools.mask_aligned_reads:main',
        'loadChemistry.py = pbalign.tools.loadChemistry:main',
        'extractUnmappedSubreads.py = pbalign.tools.extractUnmappedSubreads:main',
        'createChemistryHeader.py = pbalign.tools.createChemistryHeader:main'
    ]}
)
