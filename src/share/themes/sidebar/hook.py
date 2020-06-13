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
        self.translate = t.gettext

        self.root = root
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter
        self.tooltip = self.translate("export sidebar")
        self.loading = self.translate("loading")

    def add_metadata(self, value, label):
        return f"<tr><td>{label}</td><td>{value}</td></tr>" if value else ""

    def convert_link(self, entry):
        return f'<a href="{entry}">{entry}</a>' if entry.startswith('http') else entry

    def generateIndex(self,filePath, templatePath, localFolder):
        """ generate index file"""

        with open(templatePath,"rb") as template:
            final_index = template.read().decode()

            license = self.convert_link(self.iaobject.scene["license"])

            metadatas = ""
            metadatas += self.add_metadata(self.iaobject.scene["creator"], self.translate('creator'))
            metadatas += self.add_metadata(self.iaobject.scene["rights"], self.translate('rights'))
            metadatas += self.add_metadata(self.iaobject.scene["publisher"], self.translate('publisher'))
            metadatas += self.add_metadata(self.iaobject.scene["identifier"], self.translate('identifier'))
            metadatas += self.add_metadata(self.iaobject.scene["coverage"], self.translate('coverage'))
            metadatas += self.add_metadata(self.iaobject.scene["source"], self.translate('source'))
            metadatas += self.add_metadata(self.iaobject.scene["relation"], self.translate('relation'))
            metadatas += self.add_metadata(self.iaobject.scene["language"], self.translate('language'))
            metadatas += self.add_metadata(self.iaobject.scene["contributor"], self.translate('contributor'))
            metadatas += self.add_metadata(self.iaobject.scene["date"], self.translate('date'))
            metadatas += self.add_metadata(license, self.translate("license"))

            final_index = final_index.replace("{{METADATAS}}", metadatas)
            final_index = final_index.replace("{{AUTHOR}}", self.iaobject.scene["creator"])
            final_index = final_index.replace("{{DESCRIPTION}}", self.iaobject.scene["description"])
            final_index = final_index.replace("{{KEYWORDS}}", self.iaobject.scene["keywords"])
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"])
            if self.root.options["export_type"] == "singlefile":
                xiaWebsite = "https://xia.funraiders.org/cdn/xia30"
                final_index = final_index.replace("{{MainCSS}}", xiaWebsite + "/sidebar/css/main.css")
                final_index = final_index.replace("{{arrow_down}}",  xiaWebsite + "/sidebar/img/arrow_down.png")
                final_index = final_index.replace("{{reload}}",  xiaWebsite + "/sidebar/img/reload.png")
                final_index = final_index.replace("{{fullscreen}}", xiaWebsite + "/sidebar/img/fullscreen.png")
                final_index = final_index.replace("{{about}}", xiaWebsite + "/sidebar/img/information-outline.svg")
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", "https://cdnjs.cloudflare.com/ajax/libs/konva/6.0.0/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/sidebar/js/hooks.js")
                final_index = final_index.replace("{{quantizeJS}}", xiaWebsite + "/sidebar/js/quantization.min.js")
            else:
                final_index = final_index.replace("{{MainCSS}}", localFolder +"/css/main.css")
                final_index = final_index.replace("{{reload}}", localFolder +"/img/reload.png")
                final_index = final_index.replace("{{fullscreen}}", localFolder +"/img/fullscreen.png")
                final_index = final_index.replace("{{about}}", localFolder +"/img/information-outline.svg")
                final_index = final_index.replace("{{arrow_down}}",  localFolder + "/img/arrow_down.png")
                final_index = final_index.replace("{{datasJS}}", "")
                final_index = final_index.replace("{{lazyDatasJS}}", localFolder +'/datas/data.js')
                final_index = final_index.replace("{{sha1JS}}", localFolder +"/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", localFolder +"/js/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", localFolder +"/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", localFolder +"/js/hooks.js")
                final_index = final_index.replace("{{quantizeJS}}", localFolder +"/js/quantization.min.js")
        with open(filePath,"wb") as indexfile:
            indexfile.write(final_index.encode("utf-8"))
