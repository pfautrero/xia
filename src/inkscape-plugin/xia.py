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


#import os, shutil
import inkex
import tempfile
import tkinter
import os
import configparser
from xiaconverter.mainwindow import IADialog
from xiaconverter.loggerinkscape import LoggerInkscape

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):

        # fix inkscape bug
        # https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/944077/comments/11
        pathNodes = self.document.xpath('//sodipodi:namedview',namespaces=inkex.NSS)
        pathNodes[0].set('id','base')

        #inkexWorkingDir = "."

        # retrieve paths

        config = configparser.ConfigParser()
        config.read("./xia.cnf")
        numVersion = config.get('version', 'numVersion')
        releaseVersion = config.get('version', 'releaseVersion')
        imagesPath = inkexWorkingDir + "/" + config.get('paths', 'imagesPath')
        #langPath = inkexWorkingDir + "/" + config.get('paths', 'langPath')
        #fontsPath = inkexWorkingDir + "/" + config.get('paths', 'fontsPath')
        #themesPath = inkexWorkingDir + "/" + config.get('paths', 'themesPath')
        #labjsLib = inkexWorkingDir + "/" + config.get('paths', 'labjsLib')
        #jqueryLib = inkexWorkingDir + "/" + config.get('paths', 'jqueryLib')
        #kineticLib = inkexWorkingDir + "/" + config.get('paths', 'kineticLib')
        #sha1Lib = inkexWorkingDir + "/" + config.get('paths', 'sha1Lib')
        #quantizeLib = inkexWorkingDir + "/" + config.get('paths', 'quantizeLib')
        #xiaEngine = inkexWorkingDir + "/" + config.get('paths', 'xiaEngine')

        try:
            filePath = f"{tempfile.mkdtemp()}/temp.svg"
            with open(filePath,"w") as file:
                self.document.write(filePath)

            console = LoggerInkscape()

            root = tkinter.Tk()
            root.title("XIA " + numVersion + releaseVersion)
            root.geometry("465x310")
            root.resizable(0,0)
            img = tkinter.PhotoImage(file= imagesPath + '/xia64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)
            maindialog = IADialog(root, console, config, "./", filePath)
            root.mainloop()

        except ValueError:
           #inkex.debug(ValueError)
           pass

ia = ImageActive()
ia.run()
