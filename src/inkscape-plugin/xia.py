#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# @author : pascal.fautrero@gmail.com


import inkex
import tempfile
import os
import configparser
from xiaconverter.xiaconsole import XIAConsole
from xiaconverter.loggerinkscape import LoggerInkscape

class ImageActive(inkex.OutputExtension):
    def save(self, stream):
        pass

    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--theme")
        pars.add_argument("--directory", default=os.path.expanduser("~"),\
            help="Existing destination directory")
        pars.add_argument("--singlefile", default="true", help="export a single file or a complete files tree for local usage")

    def effect(self):

        # fix inkscape bug
        # https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/944077/comments/11
        pathNodes = self.document.xpath('//sodipodi:namedview',namespaces=inkex.NSS)
        pathNodes[0].set('id','base')

        inkexWorkingDir = "."

        # retrieve paths

        config = configparser.ConfigParser()
        config.read("./xia.cnf")
        numVersion = config.get('version', 'numVersion')
        releaseVersion = config.get('version', 'releaseVersion')
        imagesPath = inkexWorkingDir + "/" + config.get('paths', 'imagesPath')

        try:
            filePath = f"{tempfile.mkdtemp()}/temp.svg"
            self.document.write(filePath)
            console = LoggerInkscape()
            options = {
                'input_file': filePath,
                'output_dir': self.options.directory,
                'selected_theme': self.options.theme,
                'export_type': "singlefile" if self.options.singlefile == 'true' else "local"
            }
            xia = XIAConsole(config, options, console)
            xia.createIA()

        except ValueError:
           #inkex.utils.debug(ValueError)
           pass

if __name__ == '__main__':
  ia = ImageActive()
  ia.run()
