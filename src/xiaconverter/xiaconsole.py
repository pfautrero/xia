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
# @author : pascal.fautrero@ac-versailles.fr

import os
import shutil
import imp
import sys
from iaobject import iaObject
from pikipiki import PageFormatter

class XIAConsole():

    def __init__(self, langPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, svgfile, output_dir,
                 selected_theme, console):

        self.themesPath = themesPath
        self.langPath = langPath
        self.fontsPath = fontsPath
        self.labjsLib = labjsLib
        self.kineticLib = kineticLib
        self.sha1Lib = sha1Lib
        self.jqueryLib = jqueryLib
        self.resize = 3
        self.filename = svgfile
        self.dirname = output_dir
        self.theme = {}
        self.index_standalone = 0
        self.firefoxos = 0 
        
        if not os.path.isdir(self.themesPath + "/" + selected_theme):
            selected_theme = "accordionBlack"
        self.theme['name'] = selected_theme

        self.imageActive = iaObject(console)

        imp.load_source(selected_theme, themesPath + "/" + selected_theme + \
            "/hook.py")
        imported_class = __import__(selected_theme)
        self.theme['object'] = imported_class.hook(self, self.imageActive, \
            PageFormatter, self.langPath)


    def createIA(self):

        if not self.index_standalone:
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
        if self.firefoxos:
            shutil.copyfile(self.themesPath + '/' + self.theme['name'] + \
                '/manifest.webapp', self.dirname + '/manifest.webapp')

            shutil.copyfile(self.themesPath + '/' + self.theme['name'] + \
                '/deploy.html', self.dirname + '/deploy.html')

        maxNumPixels = self.defineMaxPixels(self.resize)
        self.imageActive.analyzeSVG(self.filename, maxNumPixels)

        self.imageActive.generateJSON()

        if not self.index_standalone:
            with open(self.dirname + '/datas/data.js',"w") as jsonfile:
                jsonfile.write(self.imageActive.jsonContent.encode('utf8'))
            self.theme['object'].generateIndex(self.dirname + "/index.html", \
                self.themesPath + '/' + self.theme['name'] + '/index.html')
        else:
            self.theme['object'].generateIndex(self.dirname + "/index.html", \
                self.themesPath + '/' + self.theme['name'] + '/index_standalone.html')


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