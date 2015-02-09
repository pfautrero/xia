#!/usr/bin/python
# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
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



import os
import math
import re
import tempfile
import sys
import shutil
import commands

# import PIL for windows and Linux
# For MAC OS X, use internal tool called "sips"
try:
    from PIL import Image
    HANDLE_PIL = True
except ImportError:
    if not sys.platform.startswith('darwin'):
        print "Requirement : Please, install python-pil package"
        sys.exit(1)
    else:
        HANDLE_PIL = False

import hashlib
import uuid
from xml.dom import minidom

from ctm import CurrentTransformation
import cubicsuperpath
from pikipiki import PageFormatter


class iaObject:
    """generate Image Active Object"""

    def __init__(self, console):
        """Init"""
        self.details = []
        self.scene = {}
        self.console = console

        # used to identify if background image must be resized for mobiles
        self.ratio = 1

        self.translation = 0
        self.jsonContent = ""
        self.filePath = ""

    def get_tag_value(self, node):
        if node.childNodes:
            return node.childNodes[0].nodeValue
        else:
            return ""

    def extractMetadatas(self, xml):

        metadatas = xml.getElementsByTagName('metadata')
        self.scene['date'] = ""
        self.scene['identifier'] = ""
        self.scene['coverage'] = ""
        self.scene['source'] = ""
        self.scene['relation'] = ""
        self.scene['creator'] = ""
        self.scene['rights'] = ""
        self.scene['publisher'] = ""
        self.scene['language'] = ""
        self.scene['keywords'] = ""
        self.scene['description'] = ""
        self.scene['contributor'] = ""
        if metadatas.item(0) is not None:

            metadata = metadatas.item(0).getElementsByTagName('dc:title')
            if metadata.item(0) is not None:
                if self.get_tag_value(metadata.item(0)) != "":
                    self.scene['title'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:date')
            if metadata.item(0) is not None:
                self.scene['date'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:coverage')
            if metadata.item(0) is not None:
                self.scene['coverage'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:relation')
            if metadata.item(0) is not None:
                self.scene['relation'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:source')
            if metadata.item(0) is not None:
                self.scene['source'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:identifier')
            if metadata.item(0) is not None:
                self.scene['identifier'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:creator')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['creator'] = self.get_tag_value(metadata_value.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:rights')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['rights'] = self.get_tag_value(metadata_value.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:publisher')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['publisher'] = self.get_tag_value(metadata_value.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:language')
            if metadata.item(0) is not None:
                self.scene['language'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:subject')
            if metadata.item(0) is not None:
                items = metadata.item(0).getElementsByTagName('rdf:li')
                for key_word in items:
                    if self.scene['keywords']:
                        self.scene['keywords'] += ","
                    self.scene['keywords'] += self.get_tag_value(key_word)

            metadata = metadatas.item(0).getElementsByTagName('dc:description')
            if metadata.item(0) is not None:
                self.scene['description'] = self.get_tag_value(metadata.item(0))

            metadata = metadatas.item(0).getElementsByTagName('dc:contributor')
            if metadata.item(0) is not None:
                metadata_value = metadata.item(0).getElementsByTagName('dc:title')
                if metadata_value.item(0) is not None:
                    self.scene['contributor'] = self.get_tag_value(metadata_value.item(0))

    def extractRaster(self, xlink):
        """ extract raster from xlink:href attribute """
        raster = xlink
        if not xlink.startswith("data:"):
            strStarter = 0
            if xlink.startswith("file://"):
                strStarter = len("file://")
            # look for windows drive letter
            if re.match("^[a-zA-Z]:.*$", xlink[strStarter + 1], re.UNICODE):
                strStarter = strStarter + 1
            # Embed image thanks to data URI Scheme
            imgName, imgExtension = os.path.splitext(xlink[strStarter:])
            imgMimeTypes = {}
            imgMimeTypes['.png'] = 'image/png'
            imgMimeTypes['.jpg'] = 'image/jpeg'
            imgMimeTypes['.jpeg'] = 'image/jpeg'
            imgMimeTypes['.gif'] = 'image/gif'
            imgMimeTypes['.bmp'] = 'image/bmp'
            rasterPref = u"data:" + \
                         imgMimeTypes[imgExtension.lower()] + u";base64,"
            if os.path.exists(xlink[strStarter:]):
                imgFile = xlink[strStarter:]
            else:
                localDir = os.path.dirname(self.filePath)
                imgFile = localDir + "/" + xlink[strStarter:]
            if os.path.exists(imgFile):
                with open(imgFile, 'rb') as img:
                    raster = rasterPref + img.read().encode("base64", "strict")
        return raster

    def analyzeSVG(self, filePath, maxNumPixels):
        """analyze svg file and fill self.details and self.scene"""
        self.details = []
        self.scene.clear()
        self.translation = 0
        self.ratio = 1

        # workaround to be able to read svg files 
        # generated with images actives 1
        # (xlink namespace is not available and must be added)

        with open(filePath, 'r') as svgfile:
            svgcontent = svgfile.read()
            if not re.search(r'xmlns:xlink=', svgcontent, re.M):
                svgcontent = svgcontent.replace("<svg", '<svg\nxmlns:xlink="http://www.w3.org/1999/xlink"')
                dirname = os.path.dirname(filePath)
                basename = os.path.basename(filePath)
                fixedfile = dirname + "/fixed_" + basename
                with open(fixedfile, 'w') as tempsvgfile:
                    tempsvgfile.write(svgcontent)
                filePath = fixedfile

        self.filePath = filePath

        self.xml = minidom.parse(filePath)

        head, tail = os.path.split(filePath)
        self.scene['intro_title'] = u"Description"
        self.scene['intro_detail'] = u"XIA - DANE Versailles"
        self.scene['image'] = ""
        self.scene['width'] = ""
        self.scene['height'] = ""
        self.scene['title'] = os.path.splitext(tail)[0]

        self.extractMetadatas(self.xml)

        # ==================== Look for background image

        images = self.xml.getElementsByTagName('image')
        if images.item(0) is not None:
            image = images.item(0)
            self.backgroundNode = image
            self.scene['width'] = image.attributes['width'].value
            self.scene['height'] = image.attributes['height'].value
            self.backgroundX = 0
            self.backgroundY = 0
            if image.hasAttribute('x'):
                self.backgroundX = float(image.attributes['x'].value)
            if image.hasAttribute('y'):
                self.backgroundY = float(image.attributes['y'].value)

            #print self.backgroundX
            #print self.backgroundY
            if (self.backgroundX != 0) or (self.backgroundY != 0):
                ctm = CurrentTransformation()
                ctm.extractTranslate([self.backgroundX * (-1), self.backgroundY * (-1)])
                self.translation = ctm.matrix

            #print self.translation

            desc = image.getElementsByTagName('desc')
            if desc.item(0) is None and image.parentNode.parentNode is not None:
                big_group = image.parentNode.parentNode
                #libreoffice svg export
                if big_group.nodeName == 'g':
                    if big_group.hasAttribute("class"):
                        if big_group.attributes["class"].value == "Graphic":
                            desc = big_group.getElementsByTagName('desc')
            if desc.item(0) is not None:
                #if desc.item(0).parentNode == image:
                self.scene['intro_detail'] = self.get_tag_value(desc.item(0))

            title = image.getElementsByTagName('title')
            if title.item(0) is None and image.parentNode.parentNode is not None:
                big_group = image.parentNode.parentNode
                #libreoffice svg export
                if big_group.nodeName == 'g':
                    if big_group.hasAttribute("class"):
                        if big_group.attributes["class"].value == "Graphic":
                            title = big_group.getElementsByTagName('title')
            if title.item(0) is not None:
                #if title.item(0).parentNode == image:
                self.scene['intro_title'] = self.get_tag_value(title.item(0))

            raster = self.extractRaster(image.attributes['xlink:href'].value)

            if image.hasAttribute("transform"):
                transformation = image.attributes['transform'].value
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                #print str(ctm.scaleX) + " " + str(ctm.scaleY)
                if ctm.scaleX != 1 or ctm.scaleY != 1:
                    self.scene['image'], self.scene['width'], self.scene['height'] = self.resizeImage(
                        raster,
                        int(float(self.scene['width'])) * ctm.scaleX,
                        int(float(self.scene['height'])) * ctm.scaleY)

            fixedRaster = self.fixRaster(raster, self.scene['width'], self.scene['height'])
            self.scene['image'] = fixedRaster

            # calculate ratio to resize background image down to maxNumPixels

            bgNumPixels = float(int(float(self.scene['width'])) * int(float(self.scene['height'])))
            if bgNumPixels > maxNumPixels:
                self.ratio = math.sqrt(maxNumPixels / bgNumPixels)

            if self.ratio != 1:
                self.scene['image'], self.scene['width'], self.scene['height'] = self.resizeImage(self.scene['image'],
                                                                                                  self.scene['width'],
                                                                                                  self.scene['height'])

        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image', 'g']
        mainSVG = self.xml.getElementsByTagName('svg')
        if mainSVG[0]:
            # if there is only one root group
            # just remove it
            nb_root_groups = 0
            nb_root_elements = 0
            last_group = None
            for childnode in mainSVG[0].childNodes:
                if childnode.nodeName == "g":
                    nb_root_groups += 1
                    nb_root_elements += 1
                    last_group = childnode
                elif childnode.nodeName in svgElements:
                    nb_root_elements += 1

            if (nb_root_groups == 1) and (nb_root_elements == 1):
                mainSVG[0] = last_group
            else:
                # look for libreoffice draw svg export
                if last_group is not None:
                    if last_group.hasAttribute("class"):
                        if last_group.attributes["class"].value == "SlideGroup":
                            group_childs = []
                            self.print_node(last_group, group_childs)
                            for childnode in group_childs:
                                if childnode.hasAttribute("class"):
                                    if childnode.attributes["class"].value == "Page":
                                        mainSVG[0] = childnode
                                        break

            for childnode in mainSVG[0].childNodes:
                if childnode.parentNode.nodeName == mainSVG[0].nodeName:
                    if childnode.nodeName in svgElements:
                        newrecord = getattr(self, 'extract_' + childnode.nodeName)(childnode, "")
                        if newrecord is not None:
                            self.details.append(newrecord)

    def extract_circle(self, circle, stackTransformations):
        """Analyze circle"""
        record_circle = {}
        record_circle['id'] = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if circle.hasAttribute("id"):
            record_circle['id'] = circle.attributes['id'].value

        record_circle['detail'] = self.getText("desc", circle)
        record_circle['title'] = self.getText("title", circle)
        record_circle['cx'] = unicode(0)
        record_circle['cy'] = unicode(0)
        record_circle['r'] = unicode(0)
        record_circle['options'] = ""

        if circle.hasAttribute("cx"):
            record_circle['cx'] = circle.attributes['cx'].value
            if self.translation != 0:
                record_circle['cx'] = float(record_circle['cx'])
        if circle.hasAttribute("cy"):
            record_circle['cy'] = circle.attributes['cy'].value
            if self.translation != 0:
                record_circle['cy'] = float(record_circle['cy'])
        if circle.hasAttribute("r"):
            record_circle['r'] = circle.attributes['r'].value

        if circle.hasAttribute("onclick"):
            str_onclick = circle.attributes['onclick'].value
            if str_onclick == "off":
                record_circle['options'] += " disable-click "
            else:
                record_circle['options'] += " " + str_onclick + " "
        if circle.hasAttribute("onmouseover"):
            str_onmouseover = circle.attributes['onmouseover'].value
            record_circle['options'] += " " + str_onmouseover + " "

        if record_circle['title'].startswith("http://") or \
                record_circle['title'].startswith("https://") or \
                record_circle['title'].startswith("//") or \
                record_circle['title'].startswith("./") or \
                record_circle['title'].startswith("../"):
            record_circle['options'] += " direct-link "

        if circle.hasAttribute("images_actives:zoomable"):
            str_zoom = circle.attributes['images_actives:zoomable'].value
            if str_zoom == "false":
                record_circle['fill'] = "#000000"


        if circle.hasAttribute("style"):
            str_style = circle.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key, value = item.split(":")
                style[key] = value
            if 'fill' in style:
                record_circle['fill'] = style['fill']
            if 'stroke' in style:
                record_circle['stroke'] = style['stroke']
            if 'stroke-width' in style:
                record_circle['strokewidth'] = style['stroke-width']

        # ObjectToPath
        ctm = CurrentTransformation()
        record_circle['path'] = ctm.circleToPath(record_circle)

        p = cubicsuperpath.parsePath(record_circle['path'])
        record_circle['path'] = cubicsuperpath.formatPath(p)
        record_circle['x'] = unicode(0)
        record_circle['y'] = unicode(0)
        if stackTransformations == "":
            if circle.hasAttribute("transform"):
                transformation = circle.attributes['transform'].value
                ctm.analyze(transformation)

                ctm.applyTransformToPath(ctm.matrix, p)
                record_circle['path'] = cubicsuperpath.formatPath(p)

        # apply group transformation on current object
        else:
            transformations = stackTransformations.split("#")
            for transformation in transformations[::-1]:
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                ctm.applyTransformToPath(ctm.matrix, p)
                record_circle['path'] = cubicsuperpath.formatPath(p)

                #if ctm_group:
        #    ctm_group.applyTransformToPath(ctm_group.matrix,p)
        #    record_circle['path'] = cubicsuperpath.formatPath(p)

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record_circle['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
            record_circle['path'] = cubicsuperpath.formatPath(p)

        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i % 2 == 0):
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
        record_circle["minX"] = unicode(minX)
        record_circle["minY"] = unicode(minY)
        record_circle["maxX"] = unicode(maxX)
        record_circle["maxY"] = unicode(maxY)

        record_circle['path'] = '"' + record_circle['path'] + ' z"'
        return record_circle

    def extract_ellipse(self, ellipse, stackTransformations):
        """Analyze ellipse"""

        record_ellipse = {}
        record_ellipse['id'] = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if ellipse.hasAttribute("id"):
            record_ellipse['id'] = ellipse.attributes['id'].value

        record_ellipse['detail'] = self.getText("desc", ellipse)
        record_ellipse['title'] = self.getText("title", ellipse)
        record_ellipse['cx'] = unicode(0)
        record_ellipse['cy'] = unicode(0)
        record_ellipse['rx'] = unicode(0)
        record_ellipse['ry'] = unicode(0)
        record_ellipse['options'] = ""

        if ellipse.hasAttribute("cx"):
            record_ellipse['cx'] = ellipse.attributes['cx'].value
            if self.translation != 0:
                record_ellipse['cx'] = float(record_ellipse['cx'])
        if ellipse.hasAttribute("cy"):
            record_ellipse['cy'] = ellipse.attributes['cy'].value
            if self.translation != 0:
                record_ellipse['cy'] = float(record_ellipse['cy'])
        if ellipse.hasAttribute("rx"):
            record_ellipse['rx'] = ellipse.attributes['rx'].value
        if ellipse.hasAttribute("ry"):
            record_ellipse['ry'] = ellipse.attributes['ry'].value

        if ellipse.hasAttribute("onclick"):
            str_onclick = ellipse.attributes['onclick'].value
            if str_onclick == "off":
                record_ellipse['options'] += " disable-click "
            else:
                record_ellipse['options'] += " " + str_onclick + " "
        if ellipse.hasAttribute("onmouseover"):
            str_onmouseover = ellipse.attributes['onmouseover'].value
            record_ellipse['options'] += " " + str_onmouseover + " "

        if record_ellipse['title'].startswith("http://") or \
                record_ellipse['title'].startswith("https://") or \
                record_ellipse['title'].startswith("//") or \
                record_ellipse['title'].startswith("./") or \
                record_ellipse['title'].startswith("../"):
            record_ellipse['options'] += " direct-link "

        if ellipse.hasAttribute("images_actives:zoomable"):
            str_zoom = ellipse.attributes['images_actives:zoomable'].value
            if str_zoom == "false":
                record_ellipse['fill'] = "#000000"

        if ellipse.hasAttribute("style"):
            str_style = ellipse.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key, value = item.split(":")
                style[key] = value
            if 'fill' in style:
                record_ellipse['fill'] = style['fill']
            if 'stroke' in style:
                record_ellipse['stroke'] = style['stroke']
            if 'stroke-width' in style:
                record_ellipse['strokewidth'] = style['stroke-width']

        # ObjectToPath
        ctm = CurrentTransformation()
        record_ellipse['path'] = ctm.ellipseToPath(record_ellipse)

        p = cubicsuperpath.parsePath(record_ellipse['path'])
        record_ellipse['path'] = cubicsuperpath.formatPath(p)
        record_ellipse['x'] = unicode(0)
        record_ellipse['y'] = unicode(0)
        if stackTransformations == "":
            if ellipse.hasAttribute("transform"):
                transformation = ellipse.attributes['transform'].value
                ctm.analyze(transformation)

                ctm.applyTransformToPath(ctm.matrix, p)
                record_ellipse['path'] = cubicsuperpath.formatPath(p)

        # apply group transformation on current object
        else:
            transformations = stackTransformations.split("#")
            for transformation in transformations[::-1]:
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                ctm.applyTransformToPath(ctm.matrix, p)
                record_ellipse['path'] = cubicsuperpath.formatPath(p)

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record_ellipse['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
            record_ellipse['path'] = cubicsuperpath.formatPath(p)

        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i % 2 == 0):
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
        record_ellipse["minX"] = unicode(minX)
        record_ellipse["minY"] = unicode(minY)
        record_ellipse["maxX"] = unicode(maxX)
        record_ellipse["maxY"] = unicode(maxY)

        record_ellipse['path'] = '"' + record_ellipse['path'] + ' z"'
        return record_ellipse

    def extract_line(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("line is not implemented. Convert it to path.")

    def extract_polyline(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("polyline is not implemented. Convert it to path.")

    def extract_polygon(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("polygon is not implemented. Convert it to path.")

    def extract_image(self, image, stackTransformations):
        """Analyze images"""

        if not image.isSameNode(self.backgroundNode):
            record_image = {}
            record_image['id'] = hashlib.md5(str(uuid.uuid1())).hexdigest()
            if image.hasAttribute('id'):
                record_image['id'] = image.attributes['id'].value
            record_image['width'] = image.attributes['width'].value
            record_image['height'] = image.attributes['height'].value
            raster = self.extractRaster(image.attributes['xlink:href'].value)
            #fixedRaster = self.fixRaster(raster, record_image["width"], record_image['height'])
            record_image['image'] = raster
            record_image['detail'] = self.getText("desc", image)
            record_image['title'] = self.getText("title", image)
            record_image['x'] = unicode(0)
            record_image['y'] = unicode(0)
            record_image['options'] = ""

            if image.hasAttribute("x"):
                record_image['x'] = unicode((float(image.attributes['x'].value) - self.backgroundX) * self.ratio)
            if image.hasAttribute("y"):
                record_image['y'] = unicode((float(image.attributes['y'].value) - self.backgroundY) * self.ratio)

            if self.ratio != 1:
                record_image['image'], \
                record_image['width'], \
                record_image['height'] = \
                    self.resizeImage(record_image['image'], record_image['width'], record_image['height'])
            #if not sys.platform.startswith("darwin"):
            if HANDLE_PIL:
                record_image['image'], \
                record_image['width'], \
                record_image['height'], \
                newx, newy = self.cropImage(record_image['image'], record_image['width'], record_image['height'])
                record_image['y'] = unicode(int(float(record_image['y']) + float(newy)))
                record_image['x'] = unicode(int(float(record_image['x']) + float(newx)))

            if record_image['title'].startswith("http://") or \
                    record_image['title'].startswith("https://") or \
                    record_image['title'].startswith("//") or \
                    record_image['title'].startswith("./") or \
                    record_image['title'].startswith("../"):
                record_image['options'] += " direct-link "

            if image.hasAttribute("images_actives:zoomable"):
                str_zoom = image.attributes['images_actives:zoomable'].value
                if str_zoom == "false":
                    record_image['fill'] = "#000000"

            if image.hasAttribute("style"):
                str_style = image.attributes['style'].value
                style = {}
                for item in str_style.split(";"):
                    key, value = item.split(":")
                    style[key] = value
                if 'fill' in style:
                    record_image['fill'] = style['fill']
                if 'stroke' in style:
                    record_image['stroke'] = style['stroke']
                if 'stroke-width' in style:
                    record_image['strokewidth'] = style['stroke-width']

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
            if (float(record_image['x']) + float(record_image['width'])) > float(maxX):
                maxX = float(record_image['x']) + float(record_image['width'])
            if float(record_image['y']) < float(minY):
                minY = float(record_image['y'])
            if (float(record_image['y']) + float(record_image['height'])) > float(maxY):
                maxY = float(record_image['y']) + float(record_image['height'])

            record_image["minX"] = unicode(minX)
            record_image["minY"] = unicode(minY)
            record_image["maxX"] = unicode(maxX)
            record_image["maxY"] = unicode(maxY)

            return record_image

    def extract_rect(self, rect, stackTransformations):
        """Analyze rectangles"""

        record_rect = {}
        record_rect['id'] = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if rect.hasAttribute("id"):
            record_rect['id'] = rect.attributes['id'].value
        record_rect['width'] = rect.attributes['width'].value
        record_rect['height'] = rect.attributes['height'].value

        # if dimensions are invalid, exclude this rectangle
        if not record_rect['width'] or not record_rect['height']:
            return

        record_rect['detail'] = self.getText("desc", rect)
        record_rect['title'] = self.getText("title", rect)
        record_rect['x'] = unicode(0)
        record_rect['y'] = unicode(0)
        record_rect['rx'] = unicode(0)
        record_rect['ry'] = unicode(0)
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
                record_rect['options'] += " " + str_onclick + " "
        if rect.hasAttribute("onmouseover"):
            str_onmouseover = rect.attributes['onmouseover'].value
            record_rect['options'] += " " + str_onmouseover + " "

        if record_rect['title'].startswith("http://") or \
                record_rect['title'].startswith("https://") or \
                record_rect['title'].startswith("//") or \
                record_rect['title'].startswith("./") or \
                record_rect['title'].startswith("../"):
            record_rect['options'] += " direct-link "

        if rect.hasAttribute("images_actives:zoomable"):
            str_zoom = rect.attributes['images_actives:zoomable'].value
            if str_zoom == "false":
                record_rect['fill'] = "#000000"


        if rect.hasAttribute("style"):
            str_style = rect.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key, value = item.split(":")
                style[key] = value
            if 'fill' in style:
                record_rect['fill'] = style['fill']
            if 'stroke' in style:
                record_rect['stroke'] = style['stroke']
            if 'stroke-width' in style:
                record_rect['strokewidth'] = style['stroke-width']

        # ObjectToPath                    
        ctm = CurrentTransformation()
        record_rect['path'] = ctm.rectToPath(record_rect)

        p = cubicsuperpath.parsePath(record_rect['path'])
        record_rect['path'] = cubicsuperpath.formatPath(p)
        record_rect['x'] = unicode(0)
        record_rect['y'] = unicode(0)
        if stackTransformations == "":
            if rect.hasAttribute("transform"):
                transformation = rect.attributes['transform'].value
                ctm.analyze(transformation)

                ctm.applyTransformToPath(ctm.matrix, p)
                record_rect['path'] = cubicsuperpath.formatPath(p)

        # apply group transformation on current object
        else:
            transformations = stackTransformations.split("#")
            for transformation in transformations[::-1]:
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                ctm.applyTransformToPath(ctm.matrix, p)
                record_rect['path'] = cubicsuperpath.formatPath(p)

                #if ctm_group:
        #    ctm_group.applyTransformToPath(ctm_group.matrix,p)
        #    record_rect['path'] = cubicsuperpath.formatPath(p)

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record_rect['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
            record_rect['path'] = cubicsuperpath.formatPath(p)

        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000
        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i % 2 == 0):
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
        record_rect["minX"] = unicode(minX)
        record_rect["minY"] = unicode(minY)
        record_rect["maxX"] = unicode(maxX)
        record_rect["maxY"] = unicode(maxY)

        record_rect['path'] = '"' + record_rect['path'] + ' z"'
        return record_rect

    def extract_path(self, path, stackTransformations):
        """Analyze paths"""

        record = {}
        record["path"] = ""
        record["fill"] = ""
        record["id"] = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if path.hasAttribute("id"):
            record["id"] = path.attributes['id'].value
        record["path"] = path.attributes['d'].value. \
            replace("&#xd;&#xa;", " "). \
            replace("&#x9;", " "). \
            replace("\n", " "). \
            replace("\t", " "). \
            replace("\r", " ")

        # if path is invalid, exclude this detail
        if not record["path"]:
            return

        record["style"] = ""
        record['detail'] = self.getText("desc", path)
        record['title'] = self.getText("title", path)
        record['x'] = unicode(0)
        record['y'] = unicode(0)
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

        if path.hasAttribute("images_actives:zoomable"):
            str_zoom = path.attributes['images_actives:zoomable'].value
            if str_zoom == "false":
                record['fill'] = "#000000"


        if path.hasAttribute("style") and (path.attributes['style'].value != ""):
            str_style = path.attributes['style'].value
            style = {}
            for item in str_style.split(";"):
                key, value = item.split(":")
                style[key] = value
            if 'fill' in style:
                record["fill"] = style['fill']
            if 'stroke' in style:
                record['stroke'] = style['stroke']
            if 'stroke-width' in style:
                record['strokewidth'] = style['stroke-width']

        if path.hasAttribute("x"):
            record['x'] = path.attributes['x'].value
        if path.hasAttribute("y"):
            record['y'] = path.attributes['y'].value

        # ObjectToPath
        p = cubicsuperpath.parsePath(record['path'])
        record['path'] = cubicsuperpath.formatPath(p)

        if stackTransformations == "":
            if path.hasAttribute("transform"):
                transformation = path.attributes['transform'].value
                ctm = CurrentTransformation()
                ctm.analyze(transformation)

                ctm.applyTransformToPath(ctm.matrix, p)
                record['path'] = cubicsuperpath.formatPath(p)

        # apply group transformation on current object
        # if ctm_group:
        #    ctm_group.applyTransformToPath(ctm_group.matrix,p)
        #    record['path'] = cubicsuperpath.formatPath(p)

        else:
            transformations = stackTransformations.split("#")
            for transformation in transformations[::-1]:
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                ctm.applyTransformToPath(ctm.matrix, p)
                record['path'] = cubicsuperpath.formatPath(p)

        if self.translation != 0:
            #print("apply translation")
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
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
                if (i % 2 == 0):
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
        record["minX"] = unicode(minX)
        record["minY"] = unicode(minY)
        record["maxX"] = unicode(maxX)
        record["maxY"] = unicode(maxY)
        if record["path"]:
            return record

    def getText(self, type, element):
        """ type can be 'desc' or 'title' """
        text = element.getElementsByTagName(type)
        if text.item(0) is not None:
            if text.item(0).parentNode == element:
                return self.get_tag_value(text.item(0))
        return ""

    def print_node(self, root, childs):
        if root.childNodes:
            for node in root.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    childs.append(node)
                    self.print_node(node, childs)

    def linearize_childs(self, root, childs, stackTransform):

        if root.hasAttribute("transform"):
            stackTransform.append(root.attributes['transform'].value)
        entry = {}
        entry["node"] = root
        entry["transform"] = "#".join(stackTransform)
        childs.append(entry)

        if root.childNodes:
            for node in root.childNodes:
                if node.nodeType == node.ELEMENT_NODE:
                    #childs.append(node)
                    self.linearize_childs(node, childs, stackTransform)

        if root.hasAttribute("transform"):
            stackTransform.pop()

    def extract_g(self, group, stackTransformations):
        """Analyze a svg group"""

        record = {}
        record["id"] = hashlib.md5(str(uuid.uuid1())).hexdigest()
        if group.hasAttribute("id"):
            record["id"] = group.attributes['id'].value
        record['title'] = self.getText("title", group)
        record['detail'] = self.getText("desc", group)
        record["group"] = []
        record["options"] = ""

        minX = 10000
        minY = 10000
        maxX = 0
        maxY = 0

        if group.hasAttribute("onclick"):
            str_onclick = group.attributes['onclick'].value
            if str_onclick == "off":
                record['options'] += " disable-click "
            else:
                record['options'] += " " + str_onclick + " "

        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image']
        group_childs = []
        stackTransform = []
        self.linearize_childs(group, group_childs, stackTransform)

        for childentry in group_childs:
            childnode = childentry['node']
            #print childentry['node']
            #print childentry['transform']
            if childnode.nodeName in svgElements:
                newrecord = getattr(self, 'extract_' + \
                                    childnode.nodeName)(childnode, childentry['transform'])
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

        record["minX"] = unicode(minX)
        record["minY"] = unicode(minY)
        record["maxX"] = unicode(maxX)
        record["maxY"] = unicode(maxY)

        if record["group"]:
            return record

    def fixRaster(self, raster, rasterWidth, rasterHeight):
        dirname = tempfile.mkdtemp()
        newraster = raster

        rasterStartPosition = raster.find('base64,') + 7
        rasterEncoded = raster[rasterStartPosition:]
        rasterPrefix = raster[0:rasterStartPosition]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                imageFile = dirname + os.path.sep + "image." + extension.group(1)
                imageFileFixed = dirname + \
                                 os.path.sep + "image_small." + extension.group(1)
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(rasterEncoded.decode("base64"))

                #if sys.platform.startswith('darwin'):
                if not HANDLE_PIL:
                    shutil.copyfile(imageFile, imageFileFixed)
                    w = commands.getstatusoutput('sips -g pixelWidth {0}'.format(imageFile))
                    if w != rasterWidth:
                        commands.getstatusoutput('sips -z {0} {1} {2}'.format(rasterHeight,
                                                                              rasterWidth,
                                                                              imageFileFixed))

                        with open(imageFileFixed, 'rb') as fixedImage:
                            rasterFixedEncoded = fixedImage.read().encode("base64")
                            newraster = rasterPrefix + rasterFixedEncoded

                else:
                    currentImg = Image.open(imageFile)
                    (w, h) = currentImg.size
                    if w != rasterWidth:
                        newwidth = int(float(rasterWidth))
                        newheight = int(float(rasterHeight))
                        resizedImg = currentImg.resize((newwidth, newheight), Image.BICUBIC)
                        resizedImg.save(imageFileFixed)

                        with open(imageFileFixed, 'rb') as fixedImage:
                            rasterFixedEncoded = fixedImage.read().encode("base64")
                            newraster = rasterPrefix + rasterFixedEncoded

        else:
            self.console.display('ERROR : fixRaster() - image is not embedded')
        shutil.rmtree(dirname)
        return newraster


    def cropImage(self, raster, rasterWidth, rasterHeight):
        dirname = tempfile.mkdtemp()
        newraster = raster
        newrasterWidth = rasterWidth
        newrasterHeight = rasterHeight
        x_delta = 0
        y_delta = 0
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

                #if not sys.platform.startswith('darwin'):
                if HANDLE_PIL:
                    im = Image.open(imageFile, 'r')
                    im = im.convert("RGBA")
                    pix_val = list(im.getdata())
                    (w, h) = im.size
                    alpha_threshold = 100
                    y_delta = 0
                    stop_scan = 0
                    for y in range(h):
                        row = y * w
                        for x in range(w):
                            transparency = pix_val[x + row][3] - alpha_threshold
                            if transparency >= 0:
                                stop_scan = 1
                                break
                        if stop_scan:
                            break
                        else:
                            y_delta += 1

                    y_delta2 = 0
                    stop_scan = 0
                    for y in range(h - 1, 0, -1):
                        row = y * w
                        for x in range(w - 1, 0, -1):
                            transparency = pix_val[x + row][3] - alpha_threshold
                            if transparency >= 0:
                                stop_scan = 1
                                break
                        if stop_scan:
                            break
                        else:
                            y_delta2 += 1

                    x_delta = 0
                    stop_scan = 0
                    for x in range(0, w - 1):
                        for y in range(0, h - 1):
                            row = y * w
                            transparency = pix_val[x + row][3] - alpha_threshold
                            if transparency >= 0:
                                stop_scan = 1
                                break
                        if stop_scan:
                            break
                        else:
                            x_delta += 1

                    x_delta2 = 0
                    stop_scan = 0
                    for x in range(w - 1, 0, -1):
                        for y in range(h - 1, 0, -1):
                            row = y * w
                            transparency = pix_val[x + row][3] - alpha_threshold
                            if transparency >= 0:
                                stop_scan = 1
                                break
                        if stop_scan:
                            break
                        else:
                            x_delta2 += 1

                    croppedBg = im.crop((x_delta, y_delta, w - x_delta2, h - y_delta2))
                    croppedBg.save(imageFileSmall)

                    with open(imageFileSmall, 'rb') as bgSmallImage:
                        rasterSmallEncoded = bgSmallImage.read(). \
                            encode("base64")
                        newraster = rasterPrefix + \
                                    rasterSmallEncoded
                    newrasterHeight = int((h - y_delta2 - y_delta) * float(rasterHeight) / h)
                    newrasterWidth = int((w - x_delta - x_delta2) * float(rasterWidth) / w)
        else:
            self.console.display('ERROR : cropImage() - image is not embedded ' + raster)
        shutil.rmtree(dirname)
        return [newraster, unicode(newrasterWidth), unicode(newrasterHeight), x_delta, y_delta]

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
                    #if sys.platform.startswith('darwin'):
                    if not HANDLE_PIL:
                        oldwidth = int(float(rasterWidth))
                        oldheight = int(float(rasterHeight))
                        newwidth = int(oldwidth * self.ratio)
                        newheight = int(oldheight * self.ratio)
                        shutil.copyfile(imageFile, imageFileSmall)
                        commands.getstatusoutput('sips -z {0} {1} {2}'.format(newheight, newwidth, imageFileSmall))

                        with open(imageFileSmall, 'rb') as bgSmallImage:
                            rasterSmallEncoded = bgSmallImage.read().encode("base64")
                            newraster = rasterPrefix + rasterSmallEncoded

                        newrasterWidth = newwidth
                        newrasterHeight = newheight

                    else:
                        # "Platform Linux or Windows : resizing using PIL"
                        currentBg = Image.open(imageFile)
                        oldwidth = int(float(rasterWidth))
                        oldheight = int(float(rasterHeight))
                        newwidth = int(oldwidth * self.ratio)
                        newheight = int(oldheight * self.ratio)
                        resizedBg = currentBg.resize((newwidth, newheight), Image.BICUBIC)
                        resizedBg.save(imageFileSmall)

                        with open(imageFileSmall, 'rb') as bgSmallImage:
                            rasterSmallEncoded = bgSmallImage.read().encode("base64")
                            newraster = rasterPrefix + rasterSmallEncoded

                        newrasterWidth = newwidth
                        newrasterHeight = newheight
        else:
            self.console.display('ERROR : image is not embedded')
        shutil.rmtree(dirname)
        return [newraster, unicode(newrasterWidth), unicode(newrasterHeight)]


    def generateJSON(self):
        """ generate json file"""
        final_str = u""
        final_str += u'var scene = {\n'
        for entry in self.scene:
            if entry == "image":
                final_str += u'"' + entry + u'":"' + \
                             self.scene[entry]. \
                                 replace("\n", ""). \
                                 replace("\t", ""). \
                                 replace("\r", "") + u'",\n'
            else:
                final_str += u'"' + entry + u'":"' + \
                             PageFormatter(self.scene[entry]).print_html(). \
                                 replace('"', "'"). \
                                 replace("\n", " "). \
                                 replace("\t", " "). \
                                 replace("\r", " ") + u'",\n'
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
                                             element[entry2]. \
                                                 replace('"', "'"). \
                                                 replace("\n", " "). \
                                                 replace("\t", " "). \
                                                 replace("\r", " ") + u',\n'
                            elif entry2 == "image" or entry2 == "title":
                                final_str += u'  "' + entry2 + u'":"' + \
                                             element[entry2]. \
                                                 replace('"', "'"). \
                                                 replace("\n", " "). \
                                                 replace("\t", " "). \
                                                 replace("\r", " ") + u'",\n'
                            else:
                                final_str += u'      "' + entry2 + u'":"' + \
                                             PageFormatter(element[entry2]).print_html(). \
                                                 replace('"', "'"). \
                                                 replace("\n", " "). \
                                                 replace("\t", " "). \
                                                 replace("\r", " ") + u'",\n'
                        final_str += u'  },\n'
                    final_str += u'  ],\n'
                elif entry == "path":
                    final_str += u'  "' + entry + u'":' + detail[entry] + ',\n'
                elif entry == "image":
                    final_str += u'  "' + entry + u'":"' + detail[entry]. \
                        replace('"', "'"). \
                        replace("\n", " "). \
                        replace("\t", " "). \
                        replace("\r", " ") + u'",\n'
                elif entry == "detail":
                    final_str += u'  "' + entry + u'":"' + \
                                 PageFormatter(detail[entry]).print_html(). \
                                     replace('"', "'"). \
                                     replace("\n", " "). \
                                     replace("\t", " "). \
                                     replace("\r", " ") + \
                                 u'",\n'
                else:
                    if type(detail[entry]) is not str and type(detail[entry]) is not unicode:
                        detail[entry] = unicode(detail[entry])
                    final_str += u'  "' + entry + u'":"' + \
                                 detail[entry]. \
                                     replace('"', "'"). \
                                     replace('\t', " "). \
                                     replace('\r', " "). \
                                     replace('\n', " ") + \
                                 u'",\n'
            final_str += u'},\n'
        final_str += u'];\n'
        self.jsonContent = final_str
