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
# @author : pascal.fautrero@gmail.com

import os
import math
import re
import tempfile
import sys
import shutil
import base64
import json
#import commands
from subprocess import Popen, PIPE
# import PIL for windows and Linux
# For MAC OS X, use internal tool called "sips"
try:
    from PIL import Image, ImageDraw
    HANDLE_PIL = True
    Image.MAX_IMAGE_PIXELS = None
except ImportError:
    if not sys.platform.startswith('darwin'):
        print("Requirement : Please, install python3-pil package")
        sys.exit(1)
    else:
        HANDLE_PIL = False

import hashlib
import uuid
from xml.dom import minidom

from .ctm import CurrentTransformation
from .cubicsuperpath import *
from .pikipiki import PageFormatter


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
        self.backgroundNode = ""

    def get_tag_value(self, node):
        result = ""
        if node is not None:
            if node.childNodes:
                result = node.childNodes[0].nodeValue
        return result

    def extract_metadata_item(self, metadatas, item):
        metadata = metadatas.getElementsByTagName(item).item(0)
        return self.get_tag_value(metadata)

    def extract_metadata_item2(self, metadatas, item):
        result = ""
        md = metadatas.getElementsByTagName(item).item(0)
        if md is not None:
            md2 = md.getElementsByTagName('dc:title').item(0)
            result = self.get_tag_value(md2)
        return result

    def extractMetadatas(self, xml):

        md = {
            'title': 'dc:title',
            'date': 'dc:date',
            'coverage': 'dc:coverage',
            'relation': 'dc:relation',
            'source': 'dc:source',
            'identifier': 'dc:identifier',
            'description': 'dc:description',
            'language': 'dc:language'
        }
        md_title = {
            'creator': 'dc:creator',
            'rights': 'dc:rights',
            'publisher': 'dc:publisher',
            'contributor': 'dc:contributor'
        }

        metadatas = xml.getElementsByTagName('metadata').item(0)
        self.scene['keywords'] = ""
        self.scene['license'] = ""
        for item in md:
            self.scene[item] = ""
        for item in md_title:
            self.scene[item] = ""

        if metadatas is not None:

            licenses = metadatas.getElementsByTagName('cc:license')
            licenses_items = []
            if licenses is not None:
                for i in range(licenses.length):
                    if licenses.item(i).hasAttribute("rdf:resource"):
                        licenses_items.append(licenses.item(i).attributes["rdf:resource"].value)
            self.scene['license'] = ",".join(item for item in licenses_items)

            for item in md:
                self.scene[item] = self.extract_metadata_item(metadatas, md[item])

            for item in md_title:
                self.scene[item] = self.extract_metadata_item2(metadatas, md_title[item])

            metadata = metadatas.getElementsByTagName('dc:subject').item(0)
            if metadata is not None:
                keywords = metadata.getElementsByTagName('rdf:li')
                self.scene['keywords'] = ",".join(self.get_tag_value(keyword) for keyword in keywords)

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
                    raster = rasterPref + base64.b64encode(img.read()).decode()
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

        with open(filePath, 'r', encoding="utf8") as svgfile:
            svgcontent = svgfile.read()
            if not re.search(r'xmlns:xlink=', svgcontent, re.M):
                svgcontent = svgcontent.replace("<svg", '<svg\nxmlns:xlink="http://www.w3.org/1999/xlink"')
                dirname = os.path.dirname(filePath)
                basename = os.path.basename(filePath)
                fixedfile = f"{dirname}/fixed_{basename}"
                with open(fixedfile, 'w') as tempsvgfile:
                    tempsvgfile.write(svgcontent)
                filePath = fixedfile

        self.filePath = filePath

        self.xml = minidom.parse(filePath)

        head, tail = os.path.split(filePath)
        self.scene['intro_title'] = "Description"
        self.scene['intro_detail'] = "XIA"
        self.scene['image'] = ""
        self.scene['path'] = ""
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
                self.scene['intro_title'] = self.get_tag_value(title.item(0))

            raster = self.extractRaster(image.attributes['xlink:href'].value)
            #print raster
            if image.hasAttribute("transform"):
                transformation = image.attributes['transform'].value
                ctm = CurrentTransformation()
                ctm.analyze(transformation)
                if ctm.scaleX != 1 or ctm.scaleY != 1:
                    self.scene['image'], self.scene['width'], self.scene['height'] = self.resizeImage(
                        raster,
                        int(float(self.scene['width'])) * ctm.scaleX,
                        int(float(self.scene['height'])) * ctm.scaleY)

            fixedRaster = raster
            self.scene['image'] = fixedRaster
            self.scene['ratio'] = self.calculate_raster_ratio(raster, self.scene['width'], self.scene['height'])

            # calculate ratio to resize background image down to maxNumPixels

            bgNumPixels = float(int(float(self.scene['width'])) * int(float(self.scene['height'])))
            if bgNumPixels > maxNumPixels:
                self.ratio = math.sqrt(maxNumPixels / bgNumPixels)

            if self.ratio != 1:
                self.scene['image'], \
                self.scene['width'], \
                self.scene['height'] = self.resizeImage(\
                    self.scene['image'], \
                    float(self.scene['width']) / self.ratio,\
                    float(self.scene['height']) / self.ratio)
                self.scene['ratio'] = self.calculate_raster_ratio(raster, self.scene['width'], self.scene['height'])
                self.ratio = 1

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

            # replace image by svg path if defined as background element
            linearizedChilds = []
            stackTransform = []
            self.linearize_childs(mainSVG[0], linearizedChilds, stackTransform)
            svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image']
            firstNode = None
            for childnode in linearizedChilds:
                if childnode['node'].nodeName in svgElements:
                    firstNode = childnode['node']
                    break
            if firstNode is not None and \
                firstNode.nodeName != 'image' and \
                firstNode.parentNode.nodeName != 'clipPath' and \
                firstNode.parentNode.nodeName != 'marker':

                self.translation = 0
                self.backgroundX = 0
                self.backgroundY = 0
                if firstNode.nodeName == 'path':
                    minX, minY, maxX, maxY = self.getExtrema(firstNode.attributes['d'].value)
                    self.backgroundX = float(minX)
                    self.backgroundY = float(minY)
                else:
                    if firstNode.hasAttribute('x'):
                        self.backgroundX = float(firstNode.attributes['x'].value)
                    if firstNode.hasAttribute('y'):
                        self.backgroundY = float(firstNode.attributes['y'].value)

                if (self.backgroundX != 0) or (self.backgroundY != 0):
                    ctm = CurrentTransformation()
                    ctm.extractTranslate([self.backgroundX * (-1), self.backgroundY * (-1)])
                    self.translation = ctm.matrix

                newrecord = getattr(self, 'extract_' + firstNode.nodeName)(firstNode, "")
                if newrecord is not None:
                    self.backgroundNode = firstNode
                    self.scene['width'] = float(newrecord['maxX']) - float(newrecord['minX'])
                    self.scene['height'] = float(newrecord['maxY']) - float(newrecord['minY'])
                    self.scene['path'] = newrecord['path']
                    self.scene['image'] = ""

                    if 'fill' in newrecord:
                        self.scene['fill'] = newrecord['fill']
                    else:
                        self.scene['fill'] = '#00000000'
                    if 'stroke' in newrecord:
                        self.scene['stroke'] = newrecord['stroke']
                    else:
                        self.scene['stroke'] = '#000000'
                    if 'strokewidth' in newrecord:
                        self.scene['strokewidth'] = newrecord['strokewidth']
                    else:
                        self.scene['strokewidth'] = 0

            if firstNode.parentNode.nodeName == 'g' and firstNode.parentNode != mainSVG[0]:

                self.backgroundNode = ""
                self.scene['path'] = ""
                self.scene['image'] = ""
                self.backgroundX = 0
                self.backgroundY = 0

                svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image']
                group_childs = []
                stackTransform = []
                self.linearize_childs(firstNode.parentNode, group_childs, stackTransform)

                extrema = {}
                extrema['minX'] = []
                extrema['minY'] = []
                extrema['maxX'] = []
                extrema['maxY'] = []

                for childentry in group_childs:
                    childnode = childentry['node']
                    if childnode.nodeName in svgElements:
                        if childnode.hasAttribute('d'):
                            minX, minY, maxX, maxY = self.getExtrema(childnode.attributes['d'].value)

                            extrema['minX'].append(float(minX))
                            extrema['minY'].append(float(minY))

                        else:
                            if childnode.hasAttribute('x'):
                                extrema['minX'].append(float(childnode.attributes['x'].value))
                            else:
                                extrema['minX'].append(0)
                            if childnode.hasAttribute('x'):
                                extrema['minY'].append(float(childnode.attributes['y'].value))
                            else:
                                extrema['minY'].append(0)

                self.backgroundX = min(extrema['minX'])
                self.backgroundY = min(extrema['minY'])

                if (self.backgroundX != 0) or (self.backgroundY != 0):
                    ctm = CurrentTransformation()
                    ctm.extractTranslate([self.backgroundX * (-1), self.backgroundY * (-1)])
                    self.translation = ctm.matrix

                newrecord = getattr(self, 'extract_g')(firstNode.parentNode, "")
                if newrecord is not None:

                    self.backgroundNode = firstNode.parentNode
                    self.scene['width'] = float(newrecord['maxX']) - float(newrecord['minX'])
                    self.scene['height'] = float(newrecord['maxY']) - float(newrecord['minY'])

                    self.scene['group'] = newrecord

            # main loop on svg elements

            svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image', 'g']

            for childnode in mainSVG[0].childNodes:
                if childnode.parentNode.nodeName == mainSVG[0].nodeName:
                    if childnode.nodeName in svgElements:
                        newrecord = getattr(self, 'extract_' + childnode.nodeName)(childnode, "")
                        if newrecord is not None:
                            self.details.append(newrecord)

    def extract_circle(self, circle, stackTransformations):
        """Analyze circle"""
        if circle.isSameNode(self.backgroundNode):
            return
        record_circle = {}
        record_circle['id'] = hashlib.md5(uuid.uuid4().bytes).hexdigest()
        if circle.hasAttribute("id"):
            record_circle['id'] = circle.attributes['id'].value

        record_circle['desc'] = self.getText("desc", circle)
        record_circle['title'] = self.getText("title", circle)
        record_circle['cx'] = 0
        record_circle['cy'] = 0
        record_circle['r'] = 0
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
        record_circle['x'] = 0
        record_circle['y'] = 0
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

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record_circle['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
            record_circle['path'] = cubicsuperpath.formatPath(p)

        record_circle["minX"], \
        record_circle["minY"], \
        record_circle["maxX"], \
        record_circle['maxY'] = self.getExtrema(cubicsuperpath.formatPath(p))

        record_circle['path'] = '"' + record_circle['path'] + ' z"'
        return record_circle

    def extract_ellipse(self, ellipse, stackTransformations):
        """Analyze ellipse"""
        if ellipse.isSameNode(self.backgroundNode):
            return
        record_ellipse = {}
        record_ellipse['id'] = ellipse.attributes['id'].value \
            if ellipse.hasAttribute("id") else hashlib.md5(uuid.uuid4().bytes).hexdigest()
        record_ellipse['desc'] = self.getText("desc", ellipse)
        record_ellipse['title'] = self.getText("title", ellipse)
        record_ellipse['cx'] = 0
        record_ellipse['cy'] = 0
        record_ellipse['rx'] = 0
        record_ellipse['ry'] = 0
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
        record_ellipse['x'] = 0
        record_ellipse['y'] = 0
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

        record_ellipse["minX"], \
        record_ellipse["minY"], \
        record_ellipse["maxX"], \
        record_ellipse['maxY'] = self.getExtrema(cubicsuperpath.formatPath(p))

        record_ellipse['path'] = '"' + record_ellipse['path'] + ' z"'
        return record_ellipse

    def extract_line(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("line is not implemented. Convert it to path.")

    def extract_text(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("text is not implemented. Convert it to path.")

    def extract_flowRoot(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("flowRoot is not implemented. Convert it to path.")

    def extract_polyline(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("polyline is not implemented. Convert it to path.")

    def extract_polygon(self, image, stackTransformations):
        """not yet implemented"""
        self.console.display("polygon is not implemented. Convert it to path.")

    def rotate_point(self, x, y, cx, cy, alpha):
        """
        apply rotation on point (x,y) around center (cx, cy) with angle alpha
        z' = newX + i * newY
        z = x + i * y
        a = cx + i * cy
        z' = (z - a) * (cos(alpha) + i sin(alpha)) + a
        """
        newX = (x - cx) * math.cos(alpha) - (y - cy) * math.sin(alpha) + cx
        newY = (x - cx) * math.sin(alpha) + (y - cy) * math.cos(alpha) + cy
        return newX, newY

    def transformImage(self, img, ctm):
        """
        Apply Affine transformation on Image raster
        """
        raster = img['image']
        width = img['width'] * img['ratio']
        height = img['height'] * img['ratio']
        dirname = tempfile.mkdtemp()
        newraster = raster
        rasterStartPosition = raster.find('base64,') + 7
        rasterEncoded = raster[rasterStartPosition:]
        rasterPrefix = raster[0:rasterStartPosition]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                imageFile = dirname + os.path.sep + "image." + extension.group(1)
                imageFile2 = dirname + os.path.sep + "image2.png"
                with open(imageFile, "wb") as Image1:
                    Image1.write(base64.b64decode(rasterEncoded))

                if HANDLE_PIL:
                    with open(imageFile, 'rb') as f:
                        currentImage = Image.open(f)
                        newImage = currentImage.transform((int(width), int(height)), Image.AFFINE, data=ctm.inv_matrix(), resample=Image.BICUBIC)
                        newImage.save(imageFile2)

                    with open(imageFile2, 'rb') as f:
                        rasterEncoded = base64.b64encode(f.read()).decode()
                        newraster = rasterPrefix + rasterEncoded
                else:
                    self.console.display('Affine transformation not yet implemented')

        else:
            self.console.display('ERROR : image is not embedded')
        shutil.rmtree(dirname)
        return newraster


    def transform_points(self, x, y, width, height, ctm):
        """Apply Affine transformation on box (x,y) (x+width, y+height)"""

        box = {
            'A': {'x': x, 'y': y},
            'B': {'x': x + width, 'y': y},
            'C': {'x': x,'y': y + height},
            'D': {'x': x + width,'y': y + height}
        }

        box['A']['x2'], box['A']['y2'] = ctm.applyTransformToPoint(ctm.matrix,[box['A']['x'], box['A']['y']])
        box['B']['x2'], box['B']['y2'] = ctm.applyTransformToPoint(ctm.matrix,[box['B']['x'], box['B']['y']])
        box['C']['x2'], box['C']['y2'] = ctm.applyTransformToPoint(ctm.matrix,[box['C']['x'], box['C']['y']])
        box['D']['x2'], box['D']['y2'] = ctm.applyTransformToPoint(ctm.matrix,[box['D']['x'], box['D']['y']])

        coords_min = {
            'x': min(box['A']['x2'], box['B']['x2'], box['C']['x2'], box['D']['x2']),
            'y': min(box['A']['y2'], box['B']['y2'], box['C']['y2'], box['D']['y2'])
        }
        coords_max = {
            'x': max(box['A']['x2'], box['B']['x2'], box['C']['x2'], box['D']['x2']),
            'y': max(box['A']['y2'], box['B']['y2'], box['C']['y2'], box['D']['y2'])
        }
        return coords_min, coords_max

    def transform_image(self, img, transformation):
        """Prepare affine transformation on image"""
        ctm = CurrentTransformation()
        ctm.analyze(transformation)

        # Calculate new box
        box_min, box_max = self.transform_points(img['x'], img['y'], img['width'], img['height'], ctm)

        # recenter image
        translate, _ = self.transform_points(0, 0, img['width'] * img['ratio'], img['height'] * img['ratio'], ctm)
        ctm.matrix[0][2] += (-1) * translate['x']
        ctm.matrix[1][2] += (-1) * translate['y']

        img['x'] = box_min['x']
        img['y'] = box_min['y']
        img['height'] = box_max['y'] - box_min['y']
        img['width'] = box_max['x'] - box_min['x']

        # transform Image
        img['image'] = self.transformImage(img, ctm)

        return img


    def extract_image(self, image, stackTransformations):
        """Analyze images"""

        if not image.isSameNode(self.backgroundNode):
            record_image = {}
            record_image['id'] = hashlib.md5(uuid.uuid4().bytes).hexdigest()
            if image.hasAttribute('id'):
                record_image['id'] = image.attributes['id'].value
            record_image['width'] = float(image.attributes['width'].value)
            record_image['height'] = float(image.attributes['height'].value)
            record_image['image'] = self.extractRaster(image.attributes['xlink:href'].value)
            record_image['ratio'] = self.calculate_raster_ratio(record_image['image'], record_image["width"], record_image['height'])
            record_image['desc'] = self.getText("desc", image)
            record_image['title'] = self.getText("title", image)
            record_image['x'] = 0
            record_image['y'] = 0
            record_image['options'] = ""

            if image.hasAttribute("x"):
                record_image['x'] = (float(image.attributes['x'].value) - self.backgroundX) * self.ratio
            if image.hasAttribute("y"):
                record_image['y'] = (float(image.attributes['y'].value) - self.backgroundY) * self.ratio

            if self.ratio != 1:
                record_image['image'], \
                record_image['width'], \
                record_image['height'] = \
                    self.resizeImage(record_image['image'], record_image['width'] * self.ratio, record_image['height'] * self.ratio)



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
                    if item != "":
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

            # Inkscape can apply scaling just by changing image dimensions
            # If so, just update raster
            w,h, success = self.get_dimensions(record_image['image'])
            if success:
                if w/h != record_image['width'] / record_image['height']:
                    record_image['image'], _, _ = self.resizeImage(
                        record_image['image'],
                        record_image['width'] * record_image['ratio'],
                        record_image['height'] * record_image['ratio'])

            else:
                self.console.display("failure")
            
            # apply group transformations

            if self.translation != 0:
                record_image['x'] = record_image['x'] / self.ratio + self.backgroundX
                record_image['y'] = record_image['y'] / self.ratio + self.backgroundX

            if stackTransformations == "":
                if image.hasAttribute("transform"):
                    stackTransformations = image.attributes['transform'].value 

            if stackTransformations != "":
                transformations = stackTransformations.split("#")
                for transformation in transformations[::-1]:
                    record_image = self.transform_image(record_image, transformation)

            if self.translation != 0:
                record_image['x'] = (record_image['x'] - self.backgroundX) * self.ratio
                record_image['y'] = (record_image['y'] - self.backgroundX) * self.ratio

            if HANDLE_PIL:
                record_image['image'], \
                record_image['width'], \
                record_image['height'], \
                newx, newy, \
                record_image['original_width'], \
                record_image['original_height'] = self.cropImage(record_image['image'], record_image['width'], record_image['height'])
                record_image['y'] = record_image['y'] + newy
                record_image['x'] = record_image['x'] + newx


            record_image["minX"] = record_image['x']
            record_image["minY"] = record_image['y']
            record_image["maxX"] = record_image['x'] + record_image['width']
            record_image["maxY"] = record_image['y'] + record_image['height']
            record_image['width'] = int(record_image['width'])
            record_image['height'] = int(record_image['height'])
            return record_image

    def extract_rect(self, rect, stackTransformations):
        """Analyze rectangles"""
        if rect.isSameNode(self.backgroundNode):
            return
        record_rect = {}
        record_rect['id'] = hashlib.md5(uuid.uuid4().bytes).hexdigest()
        if rect.hasAttribute("id"):
            record_rect['id'] = rect.attributes['id'].value
        record_rect['width'] = rect.attributes['width'].value
        record_rect['height'] = rect.attributes['height'].value

        # if dimensions are invalid, exclude this rectangle
        if not record_rect['width'] or not record_rect['height']:
            return

        record_rect['desc'] = self.getText("desc", rect)
        record_rect['title'] = self.getText("title", rect)
        record_rect['x'] = 0
        record_rect['y'] = 0
        record_rect['rx'] = 0
        record_rect['ry'] = 0
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
        record_rect['x'] = 0
        record_rect['y'] = 0
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

        if self.translation != 0:
            ctm = CurrentTransformation()
            ctm.applyTransformToPath(self.translation, p)
            record_rect['path'] = cubicsuperpath.formatPath(p)

        if self.ratio != 1:
            ctm = CurrentTransformation()
            ctm.extractScale([self.ratio])
            ctm.applyTransformToPath(ctm.matrix, p)
            record_rect['path'] = cubicsuperpath.formatPath(p)

        record_rect["minX"], \
        record_rect["minY"], \
        record_rect["maxX"], \
        record_rect['maxY'] = self.getExtrema(cubicsuperpath.formatPath(p))
        record_rect['path'] = '"' + record_rect['path'] + ' z"'
        return record_rect

    def extract_path(self, path, stackTransformations):
        """Analyze paths"""
        if path.isSameNode(self.backgroundNode):
            return
        record = {}
        record["path"] = ""
        record["fill"] = ""
        record["id"] = hashlib.md5(uuid.uuid4().bytes).hexdigest()
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
        record['desc'] = self.getText("desc", path)
        record['title'] = self.getText("title", path)
        record['x'] = 0
        record['y'] = 0
        record['options'] = ""

        if path.hasAttribute("inkscape:connection-start") and path.hasAttribute("inkscape:connection-end"):
            record['connectionStart'] = path.attributes['inkscape:connection-start'].value
            record['connectionEnd'] = path.attributes['inkscape:connection-end'].value

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
            record["style"] = path.attributes['style'].value
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
        record["minX"], \
        record["minY"], \
        record["maxX"], \
        record['maxY'] = self.getExtrema(cubicsuperpath.formatPath(p))
        if record["path"]:
            return record

    def getExtrema(self, path):
        """ Return MinX, MinY, maxX, maxY """
        p = cubicsuperpath.parsePath(path)

        extrema = {}
        extrema['x'] = []
        extrema['y'] = []

        for cmd, params in cubicsuperpath.unCubicSuperPath(p):
            i = 0
            for p in params:
                if (i % 2 == 0):
                    extrema['x'].append(p)
                else:
                    extrema['y'].append(p)
                i = i + 1
        return [min(extrema['x']), min(extrema['y']), max(extrema['x']), max(extrema['y'])]

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

    def format_text(self, text):
        return PageFormatter(text).print_html() \
                                .replace('"', "'") \
                                .replace("\n", " ") \
                                .replace("\t", " ") \
                                .replace("\r", " ")

    def build_sprite(self, group, record):

        minX = 10000
        minY = 10000
        maxX = 0
        maxY = 0

        dirname = tempfile.mkdtemp()
        svgElements = ['image']
        imagesSHA1 = []
        timeLine = []
        frames = []
        imagesToConcatenate = []
        group_childs = []
        stackTransform = []
        self.linearize_childs(group, group_childs, stackTransform)

        # Extract Images
        imageIndex = 0
        for childentry in group_childs:
            childnode = childentry['node']

            if childnode.nodeName in svgElements:
                newrecord = getattr(self, 'extract_' + \
                                    childnode.nodeName)(childnode, childentry['transform'])

                if newrecord is not None:
                    raster = newrecord['image']
                    rasterStartPosition = raster.find('base64,') + 7
                    rasterEncoded = raster[rasterStartPosition:]
                    rasterSHA1 = hashlib.sha1(rasterEncoded.encode()).hexdigest()
                    if rasterSHA1 not in imagesSHA1:
                        # this is an image frame pose
                        imagesSHA1.append(rasterSHA1)
                        timeLine.append(imageIndex)

                        rasterPrefix = raster[0:rasterStartPosition]
                        extension = re.search('image/(.*);base64', rasterPrefix)
                        if extension is not None:
                            if extension.group(1):
                                imageFile = dirname + os.path.sep + "image" + str(imageIndex) + "." + extension.group(1)
                                imagesToConcatenate.append(imageFile)
                                with open(imageFile, "wb") as currentImage:
                                    currentImage.write(base64.b64decode(rasterEncoded))

                        if imageIndex == 0:
                            firstRasterPrefix = rasterPrefix
                            record['x'] = newrecord['x']
                            record['y'] = newrecord['y']
                            record['width'] = newrecord['width']
                            record['height'] = newrecord['height']
                            minX = float(newrecord["minX"])
                            minY = float(newrecord["minY"])
                            maxX = float(newrecord["maxX"])
                            maxY = float(newrecord["maxY"])

                        if record['desc'] == "":
                            record['desc'] = newrecord['desc']
                        if record["title"] == "":
                            record['title'] = newrecord['title']
                        imageIndex += 1
                    else:
                        # this image is already recorded
                        currentImageIndex = imagesSHA1.index(rasterSHA1)
                        timeLine.append(currentImageIndex)
                    frames.append({
                        "x":newrecord['x'], 
                        "y":newrecord['y'], 
                        "title":newrecord['title'], 
                        "desc":self.format_text(newrecord['desc'])
                        })

        # Now, Concatenate Images
        if imageIndex != 0:
            images = []
            for x in imagesToConcatenate:
              images.append(Image.open(x))
            #images = map(Image.open, imagesToConcatenate)
            widths, heights = zip(*(i.size for i in images))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGBA', (total_width, max_height))

            x_offset = 0
            for im in images:
              new_im.paste(im, (x_offset,0))
              x_offset += im.size[0]

            imageFileFixed = dirname + os.path.sep + "imageFinal.png"
            new_im.save(imageFileFixed)

            with open(imageFileFixed, 'rb') as fixedImage:
                rasterFixedEncoded = base64.b64encode(fixedImage.read()).decode().replace('\n','')

                record["image"] = firstRasterPrefix + rasterFixedEncoded

            record["minX"] = minX
            record["minY"] = minY
            record["maxX"] = maxX
            record["maxY"] = maxY
            record["timeline"] =  ','.join([str(i) for i in timeLine])
            record['frames'] = json.dumps(frames)

        if group.hasAttribute("style") and (group.attributes['style'].value != ""):
            str_style = group.attributes['style'].value
            record["style"] = group.attributes['style'].value
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

        shutil.rmtree(dirname)

    def extract_g(self, group, stackTransformations):
        """Analyze a svg group"""

        if group.isSameNode(self.backgroundNode):
            return

        record = {}
        record["id"] = hashlib.md5(uuid.uuid4().bytes).hexdigest()
        if group.hasAttribute("id"):
            record["id"] = group.attributes['id'].value
        record['title'] = self.getText("title", group)
        record['desc'] = self.getText("desc", group)
        record["options"] = ""

        if group.hasAttribute("onclick"):
            str_onclick = group.attributes['onclick'].value
            if str_onclick == "off":
                record['options'] += " disable-click "
            else:
                record['options'] += " " + str_onclick + " "

        if record["id"].startswith("sprite"):
            self.build_sprite(group, record)
            return record

        record["group"] = []

        minX = 10000
        minY = 10000
        maxX = 0
        maxY = 0

        # TODO Vérifier que des sprites ne sont pas embarqués dans des groupes
        # si c'est le cas, il faut les extraire pour les convertir en images

        subgroups = group.getElementsByTagName('g')
        for subgroup in subgroups:
            if subgroup.hasAttribute("id"):
                if subgroup.attributes['id'].value.startswith("sprite"):
                    # sprite subgroup detected
                    newrecord = {}
                    newrecord['desc'] = ""
                    newrecord["title"] = ""
                    newrecord["options"] = ""
                    newrecord['id'] = subgroup.attributes['id'].value
                    self.build_sprite(subgroup, newrecord)
                    record["group"].append(newrecord)
                    group.removeChild(subgroup)


        svgElements = ['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path', 'image', 'text', 'flowRoot']
        group_childs = []
        stackTransform = []
        self.linearize_childs(group, group_childs, stackTransform)

        for childentry in group_childs:
            childnode = childentry['node']
            if childnode.nodeName in svgElements:
                newrecord = getattr(self, 'extract_' + \
                                    childnode.nodeName)(childnode, childentry['transform'])
                if newrecord is not None:
                    record["group"].append(newrecord)
                    if record['desc'] == "": record['desc'] = newrecord['desc'] 
                    if record["title"] == "": record['title'] = newrecord['title'] 
                    minX = min(newrecord["minX"], minX)
                    minY = min(newrecord["minY"], minY)
                    maxX = max(newrecord["maxX"], maxX)
                    maxY = max(newrecord["maxY"], maxY)

        # look for title and description in subgroups if not yet available
        if (record['title'] == "") or (record['desc'] == ""):
            subgroups = group.getElementsByTagName('g')
            for subgroup in subgroups:
                if record['desc'] == "":
                    record['desc'] = self.getText("desc", subgroup)
                if record["title"] == "":
                    record['title'] = self.getText("title", subgroup)

        if record['title'] == "":
            if group.hasAttribute("inkscape:label"):
                record['title'] = group.attributes["inkscape:label"].value

        record["minX"] = minX
        record["minY"] = minY
        record["maxX"] = maxX
        record["maxY"] = maxY

        if record["group"]:
            return record

    def calculate_raster_ratio(self, raster, rasterWidth, rasterHeight):
        """modify image internal dimensions to fit raster ones"""
        dirname = tempfile.mkdtemp()
        #newraster = raster
        ratio = 1
        rasterStartPosition = raster.find('base64,') + 7
        rasterEncoded = raster[rasterStartPosition:]
        rasterPrefix = raster[0:rasterStartPosition]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                imageFile = dirname + os.path.sep + "image." + extension.group(1)
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(base64.b64decode(rasterEncoded))

                if not HANDLE_PIL:
                    w = self.getImageWidthDarwin(imageFile)
                else:
                    with open(imageFile, 'rb') as f:
                        currentImg = Image.open(f)
                        w, _ = currentImg.size
                ratio = float(w) / float(rasterWidth)

        else:
            self.console.display('ERROR : fixRaster() - image is not embedded')
        shutil.rmtree(dirname)
        return ratio

    def resizeImageWidthDarwin(self, height, width, imageFile):
        """resize image with SIPS for MACOS X users"""
        p1 = Popen([f"sips -z {height} {width} {imageFile}"], shell=True, stdout=PIPE)
        p1.communicate()

    def getImageWidthDarwin(self, imageFile):
        """extract image width with SIPS for MACOS X users"""
        p1 = Popen([f"sips -g pixelWidth {imageFile} | grep pixelWidth | awk '{{print $2}}'"], shell=True, stdout=PIPE)
        w, _ = p1.communicate()
        w = int(w.decode().rstrip('\n'))
        return w

    def cropImage(self, raster, rasterWidth, rasterHeight):
        """crop image to remove useless transparent pixels"""
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
                imageFileSmall = dirname + os.path.sep + "image_small.png"
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(base64.b64decode(rasterEncoded))

                if HANDLE_PIL:
                    with open(imageFile, 'rb') as f:
                        im = Image.open(f, 'r')
                        im = im.convert("RGBA")
                        red, green, blue, alpha = im.split()
                        (w, h) = im.size

                        alpha_threshold = 20
                        y_delta = 0
                        stop_scan = 0
                        for y in range(h):
                            for x in range(w):
                                transparency = max(alpha.getpixel((x,y)) - alpha_threshold, 0)
                                if transparency != 0:
                                    stop_scan = 1
                                    break
                            if stop_scan:
                                break
                            else:
                                y_delta += 1

                        y_delta2 = 0
                        stop_scan = 0
                        for y in range(h - 1, 0, -1):
                            for x in range(w - 1, 0, -1):
                                transparency = max(alpha.getpixel((x,y)) - alpha_threshold, 0)
                                if transparency != 0:
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
                                transparency = max(alpha.getpixel((x,y)) - alpha_threshold, 0)
                                if transparency != 0:
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
                                transparency = max(alpha.getpixel((x,y)) - alpha_threshold, 0)
                                if transparency != 0:
                                    stop_scan = 1
                                    break
                            if stop_scan:
                                break
                            else:
                                x_delta2 += 1

                        croppedBg = im.crop((min(x_delta,w - x_delta2), min(y_delta,h - y_delta2), \
                                             max(x_delta,w - x_delta2), max(y_delta,h - y_delta2)))
                        croppedBg.save(imageFileSmall)

                    with open(imageFileSmall, 'rb') as bgSmallImage:
                        rasterSmallEncoded = base64.b64encode(bgSmallImage.read()).decode()
                        newraster = rasterPrefix + \
                                    rasterSmallEncoded
                    newrasterHeight = int((h - y_delta2 - y_delta) * float(rasterHeight) / h)
                    newrasterWidth = int((w - x_delta - x_delta2) * float(rasterWidth) / w)

        else:
            self.console.display('ERROR : cropImage() - image is not embedded ' + raster)
        shutil.rmtree(dirname)

        return [newraster, newrasterWidth, newrasterHeight, x_delta * float(rasterWidth) / w, y_delta * float(rasterHeight) / h, w, h]

    def rotateImage(self, raster, angle, x, y):
        """
        if needed, we must rotate image to be usable
        input:
          angle: rotation angle (radius)
          x,y: rotation center
        """
        angle = angle * 180 / math.pi
        dirname = tempfile.mkdtemp()
        newraster = raster
        rasterStartPosition = raster.find('base64,') + 7
        rasterEncoded = raster[rasterStartPosition:]
        rasterPrefix = raster[0:rasterStartPosition]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                imageFile = dirname + os.path.sep + "image." + extension.group(1)
                imageFileSmall = dirname + os.path.sep + "image_small.png"
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(base64.b64decode(rasterEncoded))

                if HANDLE_PIL:
                    with open(imageFile, 'rb') as f:
                        currentImage = Image.open(f)
                        rotatedImage = currentImage.rotate( (-1) * angle, expand=1 )
                        rotatedImage.save(imageFileSmall)

                    with open(imageFileSmall, 'rb') as bgSmallImage:
                        rasterSmallEncoded = base64.b64encode(bgSmallImage.read()).decode()
                        newraster = rasterPrefix + rasterSmallEncoded

                    newrasterWidth, newrasterHeight = rotatedImage.size
        else:
            self.console.display('ERROR : image is not embedded')
        shutil.rmtree(dirname)
        return [newraster, newrasterWidth, newrasterHeight]


    def get_dimensions(self,raster):
        """extract width and height from base64 raster"""
        dirname = tempfile.mkdtemp()
        width = height = 0
        success = False
        start_pos = raster.find('base64,') + 7
        rasterEncoded = raster[start_pos:]
        rasterPrefix = raster[0:start_pos]
        extension = re.search('image/(.*);base64', rasterPrefix)
        if extension is not None:
            if extension.group(1):
                if HANDLE_PIL:
                    imageFile = dirname + os.path.sep + "image." + extension.group(1)
                    with open(imageFile, "wb") as bgImage:
                        bgImage.write(base64.b64decode(rasterEncoded))
                    with open(imageFile, 'rb') as f:
                        im = Image.open(f)
                        width, height = im.size
                        success = True
        shutil.rmtree(dirname)
        return width, height, success

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
                imageFileSmall = dirname + os.path.sep + "image2.png"
                with open(imageFile, "wb") as bgImage:
                    bgImage.write(base64.b64decode(rasterEncoded))

                if not HANDLE_PIL:
                    oldwidth = int(float(rasterWidth))
                    oldheight = int(float(rasterHeight))
                    newwidth = int(oldwidth * self.ratio)
                    newheight = int(oldheight * self.ratio)
                    shutil.copyfile(imageFile, imageFileSmall)
                    self.resizeImageWidthDarwin(newheight, newwidth, imageFileSmall)

                    with open(imageFileSmall, 'rb') as bgSmallImage:
                        rasterSmallEncoded = bgSmallImage.read().encode("base64")
                        newraster = rasterPrefix + rasterSmallEncoded

                    newrasterWidth = newwidth
                    newrasterHeight = newheight

                else:
                    # "Platform Linux or Windows : resizing using PIL"
                    with open(imageFile, 'rb') as f:
                        currentBg = Image.open(f)
                        currentBg.convert('RGBA')
                        oldwidth = int(float(rasterWidth))
                        oldheight = int(float(rasterHeight))
                        newwidth = int(oldwidth * self.ratio)
                        newheight = int(oldheight * self.ratio)
                        resizedBg = currentBg.resize((newwidth, newheight), Image.ANTIALIAS)
                        resizedBg.save(imageFileSmall)
                        with open(imageFileSmall, 'rb') as bgSmallImage:
                            rasterSmallEncoded = base64.b64encode(bgSmallImage.read()).decode()
                            newraster = rasterPrefix + rasterSmallEncoded

                        newrasterWidth = newwidth
                        newrasterHeight = newheight
        else:
            self.console.display('ERROR : image is not embedded')
        shutil.rmtree(dirname)
        return [newraster, newrasterWidth, newrasterHeight]


    def generateJSON(self):
        """ generate json file"""
        final_str = ""
        final_str += 'var scene = {\n'
        for entry in self.scene:
            if entry == "image":
                final_str += '"' + entry + '":"' + \
                             self.scene[entry]. \
                                 replace("\n", ""). \
                                 replace("\t", ""). \
                                 replace("\r", "") + '",\n'
            elif entry == 'group':
                final_str += self.generateJSONGroup(self.scene['group']['group'])
            else:
                final_str += '"' + entry + '":"' + \
                             PageFormatter(self.scene[entry]).print_html(). \
                                 replace('"', "'"). \
                                 replace("\n", " "). \
                                 replace("\t", " "). \
                                 replace("\r", " ") + '",\n'
        final_str += '};\n'

        final_str += 'var details = [\n'
        for detail in self.details:
            final_str += '{\n'
            for entry in detail:
                if entry == "group":
                    final_str += self.generateJSONGroup(detail['group'])
                elif entry == "path":
                    final_str += '  "' + entry + '":' + detail[entry] + ',\n'
                elif entry == "image":
                    final_str += '  "' + entry + '":"' + detail[entry]. \
                        replace('"', "'"). \
                        replace("\n", " "). \
                        replace("\t", " "). \
                        replace("\r", " ") + '",\n'
                elif entry == "desc":
                    final_str += '  "' + entry + '":"' + \
                                 PageFormatter(detail[entry]).print_html(). \
                                     replace('"', "'"). \
                                     replace("\n", " "). \
                                     replace("\t", " "). \
                                     replace("\r", " ") + \
                                 '",\n'
                else:
                    if type(detail[entry]) is not str:
                        detail[entry] = str(detail[entry])
                    final_str += '  "' + entry + '":"' + \
                                 detail[entry]. \
                                     replace('"', "'"). \
                                     replace('\t', " "). \
                                     replace('\r', " "). \
                                     replace('\n', " ") + \
                                 '",\n'
            final_str += '},\n'
        final_str += '];\n'
        self.jsonContent = final_str

    def generateJSONGroup(self, group):
        """ generate json file"""
        final_str = ""
        final_str += '  "group": [\n'
        for element in group:
            final_str += '  {\n'
            for entry2 in element:
                if entry2 == "path":
                    final_str += '  "' + entry2 + '":' + \
                                 element[entry2]. \
                                     replace('"', "'"). \
                                     replace("\n", " "). \
                                     replace("\t", " "). \
                                     replace("\r", " ") + ',\n'
                elif entry2 == "image" or entry2 == "title" or entry2 == "fill" or entry2 == "style":
                    final_str += '  "' + entry2 + '":"' + \
                                 element[entry2]. \
                                     replace('"', "'"). \
                                     replace("\n", " "). \
                                     replace("\t", " "). \
                                     replace("\r", " ") + '",\n'
                else:
                    final_str += '      "' + entry2 + '":"' + \
                                 PageFormatter(element[entry2]).print_html(). \
                                     replace('"', "'"). \
                                     replace("\n", " "). \
                                     replace("\t", " "). \
                                     replace("\r", " ") + '",\n'
            final_str += '  },\n'
        final_str += '  ],\n'

        return final_str
