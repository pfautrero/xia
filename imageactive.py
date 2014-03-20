#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, shutil
import inkex
import tempfile
from iaConvert.lib.iaobject import iaObject

class ImageActive(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-e', '--export_path', action = 'store', type = 'string', dest = 'export_path', default = 'imageactive', help = 'What would you like to greet?')
    def effect(self):
        err_file = open("/tmp/inkscape_error_ia.txt" , "w")
        try:
            export_path = self.options.export_path
            imageActive = iaObject()
            currentDir = os.path.dirname(os.path.realpath(__file__))
            if not os.path.isdir(export_path + '/img'):
                shutil.copytree(currentDir + '/iaConvert/images_actives/img/', export_path + '/img/')
            if not os.path.isdir(export_path + '/css'):
                shutil.copytree(currentDir + '/iaConvert/images_actives/css/', export_path + '/css/')
            if not os.path.isdir(export_path + '/js'):
                shutil.copytree(currentDir + '/iaConvert/images_actives/js/', export_path + '/js/')        
            if not os.path.isdir(export_path + '/datas'):
                os.mkdir(export_path + '/datas')

            filePath = tempfile.mkdtemp() + "/" + "temp.svg"
            
            with open(filePath,"w") as file:
                self.document.write(filePath)
                imageActive.analyzeSVG(filePath)

            imageActive.generateJSON(export_path + "/datas/data.js")
            imageActive.generateAccordion(export_path + "/index.html")
        except:
           traceback.print_exc(file=err_file)
        finally:
            err_file.close()


                                    
ia = ImageActive()
ia.affect()
          			
