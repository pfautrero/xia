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
# @author : pascal.fautrero@ac-versailles.fr



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
        self.tooltip = translate("export accordionBlack !")

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        
        final_str  = u'<div class="accordion-group">\n';
        final_str += u'  <div class="accordion-heading">\n';
        final_str += u'    <a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">' + self.iaobject.scene["intro_title"] + '</a>\n';
        final_str += u'      <div id="collapsecomment" class="accordion-body collapse">\n';
        final_str += u'        <div class="accordion-inner">' + self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html() + u'\n';
        final_str += u'        </div>\n'
        final_str += u'      </div>\n'
        final_str += u'  </div>\n'
        final_str += u'</div>\n'
        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:
                final_str += u'<div class="accordion-group">\n'
                final_str += u'  <div class="accordion-heading">\n'
                final_str += u'      <a id="collapse' + unicode(str(i), "utf8") + u'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse' + unicode(str(i), "utf8") + u'">' + detail['title'] + u'</a>\n'
                final_str += u'      <div id="collapse' + unicode(str(i), "utf8") + u'" class="accordion-body collapse">\n'
                final_str += u'          <div class="accordion-inner">' + self.PageFormatter(detail["detail"]).print_html() + u'\n'
                final_str += u'          </div>\n'
                final_str += u'      </div>\n'
                final_str += u'  </div>\n'
                final_str += u'</div>\n'        

        with open(templatePath,"r") as template:
            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])            
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])            
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{RIGHTS}}", self.iaobject.scene["rights"])
            final_index = final_index.replace("{{CREATOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{PUBLISHER}}", self.iaobject.scene["publisher"])            
            final_index = final_index.replace("{{ACCORDION}}", final_str)            
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
