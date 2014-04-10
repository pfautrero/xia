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

import Tkinter, Tkconstants, tkFileDialog
import os, shutil, sys
from iaobject import iaObject

class IADialog(Tkinter.Frame):

  def __init__(self, root, localdir=".", svgfile=""):

    #Tkinter.Frame.__init__(self, root)
    Tkinter.Frame.__init__(self, root)

    self.filename = ""
    self.localdir = localdir
    #self.localdir = os.environ['HOME']
    import_img= Tkinter.PhotoImage(file=self.localdir + "/images/import.gif")
    accordion_img= Tkinter.PhotoImage(file=self.localdir + "/images/accordion.gif")    
    bubbles_img= Tkinter.PhotoImage(file=self.localdir + "/images/bubbles.gif")    
    ia_img= Tkinter.PhotoImage(file=self.localdir + "/images/ia.gif")    
    inkscape= Tkinter.PhotoImage(file=self.localdir + "/images/inkscape.gif")    
    buttons_img= Tkinter.PhotoImage(file=self.localdir + "/images/buttons.gif")    
    void_img= Tkinter.PhotoImage(file=self.localdir + "/images/void.gif")  

    self.filename = svgfile

    # define buttons
    if self.filename == "":
        button1 = Tkinter.Button(self, image=import_img, relief=Tkinter.FLAT, bd=0, height=150, width=150, command=self.askopenfilename)
        button1.image = import_img
        button1.grid(row=0,column=0, columnspan=1,sticky='W')
    else:
        label1 = Tkinter.Label(self, image=inkscape)
        label1.photo = inkscape
        label1.grid(row=0,column=0,columnspan=1, sticky='W')
    
    # TODO : Automatic import of themes
    
    #tab_path = os.path.dirname(os.path.relpath(__file__)).split("/")
    #tab_path.pop()
    #rel_path = "."
    #import_path = ""
    #for folder in tab_path:
    #    rel_path = rel_path + "/" + folder
        
    #self.themes_list = []

    #if os.path.isdir(rel_path + "/themes"):
    #    for filename in os.listdir(rel_path + "/themes"):
    #        sys.path.append(rel_path + "/themes/" + filename)
    #        __import__(filename)
    #        self.themes_list.append(filename)

        
    button2 = Tkinter.Button(self, image=accordion_img, relief=Tkinter.FLAT,bd=0, height=150, width=150,  command=self.createAccordion)
    button2.image = accordion_img
    button2.grid(row=0,column=1)

    label3 = Tkinter.Label(self, image=void_img)
    label3.photo = void_img
    label3.grid(row=0,column=2,columnspan=1, sticky='W')


    #button3 = Tkinter.Button(self, image=bubbles_img, relief=Tkinter.FLAT,bd=0, height=150, width=150,  command=self.createAccordion)
    #button3.image = bubbles_img
    #button3.grid(row=0,column=2)

    label = Tkinter.Label(self, image=ia_img)
    label.photo = ia_img
    label.grid(row=1,column=0,columnspan=2, sticky='W')


    label4 = Tkinter.Label(self, image=void_img)
    label4.photo = void_img
    label4.grid(row=1,column=2,columnspan=1, sticky='W')


    #button4 = Tkinter.Button(self, image=buttons_img, relief=Tkinter.FLAT,  padx=0, pady=0,  command=self.createAccordion)
    #button4.image = buttons_img
    #button4.grid(row=1,column=2)


    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.svg'
    options['filetypes'] = [('svg files', '.svg')]

    if os.environ.has_key('HOME'):
        options['initialdir'] = os.environ['HOME']
    options['initialfile'] = 'myfile.svg'
    options['parent'] = root
    options['title'] = 'Select a svg file'

    self.dir_opt = options = {}

    if os.environ.has_key('HOME'):
        options['initialdir'] = os.environ['HOME']
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'Select target folder'
    
  def askopenfilename(self):
    self.filename = tkFileDialog.askopenfilename(**self.file_opt)
    if self.filename:
        head, tail = os.path.split(self.filename)
        self.file_opt['initialdir'] = head

  def createAccordion(self):
      if self.filename:
          self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
          if self.dirname:
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
              shutil.copytree(self.localdir + '/themes/accordion/font/', self.dirname + '/font/')              
              shutil.copytree(self.localdir + '/themes/accordion/css/', self.dirname + '/css/')
              shutil.copytree(self.localdir + '/themes/accordion/img/', self.dirname + '/img/')
              shutil.copytree(self.localdir + '/themes/accordion/js/', self.dirname + '/js/')
              imageActive = iaObject()
              imageActive.analyzeSVG(self.filename)
              imageActive.generateJSON(self.dirname + '/datas/data.js')

              imageActive.generateAccordion(self.dirname + "/index.html")
  def quit(self):
      self.root.destroy()
