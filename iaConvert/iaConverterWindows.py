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
import os
from lib.iaobject import iaObject

class IADialog(Tkinter.Frame):

  def __init__(self, root):

    #Tkinter.Frame.__init__(self, root)
    Tkinter.Frame.__init__(self, root)

    self.filename = ""

    dessin= Tkinter.PhotoImage(file="img/image-active.gif")
    label = Tkinter.Label(self, image=dessin)
    label.photo = dessin
    label.pack(side=Tkinter.LEFT)

    # options for buttons
    button_opt = {'fill': Tkinter.BOTH,'padx': 5, 'pady': 5}

    # define buttons
    Tkinter.Button(self, text='Importer un fichier SVG', command=self.askopenfilename).pack(**button_opt)
    Tkinter.Button(self, text='Créer l\'Image Active (mode Accordéon)', command=self.createAccordion).pack(**button_opt)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.svg'
    options['filetypes'] = [('svg files', '.svg')]
    options['initialdir'] = ''
    options['initialfile'] = 'myfile.svg'
    options['parent'] = root
    options['title'] = 'Select a svg file'

  def askopenfilename(self):

    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """

    self.filename = tkFileDialog.askopenfilename(**self.file_opt)

  def createAccordion(self):
        if self.filename:
            imageActive = iaObject()
            imageActive.analyzeSVG(self.filename)
            imageActive.generateJSON("images_actives/datas/data.js")
            imageActive.generateAccordion("images_actives/index.html")
            #imageActive.createBackground("images_actives/datas")            

if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("IA2 Converter")
    root.geometry("550x200")
    root.attributes('-topmost', 1)
    img = Tkinter.PhotoImage(file='img/image-active64.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    IADialog(root).pack()
    root.mainloop()
