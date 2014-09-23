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
        self.tooltip = translate("export buttonBlue")        

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        final_str = ''        
        final_str += u'<article class="detail_content" id="general">\n'
        final_str += u'  <h1>' + self.iaobject.scene["intro_title"] + '</h1>\n'
        final_str += u'  <p>' + self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html() + u'</p>\n'
        final_str += u'</article>\n'
        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:
                if detail['detail'].find(u"Réponse:") != -1:
                    question = detail['detail'][0:detail['detail'].find(u"Réponse:")]
                    answer = detail['detail'][detail['detail'].find(u"Réponse:") + 9:]
                    final_str += u'<article class="detail_content" id="article-'+unicode(str(i), "utf8") + u'">\n'
                    final_str += u'  <h1>' + detail['title'] + u'</h1>\n'
                    final_str += u'  <p>' + self.PageFormatter(question).print_html() + u'<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_' + unicode(str(i), "utf8") + u'">Réponse</a></div>' + u'<div class="response" id="response_'+ unicode(str(i), "utf8") + u'">' + self.PageFormatter(answer).print_html() + u'</p>' + u'\n'
                    final_str += u'</article>\n'
                else:
                    final_str += u'<article class="detail_content" id="article-'+unicode(str(i), "utf8") + u'">\n'
                    final_str += u'  <h1>' + detail['title'] + u'</h1>\n'
                    final_str += u'  <p>' + self.PageFormatter(detail["detail"]).print_html() + u'<p>\n'
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
