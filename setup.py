#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Extract Airtable',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'click==6.7',
        'requests==2.20.0',
        'boto3==1.9.145'
    ],
    extras_require={
        'dev': [
            'pytest==4.4.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'extract-airtable=extract_airtable:main',
        ],
    }
)