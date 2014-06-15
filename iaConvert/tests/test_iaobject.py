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

from iaConvert.ia2.iaobject import iaObject
from nose.tools import *
from xml.dom import minidom
import tempfile

class TestiaObject:
    def test_analyzeSVG(self):
        ia = iaObject()
        ia.analyzeSVG("tests/fixtures/inkscape1.svg")
        assert_equal(ia.scene['width'],'500')
        assert_equal(ia.scene['height'],'500')
        assert_equal(ia.scene['image'],'data:image/png;base64,Q3VyaW9zaXR5IGtpbGxlZCB0aGUgY2F0')
        assert_equal(ia.scene['creator'],'creator')
        assert_equal(ia.scene['description'],'description')
        assert_equal(ia.scene['title'],'fixture 1')
        
        ia = iaObject()
        ia.analyzeSVG("tests/fixtures/generic1.svg")
        assert_equal(ia.scene['width'],'10')
        assert_equal(ia.scene['height'],'10')
        assert_equal(ia.details[0]['width'],'152')
        assert_equal(ia.details[0]['height'],'161')
        
        
        # check get_tag_value output
        ia = iaObject()        
        dom1 = minidom.parseString("<?xml version='1.0' ?><desc>description</desc>")
        desc = dom1.getElementsByTagName('desc')
        assert_equal("description",ia.get_tag_value(desc[0]))

        # check root path
        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?><svg><path d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' /></svg>")
        path = dom1.getElementsByTagName('path')
        newrecord = ia.extract_path(path[0])
        assert_equal(newrecord['path'],'"M0.0 0.0C0.0 0.0 10.0 0.0 10.0 0.0C10.0 0.0 10.0 10.0 10.0 10.0C10.0 10.0 0.0 10.0 0.0 10.0C0.0 10.0 0.0 0.0 0.0 0.0C0.0 0.0 0.0 0.0 0.0 0.0 z"')
        assert_equal(newrecord['maxX'],'10.0')
        assert_equal(newrecord['maxY'],'10.0')
        assert_equal(newrecord['minX'],'0.0')
        assert_equal(newrecord['minY'],'0.0')
        assert_equal(newrecord['x'],'0')
        assert_equal(newrecord['y'],'0')

        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?><svg><path transform='translate(10)' x='10' y='30' d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' /></svg>")
        path = dom1.getElementsByTagName('path')
        newrecord = ia.extract_path(path[0])
        assert_equal(newrecord['path'],'"M10.0 10.0C10.0 10.0 20.0 10.0 20.0 10.0C20.0 10.0 20.0 20.0 20.0 20.0C20.0 20.0 10.0 20.0 10.0 20.0C10.0 20.0 10.0 10.0 10.0 10.0C10.0 10.0 10.0 10.0 10.0 10.0 z"')
        assert_equal(newrecord['maxX'],'20.0')
        assert_equal(newrecord['maxY'],'20.0')
        assert_equal(newrecord['minX'],'10.0')
        assert_equal(newrecord['minY'],'10.0')
        assert_equal(newrecord['x'],'10')
        assert_equal(newrecord['y'],'30')

        # check path included in a group
        ia = iaObject()
        dom1 = minidom.parseString("<?xml version='1.0' ?><g><path transform='translate(10)' x='10' y='30' d='M 0,0 L 10,0 L 10,10 L 0,10 L 0,0 z' /></g>")
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0])
        assert_equal(newrecord["group"][0]['path'],'"M10.0 10.0C10.0 10.0 20.0 10.0 20.0 10.0C20.0 10.0 20.0 20.0 20.0 20.0C20.0 20.0 10.0 20.0 10.0 20.0C10.0 20.0 10.0 10.0 10.0 10.0C10.0 10.0 10.0 10.0 10.0 10.0 z"')
        assert_equal(newrecord["group"][0]['maxX'],'20.0')
        assert_equal(newrecord["group"][0]['maxY'],'20.0')
        assert_equal(newrecord["group"][0]['minX'],'10.0')
        assert_equal(newrecord["group"][0]['minY'],'10.0')
        assert_equal(newrecord["group"][0]['x'],'10')
        assert_equal(newrecord["group"][0]['y'],'30')
        
        # check image included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?><svg xmlns:xlink="http://www.w3.org/1999/xlink"><g><image xlink:href="file:///path/to/image.png" width="50" height="50"></image></g></svg>')
        group = dom1.getElementsByTagName('g')
        ia.backgroundNode = 0
        newrecord = ia.extract_g(group[0])
        assert_equal(newrecord["group"][0]['x'],'0')
        assert_equal(newrecord["group"][0]['y'],'0')        
        assert_equal(newrecord["group"][0]['width'],'50')
        assert_equal(newrecord["group"][0]['height'],'50')                

        # check rect included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?><svg><g><rect width="50" height="50"></rect></g></svg>')
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0])
        assert_equal(newrecord["group"][0]['x'],'0')
        assert_equal(newrecord["group"][0]['y'],'0')        
        assert_equal(newrecord["group"][0]['width'],'50')
        assert_equal(newrecord["group"][0]['height'],'50')                


        # check groups included in a group
        ia = iaObject()
        dom1 = minidom.parseString('<?xml version="1.0" ?><svg><g><rect width="50" height="50"></rect><g><desc>description</desc><title>title</title></g></g></svg>')
        group = dom1.getElementsByTagName('g')
        newrecord = ia.extract_g(group[0])
        assert_equal(newrecord['detail'],'description')
        assert_equal(newrecord['title'],'title')
               

        temp = tempfile.NamedTemporaryFile()
        ia = iaObject()
        ia.analyzeSVG("tests/fixtures/generic1.svg")
        ia.generateJSON(temp.name)
        temp_content = temp.read()
        #with open('tests/fixtures/temp.js', 'w') as js:
        #    js.write(temp_content)
        with open('tests/fixtures/generic1.js') as js:
            assert_equal(js.read(),temp_content)
