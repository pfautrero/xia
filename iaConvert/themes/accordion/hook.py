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


class hook:
    """do some stuff during image active generations"""

    def __init__(self, iaobject, PageFormatter):
        """Init"""
        self.iaobject = iaobject
        self.PageFormatter = PageFormatter

    def generateIndex(self,filePath, templatePath):
        """ generate index file"""
        
        final_str  = '<div class="accordion-group">\n';
        final_str += '  <div class="accordion-heading">\n';
        final_str += '    <a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">' + self.iaobject.scene["intro_title"].encode("utf-8") + '</a>\n';
        final_str += '      <div id="collapsecomment" class="accordion-body collapse">\n';
        final_str += '        <div class="accordion-inner">' + self.PageFormatter(self.iaobject.scene["intro_detail"].encode('utf-8')).print_html() + '\n';
        final_str += '        </div>\n'
        final_str += '      </div>\n'
        final_str += '  </div>\n'
        final_str += '</div>\n'
        for i, detail in enumerate(self.iaobject.details):
            detail['detail'] = detail['detail'].encode("utf-8")
            if detail['detail'].find("Réponse:") != -1:
                question = detail['detail'][0:detail['detail'].find("Réponse:")]
                answer = detail['detail'][detail['detail'].find("Réponse:") + 9:]
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8")+'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + self.PageFormatter(question).print_html() + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+str(i)+'">Réponse</a></div>' + '<div class="response" id="response_'+ str(i) +'">' + self.PageFormatter(answer).print_html() + '</div>' + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'
            else:
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8") +'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + self.PageFormatter(detail["detail"]).print_html() + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'        

        with open(templatePath,"r") as template:
            final_index = template.read()
            final_index = final_index.replace("{{TITLE}}", self.iaobject.scene["title"].encode('utf-8'))
            final_index = final_index.replace("{{ACCORDION}}", final_str)            
        with open(filePath,"w") as indexfile:
            indexfile.write(final_index)
