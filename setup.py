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
import shutil
import subprocess
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.install import install

## Important paths and filenames.
setup_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(setup_dir, 'build')
make_dir = os.path.join(setup_dir, 'make')
src_dir = os.path.join(setup_dir, 'src')
changelog = os.path.join(setup_dir, 'src/CHANGELOG.md')
readme = os.path.join(setup_dir, 'README.md')


def my_build():
    # Recreate a Cleaned build directory.
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    # Generate .mo files.
    subprocess.check_call([os.path.join(make_dir, "generate_mo.sh")])

    # Build js for each themes and in vendors/.
    subprocess.check_call([os.path.join(make_dir, "build_js.sh")])


class BuildStandalone(Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""
        pass

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""
        pass

    def run(self):
        my_build()


class Install(install):

    def run(self):
        install.run(self)
        my_build()


# Get the version of the application.
with open(changelog, 'r') as f:
  line1 = f.readline()
words = line1.split()
version = words[1]

# Get the long description of the application.
with open(readme, 'r') as f:
    long_description = f.read()

setup(
    name='xia',
    version=version,
    packages=['xiaconverter'],
    package_dir={ '': 'src'},
    cmdclass={ 'buildstandalone': BuildStandalone, 'install': Install},
    author='Pascal Fautrero',
    author_email='pascal.fautrero@ac-versailles.fr',
    description='Convert svg to full html5 interactive pictures',
    long_description=long_description,
    url='http://images-actives.crdp-versailles.fr/beta/',
    license='GPL-3',
)


