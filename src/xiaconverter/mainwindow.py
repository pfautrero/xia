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

import re
import tkinter
import tkinter.filedialog
import os
import shutil
from importlib.machinery import SourceFileLoader
import types
import sys
import configparser
import unicodedata
import base64
from .iaobject import iaObject
from .pikipiki import PageFormatter
from .splashscreen import Splash
from .tooltip import ToolTip
from .paramswindow import IAParams

import gettext
import locale
import inkex
if sys.platform.startswith('win32'):
    import ctypes

class IADialog():

    def __init__(self, root, console, langPath, imagesPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib,
                 sha1Lib, quantizeLib, svgfile=''):

        #tkinter.Frame.__init__(self, root)

        try:
            t = gettext.translation("xia-converter", langPath, languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("xia-converter", langPath, languages=['en_US'])
        translate = t.gettext
        #inkex.utils.debug(svgfile)
        self.filename = ""
        self.imagesPath = imagesPath
        self.themesPath = themesPath
        self.fontsPath = fontsPath
        self.langPath = langPath
        self.labjsLib = labjsLib
        self.kineticLib = kineticLib
        self.sha1Lib = sha1Lib
        self.quantizeLib = quantizeLib
        self.jqueryLib = jqueryLib
        self.root = root
        self.resize = 3

        self.options = {}
        self.options['export_type'] = "singlefile"

        self.grid = {}
        self.grid["height"] = 150
        self.grid["width"] = 150

        # Don't show hidden files and directories
        # (with tkinter, by default, it's the opposite).
        root.tk.call('namespace', 'import', '::tk::dialog::file::')
        root.call('set', '::tk::dialog::file::showHiddenVar', '0')
        root.call('set', '::tk::dialog::file::showHiddenBtn', '1')


        # define images
        import_img= tkinter.PhotoImage(file=self.imagesPath + "/open2.gif")
        ia_img= tkinter.PhotoImage(file=self.imagesPath + "/xia2.gif")
        file_locked= tkinter.PhotoImage(file=self.imagesPath + "/file_locked2.gif")
        void_img= tkinter.PhotoImage(file=self.imagesPath + "/void.gif")
        params_img= tkinter.PhotoImage(file=self.imagesPath + "/params2.gif")

        self.filename = svgfile

        # init Image Active Object
        self.imageActive = iaObject(console)

        # define buttons
        if self.filename == "":
            # standalone version
            label = tkinter.Label(root, image=ia_img, highlightthickness=0,
            bg='#000000', height=self.grid["height"] - 2, width=self.grid["width"] - 2, anchor=tkinter.NW)
            label.photo = ia_img
            label.grid(row=0,column=0,columnspan=1,
                sticky='NW',
                padx=0, pady=0)

            button1 = tkinter.Button(root, image=import_img,
                                     relief=tkinter.FLAT, bd=0,
                                     command=self.askopenfilename,
                                     highlightthickness=0,
                                     padx=0, pady=0,
                                     bg='#000000',
                                     anchor=tkinter.NW,
                                     height=self.grid["height"] - 2,
                                     width=self.grid["width"] - 2)
            button1.image = import_img
            button1.grid(row=0,column=1, columnspan=1,sticky='NW', padx=0, pady=0)
            tooltip = ToolTip(button1,translate("select svg file"), None, 0.1)
            self.keep_alive = "yes"
        else:
            # inkscape version
            label1 = tkinter.Label(root, image=file_locked)
            label1.photo = file_locked
            label1.grid(row=0,column=0,columnspan=2, sticky='W', padx=0, pady=0)
            self.keep_alive = "no"

        button2 = tkinter.Button(root, image=params_img,
                                 relief=tkinter.FLAT, bd=0,
                                 command=self.openparams,
                                 highlightthickness=0,
                                 padx=0, pady=0,
                                 bg='#000000',
                                 anchor=tkinter.NW,
                                 height=self.grid["height"] - 2,
                                 width=self.grid["width"] - 2)
        button2.image = params_img
        button2.grid(row=0,column=2, columnspan=1,sticky='W', padx=0, pady=0)
        tooltip2 = ToolTip(button2,translate("ajust parameters"), None, 0.1)

        # Automatic import of themes

        self.themes = []

        if os.path.isdir(themesPath):
            theme_index = 3
            themes_folders = sorted(os.listdir(themesPath))
            for filename in themes_folders:
                theme = {}
                theme['name'] = filename
                loader = SourceFileLoader(filename, themesPath + "/" + filename + "/hook.py")
                loaded = types.ModuleType(loader.name)
                loader.exec_module(loaded)
                theme['object'] = loaded.hook(self, self.imageActive, PageFormatter, self.langPath)
                self.themes.append(theme)

                img_button = tkinter.PhotoImage(file= themesPath + "/" + filename + "/" + "icon.gif")
                button = tkinter.Button(root, image=img_button,
                    relief=tkinter.FLAT,
                    overrelief=tkinter.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    padx=0, pady=0,
                    anchor=tkinter.NW,
                    bg='#000000',
                    height=self.grid["height"] - 2,
                    width=self.grid["width"] - 2)
                button["command"] = lambda t=theme:self.createIA(t)
                button.image = img_button
                button.grid(row=theme_index // 3,
                    column=theme_index % 3,
                    padx=0, pady=0,
                    sticky='NW',
                    ipadx=0, ipady=0)
                tooltip = ToolTip(button,theme['object'].tooltip, None, 0.1)
                theme_index += 1

        # padding

        while (theme_index % 3) != 0:
            label = tkinter.Label(root, image=void_img,
                highlightthickness=0, padx=0, pady=0,
                bg='#000000',
                height=self.grid["height"] - 2,
                width=self.grid["width"] - 2)
            label.photo = void_img
            label.grid(row=theme_index // 3, column=theme_index % 3, columnspan=1, sticky='W')
            theme_index += 1

        # redefine window height if necessary
        root.geometry(str(self.grid["width"] * 3) + "x" + str((theme_index // 3) * self.grid["height"]))

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.svg'
        options['filetypes'] = [('svg files', '.svg')]

        if sys.platform.startswith('win32'):
            options['initialdir'] = self.getwinuser()
        else:
            options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = translate('myfile.svg')
        options['parent'] = root
        options['title'] = translate('Select a svg file')

        self.dir_opt = options = {}

        if sys.platform.startswith('win32'):
            options['initialdir'] = self.getwinuser()
        else:
            options['initialdir'] = os.path.expanduser('~')
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = translate('Select target folder')

        # retrieves source and target directories from config file

        # Creation of config_dir if not exists.
        if sys.platform.startswith('win32'):
            self.home_dir = self.getwinuser()
        else:
            self.home_dir = os.path.expanduser('~')
        self.config_dir = os.path.join(self.home_dir, '.xia')
        self.config_ini = os.path.join(self.config_dir, 'config.ini')
        if not os.path.isdir(self.config_dir):
            try:
                os.mkdir(self.config_dir, 0o755)
            except Exception as e:
                console.display(translate("Sorry, impossible to create the {0} directory") . format(self.config_dir))
                console.display("Error({0}): {1}".format(e.errno, e.strerror))
                sys.exit(1)

        if os.path.isfile(self.config_ini):
            self.config = configparser.ConfigParser()
            self.config.read(self.config_ini)
            try:
                self.file_opt['initialdir'] = base64.b64decode(self.config.get("paths", "source_dir")).decode()
            except:
                self.config.set("paths", "source_dir", base64.b64encode(self.file_opt['initialdir'].encode("utf8")).decode("ascii"))
                self.config.write(self.config_ini)
            try:
                self.dir_opt['initialdir'] = base64.b64decode(self.config.get("paths", "target_dir")).decode()
            except:
                self.config.set("paths", "target_dir",base64.b64encode(self.dir_opt['initialdir'].encode("utf8")).decode("ascii"))
                self.config.write(self.config_ini)
        else:
            with open(self.config_ini, "w") as config_file:
                self.config = configparser.ConfigParser()
                self.config.add_section('paths')
                self.config.set("paths", "source_dir", base64.b64encode(self.file_opt['initialdir'].encode("utf8")).decode("ascii"))
                self.config.set("paths", "target_dir", base64.b64encode(self.dir_opt['initialdir'].encode("utf8")).decode("ascii"))
                self.config.write(config_file)

        self.paramsTitle = translate("Parameters")

    def getwinuser(self):
        """ fix python2 bug on os.path.expanduser
        http://bugs.python.org/issue13207
        """
        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetEnvironmentVariableW(u"USERPROFILE", buf, 1024)
        return buf.value


    def openparams(self):
        try:
            self.params.focus()
            self.params.lift()
        except:
            self.params = tkinter.Toplevel()
            self.params.title(self.paramsTitle)
            self.params.geometry("310x155")
            self.params.resizable(0,0)
            img = tkinter.PhotoImage(file=self.imagesPath + '/xia64.gif')
            self.params.tk.call('wm', 'iconphoto', self.params._w, img)
            IAParams(self.params, self, self.langPath, self.imagesPath).pack(side="left")

    def askopenfilename(self):
        self.filename = tkinter.filedialog.askopenfilename(**self.file_opt)
        if self.filename:
            head, tail = os.path.split(self.filename)
            self.file_opt['initialdir'] = head
            self.config.set("paths", "source_dir", base64.b64encode(head.encode("utf8")).decode("ascii"))
            with open(self.config_ini, "w") as config_file:
                self.config.write(config_file)

    def createIA(self, theme):
        if self.filename:
            self.dirname = tkinter.filedialog.askdirectory(**self.dir_opt)
            if self.dirname:
                self.config.set("paths", "target_dir", base64.b64encode(self.dirname.encode("utf8")).decode("ascii"))
                with open(self.config_ini, "w") as config_file:
                  self.config.write(config_file)

                mysplash = Splash(self.root, self.imagesPath + '/processing.gif', 0)
                mysplash.enter()

                self.dir_opt['initialdir'] = self.dirname

                maxNumPixels = self.defineMaxPixels(self.resize)
                self.imageActive.analyzeSVG(self.filename, maxNumPixels)

                head, tail = os.path.split(self.filename)
                filenamewithoutext = os.path.splitext(tail)[0]
                filenamewithoutext = re.sub(r"\s+", "", filenamewithoutext, flags=re.UNICODE)
                if filenamewithoutext == 'temp':
                    if self.imageActive.scene['title'] != "":
                        filenamewithoutext = re.sub(r"\s+", "_", self.clean_unicode(self.imageActive.scene['title']), flags=re.UNICODE)
                        filenamewithoutext = re.sub(r"[^-a-z0-9A-Z_]", "", filenamewithoutext, flags=re.UNICODE)
                        filenamewithoutext = filenamewithoutext[0:min(len(filenamewithoutext), 15)]

                theme['object'].generateIndex("{}/{}.html".format(self.dirname, filenamewithoutext),
                                              "{}/{}/index.html".format(self.themesPath,theme['name']),
                                              filenamewithoutext)

                if self.options['export_type'] == "local":
                    if os.path.isdir("{}/{}".format(self.dirname, filenamewithoutext)):
                        shutil.rmtree("{}/{}".format(self.dirname, filenamewithoutext))
                    os.mkdir("{}/{}".format(self.dirname, filenamewithoutext))
                    os.mkdir("{}/{}/datas".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.fontsPath , "{}/{}/font".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.themesPath + '/' + theme['name'] + '/css/', "{}/{}/css".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.themesPath + '/' + theme['name'] + '/img/', "{}/{}/img".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.themesPath + '/' + theme['name'] + '/js/', "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.labjsLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.jqueryLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.kineticLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.sha1Lib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.quantizeLib, "{}/{}/js".format(self.dirname, filenamewithoutext))

                self.imageActive.generateJSON()
                if self.options['export_type'] == "local":
                    with open("{}/{}/datas/data.js".format(self.dirname, filenamewithoutext),"wb") as jsonfile:
                        jsonfile.write(self.imageActive.jsonContent.encode('utf8'))

                mysplash.exit()

                if self.keep_alive == "no":
                    # destroy method generates error in inkscape
                    sys.exit()

    def clean_unicode(self,u):
        #assert isinstance(u, unicode)
        result = u''
        for c in u:
            result = result + unicodedata.normalize('NFD', c)[0]
        return result

    def defineMaxPixels(self, resizeCoeff):
        if resizeCoeff == 0:
            return float(1024 * 1024)
        elif resizeCoeff == 1:
            return float(2 * 1024 * 1024)
        elif resizeCoeff == 2:
            return float(3 * 1024 * 1024)
        elif resizeCoeff == 3:
            return float(5 * 1024 * 1024)
        else:
            return float(512 * 1024)

    def quit(self):
        self.root.destroy()
