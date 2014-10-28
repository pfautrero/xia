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

from xiaconverter.pikipiki import PageFormatter
from nose.tools import *
import re

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

        raw = '&lt;iframe src=&quot;http://example.com&quot;&gt;&lt;/iframe&gt;';
        expected_output = '<div class="videoWrapper4_3" data-iframe="http://example.com"></div>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = '&lt;iframe width="560" height="315" src=&quot;//example.com&quot;&gt;&lt;/iframe&gt;';
        expected_output = '<div class="videoWrapper16_9" data-iframe="http://example.com"></div>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output) 

        raw = '<iframe width="560" height="315" src="//www.youtube.com/embed/ctXwWpMz44M" frameborder="0" allowfullscreen></iframe>';
        expected_output = '<div class="videoWrapper16_9" data-iframe="http://www.youtube.com/embed/ctXwWpMz44M"></div>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output) 

        raw = "http://example.com";
        expected_output = '<a href="http://example.com" target="_blank">http://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)  

        raw = "https://example.com";
        expected_output = '<a href="https://example.com" target="_blank">https://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "ftp://example.com";
        expected_output = '<a href="ftp://example.com" target="_blank">ftp://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "nntp://example.com";
        expected_output = '<a href="nntp://example.com" target="_blank">nntp://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "news://example.com";
        expected_output = '<a href="news://example.com" target="_blank">news://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         

        raw = "mailto://example.com";
        expected_output = '<a href="mailto://example.com" target="_blank">mailto://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)         
        
        raw = " * line 1\n * line2";
        expected_output = '<ul>\n<li>line 1</li><li>line2</li></ul>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = " * ***line 1***\n * [http://test line2]";
        expected_output = '<ul>\n<li><b>line 1</b></li><li><a href="http://test" target="_blank">line2</a></li></ul>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)
       
        raw = "   * line 1\n  * line2";
        expected_output = '<ul>\n<li>line 1</li></ul>\n<ul>\n<li>line2</li></ul>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)
        
        raw = "video.mp4";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "video.mp4 autostart";
        expected_output = '<video controls preload="none" data-state="autostart">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "video.ogv";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "video.webm";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "audio.mp3";
        expected_output = '<audio controls data-state="none">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "audio.ogg";
        expected_output = '<audio controls data-state="none">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "audio.mp3  autostart";
        expected_output = '<audio controls data-state="autostart">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "audio.ogg    autostart";
        expected_output = '<audio controls data-state="autostart">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)


        raw = "[http://example.com A small test]";
        expected_output = '<a href="http://example.com" target="_blank">A small test</a>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "[http://example.com]";
        expected_output = '<a href="http://example.com" target="_blank">http://example.com</a>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "[../index.html test]";
        expected_output = '<a href="../index.html" target="_blank">test</a>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "[./index.html test]";
        expected_output = '<a href="./index.html" target="_blank">test</a>';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = " ";
        expected_output = '<br>\n';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "}}}";
        expected_output = '';
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)

        raw = "[[answer : my answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#"  data-target="##">answer </a></div><div class="response" id="response_##"><ul>\n my answer</div>\n</ul>';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        assert_equal(expected_output, output)

        raw = "[[answer (code=123456):\nmy answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##">DVBBCj9bSBJSWkZBVEA=</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        assert_equal(expected_output, output)

        raw = "[[answer (code=123456):\nmy answer\n]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##">DVBBCj9bSBJSWkZBVEA=</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        assert_equal(expected_output, output)

        raw = "[[answer (code=123456):my answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##">XEsTVVtFRldB</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        assert_equal(expected_output, output)

        raw = "[[answer : my answer";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#"  data-target="##">answer </a></div><div class="response" id="response_##"><ul>\n my answer</div>\n</ul>';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        assert_equal(expected_output, output)

        raw = "nothandled";
        expected_output = "Can't handle match nothandled";
        output = PageFormatter(raw).print_html()
        assert_equal(expected_output, output)