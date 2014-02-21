#!/usr/bin/python
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
import os, shutil
from lib.iaobject import iaObject

class IADialog(Tkinter.Frame):

  def __init__(self, root):

    #Tkinter.Frame.__init__(self, root)
    Tkinter.Frame.__init__(self, root)

    self.filename = ""

    import_img= Tkinter.PhotoImage(file="img/import.gif")
    accordion_img= Tkinter.PhotoImage(file="img/accordion.gif")    
    bubbles_img= Tkinter.PhotoImage(file="img/bubbles.gif")    
    ia_img= Tkinter.PhotoImage(file="img/ia.gif")    
    buttons_img= Tkinter.PhotoImage(file="img/buttons.gif")    

    # define buttons
    button1 = Tkinter.Button(self, image=import_img, relief=Tkinter.FLAT, bd=0, height=150, width=150, command=self.askopenfilename)
    button1.image = import_img
    button1.grid(row=0,column=0, columnspan=1,sticky='W')

    button2 = Tkinter.Button(self, image=accordion_img, relief=Tkinter.FLAT,bd=0, height=150, width=150,  command=self.createAccordion)
    button2.image = accordion_img
    button2.grid(row=0,column=1)

    button3 = Tkinter.Button(self, image=bubbles_img, relief=Tkinter.FLAT,bd=0, height=150, width=150,  command=self.createAccordion)
    button3.image = bubbles_img
    button3.grid(row=0,column=2)

    label = Tkinter.Label(self, image=ia_img)
    label.photo = ia_img
    label.grid(row=1,column=0,columnspan=2, sticky='W')

    button4 = Tkinter.Button(self, image=buttons_img, relief=Tkinter.FLAT,  padx=0, pady=0,  command=self.createAccordion)
    button4.image = buttons_img
    button4.grid(row=1,column=2)


    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.svg'
    options['filetypes'] = [('svg files', '.svg')]
    options['initialdir'] = ''
    options['initialfile'] = 'myfile.svg'
    options['parent'] = root
    options['title'] = 'Select a svg file'

    self.dir_opt = options = {}
    options['initialdir'] = ''
    options['mustexist'] = False
    options['parent'] = root
    options['title'] = 'Select target folder'
    
  def askopenfilename(self):
    self.filename = tkFileDialog.askopenfilename(**self.file_opt)

  def createAccordion(self):
        if self.filename:
            self.dirname = tkFileDialog.askdirectory(**self.dir_opt)
            if self.dirname:
                if os.path.isdir(self.dirname + '/img'):
                    shutil.rmtree(self.dirname + '/img')
                if os.path.isdir(self.dirname + '/css'):
                    shutil.rmtree(self.dirname + '/css')
                if os.path.isdir(self.dirname + '/js'):
                    shutil.rmtree(self.dirname + '/js')
                if os.path.isdir(self.dirname + '/datas'):
                    shutil.rmtree(self.dirname + '/datas')
                os.mkdir(self.dirname + '/datas')
                shutil.copytree('images_actives/css/', self.dirname + '/css/')
                shutil.copytree('images_actives/img/', self.dirname + '/img/')
                shutil.copytree('images_actives/js/', self.dirname + '/js/')
                imageActive = iaObject()
                imageActive.analyzeSVG(self.filename)
                imageActive.generateJSON(self.dirname + '/datas/data.js')
                imageActive.generateAccordion(self.dirname + "/index.html")
                #imageActive.createBackground("images_actives/datas")            

if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("IA2 Converter")
    root.geometry("465x310")
    root.attributes('-topmost', 1)
    img = Tkinter.PhotoImage(file='img/image-active64.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    IADialog(root).pack(side="left")
    root.mainloop()
