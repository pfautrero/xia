#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    import Tkinter, Tkconstants, tkFileDialog
except ImportError:
    import sys
    print "Requirement : Please, install python-tk package"
    sys.exit(1)

from ia3.mainwindow import IADialog

if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("Image Active 2")
    root.geometry("465x310")
    root.attributes('-topmost', 1)
    img = Tkinter.PhotoImage(file='images/image-active64.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    IADialog(root).pack(side="left")
    root.mainloop()
