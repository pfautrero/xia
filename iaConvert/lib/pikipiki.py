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


import re, string
class PageFormatter:
    """Object that turns Wiki markup into HTML.

    All formatting commands can be parsed one line at a time, though
    some state is carried over between lines.
    """
    def __init__(self, raw):
        self.raw = raw
        self.is_em = self.is_b = 0
        self.list_indents = []
        self.in_pre = 0

    def _emph_repl(self, word):
        if len(word) == 3:
            self.is_b = not self.is_b
            return ['</b>', '<b>'][self.is_b]
        else:
            self.is_em = not self.is_em
            return ['</em>', '<em>'][self.is_em]

    def _rule_repl(self, word):
        s = self._undent()
        if len(word) <= 4:
            s = s + "\n<hr>\n"
        else:
            s = s + "\n<hr size=%d>\n" % (len(word) - 2 )
        return s

    def _word_repl(self, word):
        return Page(word).link_to()

    def _url_repl(self, word):
        return '<a href ="%s">%s</a>' % (word, word)

    def _video_repl(self, word):
        return '<video controls><source type="video/ogg" src="%s" /></video>' % (word)

    def _audio_repl(self, word):
        return '<audio controls><source type="audio/mp3" src="%s" /></audio><p><a href="%s">bande audio</a></p>' % (word,word)

    def _email_repl(self, word):
        return '<a href ="mailto:%s">%s</a>' % (word, word)

    def _ent_repl(self, s):
        return {'&': '&amp;',
                '<': '&lt;',
                '>': '&gt;'}[s]

    def _li_repl(self, match):
        return '<li>'

    def _pre_repl(self, word):
        if word == '{{{' and not self.in_pre:
            self.in_pre = 1
            return '<pre>'
        elif self.in_pre:
            self.in_pre = 0
            return '</pre>'
        else:
            return ''

    def _indent_level(self):
        return len(self.list_indents) and self.list_indents[-1]

    def _indent_to(self, new_level):
        s = ''
        while self._indent_level() > new_level:
            del(self.list_indents[-1])
            s = s + '</ul>\n'
        while self._indent_level() < new_level:
            self.list_indents.append(new_level)
            s = s + '<ul>\n'
        return s

    def _undent(self):
        res = '</ul>' * len(self.list_indents)
        self.list_indents = []
        return res

    def replace(self, match):
        for type, hit in match.groupdict().items():
            if hit:
                return getattr(self, '_' + type + '_repl')(hit,)
        else:
            raise "Can't handle match " + `match`

    def print_html(self):
        # For each line, we scan through looking for magic
        # strings, outputting verbatim any intervening text
        final_str = ""
        
        scan_re = re.compile(
            r"(?:(?P<emph>\*{2,3})"
            + r"|(?P<ent>[<>&])"
            + r"|(?P<word>\b(?:[A-Z][a-z]+){2,}\b)"
            + r"|(?P<rule>-{4,})"
            + r"|(?P<video>https?\://[^\s'\"]+\.ogg\b)"
            + r"|(?P<audio>https?\://[^\s'\"]+\.mp3\b)"
            + r"|(?P<url>(http|ftp|nntp|news|mailto)\:[^\s'\"]+\S)"
            + r"|(?P<email>[-\w._+]+\@[\w.-]+)"
            + r"|(?P<li>^\s+\*)"
            + r"|(?P<pre>(\{\{\{|\}\}\}))"
            + r")")
        blank_re = re.compile("^\s*$")
        bullet_re = re.compile("^\s+\*")
        indent_re = re.compile("^\s*")
        eol_re = re.compile(r'\r?\n')
        raw = string.expandtabs(self.raw)
        for line in eol_re.split(raw):
            if not self.in_pre:
                # XXX: Should we check these conditions in this order?
                if blank_re.match(line):
                    final_str += '<p>'
                    continue
                indent = indent_re.match(line)
                final_str += self._indent_to(len(indent.group(0)))
            final_str += re.sub(scan_re, self.replace, line)
        if self.in_pre: final_str += '</pre>'
        #print final_str
        return final_str
        #return self._undent()
