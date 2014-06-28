#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: 2014 Francois Lafont <francois.lafont@crdp.ac-versailles.fr>
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

from setuptools import setup, find_packages

setup(
    name='ia-converter',
    version='2.0',
    packages=find_packages(),
    author='Pascal Fautrero',
    author_email='pascal.fautrero@ac-versailles.fr',
    description='Convert svg to full html5 interactive pictures',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='http://images-actives.crdp-versailles.fr',
    license='GPL-3',
)


