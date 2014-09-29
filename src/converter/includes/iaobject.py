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

import math
import re
import tempfile
import sys
import shutil
import commands

# import PIL for windows and Linux
# For MAC OS X, use internal tool called "sips"

if not sys.platform.startswith('darwin'):
    try:
        from PIL import Image
    except ImportError:
        print "Requirement : Please, install python-pil package"
        sys.exit(1)



class iaObject:
    """generate Image Active Object"""

    def __init__(self):
        """Init"""
        self.details = []
        self.scene = {}
        self.raster = ""
        
        # used to identify if background image must be resized for mobiles
        self.ratio = 1

        self.translation = 0
        
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
                    self.scene['creator'] = self.get_tag_value(\
                      metadata_value.item(0))

            self.scene['rights'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:rights')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['rights'] = self.get_tag_value(\
                      metadata_value.item(0))

            self.scene['publisher'] = ""
            metadata = metadatas.item(0).getElementsByTagName('dc:publisher')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['publisher'] = self.get_tag_value(\
                      metadata_value.item(0))

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
                    self.scene['contributor'] = self.get_tag_value(\
                      metadata_value.item(0))


    def analyzeSVG(self,filePath, maxNumPixels):
        """analyze svg file and fill self.details and self.scene"""
        self.details = []
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
            self.backgroundX = 0
            self.backgroundY = 0
            if image.hasAttribute('x'):
                self.backgroundX = float(image.attributes['x'].value)
            if image.hasAttribute('y'):
                self.backgroundY =  float(image.attributes['y'].value)
            
            if (self.backgroundX != 0) or (self.backgroundY != 0):
                ctm = CurrentTransformation()
                ctm.extractTranslate([self.backgroundX * (-1), self.backgroundY * (-1)])
                self.translation = ctm.matrix

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
                fileNameImage, fileExtensionImage = os.path.splitext(\
                    image.attributes['xlink:href'].value[7:])
                imgMimeTypes = {}
                imgMimeTypes['.png'] = 'image/png'
                imgMimeTypes['.jpg'] = 'image/jpeg'
                imgMimeTypes['.jpeg'] = 'image/jpeg'
                imgMimeTypes['.gif'] = 'image/gif'
                imgMimeTypes['.bmp'] = 'image/bmp'
                self.rasterPrefix = u"data:" + \
                    imgMimeTypes[fileExtensionImage.lower()] + u";base64,"
                with open(image.attributes['xlink:href'].value[7:], 'rb') as \
                  bgImage:
                    self.raster = self.rasterPrefix + \
                        bgImage.read().encode("base64", "strict")
            self.scene['image'] = self.raster

            # calculate ratio to resize background image down to maxNumPixels
            
            bgNumPixels = float(int(float(self.scene['width'])) * \
                int(float(self.scene['height'])))
            if (bgNumPixels > maxNumPixels):
                self.ratio = math.sqrt(maxNumPixels / bgNumPixels)
         
            if self.ratio != 1:
                self.scene['image'], self.scene['width'], self.scene['height'] = \
                  self.resizeImage(self.scene['image'], \
                    self.scene['width'], \
                    self.scene['height'])

        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', \
            'polygon', 'path', 'image', 'g']
        mainSVG = self.xml.getElementsByTagName('svg')
        if mainSVG[0]:
            for childnode in mainSVG[0].childNodes:
                if childnode.parentNode.nodeName == "svg":
                    if childnode.nodeName in svgElements:
                        newrecord = getattr(self, 'extract_' + \
                            childnode.nodeName)(childnode, 0)
                        if newrecord is not None:
                            self.details.append(newrecord)

    def extract_circle(self, image, ctm_group):
        """not yet implemented"""
        print("circle is not implemented")

    def extract_ellipse(self, image, ctm_group):
        """not yet implemented"""
        print("ellipse is not implemented")

    def extract_line(self, image, ctm_group):
        """not yet implemented"""
        print("line is not implemented")

    def extract_polyline(self, image, ctm_group):
        """not yet implemented"""
        print("polyline is not implemented")

    def extract_polygon(self, image, ctm_group):
        """not yet implemented"""
        print("polygon is not implemented")
        
    def extract_image(self, image, ctm_group):
        """Analyze images"""
        
        if not image.isSameNode(self.backgroundNode):
            record_image = {}
            if image.hasAttribute('id'):
                record_image['id'] = image.attributes['id'].value
            record_image['image'] = image.attributes['xlink:href'].value
            record_image['width'] = image.attributes['width'].value
            record_image['height'] = image.attributes['height'].value
            record_image['detail'] = self.getText("desc", image)
            record_image['title'] = self.getText("title", image)
            record_image['x'] = str(0)
            record_image['y'] = str(0)                        
            record_image['options'] = ""
            
            if image.hasAttribute("x"):
                record_image['x'] = str((float(image.attributes['x'].value) - \
                  self.backgroundX) * self.ratio)
            if image.hasAttribute("y"):
                record_image['y'] = str((float(image.attributes['y'].value) - \
                  self.backgroundY) * self.ratio)
            
            if self.ratio != 1:
                record_image['image'], \
                record_image['width'], \
                record_image['height'] = \
                    self.resizeImage(record_image['image'], \
                      record_image['width'], \
                      record_image['height'])

            if record_image['title'].startswith("http://") or \
              record_image['title'].startswith("https://") or \
              record_image['title'].startswith("//") or \
              record_image['title'].startswith("./") or \
              record_image['title'].startswith("../"):
                record_image['options'] += " direct-link "

            if image.hasAttribute("style"):                            
                str_style = image.attributes['style'].value
                style = {}
                for item in str_style.split(";"):
                    key,value = item.split(":")
                    style[key] = value
                record_image['fill'] = style['fill']

            if image.hasAttribute("onclick"):                            
                str_onclick = image.attributes['onclick'].value
                if str_onclick == "off":
                    record_image['options'] += " disable-click "
                else:
                    record_image['options'] += " " + str_onclick + " "

            if image.hasAttribute("onmouseover"):                            
                str_onmouseover = image.attributes['onmouseover'].value
                record_image['options'] += " " + str_onmouseover + " "
                        
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
            if (float(record_image['x']) + \
              float(record_image['width'])) > float(maxX):
                maxX = float(record_image['x']) + float(record_image['width'])
            if float(record_image['y']) < float(minY):
                minY = float(record_image['y'])
            if (float(record_image['y']) + \
              float(record_image['height'])) > float(maxY):
                maxY = float(record_image['y']) + float(record_image['height'])

            record_image["minX"] = str(minX)
            record_image["minY"] = str(minY)
            record_image["maxX"] = str(maxX)
            record_image["maxY"] = str(maxY) 

            return record_image

    def extract_rect(self, rect, ctm_group):
        """Analyze rectangles"""
        
        record_rect = {}
        if rect.hasAttribute("id"):
            record_rect['id'] = rect.attributes['id'].value
        record_rect['width'] = rect.attributes['width'].value
        record_rect['height'] = rect.attributes['height'].value
        record_rect['detail'] = self.getText("desc", rect)
        record_rect['title'] = self.getText("title", rect)
        record_rect['x'] = str(0)
        record_rect['y'] = str(0)
        record_rect['rx'] = str(0)
        record_rect['ry'] = str(0)
        record_rect['options'] = ""

        if rect.hasAttribute("x"):
            record_rect['x'] = rect.attributes['x'].value
            if self.translation != 0:
                record_rect['x'] = float(record_rect['x'])
        if rect.hasAttribute("y"):
            record_rect['y'] = rect.attributes['y'].value
            if self.translation != 0:
                record_rect['y'] = float(record_rect['y'])
        if rect.hasAttribute("rx"):
            record_rect['rx'] = rect.attributes['rx'].value
        if rect.hasAttribute("ry"):
            record_rect['ry'] = rect.attributes['ry'].value

        if rect.hasAttribute("onclick"):                            
            str_onclick = rect.attributes['onclick'].value
            if str_onclick == "off":
                record_rect['options'] += " disable-click "
            else:
                record_image['options'] += " " + str_onclick + " "
        if rect.hasAttribute("onmouseover"):                            
            str_onmouseover = rect.attributes['onmouseover'].value
            record_rect['options'] += " " + str_onmouseover + " "

        if record_rect['title'].startswith("http://") or \
          record_rect['title'].startswith("https://") or \
          record_rect['title'].startswith("//") or \
          record_rect['title'].startswith("./") or \
          record_rect['title'].startswith("../"):
            record_rect['options'] += " direct-link "

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

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation,p)
            record_rect['path'] = cubicsuperpath.formatPath(p) 

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
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
        return record_rect

    def extract_path(self,path, ctm_group):
        """Analyze paths"""
        
        record = {}
        record["path"] = ""
        record["fill"] = ""
        if path.hasAttribute("id"):
            record["id"] =  path.attributes['id'].value
        record["path"] =  path.attributes['d'].value. \
            replace("&#xd;&#xa;"," "). \
            replace("&#x9;"," "). \
            replace("\n"," "). \
            replace("\t"," "). \
            replace("\r"," ") 
        record["style"] = ""
        record['detail'] = self.getText("desc", path)
        record['title'] = self.getText("title", path)
        record['x'] = str(0)
        record['y'] = str(0)
        record['options'] = ""

        if path.hasAttribute("onclick"):                            
            str_onclick = path.attributes['onclick'].value
            if str_onclick == "off":
                record['options'] += " disable-click "
            else:
                record['options'] += " " + str_onclick + " "

        if path.hasAttribute("onmouseover"):                            
            str_onmouseover = path.attributes['onmouseover'].value
            record['options'] += " " + str_onmouseover + " "
                
        if record['title'].startswith("http://") or \
          record['title'].startswith("https://") or \
          record['title'].startswith("//") or \
          record['title'].startswith("./") or \
          record['title'].startswith("../"):
            record['options'] += " direct-link "
        
        if path.hasAttribute("style") and (path.attributes['style'].value != ""):
            str_style = path.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key,value = item.split(":")
                style[key] = value
            if 'fill' in style:
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

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation,p)
            record['path'] = cubicsuperpath.formatPath(p)  
            
        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
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
        if record["path"]:
            return record

    def getText(self, type, element):
        """ type can be 'desc' or 'title' """
        text = element.getElementsByTagName(type)
        if text.item(0) is not None:
            if text.item(0).parentNode == element:
                return self.get_tag_value(text.item(0))
        return ""

    def print_node(self,root, childs):
        if root.childNodes:
            for node in root.childNodes:
               if node.nodeType == node.ELEMENT_NODE:
                   #print node.tagName,"has value:",  node.nodeValue, "and is child of:", node.parentNode.tagName
                   childs.append(node)
                   self.print_node(node, childs)


    def extract_g(self,group, ctm_group):
        """Analyze a svg group"""

        record = {}
        if group.hasAttribute("id"):
            record["id"] =  group.attributes['id'].value
        record['title'] = self.getText("title", group)
        record['detail'] = self.getText("desc", group)
        record["group"] = []
        record["options"] = ""
        
        minX = 10000
        minY = 10000
        maxX = 0
        maxY = 0
        # retrieve transformations applied on master group
        # TODO : manage nested groups tranformations
       
        if group.hasAttribute("onclick"):                            
            str_onclick = group.attributes['onclick'].value
            if str_onclick == "off":
                record['options'] += " disable-click "
            else:
                record_image['options'] += " " + str_onclick + " "
        
        
        ctm_group = CurrentTransformation()
        if group.hasAttribute("transform"):
            transformation = group.attributes['transform'].value
            ctm_group.analyze(transformation)

        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', \
            'polygon', 'path', 'image']
        group_childs = []
        self.print_node(group, group_childs)
        for childnode in group_childs:
            if childnode.nodeName in svgElements:
                newrecord = getattr(self, 'extract_' + \
                    childnode.nodeName)(childnode, ctm_group)
                if newrecord is not None:
                    #newrecord["options"] += record["options"]
                    #record["options"] =  newrecord["options"]
                    record["group"].append(newrecord)
                    
                    if record["detail"] == "":
                        record['detail'] = newrecord['detail']
                    if record["title"] == "":
                        record['title'] = newrecord['title']
                        
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

        if record['title'] == "":
            if group.hasAttribute("inkscape:label"):
                record['title'] = group.attributes["inkscape:label"].value
                
        record["minX"] = str(minX)
        record["minY"] = str(minY)
        record["maxX"] = str(maxX)
        record["maxY"] = str(maxY)

        if record["group"]:
            return record

    def resizeImage(self, raster, rasterWidth, rasterHeight):
        """ 
        if needed, we must resize background image to be usable
        on tablets and mobiles. iPad limitation is approximatly 5Mb.
        """
        
        dirname = tempfile.mkdtemp()
        newraster = raster
        newrasterWidth = rasterWidth
        newrasterHeight = rasterHeight
        rasterStartPosition = raster.find('base64,') + 7
        rasterEncoded = raster[rasterStartPosition:]
        rasterPrefix = raster[0:rasterStartPosition]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                imageFile = dirname + os.path.sep + "image." + extension.group(1)
                imageFileSmall = dirname + \
                  os.path.sep + "image_small." + extension.group(1)
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(rasterEncoded.decode("base64"))
                if self.ratio != 1:
                    # Background image is too big to be used on mobiles
                    if sys.platform.startswith('darwin'):
                        #print "Platform MAC OS X : resizing using sips"
                        oldwidth = int(float(rasterWidth))
                        oldheight = int(float(rasterHeight))
                        newwidth = int( oldwidth * self.ratio)
                        newheight = int( oldheight * self.ratio)
                        shutil.copyfile(imageFile, imageFileSmall)
                        commands.getstatusoutput('sips -z {0} {1} {2}' . \
                          format(newheight, newwidth, imageFileSmall))                    

                        with open(imageFileSmall, 'rb') as bgSmallImage:
                            rasterSmallEncoded = bgSmallImage.read().\
                              encode("base64")
                            newraster = rasterPrefix + \
                              rasterSmallEncoded

                        newrasterWidth = newwidth.__str__()
                        newrasterHeight = newheight.__str__()                    


                    else:
                        # "Platform Linux or Windows : resizing using PIL"
                        currentBg = Image.open(imageFile)
                        oldwidth = int(float(rasterWidth))
                        oldheight = int(float(rasterHeight))
                        newwidth = int( oldwidth * self.ratio)
                        newheight = int( oldheight * self.ratio)
                        resizedBg = currentBg.resize( \
                            (newwidth,newheight), \
                            Image.ANTIALIAS)
                        resizedBg.save(imageFileSmall) 

                        with open(imageFileSmall, 'rb') as bgSmallImage:
                            rasterSmallEncoded = bgSmallImage.read().\
                              encode("base64")
                            newraster = rasterPrefix + \
                              rasterSmallEncoded

                        newrasterWidth = newwidth.__str__()
                        newrasterHeight = newheight.__str__()
        else:
            print('ERROR : image is not embedded')
        shutil.rmtree(dirname)
        return [newraster, newrasterWidth, newrasterHeight]


    def generateJSON(self,filePath):
        """ generate json file"""
        final_str = u""
        final_str += u'var scene = {\n'
        for entry in self.scene:
            if entry == "image":
                final_str += u'"' + entry + u'":"' + \
                    self.scene[entry]. \
                        replace("\n",""). \
                        replace("\t",""). \
                        replace("\r","") + u'",\n'
            else:
                final_str += u'"' + entry + u'":"' + \
                    PageFormatter(self.scene[entry]).print_html(). \
                        replace('"', "'"). \
                        replace("\n"," "). \
                        replace("\t"," "). \
                        replace("\r"," ") + u'",\n'
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
                                final_str += u'  "' + entry2 + u'":' + \
                                    element[entry2].\
                                        replace('"', "'").\
                                        replace("\n"," ").\
                                        replace("\t"," ").\
                                        replace("\r"," ") + u',\n'
                            elif entry2 == "image"  or entry2 == "title":
                                final_str += u'  "' + entry2 + u'":"' + \
                                    element[entry2].\
                                        replace('"', "'").\
                                        replace("\n"," ").\
                                        replace("\t"," ").\
                                        replace("\r"," ") + u'",\n'
                            else:
                                final_str += u'      "' + entry2 + u'":"' + \
                                    PageFormatter(element[entry2]).print_html().\
                                        replace('"', "'").\
                                        replace("\n"," ").\
                                        replace("\t"," ").\
                                        replace("\r"," ") + u'",\n'
                        final_str += u'  },\n'
                    final_str += u'  ],\n'
                elif entry == "path":
                    final_str += u'  "' + entry + u'":' + detail[entry] + ',\n'
                elif entry == "image":
                    final_str += u'  "' + entry + u'":"' + detail[entry] .\
                                        replace('"', "'").\
                                        replace("\n"," ").\
                                        replace("\t"," ").\
                                        replace("\r"," ") + u'",\n'
                elif entry == "detail":
                    final_str += u'  "' + entry + u'":"' + \
                        PageFormatter(detail[entry]).print_html().\
                            replace('"', "'").\
                            replace("\n"," ").\
                            replace("\t"," ").\
                            replace("\r"," ") + u'",\n'
                else:
                    final_str += u'  "' + entry + u'":"' + detail[entry] + u'",\n'
            final_str += u'},\n'
        final_str += u'];\n'
        #final_str += u'lazyload("/js/iascene.js");'

        with open(filePath,"w") as jsonfile:
            jsonfile.write(final_str.encode('utf8'))
