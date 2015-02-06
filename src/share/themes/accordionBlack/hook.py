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

    def __init__(self, root, iaobject, PageFormatter, langPath):
        """Init"""

        try:
            t = gettext.translation("xia-converter", langPath, languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("xia-converter", langPath, languages=['en_US'])
        translate = t.ugettext
        
        self.root = root
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = translate("export accordionBlack !")
        self.loading = translate("loading")

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

            metadatas = ""
            if self.iaobject.scene["creator"]:
                metadatas += self.iaobject.scene["creator"] + "<br/>"
            if self.iaobject.scene["rights"]:
                metadatas += self.iaobject.scene["rights"] + "<br/>"
            if self.iaobject.scene["publisher"]:
                metadatas += self.iaobject.scene["publisher"] + "<br/>"
            if self.iaobject.scene["identifier"]:
                metadatas += self.iaobject.scene["identifier"] + "<br/>"
            if self.iaobject.scene["coverage"]:
                metadatas += self.iaobject.scene["coverage"] + "<br/>"
            if self.iaobject.scene["source"]:
                metadatas += self.iaobject.scene["source"] + "<br/>"
            if self.iaobject.scene["relation"]:
                metadatas += self.iaobject.scene["relation"] + "<br/>"
            if self.iaobject.scene["language"]:
                metadatas += self.iaobject.scene["language"] + "<br/>"
            if self.iaobject.scene["contributor"]:
                metadatas += self.iaobject.scene["contributor"] + "<br/>"
            if self.iaobject.scene["date"]:
                metadatas += self.iaobject.scene["date"] + "<br/>"

            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{ACCORDION}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.index_standalone:
                xiaWebsite = "http://xia.dane.ac-versailles.fr/network/delivery/accordionBlack"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/css/main.css")
                final_index = final_index.replace("{{LogoLoading}}",  xiaWebsite + "/img/xia.png")
                final_index = final_index.replace("{{LogoClose}}", xiaWebsite + "/img/close.png")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{JqueryJS}}", "https://code.jquery.com/jquery-1.11.1.min.js")
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", "https://cdn.jsdelivr.net/kineticjs/5.1.0/kinetic.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/js/hooks.js")
                final_index = final_index.replace("{{labJS}}", "https://cdnjs.cloudflare.com/ajax/libs/labjs/2.0.3/LAB.min.js")
            else:
                final_index = final_index.replace("{{MainCSS}}", "css/main.css")
                final_index = final_index.replace("{{LogoLoading}}",  "img/xia.png")
                final_index = final_index.replace("{{LogoClose}}", "img/close.png")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", '.script("datas/data.js")')
                final_index = final_index.replace("{{JqueryJS}}", "js/jquery.min.js")
                final_index = final_index.replace("{{sha1JS}}", "js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", "js/kinetic.min.js")
                final_index = final_index.replace("{{xiaJS}}", "js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", "js/hooks.js")
                final_index = final_index.replace("{{labJS}}", "js/LAB.min.js")                
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
