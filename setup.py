# -*- coding: utf-8 -*-
# flake8: noqa

"""Installation script."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os
import os.path as op
import re

from setuptools import setup


#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

def _package_tree(pkgroot):
    path = op.dirname(__file__)
    subdirs = [op.relpath(i[0], path).replace(op.sep, '.')
               for i in os.walk(op.join(path, pkgroot))
               if '__init__.py' in i[2]]
    return subdirs


curdir = op.dirname(op.realpath(__file__))
with open(op.join(curdir, 'README.md')) as f:
    readme = f.read()


# Find version number from `__init__.py` without executing it.
filename = op.join(curdir, 'phy/__init__.py')
with open(filename, 'r') as f:
    version = re.search(r"__version__ = '([^']+)'", f.read()).group(1)


setup(
    name='phy',
    version=version,
    license="BSD",
    description='Interactive visualization and manual spike sorting of large-scale ephys data',
    long_description=readme,
    author='Cyrille Rossant (cortex-lab/UCL/IBL)',
    author_email='cyrille.rossant at gmail.com',
    url='https://phy.cortexlab.net',
    packages=_package_tree('phy'),
    package_dir={'phy': 'phy'},
    package_data={
        'phy': ['*.vert', '*.frag', '*.glsl', '*.npy', '*.gz', '*.txt',
                '*.html', '*.css', '*.js', '*.prb', '*.ttf', '*.png'],
    },
    entry_points={
        'console_scripts': [
            'phy = phy.apps:phycli'
        ],
    },
    include_package_data=True,
    keywords='phy,data analysis,electrophysiology,neuroscience',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Framework :: IPython",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
