# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='speedtest',
    version='1.0.0',
    packages=find_packages(),
    entry_points={'console_scripts': ['speedtest = speedtest.main:main']},
    install_requires=[
        'click==8.0.3',
        'codetiming==1.4',
        'jsonschema==4.1.0',
        'jsonpath-ng==1.5.3',
        'pytest==6.2.5',
        'pytest-cov==3.0.0',
        'Jinja2==3.1.3',
        'types-python-dateutil',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    author='Your Name',
    author_email='yourname@example.com',
    description='A description of your application',
    keywords='speedtest',
)
