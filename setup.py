#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'PyYAML==3.11',
    'six',
    'import_string'
]

test_requirements = [
    'pytest==2.9.2',
    'pytest-xdist==1.14'
]

setup(
    name='manage',
    version='0.1.9',
    description=(
        "Command Line Manager + Interactive Shell for Python Projects"
    ),
    long_description=readme + '\n\n' + history,
    author="Bruno Rocha",
    author_email='rochacbruno@gmail.com',
    url='https://github.com/rochacbruno/manage',
    packages=['manage'],
    package_dir={'manage': 'manage'},
    entry_points={
        'console_scripts': [
            'manage=manage.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='manage',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
