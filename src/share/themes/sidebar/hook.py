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
        self.tooltip = translate("export sidebar !")
        self.loading = translate("loading")

    def add_metadata(self, value):
        return value + "<br/>" if value else ""

    def generateIndex(self,filePath, templatePath, localFolder):
        """ generate index file"""

        with open(templatePath,"rb") as template:
            final_index = template.read().decode()

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

            #final_index = final_index.replace("{{METADATAS}}", metadatas)
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
                final_index = final_index.replace("{{datasJS}}", "<script>" + self.iaobject.jsonContent + "</script>")
                final_index = final_index.replace("{{lazyDatasJS}}", '')
                final_index = final_index.replace("{{sha1JS}}", xiaWebsite + "/js/git-sha1.min.js")
                final_index = final_index.replace("{{konvaJS}}", "https://cdnjs.cloudflare.com/ajax/libs/konva/3.1.7/konva.min.js")
                final_index = final_index.replace("{{xiaJS}}", xiaWebsite + "/js/xia.js")
                final_index = final_index.replace("{{hooksJS}}", xiaWebsite + "/sidebar/js/hooks.js")
                final_index = final_index.replace("{{quantizeJS}}", xiaWebsite + "/sidebar/js/quantization.min.js")
            else:
                final_index = final_index.replace("{{MainCSS}}", localFolder +"/css/main.css")
                final_index = final_index.replace("{{reload}}", localFolder +"/img/reload.png")
                final_index = final_index.replace("{{fullscreen}}", localFolder +"/img/fullscreen.png")
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
