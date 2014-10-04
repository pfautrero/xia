#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: 2014 Francois Lafont <francois.lafont@ac-versailles.fr>
#
# License: GPL-3.0+
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.core import setup
from setuptools import find_packages

# The directory which contains this script.
setup_dir = os.path.dirname(os.path.abspath(__file__))
changelog = os.path.join(setup_dir, 'CHANGELOG.md')
readme = os.path.join(setup_dir, '../README.md')

# Get the version of the application.
with open(changelog, 'r') as f:
  line1 = f.readline()
words = line1.split()
version = words[1]

# Get the long description of the application.
with open(readme, 'r') as f:
    long_description = f.read()

setup(
    name='xiaconverter',
    version=version,
    # Search all python packages in the root of setup_dir
    # (all directories which contain a __init__.py file).
    packages=find_packages(),

    # With this parameter, a non python file in a package and
    # found in MANIFEST.in will be included in the build with:
    #
    #   ./setup.py install --root=/tmp/foo --install-layout=deb
    #
    # But files in MANIFEST.in and not in a package will be
    # not included in the build with the command above.
    #
    # To create tar.gz which includes all files in MANIFEST.in,
    # use this command:
    #
    #   ./setup.py sdist
    #
    include_package_data=True,

    author='Pascal Fautrero',
    author_email='pascal.fautrero@ac-versailles.fr',
    description='Convert svg to full html5 interactive pictures',
    long_description=long_description,
    url='http://images-actives.crdp-versailles.fr/beta/',
    license='GPL-3',
)


