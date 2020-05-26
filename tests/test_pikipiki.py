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
# @author : pascal.fautrero@gmail.com

from xiaconverter.pikipiki import PageFormatter
from nose2.tools import *
from nose2.tests._common import TestCase
import re

class TestPageFormatter(TestCase):

    def test_print_html(self):
        raw = "**text**";
        expected_output = "<b>text</b>";
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html2(self):
        raw = "*text*";
        expected_output = "<em>text</em>";
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html3(self):
        raw = "{{{text}}}";
        expected_output = "<pre>\ntext</pre>\n";
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html4(self):
        raw = "photo.jpg";
        expected_output = '<img src="photo.jpg"/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html5(self):
        raw = "photo.jpeg";
        expected_output = '<img src="photo.jpeg"/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html6(self):
        raw = "photo.png";
        expected_output = '<img src="photo.png"/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html7(self):
        raw = "photo.gif";
        expected_output = '<img src="photo.gif"/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html8(self):
        raw = "admin@test.com";
        expected_output = '<a href="mailto:admin@test.com">admin@test.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html9(self):
        raw = "<&>";
        expected_output = '&lt;&amp;&gt;';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html10(self):
        raw = "----";
        expected_output = '\n<hr/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html11(self):
        raw = "-----";
        expected_output = '\n<hr size=3/>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html12(self):
        raw = '&lt;iframe src=&quot;http://example.com&quot;&gt;&lt;/iframe&gt;';
        expected_output = '<div class="videoWrapper4_3" data-iframe="http://example.com"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html13(self):
        raw = '&lt;iframe width="560" height="315" src=&quot;//example.com&quot;&gt;&lt;/iframe&gt;';
        expected_output = '<div class="videoWrapper16_9" data-iframe="http://example.com"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html14(self):
        raw = '<iframe width="560" height="315" src="//www.youtube.com/embed/ctXwWpMz44M" frameborder="0" allowfullscreen></iframe>';
        expected_output = '<div class="videoWrapper16_9" data-iframe="http://www.youtube.com/embed/ctXwWpMz44M"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html15(self):
        raw = "http://example.com";
        expected_output = '<a href="http://example.com" target="_blank">http://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html16(self):
        raw = "https://example.com";
        expected_output = '<a href="https://example.com" target="_blank">https://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html17(self):
        raw = "ftp://example.com";
        expected_output = '<a href="ftp://example.com" target="_blank">ftp://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html18(self):
        raw = "nntp://example.com";
        expected_output = '<a href="nntp://example.com" target="_blank">nntp://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html19(self):
        raw = "news://example.com";
        expected_output = '<a href="news://example.com" target="_blank">news://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html20(self):
        raw = "mailto://example.com";
        expected_output = '<a href="mailto://example.com" target="_blank">mailto://example.com</a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html21(self):
        raw = " * line 1\n * line2";
        expected_output = '<ul>\n<li>line 1</li><li>line2</li></ul>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html22(self):
        raw = " * **line 1**\n * [http://test line2]";
        expected_output = '<ul>\n<li><b>line 1</b></li><li><a href="http://test" target="_blank">line2</a></li></ul>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html23(self):
        raw = "   * line 1\n  * line2";
        expected_output = '<ul>\n<li>line 1</li></ul>\n<ul>\n<li>line2</li></ul>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html24(self):
        raw = "video.mp4";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html25(self):
        raw = "video.mp4 autostart";
        expected_output = '<video controls preload="none" data-state="autostart">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html26(self):
        raw = "video.ogv";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html27(self):
        raw = "video.webm";
        expected_output = '<video controls preload="none" data-state="none">\n\t            <source type="video/mp4" src="video.mp4" />\n\t            <source type="video/ogg" src="video.ogv" />\n\t            <source type="video/webm" src="video.webm" />\n            </video>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html28(self):
        raw = "audio.mp3";
        expected_output = '<audio controls data-state="none">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html29(self):
        raw = "audio.ogg";
        expected_output = '<audio controls data-state="none">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html30(self):
        raw = "audio.mp3  autostart";
        expected_output = '<audio controls data-state="autostart">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html31(self):
        raw = "audio.ogg    autostart";
        expected_output = '<audio controls data-state="autostart">\n\t            <source type="audio/ogg" src="audio.ogg" />\n\t            <source type="audio/mp3" src="audio.mp3" />\n            </audio>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html32(self):
        raw = "[http://example.com A small test]";
        expected_output = '<a href="http://example.com" target="_blank">A small test</a>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html33(self):
        raw = "[http://example.com]";
        expected_output = '<a href="http://example.com" target="_blank">http://example.com</a>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html34(self):
        raw = "[../index.html test]";
        expected_output = '<a href="../index.html" target="_blank">test</a>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html35(self):
        raw = "[./index.html test]";
        expected_output = '<a href="./index.html" target="_blank">test</a>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html36(self):
        raw = " ";
        expected_output = '';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html37(self):
        raw = "}}}";
        expected_output = '';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html38(self):
        self.maxDiff = None
        raw = "[[answer : my answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#"  data-target="##">answer </a></div><div class="response" id="response_##" style="display:none;"><ul>\n my answer</ul>\n</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        self.assertEqual(expected_output, output)

    def test_print_html39(self):
        raw = "[[answer (code=123456):\nmy answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##" style="display:none;">DVBBGws8XEsTVVtFRldB</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        self.assertEqual(expected_output, output)

    def test_print_html40(self):
        raw = "[[answer (code=123456):\nmy answer\n]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##" style="display:none;">DVBBGws8XEsTVVtFRldBCFdEHgw5</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        self.assertEqual(expected_output, output)

    def test_print_html41(self):
        raw = "[[answer (code=123456):my answer]]";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b" data-target="##">answer </a></div><form class="unlock" style="display:none;" id="form_##"><input type="text"><input type="submit" data-target="##" value="" data-password="7c4a8d09ca3762af61e59520943dc26494f8941b"></form><div class="response" id="response_##" style="display:none;">XEsTVVtFRldB</div>\n';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        self.assertEqual(expected_output, output)

    def test_print_html42(self):
        raw = "[[answer : my answer";
        expected_output = '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#"  data-target="##">answer </a></div><div class="response" id="response_##" style="display:none;"><ul>\n my answer</div>\n</ul>';
        output = PageFormatter(raw).print_html()
        target_id = ""
        target_entry = re.search('data-target="(.*?)"', output, re.IGNORECASE|re.DOTALL)
        if target_entry:
            target_id = target_entry.group(1)
            output = output.replace(target_id, "##")
        self.assertEqual(expected_output, output)

    def test_print_html43(self):
        raw = "nothandled";
        expected_output = "Can't handle match nothandled";
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html44(self):
        raw = "https://scolawebtv.crdp-versailles.fr/?id=1337";
        expected_output = '<div class="videoWrapper4_3" data-iframe="https://scolawebtv.crdp-versailles.fr/?iframe&id=1337"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html45(self):
        raw = "http://scolawebtv.crdp-versailles.fr/?id=1337";
        expected_output = '<div class="videoWrapper4_3" data-iframe="http://scolawebtv.crdp-versailles.fr/?iframe&id=1337"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html46(self):
        raw = "https://webtv.ac-versailles.fr/spip.php?article1337";
        expected_output = '<div class="videoWrapper4_3" data-iframe="https://webtv.ac-versailles.fr/spip.php?page=iframe-video&id_article=1337"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html47(self):
        raw = "http://webtv.ac-versailles.fr/spip.php?article1337";
        expected_output = '<div class="videoWrapper4_3" data-iframe="http://webtv.ac-versailles.fr/spip.php?page=iframe-video&id_article=1337"></div>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html48(self):
        raw = "./test.pdf";
        expected_output = '<a href="./test.pdf"><img src="{{LogoPDF}}" alt="pdf"></a>\n';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html49(self):
        raw = "# TITLE";
        expected_output = '<h1>TITLE</h1>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html50(self):
        raw = "## TITLE";
        expected_output = '<h2>TITLE</h2>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html51(self):
        raw = "### TITLE";
        expected_output = '<h3>TITLE</h3>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html52(self):
        raw = "#### TITLE";
        expected_output = '<h4>TITLE</h4>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html53(self):
        raw = "##### TITLE";
        expected_output = '<h5>TITLE</h5>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)

    def test_print_html49(self):
        raw = "###### TITLE";
        expected_output = '<h6>TITLE</h6>';
        output = PageFormatter(raw).print_html()
        self.assertEqual(expected_output, output)
