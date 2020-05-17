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
            t = gettext.translation("xia-converter", langPath, languages=[locale.getdefaultlocale()[0]])
        except:
            t = gettext.translation("xia-converter", langPath, languages=['en_US'])
        translate = t.gettext
        self.root = root
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = translate("export material")
        self.loading = translate("loading")


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
                    'data_state' : "void" if (self.PageFormatter(detail["detail"]).print_html() == "") and (detail["title"] == "") else "full",
                    'article_id' : str(i).encode(),
                    'article_title' : detail['title'],
                    'article_content' : self.PageFormatter(detail["detail"]).print_html()
                }
                final_str += u"""
                    <article data-state="{data_state}" id="article-{article_id}">
                        <h1 style="display:none;">{article_title}</h1>
                        <div>{article_content}</div>
                    </article>""".format(**params)

        with open(templatePath,"rb") as template:

            rights = self.iaobject.scene["rights"] if self.iaobject.scene["rights"] else ""
            publisher = self.iaobject.scene["publisher"] if self.iaobject.scene["publisher"] else ""
            identifier = self.iaobject.scene["identifier"] if self.iaobject.scene["identifier"] else ""
            coverage = self.iaobject.scene["coverage"] if self.iaobject.scene["coverage"] else ""
            source = self.iaobject.scene["source"] if self.iaobject.scene["source"] else ""
            relation = self.iaobject.scene["relation"] if self.iaobject.scene["relation"] else ""
            languages = self.iaobject.scene["language"] if self.iaobject.scene["language"] else ""
            contributor = self.iaobject.scene["contributor"] if self.iaobject.scene["contributor"] else ""
            datecreation = self.iaobject.scene["date"] if self.iaobject.scene["date"] else ""
            creator = self.iaobject.scene["creator"] if self.iaobject.scene["creator"] else ""
            license_origin = self.iaobject.scene["license"] if self.iaobject.scene["license"] else ""
            if license_origin.startswith('http'):
                license = u'<a href="{}">{}</a>'.format(license_origin, license_origin)
            elif license_origin == "":
                license = u"Propriétaire"
            else:
                license = license_origin

            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{LICENSE}}", license)
            final_index = final_index.replace("{{RIGHTS}}", rights)
            final_index = final_index.replace("{{PUBLISHER}}", publisher)
            final_index = final_index.replace("{{IDENTIFIER}}", identifier)
            final_index = final_index.replace("{{COVERAGE}}", coverage)
            final_index = final_index.replace("{{SOURCE}}", source)
            final_index = final_index.replace("{{RELATION}}", relation)
            final_index = final_index.replace("{{LANGUAGES}}", languages)
            final_index = final_index.replace("{{CONTRIBUTOR}}", contributor)
            final_index = final_index.replace("{{DATE}}", datecreation)
            final_index = final_index.replace("{{CREATOR}}", creator)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.dane.ac-versailles.fr/network/delivery/xia30/material"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/css/main.css")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", "https://cdnjs.cloudflare.com/ajax/libs/konva/3.1.7/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/js/hooks.js")
                final_index = final_index.replace("{{LogoDelete}}", xiaWebsite + "/img/delete.png")
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
