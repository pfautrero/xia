#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, shutil
import inkex
import tempfile
import Tkinter, Tkconstants, tkFileDialog
from iaConvert.ia2.iaobject import iaObject
from iaConvert.ia2.mainwindow import IADialog

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):

        # fix inkscape bug https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/944077/comments/11
        pathNodes = self.document.xpath('//sodipodi:namedview',namespaces=inkex.NSS)
        pathNodes[0].set('id','base')        
       
        try:
            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            with open(filePath,"w") as file:
                self.document.write(filePath)

            root = Tkinter.Tk()
            root.title("Image Active 2")
            root.geometry("465x310")
            root.attributes('-topmost', 1)
            img = Tkinter.PhotoImage(file='iaConvert/images/image-active64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)  
            maindialog = IADialog(root, "iaConvert", filePath)
            maindialog.pack(side="left")
            root.mainloop()

        except ValueError:
           #print(ValueError)
           pass
                              
ia = ImageActive()
ia.affect()
          			
