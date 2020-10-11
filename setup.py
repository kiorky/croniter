# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

install_requires = [
    a.strip()
    for a in read('requirements/base.txt').splitlines()
    if a.strip() and not a.startswith(('#', '-'))
]

long_description = "\n\n".join(
    [
        read('README.rst'),
        read('docs', 'CHANGES.rst'),
    ]
)

setup(
    name='croniter',
    version='0.3.35',
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
    install_requires=install_requires,
    license="MIT License",
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
)
