#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter, Tkconstants, tkFileDialog
from ia3.mainwindow import IADialog


if __name__=='__main__':
    root = Tkinter.Tk()
    root.title("IA2 Converter")
    root.geometry("465x310")
    root.attributes('-topmost', 1)
    img = Tkinter.PhotoImage(file='images/image-active64.gif')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    IADialog(root).pack(side="left")
    root.mainloop()
