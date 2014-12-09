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
        assert_equal(ia.scene['width'], '50')
        assert_equal(ia.scene['height'], '50')
        assert_equal(ia.scene['image'], 'data:image/png;base64,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\n')
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
        assert_equal(ia.details[0]['width'], '152')
        assert_equal(ia.details[0]['height'], '161')

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
                        xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=="\
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
