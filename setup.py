#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


def long_description():
    desc = []
    for filename in ['README.rst', 'HISTORY.rst']:
        with open(filename, 'r') as fd:
            desc.append(fd.read())

    return '\n\n'.join(desc)


setup(
    name='manage',
    version='0.1.14',
    description="Command Line Manager + Interactive Shell for Python Projects",
    long_description=long_description(),
    author="Bruno Rocha",
    author_email='rochacbruno@gmail.com',
    url='https://github.com/pthon-manage/manage',
    packages=['manage'],
    package_dir={'manage': 'manage'},
    entry_points={'console_scripts': ['manage=manage.cli:main']},
    include_package_data=True,
    install_requires=[
        'Click>=7.1',
        'PyYAML>=5.3'
    ],
    license="ISC license",
    zip_safe=False,
    keywords='manage',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    test_suite='tests',
    tests_require=[
        'pytest>=6.2',
        'pytest-xdist>=2.2'
    ],
)
