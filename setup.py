# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [
        read('README.rst'),
        read('docs', 'CHANGES.rst'),
    ]
)

setup(
    name='croniter',
    version='0.3.11.dev0',
    py_modules=['croniter', ],
    description=(
        'croniter provides iteration for datetime '
        'object with cron like format'
    ),
    long_description=long_description,
    author="Matsumoto Taichi, kiorky",
    author_email='taichino@gmail.com, kiorky@cryptelium.net',
    url='http://github.com/kiorky/croniter',
    keywords='datetime, iterator, cron',
    install_requires=[
        "python-dateutil",
        "setuptools",
    ],
    license="MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    extras_require={
        'test': [
            "pytz",
        ],
    },
)
