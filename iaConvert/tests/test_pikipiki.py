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

from iaConvert.ia2.pikipiki import PageFormatter
from nose.tools import *

class TestPageFormatter:

    def test_print_html(self):
        raw = "**text**";
        expected_output = "<em>text</em>";
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "***text***";
        expected_output = "<b>text</b>";
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "{{{text}}}";
        expected_output = "<pre>\ntext</pre>\n";
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)
        
        raw = "photo.jpg";
        expected_output = '<img src="photo.jpg">\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)        

        raw = "photo.jpeg";
        expected_output = '<img src="photo.jpeg">\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output) 

        raw = "photo.png";
        expected_output = '<img src="photo.png">\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output) 
        
        raw = "photo.gif";
        expected_output = '<img src="photo.gif">\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output) 

        raw = "admin@test.com";
        expected_output = '<a href="mailto:admin@test.com">admin@test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "<&>";
        expected_output = '&lt;&amp;&gt;';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "----";
        expected_output = '\n<hr>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "-----";
        expected_output = '\n<hr size=3>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        #raw = '&lt;iframe src="test.html"&gt;&lt;/iframe&gt;';
        #expected_output = '<iframe src="test.html" width="100%"></iframe>\n';
        #output = PageFormatter(raw).print_html()
        #assert_equal(expected_output, output)         

        raw = "http://test.com";
        expected_output = '<a href="http://test.com" target="_blank">http://test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "ftp://test.com";
        expected_output = '<a href="ftp://test.com" target="_blank">ftp://test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "nntp://test.com";
        expected_output = '<a href="nntp://test.com" target="_blank">nntp://test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "news://test.com";
        expected_output = '<a href="news://test.com" target="_blank">news://test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "mailto://test.com";
        expected_output = '<a href="mailto://test.com" target="_blank">mailto://test.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         
        
        raw = " * line 1\n * line2";
        expected_output = '<ul>\n<li> line 1</li>\n<li> line2</li>\n</ul>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)
        


