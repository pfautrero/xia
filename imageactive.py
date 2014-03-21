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
        #self.OptionParser.add_option('-e', '--export_path', action = 'store', type = 'string', dest = 'export_path', default = 'imageactive', help = 'What would you like to greet?')
    def effect(self):
        
        try:
            #export_path = self.options.export_path
            #imageActive = iaObject()
            #currentDir = os.path.dirname(os.path.realpath(__file__))
            #if not os.path.isdir(export_path + '/img'):
            #    shutil.copytree(currentDir + '/iaConvert/images_actives/img/', export_path + '/img/')
            #if not os.path.isdir(export_path + '/css'):
            #    shutil.copytree(currentDir + '/iaConvert/images_actives/css/', export_path + '/css/')
            #if not os.path.isdir(export_path + '/js'):
            #    shutil.copytree(currentDir + '/iaConvert/images_actives/js/', export_path + '/js/')        
            #if not os.path.isdir(export_path + '/datas'):
            #    os.mkdir(export_path + '/datas')

            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            
            with open(filePath,"w") as file:
                self.document.write(filePath)
            #    imageActive.analyzeSVG(filePath)

            root = Tkinter.Tk()
            root.title("IA2 Converter")
            root.geometry("465x310")
            root.attributes('-topmost', 1)
            img = Tkinter.PhotoImage(file='iaConvert/images/image-active64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)  
            maindialog = IADialog(root, "iaConvert", filePath)
            maindialog.pack(side="left")
            root.mainloop()
            


            #imageActive.generateJSON(export_path + "/datas/data.js")
            #imageActive.generateAccordion(export_path + "/index.html")
        except ValueError:
           print(ValueError)
           
        

                                    
ia = ImageActive()
ia.affect()
          			
