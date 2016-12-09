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
from xiaconverter.logger import Logger
from nose.tools import *
from xml.dom import minidom
import tempfile
import os

class LoggerMock(Logger):
    def display(self, msg):
        pass

class TestiaObject:

    def test_extractRaster(self):
        console = LoggerMock()
        ia = iaObject(console)
        # XIA logo 16x16
        originalRaster = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=='
        rasterExtracted = ia.extractRaster(originalRaster)
        assert_equal(rasterExtracted, originalRaster)

    def test_fixRaster(self):
        console = LoggerMock()
        ia = iaObject(console)
        # XIA logo 16x16
        originalRaster = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=='
        rasterFixed = ia.fixRaster(originalRaster, 16, 16)
        assert_equal(rasterFixed, originalRaster)


    def test_imageDimensions(self):
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
        ia.analyzeSVG(tempSvg.name, maxNumPixels)

        assert_equal(ia.scene['width'], '10')
        assert_equal(ia.scene['height'], '10')
        assert_equal(ia.details[0]['width'], 205.97977516275924)
        assert_equal(ia.details[0]['height'], 210.30661948701845)

    def test_analyzeSVG3(self):
        console = LoggerMock()
        ia = iaObject(console)
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <desc>description</desc>")
        desc = dom1.getElementsByTagName('desc')
        assert_equal("description", ia.get_tag_value(desc[0]))

        ia = iaObject(console)
        dom1 = minidom.parseString("<?xml version='1.0' ?><desc></desc>")
        desc = dom1.getElementsByTagName('desc')
        assert_equal("",ia.get_tag_value(desc[0]))

    def test_analyzeSVG4(self):

        # check root path
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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

        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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
        console = LoggerMock()
        ia = iaObject(console)
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

    def test_analyzeSVG10(self):

        # check invalid path
        console = LoggerMock()
        ia = iaObject(console)
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <svg>\
                <path d='' />\
            </svg>")
        path = dom1.getElementsByTagName('path')
        newrecord = ia.extract_path(path[0], "")
        assert_equal(newrecord, None)

    def test_analyzeSVG11(self):

        # check invalid rectangle
        console = LoggerMock()
        ia = iaObject(console)
        dom1 = minidom.parseString("<?xml version='1.0' ?>\
            <svg>\
                <rect width='' height='' />\
            </svg>")
        detail = dom1.getElementsByTagName('rect')
        newrecord = ia.extract_rect(detail[0], "")
        assert_equal(newrecord, None)


    def test_analyzeSVG12(self):

        # must resist if style is void
        console = LoggerMock()
        ia = iaObject(console)
        dom1 = minidom.parseString('<?xml version="1.0" ?> \
            <svg xmlns:xlink="http://www.w3.org/1999/xlink">\
                <g>\
                    <image \
                        xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=="\
                        width="50"\
                        height="50"\
                        style="">\
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

    def test_generateJSON(self):

        # check generateJSON
        tempDirSvg = tempfile.gettempdir()
        maxNumPixels = 5 * 1024 * 1024
        currentDir  = os.path.dirname(os.path.realpath(__file__))
        with open(currentDir + "/fixtures/generic1.svg", "r") as genericSvg:
            tempContent = genericSvg.read()
            tempContent = tempContent.replace("file://fixtures", "file://" + currentDir + "/fixtures")

        with open(tempDirSvg + "/generic1.svg", "w") as tempSvg:
            tempSvg.write(tempContent)

        console = LoggerMock()
        ia = iaObject(console)
        ia.analyzeSVG(tempSvg.name, maxNumPixels)

        ia.generateJSON()
        temp_content = ia.jsonContent
        #with open(currentDir + '/fixtures/temp.js', 'w') as js:
        #    js.write(temp_content)
        with open(currentDir + '/fixtures/generic1.js') as js:
            assert_equal(js.read(),temp_content)
