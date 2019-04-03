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
  xia.py --input <input-file> --output <output-dir>  [--theme <theme>] [--quality <quality>] [--export <export-type>]
  xia.py (-h | --help)
  xia.py --version

Options:
  -h --help                 Show this screen.
  --input <input-file>      svg source file (mandatory)
  --output <output-dir>     target folder (mandatory)
  --theme <theme>           name of the theme used for the current export [default: accordionBlack]
  --quality <quality>       image quality [default: 3]
  --export <export-type>    export type (singlefile, lti, local) [default: singlefile]
  --version                 Show version.

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
from xiaconverter.loggerconsole import LoggerConsole

if __name__=='__main__':

    config = ConfigParser.ConfigParser()
    config.read("xia.cnf")
    numVersion = config.get('version', 'numVersion')
    releaseVersion = config.get('version', 'releaseVersion')
    imagesPath = config.get('paths', 'imagesPath')
    langPath = config.get('paths', 'langPath')
    fontsPath = config.get('paths', 'fontsPath')
    themesPath = config.get('paths', 'themesPath')
    labjsLib = config.get('paths', 'labjsLib')
    jqueryLib = config.get('paths', 'jqueryLib')
    kineticLib = config.get('paths', 'kineticLib')
    sha1Lib = config.get('paths', 'sha1Lib')
    quantizeLib = config.get('paths', 'quantizeLib')

    arguments = docopt(__doc__)

    console = LoggerConsole()

    if arguments["--version"]:
        print(numVersion + releaseVersion)
    elif arguments["--input"] and arguments["--output"]:
        options = {}
        options['input_file'] = arguments["--input"]
        options['output_dir'] = arguments["--output"]
        options['selected_theme'] = arguments["--theme"]
        options['quality'] = arguments["--quality"]
        options['export_type'] = arguments["--export"]

        xia = XIAConsole(langPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, quantizeLib, options, console)
        xia.createIA()
    else:
        filename = ""
        if arguments["<input-file>"] is not None:
            filename = arguments["<input-file>"]
        root = Tkinter.Tk()
        root.title("XIA " + numVersion + releaseVersion)
        root.geometry("465x310")
        root.resizable(0,0)
        img = Tkinter.PhotoImage(file=imagesPath + '/xia64.gif')
        root.tk.call('wm', 'iconphoto', root._w, img)
        IADialog(root, console, langPath, imagesPath, themesPath, fontsPath, labjsLib, jqueryLib, kineticLib, sha1Lib, quantizeLib,
                 filename).pack(side="left")
        root.mainloop()
