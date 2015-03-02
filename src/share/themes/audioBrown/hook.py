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
        self.tooltip = translate("export audioBrown")
        self.loading = translate("loading")

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        
        final_str  = u'<article class="detail_content" id="general">\n'
        final_str += '<img class="article_close" src="{{LogoClose}}" alt="close"/>'
        final_str += u'  <h1>' + self.iaobject.scene["intro_title"] + '</h1>\n'
        final_str += u'  <p>' + self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html() + u'</p>\n'
        final_str += u'</article>\n'
        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:
                dataState = "full"
                if self.PageFormatter(detail["detail"]).print_html() == "":
                    dataState = "void"
                final_str += u'<article class="detail_content" data-state="' + dataState + '" id="article-'+unicode(str(i), "utf8") + u'">\n'
                final_str += '<img class="article_close" src="{{LogoClose}}" alt="close"/>'
                if detail['title'] != "":
                    final_str += u'  <h1>' + detail['title'] + u'</h1>\n'
                final_str += u'  <div>' + self.PageFormatter(detail["detail"]).print_html() + u'</div>\n'
                final_str += u'</article>\n'

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
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.index_standalone:
                xiaWebsite = "http://xia.dane.ac-versailles.fr/network/delivery/audioBrown"
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
