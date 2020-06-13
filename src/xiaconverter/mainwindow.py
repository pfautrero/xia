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
if sys.platform.startswith('win32'):
    import ctypes

class IADialog():


    def indexStandalone(self):
        self.indexStandalone_param = (self.indexStandalone_param + 1) % 2
        self.options['export_type'] = "singlefile" if self.indexStandalone_param == 0 else "local"
        self.button_indexStandalone.configure(image=self.indexStandalone_img[self.indexStandalone_param])

    def createLabel(self, root, imagePath, posx, posy, span):
        """ Create Tkinter Label"""
        import_img= tkinter.PhotoImage(file=imagePath)
        label = tkinter.Label(root,
            image=import_img,
            borderwidth=0,
            relief=tkinter.FLAT,
            highlightthickness=0,
            bg='#000000',
            height=self.grid["height"],
            width=self.grid["width"] * span,
            anchor=tkinter.NW)
        label.photo = import_img
        label.grid(row=posx,column=posy,columnspan=span,
            sticky='NW',
            padx=0, pady=0)
        return label

    def createButton(self, root, translate, imagePath, tooltipTitle, posx, posy, span):
        """ Create Tkinter Button"""
        import_img= tkinter.PhotoImage(file=imagePath)
        button = tkinter.Button(root,
                    image=import_img,
                    relief=tkinter.FLAT,
                    overrelief=tkinter.FLAT,
                    borderwidth=0,
                    highlightthickness=0,
                    padx=0, pady=0,
                    anchor=tkinter.NW,
                    bg='#000000',
                    height=self.grid["height"],
                    width=self.grid["width"])
        button.image = import_img
        button.grid(row=posx,column=posy, columnspan=span,sticky='NW', padx=0, pady=0, ipadx=0, ipady=0)
        tooltip = ToolTip(button,translate(tooltipTitle), None, 0.1)
        return button

    def __init__(self, root, console, config, workingDir, svgfile=''):

        self.filename = ""

        self.imagesPath = workingDir + config.get('paths', 'imagesPath')
        self.langPath = workingDir + config.get('paths', 'langPath')
        self.fontsPath = workingDir + config.get('paths', 'fontsPath')
        self.themesPath = workingDir + config.get('paths', 'themesPath')
        self.labjsLib = workingDir + config.get('paths', 'labjsLib')
        self.kineticLib = workingDir + config.get('paths', 'kineticLib')
        self.jqueryLib = workingDir + config.get('paths', 'jqueryLib')
        self.sha1Lib = workingDir + config.get('paths', 'sha1Lib')
        self.quantizeLib = workingDir + config.get('paths', 'quantizeLib')
        self.xiaEngine = workingDir + config.get('paths', 'xiaEngine')

        try:
            t = gettext.translation("xia-converter", self.langPath, languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("xia-converter", self.langPath, languages=['en_US'])
        translate = t.gettext

        self.root = root
        self.resize = 3

        self.options = {
            'export_type': "singlefile"
        }

        self.grid = {
            "height": 150,
            "width": 150
        }

        # Don't show hidden files and directories
        # (with tkinter, by default, it's the opposite).
        root.tk.call('namespace', 'import', '::tk::dialog::file::')
        root.call('set', '::tk::dialog::file::showHiddenVar', '0')
        root.call('set', '::tk::dialog::file::showHiddenBtn', '1')

        self.filename = svgfile
        self.imageActive = iaObject(console)

        # define buttons
        if self.filename == "":
            # standalone
            label = self.createLabel(root, f"{self.imagesPath}/xialarge.gif",0,0,2)
            button1 = self.createButton(root, translate,
                f"{self.imagesPath}/folder.gif",
                "select svg file",
                1, 0, 1)
            button1["command"] = self.askopenfilename
            self.keep_alive = "yes"
            theme_index = 4
            row_params = 1
        else:
            # inkscape
            label1 = self.createLabel(root,f"{self.imagesPath}/xia2.gif",0,0,1)
            self.keep_alive = "no"
            theme_index = 2
            row_params = 0

        self.indexStandalone_img = {}
        self.indexStandalone_img[0] = tkinter.PhotoImage(file=f"{self.imagesPath}/unique.gif")
        self.indexStandalone_img[1] = tkinter.PhotoImage(file=f"{self.imagesPath}/unique-no.gif")
        self.indexStandalone_param = 0 if self.options['export_type'] == "singlefile" else 1

        self.button_indexStandalone = self.createButton(root, translate,
            f"{self.imagesPath}/unique.gif" if self.options['export_type'] == "singlefile" else f"{self.imagesPath}/unique-no.gif",
            "index standalone",
            row_params, 1, 1)
        self.button_indexStandalone["command"] = self.indexStandalone

        # Automatic import of themes

        self.themes = []

        if os.path.isdir(self.themesPath):
            themes_folders = sorted(os.listdir(self.themesPath))
            for filename in themes_folders:
                theme = {}
                theme['name'] = filename
                loader = SourceFileLoader(filename, f"{self.themesPath}/{filename}/hook.py")
                loaded = types.ModuleType(loader.name)
                loader.exec_module(loaded)
                theme['object'] = loaded.hook(self, self.imageActive, PageFormatter, self.langPath)
                self.themes.append(theme)

                button = self.createButton(root, translate,
                    f"{self.themesPath}/{filename}/icon.gif",
                    theme['object'].tooltip,
                    theme_index // 2,
                    theme_index % 2,
                    1)
                button["command"] = lambda t=theme:self.createIA(t)
                theme_index += 1

        # padding

        while (theme_index % 2) != 0:
            label = self.createLabel(root,
                f"{self.imagesPath}/void.gif",
                theme_index // 2,
                theme_index % 2,
                1)
            theme_index += 1

        # redefine window height if necessary
        root.geometry(str(self.grid["width"] * 2) + "x" + str((theme_index // 2) * self.grid["height"]))

        # define options for opening or saving a file
        self.file_opt = options = {
            'defaultextension': '.svg',
            'filetypes': [('svg files', '.svg')]
        }
        
        if sys.platform.startswith('win32'):
            options['initialdir'] = self.getwinuser()
        else:
            options['initialdir'] = os.path.expanduser('~')
        options['initialfile'] = translate('myfile.svg')
        # Remove this option the avoid warning on MAC OS X
        if not sys.platform.startswith('darwin'):
            options['parent'] = root
        options['title'] = translate('Select a svg file')

        self.dir_opt = options = {}

        if sys.platform.startswith('win32'):
            options['initialdir'] = self.getwinuser()
        else:
            options['initialdir'] = os.path.expanduser('~')
        options['mustexist'] = False
        #options['parent'] = root
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
                self.imageActive.generateJSON()
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
                    os.mkdir("{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.xiaEngine, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.fontsPath , "{}/{}/font".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.themesPath + '/' + theme['name'] + '/css/', "{}/{}/css".format(self.dirname, filenamewithoutext))
                    shutil.copytree(self.themesPath + '/' + theme['name'] + '/img/', "{}/{}/img".format(self.dirname, filenamewithoutext))
                    src = f"{self.themesPath}/{theme['name']}/js/"
                    dst = f"{self.dirname}/{filenamewithoutext}/js"
                    names = os.listdir(src)
                    for name in names:
                        srcname = os.path.join(src, name)
                        dstname = os.path.join(dst, name)
                        shutil.copyfile(srcname, dstname)
                    #shutil.copytree(self.themesPath + '/' + theme['name'] + '/js/', "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.labjsLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.jqueryLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.kineticLib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.sha1Lib, "{}/{}/js".format(self.dirname, filenamewithoutext))
                    shutil.copy(self.quantizeLib, "{}/{}/js".format(self.dirname, filenamewithoutext))

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

        if resizeCoeff == 3:
            # This resolution keeps image under iOS resource limit
            return float(5 * 1024 * 1024)
        else:
            # arbitrary huge size
            return float(100 * 512 * 1024)

    def quit(self):
        self.root.destroy()
