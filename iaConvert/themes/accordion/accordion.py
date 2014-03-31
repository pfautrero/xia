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


class accordion:
    """do some stuff during image active generations"""

    def __init__(self):
        """Init"""
        self.details = []
        self.scene = {}
        self.raster = ""

    def generateIndex(self,filePath):
        """ generate accordion index file"""

        final_str  = '<!DOCTYPE html>\n'
        final_str += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
        final_str += '<head>\n'
        final_str += '  <meta charset="utf-8"/>\n'
        final_str += '  <link rel="stylesheet" type="text/css" href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.no-icons.min.css"/>\n'
        final_str += '  <link rel="stylesheet" type="text/css" href="css/main.css"/>\n'
        final_str += '</head>\n'
        final_str += '<body>\n'
        final_str += '  <div id="container">\n'
        final_str += '      <div id="detect"></div>\n'
        final_str += '      <h3 id="title">' + self.scene["title"].encode('utf-8') + '</h3>\n'
        final_str += '      <div class="accordion" id="accordion2">\n'
        final_str += '          <div class="accordion-group">\n';
        final_str += '              <div class="accordion-heading">\n';
        final_str += '                  <a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">' + self.scene["intro_title"].encode("utf-8") + '</a>\n';
        final_str += '                  <div id="collapsecomment" class="accordion-body collapse">\n';
        final_str += '                      <div class="accordion-inner">' + PageFormatter(self.scene["intro_detail"].encode('utf-8')).print_html() + '\n';
        final_str += '                      </div>\n'
        final_str += '                  </div>\n'
        final_str += '              </div>\n'
        final_str += '          </div>\n'
        for i, detail in enumerate(self.details):
            if detail['detail'].encode("utf-8").find("Réponse:") != -1:
                question = detail['detail'][0:detail['detail'].encode("utf-8").find("Réponse:")-1].encode("utf-8")
                answer = detail['detail'][detail['detail'].encode("utf-8").find("Réponse:")+8:].encode("utf-8")
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8")+'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + PageFormatter(question).print_html() + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+str(i)+'">Réponse</a></div>' + '<div class="response" id="response_'+ str(i) +'">' + PageFormatter(answer).print_html() + '</div>' + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'
            else:
                final_str += '<div class="accordion-group">\n'
                final_str += '  <div class="accordion-heading">\n'
                final_str += '      <a id="collapse'+str(i)+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+str(i)+'">'+detail['title'].encode("utf-8") +'</a>\n'
                final_str += '      <div id="collapse'+str(i)+'" class="accordion-body collapse">\n'
                final_str += '          <div class="accordion-inner">' + PageFormatter(detail["detail"].encode('utf-8')).print_html() + '\n'
                final_str += '          </div>\n'
                final_str += '      </div>\n'
                final_str += '  </div>\n'
                final_str += '</div>\n'

        final_str += '      </div>\n'
        final_str += '      <div id="canvas"></div>\n'
        final_str += '  </div>\n'
        final_str += '  <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.js"></script>\n'
        final_str += '  <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>\n'
        final_str += '  <script src="js/kinetic.js"></script>\n'
        final_str += '  <script src="datas/data.js"></script>\n'
        final_str += '  <script defer="defer" src="js/main.js"></script>\n'
        final_str += '</body>\n'
        final_str += '</html>'
        with open(filePath,"w") as indexfile:
            indexfile.write(final_str)

