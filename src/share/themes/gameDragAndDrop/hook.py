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
import json

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
        self.tooltip = translate("export gameDragAndDrop")
        self.score = "0"
        self.collisions = "off"
        self.message = translate("You win !")
        self.loading = translate("loading")

    def search(self, regexp, string_to_parse, failed):
        found_exp = re.search(regexp, string_to_parse, re.IGNORECASE|re.DOTALL)
        return found_exp.group(1) if found_exp else failed

    def add_metadata(self, value):
        return value + "<br/>" if value else ""

    def generateIndex(self,filePath, templatePath, localFolder):
        """ generate index file"""

        self.score = self.search('<score>(.*?)</score>', self.iaobject.scene["intro_detail"], "0")
        self.message = self.search('<message>(.*?)</message>', self.iaobject.scene["intro_detail"], "")
        self.score2 = self.search('<score2>(.*?)</score2>', self.iaobject.scene["intro_detail"], "0")
        self.message2 = self.search('<message2>(.*?)</message2>', self.iaobject.scene["intro_detail"], "")
        self.collisions = self.search('<collisions>(.*?)</collisions>', self.iaobject.scene["intro_detail"], "off")
        self.magnet = self.search('<magnet>(.*?)</magnet>', self.iaobject.scene["intro_detail"], "off")

        params_global = {
            'magnet' : self.magnet,
            'collisions' : self.collisions,
            'score' : self.score,
            'message' : self.PageFormatter(self.message).print_html(),
            'score2' : self.score2,
            'message2' : self.PageFormatter(self.message2).print_html(),
            'intro_title' : self.iaobject.scene["intro_title"],
            'intro_content' : self.PageFormatter(self.iaobject.scene["intro_detail"]).print_html()
        }

        final_str = u"""
            <article class="message_success" id="message_success" data-magnet="{magnet}" data-collisions="{collisions}" data-score="{score}">
                <div class="message_success_border">
                    <img id="popup_toggle" src="[[LogoHide]]" alt="toggle"/>
                    <div id="message_success_content">{message}</div>
                </div>
            </article>
            <article class="message_success" id="message_success2" data-magnet="{magnet}" data-collisions="{collisions}" data-score="{score2}">
                <div class="message_success_border">
                    <img id="popup_toggle2" src="[[LogoHide]]" alt="toggle"/>
                    <div id="message_success_content2">{message2}</div>
                </div>
            </article>
            <article style="display:none" id="general">
                <h1>{intro_title}</h1>
                <p>{intro_content}</p>
            </article>""".format(**params_global)

        for i, detail in enumerate(self.iaobject.details):

            params = {
                'tooltip' : self.search('<tooltip>(.*?)</tooltip>', detail["desc"], ""),
                'collisions' : self.search('<collisions>(.*?)</collisions>', detail["desc"], "on"),
                'onfail' : self.search('<onfail>(.*?)</onfail>', detail["desc"], ""),
                'magnet' : self.search('<magnet>(.*?)</magnet>', detail["desc"], "off"),
                'kinetic_id' : detail["id"],
                'target' : self.search('<target>(.*?)</target>', detail["desc"], ""),
                'article_id' : str(i),
                'article_title' : detail['title'],
                'article_content' : self.PageFormatter(detail["desc"]).print_html()
            }
            final_str += u"""
                <article class="detail_content" data-tooltip="{tooltip}" data-collisions="{collisions}" data-onfail="{onfail}" data-magnet="{magnet}" data-kinetic_id="{kinetic_id}" data-target="{target}" id="article-{article_id}">
                    <h1>{article_title}</h1>
                    <p>{article_content}</p>
                </article>""".format(**params)

        with open(templatePath,"rb") as template:
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
            final_index = final_index.replace("{{SCENESPECIFICOPTIONS}}", json.dumps(params_global))
            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{INTRODUCTION}}", self.PageFormatter(self.iaobject.scene["description"]).print_html())
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            final_index = final_index.replace("{{CONTENT}}", final_str)
            final_index = final_index.replace("{{LOADING}}", self.loading)
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.funraiders.org/cdn/xia30"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/gameDragAndDrop/css/main.css")
                final_index = final_index.replace("{{LogoHide}}",  xiaWebsite + "/gameDragAndDrop/img/hide.png")
                final_index = final_index.replace("{{LogoLoading}}",  xiaWebsite + "/gameDragAndDrop/img/xia.png")
                final_index = final_index.replace("{{LogoPDF}}",  xiaWebsite + "/gameDragAndDrop/img/pdf.png")
                final_index = final_index.replace("{{LogoClose}}", xiaWebsite + "/gameDragAndDrop/img/close.png")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{JqueryJS}}", "https://code.jquery.com/jquery-1.11.1.min.js")
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", xiaWebsite + "/gameDragAndDrop/js/kinetic-xia.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/gameDragAndDrop/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/gameDragAndDrop/js/hooks.js")
                final_index = final_index.replace("{{labJS}}", "https://cdnjs.cloudflare.com/ajax/libs/labjs/2.0.3/LAB.min.js")
            else:
                final_index = final_index.replace("{{MainCSS}}", localFolder +"/css/main.css")
                final_index = final_index.replace("{{LogoLoading}}", localFolder +"/img/xia.png")
                final_index = final_index.replace("{{LogoPDF}}", localFolder +"/img/pdf.png")
                final_index = final_index.replace("{{LogoHide}}", localFolder +"/img/hide.png")
                final_index = final_index.replace("{{LogoClose}}", localFolder +"/img/close.png")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", localFolder +'/datas/data.js')
                final_index = final_index.replace("{{JqueryJS}}", localFolder +"/js/jquery.min.js")
                final_index = final_index.replace("{{sha1JS}}", localFolder +"/js/git-sha1.min.js")
                final_index = final_index.replace("{{kineticJS}}", localFolder +"/js/kinetic-xia.min.js")
                final_index = final_index.replace("{{xiaJS}}", localFolder +"/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", localFolder +"/js/hooks.js")
                final_index = final_index.replace("{{labJS}}", localFolder +"/js/LAB.min.js")
        with open(filePath,"wb") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
