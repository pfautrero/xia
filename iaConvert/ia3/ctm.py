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

import re

class ctm:
    """ Used to analyze transformation applied on svg element
        CTM (Current Transformation Matrix)
        expected forms :
            matrix(a b c d e f)
            translate(x y)
            translate(a)
            scale(a)
            scale(sx sy)
            rotate(angle cx cy)
            skewX(x)
            skewY(y)

        translateX = e
        translateY = f
        scaleX = sqrt(a*a+b*b)
        scaleY = sqrt(c*c+d*d)
        rotate = (180/pi) * arctan(d/c) - 90
        skewY = (180/pi) * arctan(b/a)
    
    """

    def __init__(self):
        """Init"""
        self.rotate = 0
        self.rX = 0
        self.rY = 0
        self.translateX = 0
        self.translateY = 0
        self.scaleX = 0
        self.scaleY = 0

    def analyze(self,entry):
        """Analyze transform attribute"""
        regex_group = r'([^\s,])\s*,?\s*'
        
        # look for something with such a form : "matrix(a b c d e f)"
        regex_matrix = r'matrix\(\s*' + regex_group * 6 + r'\)'
        matchObj = re.match( regex_matrix, entry)
        if matchObj:
            self.extractMatrix(matchObj.groups())
            return
        
        # look for something with such a form : "translate(a b)"
        regex_translate = r'translate\(\s*' + regex_group * 2 + r'\)'
        matchObj = re.match( regex_translate, entry)
        if matchObj:
            self.extractTranslate(matchObj.groups())
            return

        # look for something with such a form : "translate(a)"
        regex_translate = r'translate\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_translate, entry)
        if matchObj:
            self.extractTranslate(matchObj.groups())
            return
        
        # look for something with such a form : "rotate(a b c)"
        regex_rotate = r'rotate\(\s*' + regex_group * 3 + r'\)'
        matchObj = re.match( regex_rotate, entry)
        if matchObj:
            self.extractRotation(matchObj.groups())
            return        

        # look for something with such a form : "rotate(a)"
        regex_rotate = r'rotate\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_rotate, entry)
        if matchObj:
            self.extractRotation(matchObj.groups())
            return        

        # look for something with such a form : "scale(a b)"
        regex_scale = r'scale\(\s*' + regex_group * 2 + r'\)'
        matchObj = re.match( regex_scale, entry)
        if matchObj:
            self.extractScale(matchObj.groups())
            return        

        # look for something with such a form : "scale(a)"
        regex_scale = r'scale\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_scale, entry)
        if matchObj:
            self.extractScale(matchObj.groups())
            return        
        
    def extractTranslate(self,groups):
        """extract a and b from translate(a b) pattern"""
        self.translateX = groups[0]
        self.translateY = 0
        if len(groups) == 2:
            self.translateY = groups[1]

    def extractScale(self,groups):
        """extract a and b from scale(a b) pattern"""
        self.scaleX = groups[0]
        self.scaleY = groups[0]
        if len(groups) == 2:
            self.scaleY = groups[1]

    def extractRotate(self,groups):
        """extract a,b and c from rotate(a b c) pattern"""
        self.rotate = groups[0]
        if len(groups) == 3:
            self.rX = groups[1]
            self.rY = groups[2]

    def extractMatrix(self,groups):
        """extract a,b,c,d,e,f from matrix(a b c d e f) pattern"""
        a = groups[0]
        b = groups[1]
        c = groups[2]
        d = groups[3]
        e = groups[4]
        f = groups[5]
        self.translateX = e
        self.translateY = f
        self.scaleX = math.sqrt(a*a+b*b)
        self.scaleY = math.sqrt(c*c+d*d)
        self.rotate = (180/math.pi) * math.atan2(d,c) - 90
        
