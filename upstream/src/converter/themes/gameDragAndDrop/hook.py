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
import re

import gettext
import locale

class hook:
    """do some stuff during image active generations"""

    def __init__(self, iaobject, PageFormatter, localdir):
        """Init"""
        try:
            t = gettext.translation("messages", localdir + "/i18n", languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("messages", localdir + "/i18n", languages=['en_US'])
        translate = t.ugettext
        
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = translate("export gameDragAndDrop")        
        self.score = "0"
        self.collisions = "off"
        self.message = translate("This game is not properly configured")

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        
        score = re.search('<score>(.*)</score>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if score:
            self.score = score.group(1)

        message = re.search('<message>(.*)</message>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if message:
            self.message = message.group(1)

        collisions = re.search('<collisions>(.*)</collisions>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if collisions:
            self.collisions = collisions.group(1)        
        
        final_str = u'<article class="message_success" id="message_success" data-collisions="' + self.collisions + '" data-score="' + self.score + '">\n'
        final_str += '<img id="popup_toggle" src="img/hide.png" alt="toggle"/>\n'
        final_str += u'  <p id="message_success_content">' + self.PageFormatter(self.message).print_html() + u'</p>\n'
        final_str += u'</article>\n'
        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:            
                #xml = minidom.parseString(u"<detail>"+detail["detail"]+u"</detail>")

                target_id = ""
                target = re.search('<target>(.*)</target>', detail["detail"], re.IGNORECASE|re.DOTALL)
                if target:
                    target_id = target.group(1)

                magnet_state = "off"
                magnet = re.search('<magnet>(.*)</magnet>', detail["detail"], re.IGNORECASE|re.DOTALL)
                if magnet:
                    magnet_state = magnet.group(1)

                collision_state = "on"
                collision = re.search('<collisions>(.*)</collisions>', detail["detail"], re.IGNORECASE|re.DOTALL)
                if collision:
                    collision_state = collision.group(1)

                #target = xml.getElementsByTagName("target");
                #target_id = ""
                #if target.item(0) is not None:
                #    target_id = target.item(0).childNodes[0].nodeValue

                #magnet = xml.getElementsByTagName("magnet");
                #magnet_state = "off"
                #if magnet.item(0) is not None:
                #    magnet_state = magnet.item(0).childNodes[0].nodeValue   
                    

                final_str += u'<article class="detail_content" data-collisions="'+ collision_state +'" data-magnet="'+ magnet_state +'" data-kinetic_id="'+detail["id"]+'" data-target="'+target_id+'" id="article-'+unicode(str(i), "utf8") + u'">\n'
                final_str += u'  <h1>' + detail['title'] + u'</h1>\n'
                final_str += u'  <p>' + self.PageFormatter(detail["detail"]).print_html() + u'<p>\n'
                final_str += u'</article>\n'

        with open(templatePath,"r") as template:
            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{INTRODUCTION}}", self.PageFormatter(self.iaobject.scene["description"]).print_html())            
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{RIGHTS}}", self.iaobject.scene["rights"])
            final_index = final_index.replace("{{CREATOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{PUBLISHER}}", self.iaobject.scene["publisher"])
            final_index = final_index.replace("{{CONTENT}}", final_str)            
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
