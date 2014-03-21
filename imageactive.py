#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, shutil
import inkex
import tempfile
from iaConvert.lib.iaobject import iaObject
import Tkinter, Tkconstants, tkFileDialog
from iaConvert.ia3.mainwindow import IADialog

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        
        try:
            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            with open(filePath,"w") as file:
                self.document.write(filePath)

            root = Tkinter.Tk()
            root.title("Image Active 3")
            root.geometry("465x310")
            root.attributes('-topmost', 1)
            img = Tkinter.PhotoImage(file='iaConvert/images/image-active64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)  
            maindialog = IADialog(root, "iaConvert", filePath)
            maindialog.pack(side="left")
            root.mainloop()

        except ValueError:
           print(ValueError)
                              
ia = ImageActive()
ia.affect()
          			
