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

    def __init__(self, iaobject, PageFormatter, langPath):
        """Init"""

        try:
            t = gettext.translation("xia-converter", langPath, languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("xia-converter", langPath, languages=['en_US'])
        translate = t.ugettext
        
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = translate("export game1clic")
        self.score = "0"
        self.game_not_configured = translate("You win !")
        self.message = self.game_not_configured

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        
        self.score = "0"
        self.message = self.game_not_configured

        self.score2 = "0"
        self.message2 = self.game_not_configured
        
        score = re.search('<score>(.*?)</score>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if score:
            self.score = score.group(1)

        message = re.search('<message>(.*?)</message>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if message:
            self.message = message.group(1)

        score2 = re.search('<score2>(.*?)</score2>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if score2:
            self.score2 = score2.group(1)

        message2 = re.search('<message2>(.*?)</message2>', self.iaobject.scene["intro_detail"], re.IGNORECASE|re.DOTALL)
        if message2:
            self.message2 = message2.group(1)
       
       
        final_str = u'<article class="message_success" id="message_success" data-score="' + self.score + '">\n'
        final_str += '<img id="popup_toggle" src="img/hide.png" alt="toggle"/>\n'        
        final_str += u'  <div id="message_success_content">' + self.PageFormatter(self.message).print_html() + u'</div>\n'
        final_str += u'</article>\n'

        final_str += u'<article class="message_success" id="message_success2" data-score="' + self.score2 + '">\n'
        final_str += '<img id="popup_toggle2" src="img/hide.png" alt="toggle"/>\n'        
        final_str += u'  <div id="message_success_content2">' + self.PageFormatter(self.message2).print_html() + u'</div>\n'
        final_str += u'</article>\n'
            
        for i, detail in enumerate(self.iaobject.details):

            tooltip_state = ""
            tooltip = re.search('<tooltip>(.*)</tooltip>', detail["detail"], re.IGNORECASE|re.DOTALL)
            if tooltip:
                tooltip_state = tooltip.group(1)            

            final_str += u'<article class="detail_content" data-kinetic_id="'+detail["id"]+'" data-tooltip="' + tooltip_state + '" data-options="' + detail['options'] + u'" id="article-'+unicode(str(i), "utf8") + u'">\n'
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
