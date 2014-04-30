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
# @author : pascal.fautrero@crdp.ac-versailles.fr

import Tkinter, tkFileDialog
import os, shutil, imp, sys
import ConfigParser
from iaobject import iaObject
from pikipiki import PageFormatter
from splashscreen import Splash

class IADialog(Tkinter.Frame):

  def __init__(self, root, localdir=".", svgfile=""):

    Tkinter.Frame.__init__(self, root)

    self.filename = ""
    self.localdir = localdir
    
    self.root = root
    
    # define images

    import_img= Tkinter.PhotoImage(file=self.localdir + "/images/import.gif")
    ia_img= Tkinter.PhotoImage(file=self.localdir + "/images/ia.gif")    
    inkscape= Tkinter.PhotoImage(file=self.localdir + "/images/inkscape.gif")    
    void_img= Tkinter.PhotoImage(file=self.localdir + "/images/void.gif")  

    self.filename = svgfile

    # init Image Active Object
    
    self.imageActive = iaObject()

    # define buttons
    
    if self.filename == "":
        button1 = Tkinter.Button(self, image=import_img, relief=Tkinter.FLAT, bd=0, height=150, width=150, command=self.askopenfilename)
        button1.image = import_img
        button1.grid(row=0,column=0, columnspan=1,sticky='W')
        self.keep_alive = "yes"
    else:
        label1 = Tkinter.Label(self, image=inkscape)
        label1.photo = inkscape
        label1.grid(row=0,column=0,columnspan=1, sticky='W')
        self.keep_alive = "no"

    # Automatic import of themes
    
    tab_path = os.path.dirname(os.path.relpath(__file__)).split("/")
    tab_path.pop()
    rel_path = "."
    for folder in tab_path:
        rel_path = rel_path + "/" + folder

    self.themes = []
        
    if os.path.isdir(rel_path + "/themes"):
        theme_index = 1
        for filename in os.listdir(rel_path + "/themes"):
            theme = {}
            theme['name'] = filename
            imp.load_source(filename, rel_path + "/themes/" + filename + "/hook.py")
            imported_class = __import__(filename)
            theme['object'] = imported_class.hook(self.imageActive, PageFormatter)
            self.themes.append(theme)

            img_button = Tkinter.PhotoImage(file= rel_path + "/themes/" + filename + "/" + "icon.gif")    
            button = Tkinter.Button(self, image=img_button, relief=Tkinter.FLAT,bd=0, height=150, width=150)
            button["command"] = lambda t=theme:self.createIA(t)
            button.image = img_button
            button.grid(row=theme_index // 3,column=theme_index % 3)
            theme_index = theme_index + 1
            if theme_index == 3:
                theme_index = 5

    # padding
    
    while (theme_index % 3) != 0:
        label = Tkinter.Label(self, image=void_img)
        label.photo = void_img
        label.grid(row=theme_index // 3,column=theme_index % 3,columnspan=1, sticky='W')
        theme_index = theme_index + 1
        if theme_index == 3:
            theme_index = 5
            
    # redefine window height if necessary

    root.geometry("465x" + str((theme_index // 3) * 155))

    # title
    
    label = Tkinter.Label(self, image=ia_img)
    label.photo = ia_img
    label.grid(row=1,column=0,columnspan=2, sticky='W')


    # define options for opening or saving a file

    self.file_opt = options = {}
    options['defaultextension'] = '.svg'
    options['filetypes'] = [('svg files', '.svg')]

    options['initialdir'] = os.path.expanduser('~')
    options['initialfile'] = 'myfile.svg'
    options['parent'] = root
    options['title'] = 'Select a svg file'

    self.dir_opt = options = {}

    options['initialdir'] = os.path.expanduser('~')
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'Select target folder'

    # retrieves source and target directories from config file

    # Creation of config_dir if not exists.
    self.home_dir = os.path.expanduser('~')
    self.config_dir = os.path.join(self.home_dir, '.image-active')
    self.config_ini = os.path.join(self.config_dir, 'config_ia.ini')
    if not os.path.isdir(self.config_dir):
        try:
            os.mkdir(self.config_dir, 0755)
        except Exception as e:
            print("Sorry, impossible to create the {0} directory".format(self.config_dir))
            print("Error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)

    if os.path.isfile(self.config_ini):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_ini)
        self.file_opt['initialdir'] = self.config.get("paths", "source_dir")
        self.dir_opt['initialdir'] = self.config.get("paths", "target_dir")
    else:
        with open(self.config_ini, "w") as config_file:
            self.config = ConfigParser.ConfigParser()
            self.config.add_section('paths')
            self.config.set("paths", "source_dir", self.file_opt['initialdir'])
            self.config.set("paths", "target_dir", self.dir_opt['initialdir'])
            self.config.write(config_file)
        
  def askopenfilename(self):
    self.filename = tkFileDialog.askopenfilename(**self.file_opt)
    if self.filename:
        head, tail = os.path.split(self.filename)
        self.file_opt['initialdir'] = head
        self.config.set("paths", "source_dir", head)
        with open(self.config_ini, "w") as config_file:
            self.config.write(config_file)

  def createIA(self, theme):
      if self.filename:
          self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
          if self.dirname:
              self.config.set("paths", "target_dir", self.dirname)
              with open(self.config_ini, "w") as config_file:
                self.config.write(config_file)
                
              mysplash = Splash(self.root , self.localdir + '/images/processing.gif', 0)
              mysplash.enter()              
              
              self.dir_opt['initialdir'] = self.dirname
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
              shutil.copytree(self.localdir + '/themes/' + theme['name']+ '/font/', self.dirname + '/font/')              
              shutil.copytree(self.localdir + '/themes/' + theme['name']+ '/css/', self.dirname + '/css/')
              shutil.copytree(self.localdir + '/themes/' + theme['name']+ '/img/', self.dirname + '/img/')
              shutil.copytree(self.localdir + '/themes/' + theme['name']+ '/js/', self.dirname + '/js/')

              self.imageActive.analyzeSVG(self.filename)
              self.imageActive.generateJSON(self.dirname + '/datas/data.js')
              theme['object'].generateIndex(self.dirname + "/index.html", self.localdir + '/themes/' + theme['name']+ '/index.html')

              mysplash.exit()

              if self.keep_alive == "no":
                  self.root.destroy()
              
  def quit(self):
      self.root.destroy()
