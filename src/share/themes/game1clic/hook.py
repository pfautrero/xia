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
        self.tooltip = translate("export game1clic")
        self.game_not_configured = translate("You win !")
        self.loading = translate("loading")

    def search(self, regexp, string_to_parse, failed):
        found_exp = re.search(regexp, string_to_parse, re.IGNORECASE|re.DOTALL)
        if found_exp:
            return found_exp.group(1)
        else:
            return failed

    def add_metadata(self, value):
        return value + "<br/>" if value else ""

    def generateIndex(self,filePath, templatePath, localFolder):
        """ generate index file"""

        self.score = self.search('<score>(.*?)</score>', self.iaobject.scene["intro_detail"], "0")
        self.message = self.search('<message>(.*?)</message>', self.iaobject.scene["intro_detail"], self.game_not_configured)
        self.score2 = self.search('<score2>(.*?)</score2>', self.iaobject.scene["intro_detail"], "0")
        self.message2 = self.search('<message2>(.*?)</message2>', self.iaobject.scene["intro_detail"], self.game_not_configured)

        params = {
            'score' : self.score,
            'message_success' : self.PageFormatter(self.message).print_html(),
            'score2' : self.score2,
            'message_success2' : self.PageFormatter(self.message2).print_html(),
            'intro_title' : self.iaobject.scene["intro_title"],
            'intro_detail' : self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html()
        }

        final_str = u"""
            <article class="message_success" id="message_success" data-score="{score}">
                <img id="popup_toggle" src="[[LogoHide]]" alt="toggle"/>
                <div id="message_success_content">{message_success}</div>
            </article>
            <article class="message_success" id="message_success2" data-score="{score2}">
                <img id="popup_toggle2" src="[[LogoHide]]" alt="toggle"/>
                <div id="message_success_content2">{message_success2}</div>
            </article>
            <article style="display:none" id="general">
                <h1>{intro_title}</h1>
                <p>{intro_detail}</p>
            </article>""".format(**params)

        for i, detail in enumerate(self.iaobject.details):
            params = {
                'kinetic_id' : detail["id"],
                'tooltip_attr' : self.search('<tooltip>(.*)</tooltip>', detail["detail"], ""),
                'options' : detail['options'],
                'article_id' : unicode(str(i), "utf8"),
                'detail_title' : detail['title'],
                'detail_desc' : self.PageFormatter(detail["detail"]).print_html()
            }
            final_str += u"""
                <article class="detail_content" data-kinetic_id="{kinetic_id}" data-tooltip="{tooltip_attr}" data-options="{options}" id="article-{article_id}">
                    <h1>{detail_title}</h1>
                    <p>{detail_desc}</p>
                </article>""".format(**params)


        with open(templatePath,"r") as template:

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

            final_index = template.read().decode("utf-8")
            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{INTRODUCTION}}", self.PageFormatter(self.iaobject.scene["description"]).print_html())
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.dane.ac-versailles.fr/network/delivery/xia30/game1clic"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/css/main.css")
                final_index = final_index.replace("{{LogoLoading}}",  xiaWebsite + "/img/xia.png")
                final_index = final_index.replace("{{LogoPDF}}",  xiaWebsite + "/img/pdf.png")
                final_index = final_index.replace("[[LogoHide]]",  xiaWebsite + "/img/hide.png")
                final_index = final_index.replace("{{LogoClose}}", xiaWebsite + "/img/close.png")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{JqueryJS}}", "https://code.jquery.com/jquery-1.11.1.min.js")
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", xiaWebsite + "/js/kinetic-xia.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/js/hooks.js")
                final_index = final_index.replace("{{labJS}}", "https://cdnjs.cloudflare.com/ajax/libs/labjs/2.0.3/LAB.min.js")
            else:
                final_index = final_index.replace("{{MainCSS}}", localFolder +"/css/main.css")
                final_index = final_index.replace("{{LogoLoading}}", localFolder +"/img/xia.png")
                final_index = final_index.replace("{{LogoPDF}}", localFolder +"/img/pdf.png")
                final_index = final_index.replace("[[LogoHide]]", localFolder +"/img/hide.png")
                final_index = final_index.replace("{{LogoClose}}", localFolder +"/img/close.png")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", localFolder +'/datas/data.js')
                final_index = final_index.replace("{{JqueryJS}}", localFolder +"/js/jquery.min.js")
                final_index = final_index.replace("{{sha1JS}}", localFolder +"/js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", localFolder +"/js/kinetic-xia.min.js")
                final_index = final_index.replace("{{xiaJS}}", localFolder +"/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", localFolder +"/js/hooks.js")
                final_index = final_index.replace("{{labJS}}", localFolder +"/js/LAB.min.js")
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
