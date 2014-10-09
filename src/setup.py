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
import stat
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


# start application building
#grunt.registerTask('default', ['clean:build', 'copy:main' , 'pot', 'shell:msgmerge', 'potomo', 'chmod', 'concat:jsfiles', 'clean:js']);  

class default():
    def __init__(self):
        self.locales = ['en_US', 'fr_FR']
        self.dirbuild = 'build'
        self.dirsource = 'src'
        self.themes = [ 
              "accordionBlack", 
              "accordionCloud", 
              "audioBrown", 
              "popBlue", 
              "popYellow", 
              "buttonBlue", 
              "game1clic", 
              "gameDragAndDrop" 
        ]

        self.jsfiles = [ 
            "iaobject.js", 
            "hooks.js", 
            "iascene.js", 
            "iframe.js", 
            "main.js" 
        ]    

    def mos(self, locale):
        return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.mo'

    def pos(self, locale):
        return 'build/share/i18n/' + locale + '/LC_MESSAGES/xia-converter.po'

    def cleanbuild(self):
        if os.path.isdir(self.dirbuild):
            shutil.rmtree(self.dirbuild)
        os.mkdir(self.dirbuild)
        
    def cleanjs(self):
        for theme in themes:
            for script_name in self.jsfiles:
                os.remove(self.map_jsfiletoremove(theme, script_name))
        
    def copy(self):
        shutil.copytree(self.dirsource, self.dirbuild)

    def pot(self):
        continue
        
    def msgmerge(self):
        continue

    def potomo(self):
        continue
        
    def chmod(self):
        os.fchmod(self.dirbuild + "/xia.py", stat.S_IRWXU)
        continue
    
    def map_xiajs(self, theme):
        return self.dirbuild + '/share/themes/' + theme + '/js/xia.js'

    def map_jsfilestoconcat(self, theme, jsfile):
        return self.dirsource + '/share/themes/' + theme + '/js/' + jsfile

    def map_jsfilestoremove(self, theme, jsfile):
        return self.dirbuild + '/share/themes/' + theme + '/js/' + jsfile
            
    def concatjs(self):
        for theme in themes:
            final_script = ''            
            for script_name in self.jsfiles:
                with open(self.map_jsfiletoconcat(theme, script_name), 'r') as f:
                    final_script += ('\n' + f.read())
                with open(self.map_xiajs(theme), 'w') as f:
                    f.write(final_script)
