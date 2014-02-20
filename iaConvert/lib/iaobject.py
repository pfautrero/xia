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

from xml.dom import minidom
from lib.pikipiki import PageFormatter
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
        groups = self.xml.getElementsByTagName('g')

        head, tail = os.path.split(filePath)
        
        self.scene['intro_title'] = u"Description"
        self.scene['intro_detail'] = u"Image Active - Canopé Versailles"
        self.scene['image'] = "datas/background.jpg"
        self.scene['width'] = ""
        self.scene['height'] = ""
        self.scene['title'] = os.path.splitext(tail)[0]

        # ==================== Look for images

        images = self.xml.getElementsByTagName('image')
        print "NB IMAGES = " + str(images.length)
        if images.length is not 0:
            for index, image in enumerate(images):
                if index == 0:
                    # first image is considered as background image
                    self.scene['width'] = image.attributes['width'].value
                    self.scene['height'] =  image.attributes['height'].value

                    desc = image.getElementsByTagName('desc')
                    if desc.item(0) is not None:
                        if desc.item(0).parentNode == image:
                            self.scene['intro_detail'] = self.get_tag_value(desc.item(0)).replace("\n","<br>").replace("\t"," ").replace("\r"," ")

                    title = image.getElementsByTagName('title')
                    if title.item(0) is not None:
                        if title.item(0).parentNode == image:
                            self.scene['intro_title'] = self.get_tag_value(title.item(0)).replace("\n","<br>").replace("\t"," ").replace("\r"," ")

                    self.raster = image.attributes['xlink:href'].value
                    self.scene['image'] = image.attributes['xlink:href'].value
                else:
                    # other images are considered as details
                    record = {}
                    record['width'] = image.attributes['width'].value
                    record['height'] =  image.attributes['height'].value
                    record['detail'] = ""
                    record['title'] = ""
                    desc = image.getElementsByTagName('desc')
                    if desc.item(0) is not None:
                        if desc.item(0).parentNode == image:
                            record['detail'] = self.get_tag_value(desc.item(0))

                    title = image.getElementsByTagName('title')
                    if title.item(0) is not None:
                        if title.item(0).parentNode == image:
                            record['title'] = self.get_tag_value(title.item(0))

                    record['image'] = image.attributes['xlink:href'].value

                    if image.hasAttribute("x") and image.hasAttribute("y"):
                        record['x'] = image.attributes['x'].value
                        record['y'] = image.attributes['y'].value
                    elif image.hasAttribute("transform"):
                        print "1"
                        matrix = image.attributes['transform'].value
                        m = matrix[matrix.find('(')+1:matrix.find(')')].split(" ")
                        record['x'] = m[4]
                        record['y'] = m[5]                        
                    else:
                        record['x'] = str(0)
                        record['y'] = str(0)                        

                    self.details.append(record)

        # ==================== Look for paths not included in groups

        paths = self.xml.getElementsByTagName('path')
        self.analyzeRootPaths(paths)

        # ==================== Look for paths in groups root
        for group in groups:
            if group.parentNode.nodeName == "svg":
                self.analyzeGroup(group)


    def analyzeRootPaths(self,paths):
        """Analyze paths not included in a specific group"""
        
        if paths.length is not 0:
            
            for path in paths:
                print "Root path detected"
                if path.parentNode.nodeName == "svg":
                    record = {}
                    record["title"] = ""
                    record["detail"] = ""
                    record["path"] = "["
                    record["fill"] = ""
                    record["path"] += '"' + path.attributes['d'].value.replace("&#xd;&#xa;"," ").replace("&#x9;"," ").replace("\n"," ").replace("\t"," ").replace("\r"," ") 
                    record["style"] = ""

                    if path.attributes['d'].value.lower().find("z") == -1:
                        record["path"] += " z"
                    record['path'] += '"'
            
                    desc = path.getElementsByTagName('desc')
                    if desc.item(0) is not None:
                        if record["detail"] == "":
                            record["detail"] = self.get_tag_value(desc.item(0))
            
                    title = path.getElementsByTagName('title')
                    if title.item(0) is not None:
                        if record["title"] == "":
                            record["title"] = self.get_tag_value(title.item(0)).replace("\n"," ").replace("\t"," ").replace("\r"," ")
            
                    if path.hasAttribute("style"):
                        str_style = path.attributes['style'].value
                        style = {}
                        for item in str_style.split(";"):
                            key,value = item.split(":")
                            style[key] = value

                        record["fill"] = style['fill']
                    record["path"] += "]"
                    if (record["path"] != "["):
                        self.details.append(record)

    def analyzeGroup(self,group):
        """Analyze a svg group"""

        record = {}
        record["title"] = ""
        record["detail"] = ""
        record["path"] = "["
        record["fill"] = ""

        desc = group.getElementsByTagName('desc')
        if desc.item(0) is not None:
            if desc.item(0).parentNode == group:
                #print "DESC = " + self.get_tag_value(desc.item(0))
                record["detail"] = self.get_tag_value(desc.item(0))
        title = group.getElementsByTagName('title')
        if title.item(0) is not None:
            if title.item(0).parentNode == group:
                #print "TITLE = " + self.get_tag_value(title.item(0))
                record["title"] = self.get_tag_value(title.item(0))

        paths = group.getElementsByTagName('path')        
        subgroups = group.getElementsByTagName('g')
        # if current group is named or if it is a leaf
        # retrieve all its paths (even if they are in subgroups)
        if (record["title"] != "") or (record["detail"] != "") or (subgroups.length is 0): 
            if paths.length is not 0:
                for path in paths:
                    #if path.parentNode == group:
                    if record["path"] != "[":
                        record["path"] += ","
                    record["path"] += '"' + path.attributes['d'].value.replace("&#xd;&#xa;"," ").replace("&#x9;"," ").replace("\n"," ").replace("\t"," ").replace("\r"," ") 
                    if path.attributes['d'].value.lower().find("z") == -1:
                        record["path"] += " z"
                    record['path'] += '"'
                    desc = path.getElementsByTagName('desc')
                    if desc.item(0) is not None:
                        #print "DESC = " + self.get_tag_value(desc.item(0))
                        if record["detail"] == "":
                            record["detail"] = self.get_tag_value(desc.item(0))
                    title = path.getElementsByTagName('title')
                    if title.item(0) is not None:
                        #print "TITLE = " + self.get_tag_value(title.item(0))
                        if record["title"] == "":
                            record["title"] = self.get_tag_value(title.item(0)).replace("\n"," ").replace("\t"," ").replace("\r"," ")
                    if path.hasAttribute("style"):                            
                        str_style = path.attributes['style'].value
                        style = {}
                        for item in str_style.split(";"):
                            key,value = item.split(":")
                            style[key] = value

                        record["fill"] = style['fill']
                record["path"] += "]"
            if (record["path"] != "["):
                self.details.append(record)
        # if current group is unamed and contains subgroups
        # analyze each subgroup
        # if current group contains direct paths, they are not retrieved !
        elif subgroups.length is not 0:
            for subgroup in subgroups:
                self.analyzeGroup(subgroup)


    def generateJSON(self,filePath):
        """ generate json file"""
        final_str = ""

        final_str += 'var scene = {\n'
        for entry in self.scene:
            final_str += '"' + entry + '":"' + self.scene[entry].encode('utf-8') + '",\n'
        final_str += '};\n'

        final_str += 'var details = [\n'
        for detail in self.details:
            final_str += '{\n'
            for entry in detail:
                if entry == "path":
                    final_str += '"' + entry + '":' + detail[entry].encode('utf-8') + ',\n'
                elif entry == "detail":
                    final_str += '"' + entry + '":"' + PageFormatter(detail[entry]).print_html().encode('utf-8').replace('"', "'") + '",\n'
                else:
                    final_str += '"' + entry + '":"' + detail[entry].encode('utf-8') + '",\n'
            final_str += '},\n'
        final_str += '];\n'

        with open(filePath,"w") as jsonfile:
            jsonfile.write(final_str)


    def createBackground(self,filePath):
        """if raster is included in svg file, generate file from that raster"""
        if self.raster != "":
            if self.raster.find("base64,"):
                self.raster = self.raster[self.raster.find("base64,")+7:]
                if self.raster.find("image/png"):
                    self.scene['image'] = filePath +"/background.png"
                if self.raster.find("image/jpeg"):
                    self.scene['image'] = filePath + "/background.jpg"
                with open(self.scene['image'],"w") as image:
                    image.write(self.raster.decode('base64','strict'))
        

    def generateAccordion(self,filePath):
        """ generate accordion index file"""

        final_str  = '<!DOCTYPE html>\n'
        final_str += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
        final_str += '<head>\n'
        final_str += '  <meta charset="utf-8"/>\n'
        final_str += '  <link rel="stylesheet" type="text/css" href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.no-icons.min.css"/>\n'
        final_str += '  <link rel="stylesheet" type="text/css" href="css/main.css"/>\n'
        final_str += '</head>\n'
        final_str += '<body>\n'
        final_str += '  <div id="container">\n'
        final_str += '      <div id="detect"></div>\n'
        final_str += '      <h3 id="title">' + self.scene["title"].encode('utf-8') + '</h3>\n'
        final_str += '      <div class="accordion" id="accordion2">\n'
        final_str += '          <div class="accordion-group">\n';
        final_str += '              <div class="accordion-heading">\n';
        final_str += '                  <a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">' + self.scene["intro_title"].encode("utf-8") + '</a>\n';
        final_str += '                  <div id="collapsecomment" class="accordion-body collapse">\n';
        final_str += '                      <div class="accordion-inner">' + PageFormatter(self.scene["intro_detail"].encode('utf-8')).print_html() + '\n';
        final_str += '                      </div>\n'
        final_str += '                  </div>\n'
        final_str += '              </div>\n'
        final_str += '          </div>\n'
        for i, detail in enumerate(self.details):
            if detail['detail'].encode("utf-8").find("Réponse:") != -1:
                question = detail['detail'][0:detail['detail'].encode("utf-8").find("Réponse:")-1].encode("utf-8")
                answer = detail['detail'][detail['detail'].encode("utf-8").find("Réponse:")+8:].encode("utf-8")
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8")+'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + PageFormatter(question).print_html() + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+str(i)+'">Réponse</a></div>' + '<div class="response" id="response_'+ str(i) +'">' + PageFormatter(answer).print_html() + '</div>' + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'
            else:
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8") +'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + PageFormatter(detail["detail"].encode('utf-8')).print_html() + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'

        final_str += '      </div>\n'
        final_str += '      <div id="canvas"></div>\n'
        final_str += '  </div>\n'
        final_str += '  <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>\n'
        final_str += '  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>\n'
        final_str += '  <script src="js/kinetic.js"></script>\n'
        final_str += '  <script src="datas/data.js"></script>\n'
        final_str += '  <script defer="defer" src="js/main.js"></script>\n'
        final_str += '</body>\n'
        final_str += '</html>'
        with open(filePath,"w") as indexfile:
            indexfile.write(final_str)

