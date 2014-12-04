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

from xiaconverter.iaobject import iaObject
from nose.tools import *
from xml.dom import minidom
import tempfile
import os
import tempfile

class TestiaObject:
    def test_analyzeSVG(self):
        ia = iaObject()
        maxNumPixels = 5 * 1024 * 1024
        currentDir  = os.path.dirname(os.path.realpath(__file__))
        ia.analyzeSVG(currentDir + "/fixtures/inkscape1.svg", maxNumPixels)
        assert_equal(ia.scene['width'], '500')
        assert_equal(ia.scene['height'], '500')
        assert_equal(ia.scene['image'], 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg==')
        assert_equal(ia.scene['creator'], 'creator')
        assert_equal(ia.scene['description'], 'description')
        assert_equal(ia.scene['title'], 'fixture 1')

    def test_analyzeSVG2(self):

        tempDirSvg = tempfile.gettempdir()
        maxNumPixels = 5 * 1024 * 1024
        currentDir  = os.path.dirname(os.path.realpath(__file__))
        with open(currentDir + "/fixtures/generic1.svg", "r") as genericSvg:
            tempContent = genericSvg.read()
            tempContent = tempContent.replace("file://fixtures", "file://" + currentDir + "/fixtures")

        with open(tempDirSvg + "/generic1.svg", "w") as tempSvg:
            tempSvg.write(tempContent)

        ia = iaObject()
        ia.analyzeSVG(tempSvg.name, maxNumPixels)
        
        assert_equal(ia.scene['width'], '10')
        assert_equal(ia.scene['height'], '10')
        assert_equal(ia.details[0]['width'], '100')
        assert_equal(ia.details[0]['height'], '100')

    def test_analyzeSVG3(self):

        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <desc>description</desc>")
        desc = dom1.getElementsByTagName('desc')
        assert_equal("description", ia.get_tag_value(desc[0]))

        ia = iaObject()        
        dom1 = minidom.parseString("<?xml version='1.0' ?><desc></desc>")
        desc = dom1.getElementsByTagName('desc')
        assert_equal("",ia.get_tag_value(desc[0]))

    def test_analyzeSVG4(self):

        # check root path
        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <svg>\
                <path d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' />\
            </svg>")
        path = dom1.getElementsByTagName('path')
        newrecord = ia.extract_path(path[0], "")
        assert_equal(newrecord['path'], '"M0.0 0.0C0.0 0.0 10.0 0.0 10.0 0.0C10.0 0.0 10.0 10.0 10.0 10.0C10.0 10.0 0.0 10.0 0.0 10.0C0.0 10.0 0.0 0.0 0.0 0.0C0.0 0.0 0.0 0.0 0.0 0.0 z"')
        assert_equal(newrecord['maxX'], '10.0')
        assert_equal(newrecord['maxY'], '10.0')
        assert_equal(newrecord['minX'], '0.0')
        assert_equal(newrecord['minY'], '0.0')
        assert_equal(newrecord['x'], '0')
        assert_equal(newrecord['y'], '0')

    def test_analyzeSVG4(self):

        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <svg>\
                <path \
                    transform='translate(10)'\
                    x='10'\
                    y='30'\
                    d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' />\
            </svg>")
        path = dom1.getElementsByTagName('path')
        newrecord = ia.extract_path(path[0], "")
        assert_equal(newrecord['path'], '"M10.0 10.0C10.0 10.0 20.0 10.0 20.0 10.0C20.0 10.0 20.0 20.0 20.0 20.0C20.0 20.0 10.0 20.0 10.0 20.0C10.0 20.0 10.0 10.0 10.0 10.0C10.0 10.0 10.0 10.0 10.0 10.0 z"')
        assert_equal(newrecord['maxX'], '20.0')
        assert_equal(newrecord['maxY'], '20.0')
        assert_equal(newrecord['minX'], '10.0')
        assert_equal(newrecord['minY'], '10.0')
        assert_equal(newrecord['x'], '10')
        assert_equal(newrecord['y'], '30')

    def test_analyzeSVG4(self):

        # check path included in a group
        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <g>\
                <path \
                    transform='translate(10)'\
                    x='10'\
                    y='30'\
                    d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' />\
            </g>")
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0], "")
        assert_equal(newrecord["group"][0]['path'], '"M10.0 10.0C10.0 10.0 20.0 10.0 20.0 10.0C20.0 10.0 20.0 20.0 20.0 20.0C20.0 20.0 10.0 20.0 10.0 20.0C10.0 20.0 10.0 10.0 10.0 10.0C10.0 10.0 10.0 10.0 10.0 10.0 z"')
        assert_equal(newrecord["group"][0]['maxX'], '20.0')
        assert_equal(newrecord["group"][0]['maxY'], '20.0')
        assert_equal(newrecord["group"][0]['minX'], '10.0')
        assert_equal(newrecord["group"][0]['minY'], '10.0')
        assert_equal(newrecord["group"][0]['x'], '10')
        assert_equal(newrecord["group"][0]['y'], '30')

    def test_analyzeSVG5(self):

        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <g transform='rotate(40)'>\
                <path \
                    transform='rotate(10)' \
                    x='10' \
                    y='30' \
                    d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' />\
            </g>")
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0], "")
        assert_equal(newrecord["group"][0]['path'], '"M0.0 0.0C0.0 0.0 9.64966028492 -2.62374853704 9.64966028492 -2.62374853704C9.64966028492 -2.62374853704 12.273408822 7.02591174788 12.273408822 7.02591174788C12.273408822 7.02591174788 2.62374853704 9.64966028492 2.62374853704 9.64966028492C2.62374853704 9.64966028492 0.0 0.0 0.0 0.0C0.0 0.0 0.0 0.0 0.0 0.0 z"')
        assert_equal(newrecord["group"][0]['maxX'], '12.273408822')
        assert_equal(newrecord["group"][0]['maxY'], '9.64966028492')
        assert_equal(newrecord["group"][0]['minX'], '0.0')
        assert_equal(newrecord["group"][0]['minY'], '-2.62374853704')
        assert_equal(newrecord["group"][0]['x'], '10')
        assert_equal(newrecord["group"][0]['y'], '30')

    def test_analyzeSVG6(self):

        # check image included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?> \
            <svg xmlns:xlink="http://www.w3.org/1999/xlink">\
                <g>\
                    <image \
                        xlink:href="file:///path/to/image.png"\
                        width="50"\
                        height="50">\
                    </image>\
                </g>\
            </svg>')
        group = dom1.getElementsByTagName('g')
        ia.backgroundNode = 0
        newrecord = ia.extract_g(group[0], "")
        assert_equal(newrecord["group"][0]['x'],'0')
        assert_equal(newrecord["group"][0]['y'],'0')        
        assert_equal(newrecord["group"][0]['width'],'50')
        assert_equal(newrecord["group"][0]['height'],'50')                

    def test_analyzeSVG7(self):

        # check rect included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?>\
            <svg>\
                <g>\
                    <rect width="50" height="50"></rect>\
                </g>\
            </svg>')
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0], "")
        assert_equal(newrecord["group"][0]['x'], '0')
        assert_equal(newrecord["group"][0]['y'], '0')
        assert_equal(newrecord["group"][0]['width'], '50')
        assert_equal(newrecord["group"][0]['height'], '50')

    def test_analyzeSVG8(self):

        # check groups included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?> \
            <svg> \
                <g> \
                    <rect width="50" height="50"></rect> \
                    <g> \
                        <desc>description</desc> \
                        <title>title</title> \
                    </g> \
                </g> \
            </svg>')
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0], "")
        assert_equal(newrecord['detail'], 'description')
        assert_equal(newrecord['title'], 'title')

    def test_analyzeSVG9(self):

        # check metadatas
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?> \
            <svg \
                xmlns:dc="http://purl.org/dc/elements/1.1/" \
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" > \
                <metadata> \
                    <rdf:RDF> \
                        <dc:title>title</dc:title>\
                        <dc:date>16/06/2014</dc:date>\
                        <dc:creator><dc:title>creator</dc:title></dc:creator>\
                        <dc:rights><dc:title>GPL</dc:title></dc:rights>\
                        <dc:publisher><dc:title>publisher</dc:title></dc:publisher>\
                        <dc:language>FR</dc:language>\
                        <dc:subject>\
                            <rdf:li>keyword1</rdf:li>\
                            <rdf:li>keyword2</rdf:li>\
                        </dc:subject>\
                        <dc:contributor><dc:title>contributor</dc:title></dc:contributor>\
                    </rdf:RDF> \
                </metadata> \
            </svg>')
        ia.extractMetadatas(dom1)
        assert_equal(ia.scene['title'], 'title')
        assert_equal(ia.scene['date'], '16/06/2014')
        assert_equal(ia.scene['creator'], 'creator')
        assert_equal(ia.scene['rights'], 'GPL')
        assert_equal(ia.scene['publisher'], 'publisher')
        assert_equal(ia.scene['language'], 'FR')
        assert_equal(ia.scene['keywords'], 'keyword1,keyword2')
        assert_equal(ia.scene['contributor'], 'contributor')
        
        # check generateJSON
        #temp = tempfile.NamedTemporaryFile()
        #ia = iaObject()
        #ia.analyzeSVG(currentDir + "/fixtures/generic1.svg", maxNumPixels)
        #ia.generateJSON(temp.name)
        #temp_content = temp.read()
        #with open('fixtures/temp.js', 'w') as js:
        #    js.write(temp_content)
        #with open(currentDir + '/fixtures/generic1.js') as js:
        #    assert_equal(js.read(),temp_content)
