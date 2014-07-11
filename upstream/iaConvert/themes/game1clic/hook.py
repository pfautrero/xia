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

# dom manipulation
from xml.dom import minidom

class hook:
    """do some stuff during image active generations"""

    def __init__(self, iaobject, PageFormatter):
        """Init"""
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = "export game1clic"        
        self.score = 0
        self.message = "Ce jeu n'a pas été configuré correctement !"

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        print self.iaobject.scene["intro_detail"]
        xml = minidom.parseString("<game>"+self.iaobject.scene["intro_detail"]+"</game>")
        
        score = xml.getElementsByTagName('score')
        if score.item(0) is not None:
            self.score = score.item(0).childNodes[0].nodeValue

        message = xml.getElementsByTagName('message')
        if message.item(0) is not None:
            self.message = message.item(0).childNodes[0].nodeValue
        
        
        final_str = u'<article class="message_success" id="message_success" data-score="' + self.score + '">\n'
        final_str += u'  <p>' + self.PageFormatter(self.message).print_html() + u'</p>\n'
        final_str += u'</article>\n'

        with open(templatePath,"r") as template:
            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{RIGHTS}}", self.iaobject.scene["rights"])
            final_index = final_index.replace("{{CREATOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{PUBLISHER}}", self.iaobject.scene["publisher"])
            final_index = final_index.replace("{{CONTENT}}", final_str)            
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
