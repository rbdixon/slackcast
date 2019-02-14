#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'slackclient',
    'ipython>=7.0.0',
    'attrs',
    'prompt_toolkit',
    'pyparsing',
    'keyring',
]

setup_requirements = ['pytest-runner']

test_requirements = ['pytest']

setup(
    author="Brad Dixon",
    author_email='rbdixon@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Send cells from IPython to slack.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slackcast',
    name='slackcast',
    packages=find_packages(include=['slackcast']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rbdixon/slackcast',
    version='0.4.0',
    zip_safe=False,
)
