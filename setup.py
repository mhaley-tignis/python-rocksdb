#!/usr/bin/env python3

import os
import platform
import sys

import pkgconfig
from Cython.Build import cythonize
from setuptools import Extension, setup, find_packages

extra_compile_args = [
    '-std=c++11',
    '-O3',
    '-Wall',
    '-Wextra',
    '-Wconversion',
    '-fno-strict-aliasing',
    '-fno-rtti',
]

if sys.version_info < (3 , 0):
    raise Exception('python-rocksdb requires Python 3.x')

join = os.path.join

rocksdb_dir = join("src", "db")
utils_dir = join("src", "util")

rocksdb_sources = [
    join(rocksdb_dir, file)
    for file in os.listdir(rocksdb_dir)
    if file.endswith(".cc")
]
util_sources = [
    join(rocksdb_dir, file)
    for file in os.listdir(utils_dir)
    if file.endswith(".cc")
]
rocksdb_sources.append(
    os.path.join('rocksdb', '_rocksdb.pyx')
)
sources = rocksdb_sources + util_sources

ext_args = {
    "include_dirs": rocksdb_dir.split(os.pathsep) + utils_dir.split(os.pathsep),
    "library_dirs": rocksdb_dir.split(os.pathsep) + utils_dir.split(os.pathsep),
}


if platform.system() == 'Darwin':
    extra_compile_args += ['-mmacosx-version-min=10.9', '-stdlib=libc++']

if platform.system() == 'Windows':
    extra_compile_args.remove('-Wextra')
    extra_compile_args.remove('-Wconversion')
    ext_args['libraries'].remove('z')
    ext_args['libraries'].append('zlib')

rocksdb_module = Extension("rocksdb._rocksdb", sources, language="c++", extra_compile_args=extra_compile_args, **ext_args)


setup(
    name="faust-streaming-rocksdb",
    use_scm_version=True,
    description="Python bindings for RocksDB, primarily for use with Faust",
    keywords='rocksdb',
    author='William Barnhart',
    author_email="williambbarnhart@gmail.com",
    url="https://github.com/faust-streaming/python-rocksdb",
    license='BSD License',
    setup_requires=['setuptools>=25', 'Cython>=0.20', 'setuptools_scm'],
    install_requires=['setuptools>=25'],
    package_dir={'rocksdb': 'rocksdb'},
    packages=[
        "rocksdb",
    ],
    ext_modules=cythonize(
        [
            rocksdb_module,
        ],
        cplus=True,
        compiler_directives={"language_level": "3"},  # Python 3
    ),
)
