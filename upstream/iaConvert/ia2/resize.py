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

# Comment : just to keep it in mind. We have to find SIMPLE solution
# to resize images.
# - Mac OS X : sips (command line tool - seems to be a pain to install PIL)
# - Windows : PIL (included in Python 2.7 portable)
# - Linux : PIL (apt-get install python-pil)

# this module implements the MAC OS X part.

import os
import sys
import commands
 
 
def getHeightWidth(file):
    widthstr = commands.getstatusoutput('sips -g pixelWidth {0}'.format(file))[1]
    heightstr = commands.getstatusoutput('sips -g pixelHeight {0}'.format(file))[1]
    width = int(widthstr.split('pixelWidth: ')[1])
    height = int(heightstr.split('pixelHeight: ')[1])
 
    return height, width
 
 
def resize(file, height, width, target_height, target_width):
    if height <= width:
        commands.getstatusoutput('sips -z {0} {1} {2}'.format(min(target_width, target_height), max(target_width, target_height), file))
    else:
        commands.getstatusoutput('sips -z {0} {1} {2}'.format(max(target_width, target_height), min(target_width, target_height), file))
 
 
def main(args):
    if len(args) == 3:
        target_height = int(args[0])
        target_width = int(args[1])
 
        for f in os.listdir(args[2]):
            if 'jpg' in f.lower() or 'png' in f.lower():
                f = args[2] + '/' + f
                height, width = getHeightWidth(f)
                resize(f, height, width, target_height, target_width)
 
 
if __name__ == '__main__':
    main(sys.argv[1:])