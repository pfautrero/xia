#!/usr/bin/env python3

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
from importlib.machinery import SourceFileLoader
import types
import sys
import re
import unicodedata
from .iaobject import iaObject
from .pikipiki import PageFormatter

class XIAConsole():

    def __init__(self, config, options, console):

        self.langPath = config.get('paths', 'langPath')
        self.fontsPath = config.get('paths', 'fontsPath')
        self.themesPath = config.get('paths', 'themesPath')
        self.labjsLib = config.get('paths', 'labjsLib')
        self.kineticLib = config.get('paths', 'kineticLib')
        self.jqueryLib = config.get('paths', 'jqueryLib')
        self.sha1Lib = config.get('paths', 'sha1Lib')
        self.quantizeLib = config.get('paths', 'quantizeLib')
        self.xiaEngine = config.get('paths', 'xiaEngine')

        self.resize = 3
        self.filename = options['input_file']
        if options['output_dir'].endswith('/'):
            self.dirname = options['output_dir'][:-1]
        else:
            self.dirname = options['output_dir']
        self.export_type = options['export_type']
        self.options = options
        self.theme = {}
        self.theme['name'] = "sidebar"

        if os.path.isdir(self.themesPath + "/" + options['selected_theme']):
            self.theme['name'] = options['selected_theme']

        self.imageActive = iaObject(console)

        loader = SourceFileLoader(self.theme['name'], f"{self.themesPath}/{self.theme['name']}/hook.py")
        loaded = types.ModuleType(loader.name)
        loader.exec_module(loaded)
        self.theme['object'] = loaded.hook(self, self.imageActive, PageFormatter, self.langPath)

    def createIA(self):

        if self.export_type == 'local':
            head, tail = os.path.split(self.filename)
            filenamewithoutext = os.path.splitext(tail)[0]
            filenamewithoutext = re.sub(r"\s+", "", filenamewithoutext, flags=re.UNICODE)
            if filenamewithoutext == 'temp':
                if self.imageActive.scene['title'] != "":
                    filenamewithoutext = re.sub(r"\s+", "_", self.clean_unicode(self.imageActive.scene['title']), flags=re.UNICODE)
                    filenamewithoutext = re.sub(r"[^-a-z0-9A-Z_]", "", filenamewithoutext, flags=re.UNICODE)
                    filenamewithoutext = filenamewithoutext[0:min(len(filenamewithoutext), 15)]

            if os.path.isdir("{}/{}".format(self.dirname, filenamewithoutext)):
                shutil.rmtree("{}/{}".format(self.dirname, filenamewithoutext))
            os.mkdir("{}/{}".format(self.dirname, filenamewithoutext))
            os.mkdir("{}/{}/datas".format(self.dirname, filenamewithoutext))
            os.makedirs("{}/{}/js".format(self.dirname, filenamewithoutext), exist_ok=True)
            shutil.copy(self.xiaEngine, "{}/{}/js".format(self.dirname, filenamewithoutext))
            shutil.copytree(self.fontsPath , f"{self.dirname}/{filenamewithoutext}/font/")
            shutil.copytree(self.themesPath + '/' + self.theme['name'] + \
                '/css/', f"{self.dirname}/{filenamewithoutext}/css/")
            shutil.copytree(self.themesPath + '/' + self.theme['name'] + \
                '/img/', f"{self.dirname}/{filenamewithoutext}/img/")
            src = f"{self.themesPath}/{self.theme['name']}/js/"
            dst = f"{self.dirname}/{filenamewithoutext}/js"
            names = os.listdir(src)
            for name in names:
                srcname = os.path.join(src, name)
                dstname = os.path.join(dst, name)
                shutil.copyfile(srcname, dstname)

            shutil.copy(self.labjsLib , f"{self.dirname}/{filenamewithoutext}/js")
            shutil.copy(self.jqueryLib , f"{self.dirname}/{filenamewithoutext}/js")
            shutil.copy(self.kineticLib , f"{self.dirname}/{filenamewithoutext}/js")
            shutil.copy(self.sha1Lib , f"{self.dirname}/{filenamewithoutext}/js")
            shutil.copy(self.quantizeLib , f"{self.dirname}/{filenamewithoutext}/js")

        maxNumPixels = self.defineMaxPixels(self.resize)
        self.imageActive.analyzeSVG(self.filename, maxNumPixels)

        self.imageActive.generateJSON()

        head, tail = os.path.split(self.filename)
        filenamewithoutext = os.path.splitext(tail)[0]
        filenamewithoutext = re.sub(r"\s+", "", filenamewithoutext, flags=re.UNICODE)
        if filenamewithoutext == 'temp':
            if self.imageActive.scene['title'] != "":
                filenamewithoutext = re.sub(r"\s+", "_", self.clean_unicode(self.imageActive.scene['title']), flags=re.UNICODE)
                filenamewithoutext = re.sub(r"[^-a-z0-9A-Z_]", "", filenamewithoutext, flags=re.UNICODE)
                filenamewithoutext = filenamewithoutext[0:min(len(filenamewithoutext), 15)]
                
        if self.export_type == 'local':
            with open(f"{self.dirname}/{filenamewithoutext}/datas/data.js","wb") as jsonfile:
                jsonfile.write(self.imageActive.jsonContent.encode('utf8'))
            self.theme['object'].generateIndex(self.dirname + "/" + filenamewithoutext + ".html", \
                self.themesPath + '/' + self.theme['name'] + '/index.html', filenamewithoutext)
        else:
            self.theme['object'].generateIndex(self.dirname + "/" + filenamewithoutext + ".html", \
                self.themesPath + '/' + self.theme['name'] + '/index.html', filenamewithoutext)

    def clean_unicode(self,u):
        #assert isinstance(u, unicode)
        result = ""
        for c in u:
            result = result + unicodedata.normalize('NFD', c)[0]
        return result

    def defineMaxPixels(self, resizeCoeff):
        if resizeCoeff == 3:
            return float(5 * 1024 * 1024)
        else:
            return float(100 * 1024 * 1024)
