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

# inkscape transformations
import cubicsuperpath

# dom manipulation
from xml.dom import minidom

# wiki engine
from pikipiki import PageFormatter

# svg transform analyzer
from ctm import CurrentTransformation
import os

class iaObject:
    """generate Image Active Object"""

    def __init__(self):
        """Init"""
        self.details = []
        self.scene = {}
        self.raster = ""

    def get_tag_value(self,node):
        if node.childNodes:
            return node.childNodes[0].nodeValue
        else:
            return ""


    def extractMetadatas(self, xml):
        
        metadatas = xml.getElementsByTagName('metadata')
        if metadatas.item(0) is not None:
            
            metadata = metadatas.item(0).getElementsByTagName('dc:title')
            if metadata.item(0) is not None:
                if self.get_tag_value(metadata.item(0)) != "":
                    self.scene['title'] = self.get_tag_value(metadata.item(0))

            self.scene['date'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:date')
            if metadata.item(0) is not None:
                self.scene['date'] = self.get_tag_value(metadata.item(0))            

            self.scene['creator'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:creator')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['creator'] = self.get_tag_value(metadata_value.item(0))

            self.scene['rights'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:rights')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['rights'] = self.get_tag_value(metadata_value.item(0))

            self.scene['publisher'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:publisher')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['publisher'] = self.get_tag_value(metadata_value.item(0))

            self.scene['language'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:language')
            if metadata.item(0) is not None:
                self.scene['language'] = self.get_tag_value(metadata.item(0))
            
            self.scene['keywords'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:subject')
            if metadata.item(0) is not None:
                items = metadata.item(0).getElementsByTagName('rdf:li')
                for key_word in items:
                    if self.scene['keywords']:
                        self.scene['keywords'] += ","
                    self.scene['keywords'] += self.get_tag_value(key_word) 
            
            self.scene['description'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:description')
            if metadata.item(0) is not None:
                self.scene['description'] = self.get_tag_value(metadata.item(0))

            self.scene['contributor'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:contributor')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['contributor'] = self.get_tag_value(metadata_value.item(0))


    def analyzeSVG(self,filePath):
        """analyze svg file and fill self.details and self.scene"""
        self.details[:] = []
        self.scene.clear()
        
        self.xml = minidom.parse(filePath)

        head, tail = os.path.split(filePath)
        self.scene['intro_title'] = u"Description"
        self.scene['intro_detail'] = u"Images Actives - Canopé Versailles"
        self.scene['image'] = ""
        self.scene['width'] = ""
        self.scene['height'] = ""
        self.scene['title'] = os.path.splitext(tail)[0]

        self.extractMetadatas(self.xml)

        # ==================== Look for background image

        images = self.xml.getElementsByTagName('image')
        if images.item(0) is not None:
            image = images.item(0)
            self.backgroundNode = image;
            self.scene['width'] = image.attributes['width'].value
            self.scene['height'] =  image.attributes['height'].value

            desc = image.getElementsByTagName('desc')
            if desc.item(0) is not None:
                if desc.item(0).parentNode == image:
                    self.scene['intro_detail'] = self.get_tag_value(desc.item(0))

            title = image.getElementsByTagName('title')
            if title.item(0) is not None:
                if title.item(0).parentNode == image:
                    self.scene['intro_title'] = self.get_tag_value(title.item(0))

            self.raster = image.attributes['xlink:href'].value
            if image.attributes['xlink:href'].value.startswith("file://"):
                # Embed background image thanks to data URI Scheme
                fileNameImage, fileExtensionImage = os.path.splitext(image.attributes['xlink:href'].value[7:])
                imgMimeTypes = {}
                imgMimeTypes['.png'] = 'image/png'
                imgMimeTypes['.jpg'] = 'image/jpeg'
                imgMimeTypes['.jpeg'] = 'image/jpeg'
                imgMimeTypes['.gif'] = 'image/gif'
                imgMimeTypes['.bmp'] = 'image/bmp'
                self.rasterPrefix = u"data:" + imgMimeTypes[fileExtensionImage.lower()] + u";base64,"
                with open(image.attributes['xlink:href'].value[7:], 'rb') as bgImage:
                    self.raster = self.rasterPrefix + bgImage.read().encode("base64", "strict")
            self.scene['image'] = self.raster

                
        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image', 'g']
        mainSVG = self.xml.getElementsByTagName('svg')
        if mainSVG[0]:
            for childnode in mainSVG[0].childNodes:
                if childnode.parentNode.nodeName == "svg":
                    if childnode.nodeName in svgElements:
                        newrecord = getattr(self, 'extract_' + childnode.nodeName)(childnode, 0)
                        if newrecord is not None:
                            self.details.append(newrecord)

    def extract_image(self, image, ctm_group):
        """Analyze images"""
        
        if not image.isSameNode(self.backgroundNode):
            record_image = {}
            record_image['image'] = image.attributes['xlink:href'].value
            record_image['width'] = image.attributes['width'].value
            record_image['height'] = image.attributes['height'].value
            record_image['detail'] = self.getText("desc", image)
            record_image['title'] = self.getText("title", image)
            record_image['x'] = str(0)
            record_image['y'] = str(0)                        

            if image.hasAttribute("x"):
                record_image['x'] = image.attributes['x'].value
            if image.hasAttribute("y"):
                record_image['y'] = image.attributes['y'].value
            
            if image.hasAttribute("style"):                            
                str_style = image.attributes['style'].value
                style = {}
                for item in str_style.split(";"):
                    key,value = item.split(":")
                    style[key] = value
                record_image['fill'] = style['fill']

            if image.hasAttribute("transform"):
                transformation = image.attributes['transform'].value
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                record_image['x'] = ctm.translateX
                record_image['y'] = ctm.translateY

            minX = 10000
            minY = 10000
            maxX = -10000
            maxY = -10000
            if float(record_image['x']) < float(minX):
                minX = float(record_image['x'])
            if (float(record_image['x']) + float(record_image['width'])) > float(maxX):
                maxX = float(record_image['x']) + float(record_image['width'])
            if float(record_image['y']) < float(minY):
                minY = float(record_image['y'])
            if (float(record_image['y']) + float(record_image['height'])) > float(maxY):
                maxY = float(record_image['y']) + float(record_image['height'])

            record_image["minX"] = str(minX)
            record_image["minY"] = str(minY)
            record_image["maxX"] = str(maxX)
            record_image["maxY"] = str(maxY) 

            return record_image

    def extract_rect(self, rect, ctm_group):
        """Analyze rectangles"""
        
        record_rect = {}
        record_rect['width'] = rect.attributes['width'].value
        record_rect['height'] = rect.attributes['height'].value
        record_rect['detail'] = self.getText("desc", rect)
        record_rect['title'] = self.getText("title", rect)
        record_rect['x'] = str(0)
        record_rect['y'] = str(0)
        record_rect['rx'] = str(0)
        record_rect['ry'] = str(0)                     

        if rect.hasAttribute("x"):
            record_rect['x'] = rect.attributes['x'].value
        if rect.hasAttribute("y"):
            record_rect['y'] = rect.attributes['y'].value
        if rect.hasAttribute("rx"):
            record_rect['rx'] = rect.attributes['rx'].value
        if rect.hasAttribute("ry"):
            record_rect['ry'] = rect.attributes['ry'].value

        if rect.hasAttribute("style"):                            
            str_style = rect.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key,value = item.split(":")
                style[key] = value
            record_rect['fill'] = style['fill']

        # ObjectToPath                    
        ctm = CurrentTransformation()
        record_rect['path'] = ctm.rectToPath(record_rect)

        p = cubicsuperpath.parsePath(record_rect['path'])
        record_rect['path'] = cubicsuperpath.formatPath(p)
        record_rect['x'] = str(0)
        record_rect['y'] = str(0)                        

        if rect.hasAttribute("transform"):
            transformation = rect.attributes['transform'].value
            ctm.analyze(transformation)

            ctm.applyTransformToPath(ctm.matrix,p)
            record_rect['path'] = cubicsuperpath.formatPath(p)


        # apply group transformation on current object
        if ctm_group:
            ctm_group.applyTransformToPath(ctm_group.matrix,p)
            record_rect['path'] = cubicsuperpath.formatPath(p)

        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i%2 == 0):
                    if float(p) < float(minX):
                        minX = float(p)
                    if float(p) > float(maxX):
                        maxX = float(p)
                else:
                    if float(p) < float(minY):
                        minY = float(p)
                    if float(p) > float(maxY):
                        maxY = float(p)
                i = i + 1
        record_rect["minX"] = str(minX)
        record_rect["minY"] = str(minY)
        record_rect["maxX"] = str(maxX)
        record_rect["maxY"] = str(maxY)

        record_rect['path'] = '"' + record_rect['path'] + ' z"'
        return record_rect

    def extract_path(self,path, ctm_group):
        """Analyze paths"""
        
        record = {}
        record["path"] = ""
        record["fill"] = ""
        record["path"] =  path.attributes['d'].value.replace("&#xd;&#xa;"," ").replace("&#x9;"," ").replace("\n"," ").replace("\t"," ").replace("\r"," ") 
        record["style"] = ""
        record['detail'] = self.getText("desc", path)
        record['title'] = self.getText("title", path)
        record['x'] = str(0)
        record['y'] = str(0)
        if path.hasAttribute("style") and (path.attributes['style'].value != ""):
            str_style = path.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key,value = item.split(":")
                style[key] = value
            record["fill"] = style['fill']

        if path.hasAttribute("x"):
            record['x'] = path.attributes['x'].value
        if path.hasAttribute("y"):            
            record['y'] = path.attributes['y'].value

        # ObjectToPath
        p = cubicsuperpath.parsePath(record['path'])
        record['path'] = cubicsuperpath.formatPath(p)

        if path.hasAttribute("transform"):
            transformation = path.attributes['transform'].value
            ctm = CurrentTransformation()
            ctm.analyze(transformation)

            ctm.applyTransformToPath(ctm.matrix,p)
            record['path'] = cubicsuperpath.formatPath(p)

        # apply group transformation on current object
        if ctm_group:
            ctm_group.applyTransformToPath(ctm_group.matrix,p)
            record['path'] = cubicsuperpath.formatPath(p)


        if record["path"].lower().find("z") == -1:
            record["path"] += " z"
        record['path'] = '"' + record['path'] + '"'
        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i%2 == 0):
                    if float(p) < float(minX):
                        minX = float(p)
                    if float(p) > float(maxX):
                        maxX = float(p)
                else:
                    if float(p) < float(minY):
                        minY = float(p)
                    if float(p) > float(maxY):
                        maxY = float(p)
                i = i + 1
        record["minX"] = str(minX)
        record["minY"] = str(minY)
        record["maxX"] = str(maxX)
        record["maxY"] = str(maxY)
        if record["path"]:
            return record

    def getText(self, type, element):
        """ type can be 'desc' or 'title' """
        text = element.getElementsByTagName(type)
        if text.item(0) is not None:
            if text.item(0).parentNode == element:
                #return self.get_tag_value(text.item(0)).replace("\n"," ").replace("\t"," ").replace("\r"," ")
                return self.get_tag_value(text.item(0))
        return ""

    def extract_g(self,group, ctm_group):
        """Analyze a svg group"""

        record = {}
        record['title'] = self.getText("title", group)
        record['detail'] = self.getText("desc", group)
        record["group"] = []
        minX = 10000
        minY = 10000
        maxX = 0
        maxY = 0
        # retrieve transformations applied on master group
        # TODO : manage nested groups tranformations
        
        ctm_group = CurrentTransformation()
        if group.hasAttribute("transform"):
            transformation = group.attributes['transform'].value
            ctm_group.analyze(transformation)

        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image']
        for childnode in group.childNodes:
            if childnode.nodeName in svgElements:
                newrecord = getattr(self, 'extract_' + childnode.nodeName)(childnode, ctm_group)
                if newrecord is not None:
                    record["group"].append(newrecord)

                    if float(newrecord["minX"]) < minX:
                        minX = float(newrecord["minX"])
                    if float(newrecord["minY"]) < minY:
                        minY = float(newrecord["minY"])
                    if float(newrecord["maxX"]) > maxX:
                        maxX = float(newrecord["maxX"])
                    if float(newrecord["maxY"]) > maxY:
                        maxY = float(newrecord["maxY"])

        # look for title and description in subgroups if not yet available
        if (record['title'] == "") or (record['detail'] == ""):
            subgroups = group.getElementsByTagName('g')
            for subgroup in subgroups:
                if record["detail"] == "":
                    record['detail'] = self.getText("desc", subgroup)
                if record["title"] == "":
                    record['title'] = self.getText("title", subgroup)

        record["minX"] = str(minX)
        record["minY"] = str(minY)
        record["maxX"] = str(maxX)
        record["maxY"] = str(maxY)

        if record["group"]:
            return record

    def generateJSON(self,filePath):
        """ generate json file"""
        final_str = u""
        final_str += u'var scene = {\n'
        for entry in self.scene:
            if entry == "image":
                final_str += u'"' + entry + u'":"' + self.scene[entry].replace("\n","").replace("\t","").replace("\r","") + u'",\n'
            else:
                final_str += u'"' + entry + u'":"' + PageFormatter(self.scene[entry]).print_html().replace('"', "'").replace("\n"," ").replace("\t"," ").replace("\r"," ") + u'",\n'
        final_str += u'};\n'

        final_str += u'var details = [\n'
        for detail in self.details:
            final_str += u'{\n'
            for entry in detail:
                if entry == "group":
                    final_str += u'  "' + entry + u'": [\n'
                    for element in detail['group']:
                        final_str += '  {\n'
                        for entry2 in element:
                            if entry2 == "path":
                                final_str += u'  "' + entry2 + u'":' + PageFormatter(element[entry2]).print_html().replace('"', "'").replace("\n"," ").replace("\t"," ").replace("\r"," ") + u',\n'
                            else:
                                final_str += u'      "' + entry2 + u'":"' + PageFormatter(element[entry2]).print_html().replace('"', "'").replace("\n"," ").replace("\t"," ").replace("\r"," ") + u'",\n'
                        final_str += u'  },\n'
                    final_str += u'  ],\n'
                elif entry == "path":
                    final_str += u'  "' + entry + u'":' + detail[entry] + ',\n'
                elif entry == "detail":
                    final_str += u'  "' + entry + u'":"' + PageFormatter(detail[entry]).print_html().replace('"', "'").replace("\n"," ").replace("\t"," ").replace("\r"," ") + u'",\n'
                else:
                    final_str += u'  "' + entry + u'":"' + detail[entry] + u'",\n'
            final_str += u'},\n'
        final_str += u'];\n'

        with open(filePath,"w") as jsonfile:
            jsonfile.write(final_str.encode('utf8'))
