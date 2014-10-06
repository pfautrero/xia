#!/usr/bin/env python
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
# @author : pascal.fautrero@ac-versailles.fr


#import os, shutil
import inkex
import tempfile
import Tkinter
import ConfigParser
from xiaconverter.mainwindow import IADialog

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):

        # fix inkscape bug 
        # https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/944077/comments/11
        pathNodes = self.document.xpath('//sodipodi:namedview',namespaces=inkex.NSS)
        pathNodes[0].set('id','base')        

        config = ConfigParser.ConfigParser()
        config.read("xia.cnf")
        imagesPath = config.get('paths', 'imagesPath')
        langPath = config.get('paths', 'langPath')
        fontsPath = config.get('paths', 'fontsPath')
        themesPath = config.get('paths', 'themesPath')        
        labjsLib = config.get('paths', 'labjsLib')
        jqueryLib = config.get('paths', 'jqueryLib')
        kineticLib = config.get('paths', 'kineticLib')
        bootstrapLib = config.get('paths', 'bootstrapLib')        
       
        try:
            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            with open(filePath,"w") as file:
                self.document.write(filePath)

            root = Tkinter.Tk()
            root.title("Xia - 1.0-alpha8")
            root.geometry("465x310")
            root.resizable(0,0)
            img = Tkinter.PhotoImage(file= imagesPath + '/image-active64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)  
            maindialog = IADialog(root,langPath, imagesPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, bootstrapLib, filePath)
            maindialog.pack(side="left")
            root.mainloop()

        except ValueError:
           #print(ValueError)
           pass
                              
ia = ImageActive()
ia.affect()
          			
