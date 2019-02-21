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
        self.tooltip = translate("export buttonBlue")
        self.loading = translate("loading")

    def add_metadata(self, value):
        return value + "<br/>" if value else ""

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""

        params = {
            'intro_title' : self.iaobject.scene["intro_title"],
            'intro_content' : self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html()
        }
        final_str = u"""
            <article class="detail_content" id="general">
                <h1>{intro_title}</h1>
                <p>{intro_content}</p>
            </article>""".format(**params)

        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:
                dataState = "void" if self.PageFormatter(detail["detail"]).print_html() == "" else "full"
                params = {
                    'data_state' : "void" if self.PageFormatter(detail["detail"]).print_html() == "" else "full",
                    'article_id' : unicode(str(i), "utf8"),
                    'article_title' : detail['title'],
                    'article_content' : self.PageFormatter(detail["detail"]).print_html()
                }
                final_str += u"""
                    <article class="detail_content" data-state="{data_state}" id="article-{article_id}">
                        <h1>{article_title}</h1>
                        <div>{article_content}</div>
                    </article>
                """.format(**params)

        with open(templatePath,"r") as template:
            final_index = template.read().decode("utf-8")

            metadatas = ""
            metadatas += self.add_metadata(self.iaobject.scene["creator"])
            metadatas += self.add_metadata(self.iaobject.scene["rights"])
            metadatas += self.add_metadata(self.iaobject.scene["publisher"])
            metadatas += self.add_metadata(self.iaobject.scene["identifier"])
            metadatas += self.add_metadata(self.iaobject.scene["coverage"])
            metadatas += self.add_metadata(self.iaobject.scene["source"])
            metadatas += self.add_metadata(self.iaobject.scene["relation"])
            metadatas += self.add_metadata(self.iaobject.scene["language"])
            metadatas += self.add_metadata(self.iaobject.scene["contributor"])
            metadatas += self.add_metadata(self.iaobject.scene["date"])

            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.dane.ac-versailles.fr/network/delivery/xia30/buttonBlue"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/css/main.css")
                final_index = final_index.replace("{{LogoLoading}}",  xiaWebsite + "/img/xia.png")
                final_index = final_index.replace("{{LogoPDF}}",  xiaWebsite + "/img/pdf.png")
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
                final_index = final_index.replace("{{LogoPDF}}",  "img/pdf.png")
                final_index = final_index.replace("{{LogoClose}}", "img/close.png")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", 'datas/data.js')
                final_index = final_index.replace("{{JqueryJS}}", "js/jquery.min.js")
                final_index = final_index.replace("{{sha1JS}}", "js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", "js/kinetic.min.js")
                final_index = final_index.replace("{{xiaJS}}", "js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", "js/hooks.js")
                final_index = final_index.replace("{{labJS}}", "js/LAB.min.js")
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
