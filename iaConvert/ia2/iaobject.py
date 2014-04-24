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
        """retrieves value of given XML node - used here for desc and title"""
        xml_str = node.toxml()
        start = xml_str.find('>')
        if start == -1:
            return ''
        end = xml_str.rfind('<')
        if end < start:
            return ''
        return xml_str[start + 1:end]

    def analyzeSVG(self,filePath):
        """analyze svg file and fill self.details and self.scene"""
        self.xml = minidom.parse(filePath)

        head, tail = os.path.split(filePath)
        self.scene['intro_title'] = u"Description"
        self.scene['intro_detail'] = u"Images Actives - Canopé Versailles"
        self.scene['image'] = ""
        self.scene['width'] = ""
        self.scene['height'] = ""
        self.scene['title'] = os.path.splitext(tail)[0]

        # ==================== Retrieve metadatas
        
        metadatas = self.xml.getElementsByTagName('metadata')
        if metadatas.item(0) is not None:
            metadata = metadatas.item(0).getElementsByTagName('dc:title')
            if metadata.item(0) is not None:
                if self.get_tag_value(metadata.item(0)) != "":
                    self.scene['title'] = self.get_tag_value(metadata.item(0))
            
            metacreator = metadatas.item(0).getElementsByTagName('dc:creator')
            if metacreator.item(0) is not None:
                creator = metacreator.item(0).getElementsByTagName('dc:title')
                if creator.item(0) is not None:
                    self.scene['creator'] = self.get_tag_value(creator.item(0))
            
            metadata = metadatas.item(0).getElementsByTagName('dc:description')
            if metadata.item(0) is not None:
                self.scene['description'] = self.get_tag_value(metadata.item(0))

        # ==================== Look for images

        images = self.xml.getElementsByTagName('image')
        if images.length is not 0:
            for image in images:
                    
                # first image is considered as background image
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
                if image.attributes['xlink:href'].value.find(u"file://") != -1:
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
                break
                
        mainSVG = self.xml.getElementsByTagName('svg')[0].childNodes
        for childnode in mainSVG:
            if childnode.parentNode.nodeName == "svg":
                if childnode.nodeName == "path":
                    self.analyzeRootPaths(childnode)
                if childnode.nodeName == "image":
                    self.analyzeRootImages(childnode)
                if childnode.nodeName == "rect":
                    self.analyzeRootRects(childnode)
                if childnode.nodeName == "g":
                    self.analyzeGroup(childnode)

    def analyzeRootImages(self, image):
        """Analyze images not included in a specific group"""
        
        if not image.isSameNode(self.backgroundNode):
            record_image = {}
            record_image['image'] = image.attributes['xlink:href'].value
            record_image['width'] = image.attributes['width'].value
            record_image['height'] = image.attributes['height'].value
            record_image['detail'] = self.getText("desc", image)
            record_image['title'] = self.getText("title", image)

            if image.hasAttribute("x") and image.hasAttribute("y"):
                record_image['x'] = image.attributes['x'].value
                record_image['y'] = image.attributes['y'].value
            else:
                record_image['x'] = str(0)
                record_image['y'] = str(0)                        

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

            self.details.append(record_image)               

    def analyzeRootRects(self, rect):
        """Analyze images not included in a specific group"""
        
        record_rect = {}
        record_rect['width'] = rect.attributes['width'].value
        record_rect['height'] = rect.attributes['height'].value
        record_rect['detail'] = self.getText("desc", rect)
        record_rect['title'] = self.getText("title", rect)

        if rect.hasAttribute("x") and rect.hasAttribute("y"):
            record_rect['x'] = rect.attributes['x'].value
            record_rect['y'] = rect.attributes['y'].value
        else:
            record_rect['x'] = str(0)
            record_rect['y'] = str(0)                        

        if rect.hasAttribute("rx") and rect.hasAttribute("ry"):
            record_rect['rx'] = rect.attributes['rx'].value
            record_rect['ry'] = rect.attributes['ry'].value
        else:
            record_rect['rx'] = str(0)
            record_rect['ry'] = str(0)                     

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
        self.details.append(record_rect)  

    def analyzeRootPaths(self,path):
        """Analyze paths not included in a specific group"""
        
        record = {}
        record["title"] = ""
        record["detail"] = ""
        record["path"] = ""
        record["fill"] = ""
        record["path"] =  path.attributes['d'].value.replace("&#xd;&#xa;"," ").replace("&#x9;"," ").replace("\n"," ").replace("\t"," ").replace("\r"," ") 
        record["style"] = ""

        if record["detail"] == "":
            record['detail'] = self.getText("desc", path)
        if record["title"] == "":
            record['title'] = self.getText("title", path)

        if path.hasAttribute("style") and (path.attributes['style'].value != ""):
            str_style = path.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key,value = item.split(":")
                style[key] = value
            record["fill"] = style['fill']

        if path.hasAttribute("x") and path.hasAttribute("y"):
            record['x'] = path.attributes['x'].value
            record['y'] = path.attributes['y'].value
        else:
            record['x'] = str(0)
            record['y'] = str(0)                        

        # ObjectToPath
        p = cubicsuperpath.parsePath(record['path'])
        record['path'] = cubicsuperpath.formatPath(p)

        if path.hasAttribute("transform"):
            transformation = path.attributes['transform'].value
            ctm = CurrentTransformation()
            ctm.analyze(transformation)

            ctm.applyTransformToPath(ctm.matrix,p)
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
        if (record["path"] != ""):
            self.details.append(record)

    def getText(self, type, element):
        """ type can be 'desc' or 'title' """
        text = element.getElementsByTagName(type)
        if text.item(0) is not None:
            if text.item(0).parentNode == element:
                #return self.get_tag_value(text.item(0)).replace("\n"," ").replace("\t"," ").replace("\r"," ")
                return self.get_tag_value(text.item(0))
        return ""

    def analyzeGroup(self,group):
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

        paths = group.getElementsByTagName('path')
        if paths.length is not 0:
            for path in paths:
                record_path = {}
                record_path['path'] = path.attributes['d'].value.replace("&#xd;&#xa;"," ").replace("&#x9;"," ").replace("\n"," ").replace("\t"," ").replace("\r"," ") 
                if record["detail"] == "":
                    record['detail'] = self.getText("desc", path)
                if record["title"] == "":
                    record['title'] = self.getText("title", path)
                if path.hasAttribute("style") and (path.attributes['style'].value != ""):                            
                    str_style = path.attributes['style'].value
                    style = {}
                    for item in str_style.split(";"):
                        key,value = item.split(":")
                        style[key] = value
                    record_path['fill'] = style['fill']
                if path.hasAttribute("x") and path.hasAttribute("y"):
                    record_path['x'] = path.attributes['x'].value
                    record_path['y'] = path.attributes['y'].value
                else:
                    record_path['x'] = str(0)
                    record_path['y'] = str(0)                        

                # ObjectToPath
                p = cubicsuperpath.parsePath(record_path['path'])
                record_path['path'] = cubicsuperpath.formatPath(p)

                if path.hasAttribute("transform"):
                    transformation = path.attributes['transform'].value
                    ctm = CurrentTransformation()
                    ctm.analyze(transformation)

                    ctm.applyTransformToPath(ctm.matrix,p)

                # apply group transformation on current object
                ctm_group.applyTransformToPath(ctm_group.matrix,p)
                record_path['path'] = cubicsuperpath.formatPath(p)

                localminX = 10000
                localminY = 10000
                localmaxX = -10000
                localmaxY = -10000
                for cmd, params in cubicsuperpath.unCubicSuperPath(p):
                    i = 0
                    for p in params:
                        if (i%2 == 0):
                            if float(p) < float(minX):
                                minX = float(p)
                            if float(p) > float(maxX):
                                maxX = float(p)
                            if float(p) < float(localminX):
                                localminX = float(p)
                            if float(p) > float(localmaxX):
                                localmaxX = float(p)

                        else:
                            if float(p) < float(minY):
                                minY = float(p)
                            if float(p) > float(maxY):
                                maxY = float(p)
                            if float(p) < float(localminY):
                                localminY = float(p)
                            if float(p) > float(localmaxY):
                                localmaxY = float(p)

                        i = i + 1
                record_path["minX"] = str(localminX)
                record_path["minY"] = str(localminY)
                record_path["maxX"] = str(localmaxX)
                record_path["maxY"] = str(localmaxY)

                record["minX"] = str(minX)
                record["minY"] = str(minY)
                record["maxX"] = str(maxX)
                record["maxY"] = str(maxY)                
                
                if record_path["path"].lower().find("z") == -1:
                    record_path["path"] += " z"
                record_path['path'] = '"' + record_path['path'] + '"'

                record["group"].append(record_path)

        images = group.getElementsByTagName('image')        
        if images.length is not 0:
            for image in images:
                if not image.isSameNode(self.backgroundNode):
                    record_image = {}
                    record_image["image"] = image.attributes['xlink:href'].value
                    record_image['width'] = image.attributes['width'].value
                    record_image['height'] = image.attributes['height'].value                
                    if record["detail"] == "":
                        record['detail'] = self.getText("desc", image)
                    if record["title"] == "":
                        record['title'] = self.getText("title", image)

                    if image.hasAttribute("x") and image.hasAttribute("y"):
                        record_image['x'] = image.attributes['x'].value
                        record_image['y'] = image.attributes['y'].value
                    else:
                        record_image['x'] = str(0)
                        record_image['y'] = str(0)                        

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

                    record["group"].append(record_image)        

        rects = group.getElementsByTagName('rect')        
        if rects.length is not 0:
            for rect in rects:

                record_rect = {}
                record_rect['width'] = rect.attributes['width'].value
                record_rect['height'] = rect.attributes['height'].value                
                if record["detail"] == "":
                    record['detail'] = self.getText("desc", rect)
                if record["title"] == "":
                    record['title'] = self.getText("title", rect)

                if rect.hasAttribute("x") and rect.hasAttribute("y"):
                    record_rect['x'] = rect.attributes['x'].value
                    record_rect['y'] = rect.attributes['y'].value
                else:
                    record_rect['x'] = str(0)
                    record_rect['y'] = str(0)                        

                if rect.hasAttribute("rx") and rect.hasAttribute("ry"):
                    record_rect['rx'] = rect.attributes['rx'].value
                    record_rect['ry'] = rect.attributes['ry'].value
                else:
                    record_rect['rx'] = str(0)
                    record_rect['ry'] = str(0)                     

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

                # apply group transformation on current object
                ctm_group.applyTransformToPath(ctm_group.matrix,p)
                record_rect['path'] = cubicsuperpath.formatPath(p)

                localminX = 10000
                localminY = 10000
                localmaxX = -10000
                localmaxY = -10000
                for cmd, params in cubicsuperpath.unCubicSuperPath(p):
                    i = 0
                    for p in params:
                        if (i%2 == 0):
                            if float(p) < float(minX):
                                minX = float(p)
                            if float(p) > float(maxX):
                                maxX = float(p)
                            if float(p) < float(localminX):
                                localminX = float(p)
                            if float(p) > float(localmaxX):
                                localmaxX = float(p)

                        else:
                            if float(p) < float(minY):
                                minY = float(p)
                            if float(p) > float(maxY):
                                maxY = float(p)
                            if float(p) < float(localminY):
                                localminY = float(p)
                            if float(p) > float(localmaxY):
                                localmaxY = float(p)

                        i = i + 1
                record_rect["minX"] = str(localminX)
                record_rect["minY"] = str(localminY)
                record_rect["maxX"] = str(localmaxX)
                record_rect["maxY"] = str(localmaxY)

                record["minX"] = str(minX)
                record["minY"] = str(minY)
                record["maxX"] = str(maxX)
                record["maxY"] = str(maxY)

                record_rect['path'] = "'" + record_rect['path'] + " z'"
                record["group"].append(record_rect)        

        # look for title and description in subgroups if not yet available
        if (record['title'] == "") and (record['detail'] == ""):
            subgroups = group.getElementsByTagName('g')
            for subgroup in subgroups:
                if record["detail"] == "":
                    record['detail'] = self.getText("desc", subgroup)
                if record["title"] == "":
                    record['title'] = self.getText("title", subgroup)

        if len(record["group"]):
            self.details.append(record)

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
                                final_str += u'  "' + entry2 + u'":' + element[entry2] + u',\n'                                
                            elif entry2 == "detail":
                                final_str += u'      "' + entry2 + u'":"' + PageFormatter(element[entry2]).print_html().replace('"', "'").replace("\n"," ").replace("\t"," ").replace("\r"," ") + u'",\n'
                            else:
                                final_str += u'      "' + entry2 + u'":"' + element[entry2] + u'",\n'                            
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
