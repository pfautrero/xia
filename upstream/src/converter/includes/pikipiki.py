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
class PageFormatter:
    """Object that turns Wiki markup into HTML.

    All formatting commands can be parsed one line at a time, though
    some state is carried over between lines.
    """
    def __init__(self, raw):
        if type(raw) != unicode:
            raw = raw.decode("utf-8")
        self.raw = raw
        self.is_em = self.is_b = 0
        self.list_indents = []
        self.in_pre = 0

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
            s = s + u"\n<hr>\n"
        else:
            s = s + u"\n<hr size=%d>\n" % (len(word) - 2 )
        return s

    def _url_repl(self, word):
        return u'<a href="%s" target="_blank">%s</a>\n' % (word, word)

    def _videostart_repl(self, word):
        return u'<video controls preload="none" data-state="autostart">\n\t\
            <source type="video/mp4" src="%s.mp4" />\n\t\
            <source type="video/ogg" src="%s.ogv" />\n\t\
            <source type="video/webm" src="%s.webm" />\n\
            </video>\n' % (os.path.splitext(word)[0], \
              os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _video_repl(self, word):
        return u'<video controls preload="none" data-state="none">\n\t\
            <source type="video/mp4" src="%s.mp4" />\n\t\
            <source type="video/ogg" src="%s.ogv" />\n\t\
            <source type="video/webm" src="%s.webm" />\n\
            </video>\n' % (os.path.splitext(word)[0], \
              os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _img_repl(self, word):
        return u'<img src="%s">\n' % (word)

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
        return u'<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word_url)

    def _iframe2_repl(self, word):
        word_url = word.split('src="')[1].split('"')[0]
        if word_url[0:2] == "//":
            word_url = "http:" + word_url
        iframe_width = word.split('width="')[1].split('"')[0]
        iframe_height = word.split('height="')[1].split('"')[0]
        videoClass = 'videoWrapper4_3'
        if iframe_width and iframe_height:
            ratio = (float(iframe_height) / float(iframe_width)) * 16
            if (ratio == 9):
                videoClass = 'videoWrapper16_9'
        return u'<div class="' + videoClass + \
          '" data-iframe="%s"></div>\n' % (word_url)
    
    def _audiostart_repl(self, word):
        return u'<audio controls data-state="autostart">\n\t\
            <source type="audio/ogg" src="%s.ogg" />\n\t\
            <source type="audio/mp3" src="%s.mp3" />\n\
            </audio>\n' % (os.path.splitext(word)[0], os.path.splitext(word)[0])


    def _audio_repl(self, word):
        return u'<audio controls data-state="none">\n\t\
            <source type="audio/ogg" src="%s.ogg" />\n\t\
            <source type="audio/mp3" src="%s.mp3" />\n\
            </audio>\n' % (os.path.splitext(word)[0], os.path.splitext(word)[0])

    def _email_repl(self, word):
        return u'<a href="mailto:%s">%s</a>\n' % (word, word)

    def _ent_repl(self, s):
        return {'&': '&amp;',
                '<': '&lt;',
                '>': '&gt;'}[s]

    def _li_repl(self, match):
        return u'<li>%s</li>\n' %(match[match.find('*')+1:])

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
        return u'<a href="%s" target="_blank">%s</a>' %(word_url, word_displayed)

    def _pre_repl(self, word):
        if word == '{{{' and not self.in_pre:
            self.in_pre = 1
            return u'<pre>\n'
        elif self.in_pre:
            self.in_pre = 0
            return u'</pre>\n'
        else:
            return u''

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
        final_str = u""
        scan_re = re.compile(
            r"(?:(?P<emph>\*{2,3})"
            + r'|(?P<iframe2><iframe(.*)></iframe>)'
            + r"|(?P<iframe>&lt;iframe(.*)&gt;&lt;/iframe&gt;)"        
            + r"|(?P<ent>[<>&])"
            + r"|(?P<rule>-{4,})"
            + r"|(?P<videostart>[^\s'\"]+\.(ogv|mp4|webm)(\s*)autostart$)"
            + r"|(?P<video>[^\s'\"]+\.(ogv|mp4|webm)$)"
            + r"|(?P<link>\[http(.*)\])"
            + r"|(?P<img>[^\s'\"]+\.(jpg|jpeg|png|gif)$)"
            + r"|(?P<audiostart>[^\s'\"]+\.(ogg|mp3)(\s*)autostart$)"
            + r"|(?P<audio>[^\s'\"]+\.(ogg|mp3)$)"
            + r"|(?P<url>(http|ftp|nntp|news|mailto|https)\:[^\s'\"]+\S)"
            + r"|(?P<email>[-\w._+]+\@[\w.-]+)"
            + r"|(?P<li>^\s+\*(.*))"
            + r"|(?P<nothandled>nothandled)"
            + r"|(?P<pre>(\{\{\{|\}\}\}))"
            + r")")
        blank_re = re.compile("^\s*$")
        indent_re = re.compile("^\s*")
        eol_re = re.compile(r'\r?\n')
        raw = string.expandtabs(self.raw)

        for line in eol_re.split(raw):
            if not self.in_pre:
                if blank_re.match(line):
                    final_str += u'<br>\n'
                    continue
                indent = indent_re.match(line)
                final_str += self._indent_to(len(indent.group(0)))
            final_str += re.sub(scan_re, self.replace, line)
        if self.in_pre: final_str += u'</pre>\n'
        final_str += self._undent()
        return final_str
