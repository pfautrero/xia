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

"""xia-converter.

Usage:
  xia.py [<input-file>]
  xia.py -i <input-file> -o <output-dir>  -t <theme>
  xia.py (-h | --help)
  xia.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

try:
    import Tkinter, Tkconstants, tkFileDialog
except ImportError:
    import sys
    print "Requirement : Please, install python-tk package"
    sys.exit(1)

from xiaconverter.mainwindow import IADialog
import ConfigParser
from xiaconverter.docopt import docopt
from xiaconverter.xiaconsole import XIAConsole

if __name__=='__main__':
    
    numVersion = "Xia - 1.0-beta3"
    config = ConfigParser.ConfigParser()
    config.read("xia.cnf")
    imagesPath = config.get('paths', 'imagesPath')
    langPath = config.get('paths', 'langPath')
    fontsPath = config.get('paths', 'fontsPath')
    themesPath = config.get('paths', 'themesPath')
    labjsLib = config.get('paths', 'labjsLib')
    jqueryLib = config.get('paths', 'jqueryLib')
    kineticLib = config.get('paths', 'kineticLib')
    sha1Lib = config.get('paths', 'sha1Lib')

    arguments = docopt(__doc__)
    
    if arguments["--version"]:
        print(numVersion)
    elif arguments["-i"] and arguments["-o"] and arguments["-t"]:
        input_file = arguments["<input-file>"]
        output_dir = arguments["<output-dir>"]
        selected_theme = arguments["<theme>"]
        xia = XIAConsole(langPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, input_file, output_dir, selected_theme)
        xia.createIA()
    else:
        filename = ""
        if arguments["<input-file>"] is not None:
            filename = arguments["<input-file>"]
        root = Tkinter.Tk()
        root.title(numVersion)
        root.geometry("465x310")
        root.resizable(0,0)
        img = Tkinter.PhotoImage(file=imagesPath + '/image-active64.gif')
        root.tk.call('wm', 'iconphoto', root._w, img)    
        IADialog(root,langPath, imagesPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, filename).pack(side="left")
        root.mainloop()
