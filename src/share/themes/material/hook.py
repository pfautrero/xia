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
# @author : pascal.fautrero@gmail.com

import gettext
import locale

class hook:
    """do some stuff during image active generations"""

    def __init__(self, root, iaobject, PageFormatter, langPath):
        """Init"""

        try:
            t = gettext.translation("xia-converter", langPath, languages=[locale.getlocale()[0]])
        except:
            t = gettext.translation("xia-converter", langPath, languages=['en_US'])
        self.translate = t.gettext
        self.root = root
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = self.translate("export material")
        self.loading = self.translate("loading")

    def add_metadata(self, value, label):
        return f"<tr><td>{label}</td><td>{value}</td></tr>" if value else ""

    def convert_link(self, entry):
        return f'<a href="{entry}">{entry}</a>' if entry.startswith('http') else entry

    def generateIndex(self,filePath, templatePath, localFolder):
        """ generate index file"""

        params = {
            'intro_title' : self.iaobject.scene["intro_title"],
            'intro_content' : self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html()
        }
        final_str = u"""
            <article id="general">
                <h1 style="display:none;">{intro_title}</h1>
                <p>{intro_content}</p>
            </article>""".format(**params)

        for i, detail in enumerate(self.iaobject.details):
            if detail['options'].find(u"direct-link") == -1:
                params = {
                    'data_state' : "void" if (self.PageFormatter(detail["desc"]).print_html() == "") and (detail["title"] == "") else "full",
                    'article_id' : str(i).encode(),
                    'article_title' : detail['title'],
                    'article_content' : self.PageFormatter(detail["desc"]).print_html()
                }
                final_str += u"""
                    <article data-state="{data_state}" id="article-{article_id}">
                        <h1 style="display:none;">{article_title}</h1>
                        <div>{article_content}</div>
                    </article>""".format(**params)

        with open(templatePath,"rb") as template:

            license = self.convert_link(self.iaobject.scene["license"])

            metadatas = ""
            metadatas += self.add_metadata(self.iaobject.scene["creator"], self.translate("creator"))
            metadatas += self.add_metadata(self.iaobject.scene["rights"], self.translate("rights"))
            metadatas += self.add_metadata(self.iaobject.scene["publisher"], self.translate("publisher"))
            metadatas += self.add_metadata(self.iaobject.scene["identifier"], self.translate("identifier"))
            metadatas += self.add_metadata(self.iaobject.scene["coverage"], self.translate("coverage"))
            metadatas += self.add_metadata(self.iaobject.scene["source"], self.translate("source"))
            metadatas += self.add_metadata(self.iaobject.scene["relation"], self.translate("relation"))
            metadatas += self.add_metadata(self.iaobject.scene["language"], self.translate("language"))
            metadatas += self.add_metadata(self.iaobject.scene["contributor"], self.translate("contributor"))
            metadatas += self.add_metadata(self.iaobject.scene["date"], self.translate("date"))
            metadatas += self.add_metadata(license, self.translate("license"))

            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.funraiders.org/cdn/xia30"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/material/css/main.css")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", "https://cdnjs.cloudflare.com/ajax/libs/konva/7.1.1/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/material/js/hooks.js")
                final_index = final_index.replace("{{LogoDelete}}", xiaWebsite + "/material/img/delete.png")
            else:
                final_index = final_index.replace("{{MainCSS}}", localFolder +"/css/main.css")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", localFolder +'/datas/data.js')
                final_index = final_index.replace("{{sha1JS}}", localFolder +"/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", localFolder +"/js/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", localFolder +"/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", localFolder +"/js/hooks.js")
                final_index = final_index.replace("{{LogoDelete}}", localFolder + "/img/delete.png")
        with open(filePath,"wb") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
