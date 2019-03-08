#! /usr/bin/python

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

import os
import shutil
import imp
import sys
import re
from iaobject import iaObject
from pikipiki import PageFormatter

class XIAConsole():

    def __init__(self, langPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, options, console):

        self.themesPath = themesPath
        self.langPath = langPath
        self.fontsPath = fontsPath
        self.labjsLib = labjsLib
        self.kineticLib = kineticLib
        self.sha1Lib = sha1Lib
        self.jqueryLib = jqueryLib
        self.resize = options['quality']
        self.filename = options['input_file']
        self.dirname = options['output_dir']
        self.export_type = options['export_type']
        self.options = options
        self.theme = {}
        self.theme['name'] = "accordionBlack"

        if os.path.isdir(self.themesPath + "/" + options['selected_theme']):
            self.theme['name'] = options['selected_theme']

        self.imageActive = iaObject(console)

        imp.load_source(self.theme['name'], themesPath + "/" + self.theme['name'] + \
            "/hook.py")
        imported_class = __import__(self.theme['name'])
        self.theme['object'] = imported_class.hook(self, self.imageActive, \
            PageFormatter, self.langPath)


    def createIA(self):

        if self.export_type == 'local':
            if os.path.isdir(self.dirname + '/font'):
                shutil.rmtree(self.dirname + '/font')
            if os.path.isdir(self.dirname + '/img'):
                shutil.rmtree(self.dirname + '/img')
            if os.path.isdir(self.dirname + '/css'):
                shutil.rmtree(self.dirname + '/css')
            if os.path.isdir(self.dirname + '/js'):
                shutil.rmtree(self.dirname + '/js')
            if os.path.isdir(self.dirname + '/datas'):
                shutil.rmtree(self.dirname + '/datas')
            os.mkdir(self.dirname + '/datas')
            shutil.copytree(self.fontsPath , self.dirname + '/font/')
            shutil.copytree(self.themesPath + '/' + self.theme['name'] + \
                '/css/', self.dirname + '/css/')
            shutil.copytree(self.themesPath + '/' + self.theme['name'] + \
                '/img/', self.dirname + '/img/')
            shutil.copytree(self.themesPath + '/' + self.theme['name'] + \
                '/js/', self.dirname + '/js/')
            shutil.copy(self.labjsLib , self.dirname + '/js')
            shutil.copy(self.jqueryLib , self.dirname + '/js')
            shutil.copy(self.kineticLib , self.dirname + '/js')
            shutil.copy(self.sha1Lib , self.dirname + '/js')

        maxNumPixels = self.defineMaxPixels(self.resize)
        self.imageActive.analyzeSVG(self.filename, maxNumPixels)

        self.imageActive.generateJSON()

        head, tail = os.path.split(self.filename)
        filenamewithoutext = os.path.splitext(tail)[0]
        filenamewithoutext = re.sub(r"\s+", "", filenamewithoutext, flags=re.UNICODE)

        if self.export_type == 'local':
            with open(self.dirname + '/datas/data.js',"w") as jsonfile:
                jsonfile.write(self.imageActive.jsonContent.encode('utf8'))
            self.theme['object'].generateIndex(self.dirname + "/" + filenamewithoutext + "_" + self.theme['name'] + ".html", \
                self.themesPath + '/' + self.theme['name'] + '/index.html')
        else:
            self.theme['object'].generateIndex(self.dirname + "/" + filenamewithoutext + "_" + self.theme['name'] + ".html", \
                self.themesPath + '/' + self.theme['name'] + '/index.html')


    def defineMaxPixels(self, resizeCoeff):
        if resizeCoeff == 0:
            return float(512 * 512)
        elif resizeCoeff == 1:
            return float(1024 * 1024)
        elif resizeCoeff == 2:
            return float(3 * 1024 * 1024)
        elif resizeCoeff == 3:
            return float(5 * 1024 * 1024)
        else:
            return float(512 * 1024)
