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
# source code from pikipiki parser (sligthly modified)


import re
import string
import os
from datetime import datetime
import hashlib
import base64
import uuid
import math

class PageFormatter:
    """Object that turns Wiki markup into HTML.

    All formatting commands can be parsed one line at a time, though
    some state is carried over between lines.
    """
    def __init__(self, raw):
        if type(raw) == bytes:
            raw = raw.decode("utf-8")
        elif type(raw) == int or type(raw) == float:
            raw = str(raw)

        self.raw = raw
        self.is_em = self.is_b = 0
        self.list_indents = []
        self.in_pre = 0
        self.in_li = 0
        self.hidden_block = []
        self.final_str = ""

    def _emph_repl(self, word):
        if len(word) == 3:
            self.is_b = not self.is_b
            return [u'</b>', u'<b>'][self.is_b]
        else:
            self.is_em = not self.is_em
            return [u'</em>', u'<em>'][self.is_em]

    def _rule_repl(self, word):
        s = self._undent()
        if len(word) <= 4:
            s = s + "\n<hr/>\n"
        else:
            s = s + "\n<hr size=%d/>\n" % (len(word) - 2 )
        return s
    def _markdownheaders_repl(self, word):
        nbTag = word.count("#")
        return '<h%s>%s</h%s>' %(nbTag, word[nbTag:].strip(), nbTag)

    def _url_repl(self, word):
        return '<a href="%s" target="_blank">%s</a>\n' % (word, word)

    def _flicker_repl(self, word):
        return '<div class="flickr_oembed" data-oembed="%s"></div>\n' % (word)

    def _scolawebtv_repl(self, word):
        videoClass = 'videoWrapper4_3'
        word = word.replace("scolawebtv.crdp-versailles.fr/?id=", "scolawebtv.crdp-versailles.fr/?iframe&id=")
        return '<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word)

    def _webtv_repl(self, word):
        videoClass = 'videoWrapper4_3'
        word = word.replace("webtv.ac-versailles.fr/spip.php?article", "webtv.ac-versailles.fr/spip.php?page=iframe-video&id_article=")
        return '<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word)

    def _videostart_repl(self, word):
        return '<video controls preload="none" data-state="autostart">\n\t\
            <source type="video/mp4" src="%s.mp4" />\n\t\
            <source type="video/ogg" src="%s.ogv" />\n\t\
            <source type="video/webm" src="%s.webm" />\n\
            </video>\n' % (os.path.splitext(word)[0], \
              os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _video_repl(self, word):
        return '<video controls preload="none" data-state="none">\n\t\
            <source type="video/mp4" src="%s.mp4" />\n\t\
            <source type="video/ogg" src="%s.ogv" />\n\t\
            <source type="video/webm" src="%s.webm" />\n\
            </video>\n' % (os.path.splitext(word)[0], \
              os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _img_repl(self, word):
        return '<img src="%s"/>\n' % (word)

    def _pdf_repl(self, word):
        return '<a href="%s"><img src="{{LogoPDF}}" alt="pdf"></a>\n' % (word)

    def _iframe_repl(self, word):
        word_url = word.split("src=&quot;")[1].split("&quot;")[0]
        if word_url[0:2] == "//":
            word_url = "http:" + word_url
        iframe_width = 0
        iframe_height = 0
        if len(word.split('width="')) > 1:
            iframe_width = word.split('width="')[1].split('"')[0]
        if len(word.split('height="')) > 1:
            iframe_height = word.split('height="')[1].split('"')[0]
        videoClass = 'videoWrapper4_3'
        if iframe_width and iframe_height:
            ratio = (float(iframe_height) / float(iframe_width)) * 16
            if (ratio == 9):
                videoClass = 'videoWrapper16_9'
        return '<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word_url)

    def _iframe2_repl(self, word):

        word_url = ""
        srccheck = re.search('src=("|\')(.*?)("|\')', word, re.IGNORECASE|re.DOTALL)
        if srccheck:
            word_url = srccheck.group(2)

        if word_url[0:2] == "//":
            word_url = "http:" + word_url

        iframe_width = ""
        widthcheck = re.search('width=("|\')(.*?)("|\')', word, re.IGNORECASE|re.DOTALL)
        if widthcheck:
            iframe_width = widthcheck.group(2)

        iframe_height = ""
        heightcheck = re.search('height=("|\')(.*?)("|\')', word, re.IGNORECASE|re.DOTALL)
        if heightcheck:
            iframe_height = heightcheck.group(2)

        videoClass = 'videoWrapper4_3'
        if iframe_width and iframe_height:
            ratio = (float(iframe_height) / float(iframe_width)) * 16
            if (ratio == 9):
                videoClass = 'videoWrapper16_9'
        return '<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word_url)

    def _audiostart_repl(self, word):
        return '<audio controls data-state="autostart">\n\t\
            <source type="audio/ogg" src="%s.ogg" />\n\t\
            <source type="audio/mp3" src="%s.mp3" />\n\
            </audio>\n' % (os.path.splitext(word)[0], os.path.splitext(word)[0])


    def _audio_repl(self, word):
        return '<audio controls data-state="none">\n\t\
            <source type="audio/ogg" src="%s.ogg" />\n\t\
            <source type="audio/mp3" src="%s.mp3" />\n\
            </audio>\n' % (os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _email_repl(self, word):
        return '<a href="mailto:%s">%s</a>\n' % (word, word)

    def _ent_repl(self, s):
        return {'&': '&amp;',
                '<': '&lt;',
                '>': '&gt;'}[s]

    def _li_repl(self, match):
        self.in_li = 1
        return '<li>'

    def _link_repl(self, word):
        word_filtered = re.sub(' +', ' ', word[1:-1])
        word_displayed = ""
        word_url = ""
        for i in word_filtered.split(" "):
            if word_url == "":
                word_url = i
            elif word_displayed == "":
                word_displayed = i
            else:
                word_displayed = word_displayed + " " + i
        if word_displayed == "":
            word_displayed = word_url
        return '<a href="%s" target="_blank">%s</a>' %(word_url, word_displayed)

    def _ialink_repl(self, word):
        """compatibility with image active 1 format"""
        subword = word.split("@")
        return '<a href="%s" target="_blank">%s</a>' %(subword[1][:-1], subword[0][1:])

    def _pre_repl(self, word):
        if word == '{{{' and not self.in_pre:
            self.in_pre = 1
            return '<pre>\n'
        elif self.in_pre:
            self.in_pre = 0
            return '</pre>\n'
        else:
            return ''

    def _hidden_block_repl(self, word):
        if word.startswith('[['):
            #self.hidden_block.append(1)
            stack_value = 0
            data_password=""
            code_present = re.search(r'\(code=(.*)\)', word, re.IGNORECASE|re.DOTALL)
            content =  word[2:len(word) - 1]
            final_result = ""
            if code_present:
                password = code_present.group(1)
                stack_value = password
                data_password = 'data-password="' + hashlib.sha1(password.encode("utf-8")).hexdigest() + '"'
                content = re.sub(r'\(code=(.*)\)', '', content)

            random_id = hashlib.md5(uuid.uuid1().bytes).hexdigest()
            final_result =  '<div style="margin-top:5px;margin-bottom:5px;">' + \
                '<a class="button" href="#" ' + data_password + \
                ' data-target="' + random_id + '">' + \
                content + \
                '</a>' + \
                '</div>'
            if data_password != "":
                final_result += '<form class="unlock" style="display:none;" id="form_' + random_id + '">' + \
                            '<input type="text">' + \
                            '<input type="submit" data-target="' + random_id + '" value="" ' + data_password + '>' + \
                            '</form>'
            final_result += '<div class="response" id="response_' + random_id + '">'
            if data_password != "":
                final_result += '<!-- ==HIDDEN_BLOCK== -->'

            self.hidden_block.append(stack_value)
            return final_result

        elif len(self.hidden_block):
            password = self.hidden_block.pop()
            current_str = word[0:word.find("]]")]
            if password:
                # encrypt hidden_block
                start_block = self.final_str.rfind("<!-- ==HIDDEN_BLOCK== -->")
                str_to_encrypt = self.final_str[start_block + len("<!-- ==HIDDEN_BLOCK== -->"):]
                str_to_encrypt = str_to_encrypt + current_str
                while len(password) < len(str_to_encrypt):
                    password += password
                str_encrypted = base64.b64encode(self.str_xor(str_to_encrypt.encode("utf-8"), password.encode("utf-8")))
                self.final_str = self.final_str[0:start_block] + str_encrypted.decode()
                return '</div>\n'
            else:
                return current_str + '</div>\n'
        else:
            return ''

    def str_xor(self, s1, s2):
        return "".join([chr(c1 ^ c2) for (c1,c2) in zip(s1,s2)]).encode()

    def _indent_level(self):
        return len(self.list_indents) and self.list_indents[-1]

    def _indent_to(self, new_level):
        s = u''
        while self._indent_level() > new_level:
            del(self.list_indents[-1])
            s = s + u'</ul>\n'
        while self._indent_level() < new_level:
            self.list_indents.append(new_level)
            s = s + u'<ul>\n'
        return s

    def _undent(self):
        res = u'</ul>' * len(self.list_indents)
        self.list_indents = []
        return res

    def replace(self, match):
        for type, hit in match.groupdict().items():
            if hit:
                if hasattr(self, '_' + type + '_repl'):
                    return getattr(self, '_' + type + '_repl')(hit,)
                else:
                    return "Can't handle match %s" % type

    def print_html(self):
        # For each line, we scan through looking for magic
        # strings, outputting verbatim any intervening text
        #final_str = u""
        scan_re = re.compile(
            r"(?:(?P<emph>\*{2,3})"
            + r'|(?P<iframe2><iframe(.*)></iframe>)'
            + r"|(?P<iframe>&lt;iframe(.*)&gt;&lt;/iframe&gt;)"
            + r"|(?P<ent>[<>&])"
            + r"|(?P<rule>-{4,})"
            + r"|(?P<markdownheaders>#{1,6}(.*))"
            + r"|(?P<videostart>[^\s'\"]+\.(ogv|mp4|webm)(\s*)autostart$)"
            + r"|(?P<video>[^\s'\"]+\.(ogv|mp4|webm)$)"
            + r"|(?P<scolawebtv>(https|http)\:\/\/scolawebtv\.crdp-versailles\.fr\/\?id=(.*))"
            + r"|(?P<webtv>(https|http)\:\/\/webtv\.ac-versailles\.fr\/spip\.php\?article(.*))"
            + r"|(?P<flicker>https\:\/\/flic\.kr\/p\/(.*))"
            + r"|(?P<link>\[(http|\.\.\/|\.\/)(.*)\])"
            + r"|(?P<img>[^\s'\"]+\.(jpg|jpeg|png|gif)$)"
            + r"|(?P<pdf>[^\s'\"]+\.(pdf)$)"
            + r"|(?P<audiostart>[^\s'\"]+\.(ogg|mp3)(\s*)autostart$)"
            + r"|(?P<audio>[^\s'\"]+\.(ogg|mp3)$)"
            + r"|(?P<url>(http|ftp|nntp|news|mailto|https)\:[^\s'\"]+\S)"
            + r"|(?P<ialink>\{(.*)\@(.*)\})"
            + r"|(?P<email>[-\w._+]+\@[\w.-]+)"
            + r"|(?P<li>^\s+\*(.*))"
            + r"|(?P<nothandled>nothandled)"
            + r"|(?P<pre>(\{\{\{|\}\}\}))"
            + r"|(?P<hidden_block>(\[\[(.*?)\:|\]\]))"
            + r")", re.IGNORECASE)
        blank_re = re.compile(r"^\s*$")
        indent_re = re.compile(r"^\s*")
        eol_re = re.compile(r'\r?\n')
        raw = self.raw.expandtabs()
        html_feed = u'<br/>\n'

        # fix some elements
        fix_element = re.sub(r"\[\[(.*?):", r"[[\1:\n", raw)
        raw = fix_element

        fix_element = re.sub(r"(.*?)\]\]", r"\1\n]]", raw)
        raw = fix_element

        # loop on lines
        for line in eol_re.split(raw):
            if not self.in_pre:
                if blank_re.match(line):
                    self.final_str += html_feed
                    continue
                indent = indent_re.match(line)
                self.final_str += self._indent_to(len(indent.group(0)))
            test = re.sub(scan_re, self.replace, line)
            self.final_str += test
            if self.in_li:
                test = re.sub(scan_re, self.replace, line[line.find("*")+1:].strip())
                self.final_str += test
                self.final_str += "</li>"
                self.in_li = 0

        if self.in_pre: self.final_str += '</pre>\n'
        while len(self.hidden_block):
            self.hidden_block.pop(0)
            self.final_str += '</div>\n'
        self.final_str += self._undent()
        if self.final_str == html_feed:
            return ""
        else:
            return self.final_str
