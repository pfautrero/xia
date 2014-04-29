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

try:
    import Tkinter, Tkconstants, tkFileDialog
except ImportError:
    import sys
    print "Requirement : Please, install python-tk package"
    sys.exit(1)

from ia2.mainwindow import IADialog


if __name__=='__main__':

    root = Tkinter.Tk()

    root.title("Image Active 2 - alpha 2")
    root.geometry("465x310")
    #root.attributes('-topmost', 1)
    img = Tkinter.PhotoImage(file='images/image-active64.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    IADialog(root).pack(side="left")
    root.mainloop()
