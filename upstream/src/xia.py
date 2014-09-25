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
#from iaConvert.ia2.iaobject import iaObject
from converter.includes.mainwindow import IADialog

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):

        # fix inkscape bug 
        # https://bugs.launchpad.net/ubuntu/+source/inkscape/+bug/944077/comments/11
        pathNodes = self.document.xpath('//sodipodi:namedview',namespaces=inkex.NSS)
        pathNodes[0].set('id','base')        
       
        try:
            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            with open(filePath,"w") as file:
                self.document.write(filePath)

            root = Tkinter.Tk()
            root.title("Xia - alpha 6")
            root.geometry("465x310")
            root.resizable(0,0)
            img = Tkinter.PhotoImage(file='converter/images/image-active64.gif')
            root.tk.call('wm', 'iconphoto', root._w, img)  
            maindialog = IADialog(root, "converter", filePath)
            maindialog.pack(side="left")
            root.mainloop()

        except ValueError:
           #print(ValueError)
           pass
                              
ia = ImageActive()
ia.affect()
          			
