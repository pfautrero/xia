#!/usr/bin/env python3
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

'''
Usage:
  xia.py [<input-file>]
  xia.py --input <input-file> --output <output-dir>  [--theme <theme>] [--export <export-type>]
  xia.py (-h | --help)
  xia.py --version

Options:
  -h --help                 Show this screen.
  --input <input-file>      svg source file (mandatory)
  --output <output-dir>     target folder (mandatory)
  --theme <theme>           name of the theme used for the current export [default: sidebar]
  --export <export-type>    export type (singlefile, lti, local) [default: singlefile]
  --version                 Show version.

'''

try:
    import tkinter
except ImportError:
    import sys
    print("Requirement : Please, install python3-tk package")
    sys.exit(1)

import sys
from xiaconverter.mainwindow import IADialog
import configparser
from xiaconverter.docopt import docopt
from xiaconverter.xiaconsole import XIAConsole
from xiaconverter.loggerconsole import LoggerConsole

if __name__=='__main__':

    config = configparser.ConfigParser()
    config.read("xia.cnf")
    numVersion = config.get('version', 'numVersion')
    releaseVersion = config.get('version', 'releaseVersion')
    imagesPath = config.get('paths', 'imagesPath')
    arguments = docopt(__doc__)
    console = LoggerConsole()

    if arguments["--version"]:
        print(numVersion + releaseVersion)
    elif arguments["--input"] and arguments["--output"]:
        options = {}
        options['input_file'] = arguments["--input"]
        options['output_dir'] = arguments["--output"]
        options['selected_theme'] = arguments["--theme"]
        options['export_type'] = arguments["--export"]

        xia = XIAConsole(config, options, console)
        xia.createIA()
    else:
        filename = ""
        if arguments["<input-file>"] is not None:
            filename = arguments["<input-file>"]
        root = tkinter.Tk()
        root.title("XIA " + numVersion + releaseVersion)
        #root.geometry("400x300")
        root.configure(background='black')
        root.resizable(0,0)
        root.columnconfigure(0, pad=0)
        img = tkinter.PhotoImage(file=imagesPath + '/xia64.gif')
        root.tk.call('wm', 'iconphoto', root._w, img)
        IADialog(root, console, config, "", filename)  #.pack(side="left")
        root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
        root.mainloop()
