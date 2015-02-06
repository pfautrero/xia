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

import re, math

class CurrentTransformation:
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
   
    """

    def __init__(self):
        """Init"""
        self.matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        self.rotate = 0
        self.rX = 0
        self.rY = 0
        self.translateX = 0
        self.translateY = 0
        self.scaleX = 1
        self.scaleY = 1

    def analyze(self,entry):
        """Analyze transform attribute"""
        regex_group = r'([^\s,]*)\s*,?\s*'
        
        # look for something with such a form : "matrix(a b c d e f)"
        regex_matrix = r'matrix\(\s*' + regex_group * 6 + r'\)'
        matchObj = re.match( regex_matrix, entry)
        if matchObj:
            self.extractMatrix(matchObj.groups())
            return

        # look for something with such a form : "translate(a)"
        regex_translate = r'translate\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_translate, entry)
        if matchObj:
            self.extractTranslate(matchObj.groups())
            return

        # look for something with such a form : "translate(a b)"
        regex_translate = r'translate\(\s*' + regex_group * 2 + r'\)'
        matchObj = re.match( regex_translate, entry)
        if matchObj:
            self.extractTranslate(matchObj.groups())
            return

        # look for something with such a form : "rotate(a)"
        regex_rotate = r'rotate\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_rotate, entry)
        if matchObj:
            self.extractRotate(matchObj.groups())
            return        
       
        # look for something with such a form : "rotate(a b c)"
        regex_rotate = r'rotate\(\s*' + regex_group * 3 + r'\)'
        matchObj = re.match( regex_rotate, entry)
        if matchObj:
            self.extractRotate(matchObj.groups())
            return        

        # look for something with such a form : "scale(a)"
        regex_scale = r'scale\(\s*' + regex_group * 1 + r'\)'
        matchObj = re.match( regex_scale, entry)
        if matchObj:
            self.extractScale(matchObj.groups())
            return        

        # look for something with such a form : "scale(a b)"
        regex_scale = r'scale\(\s*' + regex_group * 2 + r'\)'
        matchObj = re.match( regex_scale, entry)
        if matchObj:
            self.extractScale(matchObj.groups())
            return        

        
    def extractTranslate(self,groups):
        """extract a and b from translate(a b) pattern"""
        self.translateX = groups[0]
        self.translateY = groups[0]
        if len(groups) == 2 and groups[1]:
            self.translateY = groups[1]
        self.matrix = [[1.0, 0.0, float(self.translateX)], \
          [0.0, 1.0, float(self.translateY)]]

    def extractScale(self,groups):
        """extract a and b from scale(a b) pattern"""
        self.scaleX = groups[0]
        self.scaleY = groups[0]        
        if len(groups) == 2 and groups[1]:
            self.scaleY = groups[1]
        self.matrix = [[float(self.scaleX), 0.0, 0.0], \
          [0.0, float(self.scaleY), 0.0]]
        
        
    def extractRotate(self,groups):
        """extract a,b and c from rotate(a b c) pattern
            cos(a)  -sin(a)  -cx.cos(a) + cy.sin(a) + cx
            sin(a)   cos(a)  -cx.sin(a) - cy.cos(a) + cy
            0       0        1
        """
        self.rotate = groups[0]
        self.rX = "0"
        self.rY = "0"
        if len(groups) == 3:
            if groups[1]:
            	self.rX = groups[1]
            if groups[2]:
            	self.rY = groups[2]
            
        alpha = float(self.rotate)
        cx = float(self.rX)
        cy = float(self.rY)
        self.matrix = [ [
                          math.cos(alpha), 
                          -math.sin(alpha), 
                          -cx * math.cos(alpha) + cy * math.sin(alpha) + cx
                        ], 
                        [
                          math.sin(alpha), 
                          math.cos(alpha), 
                          -cx * math.sin(alpha) - cy * math.cos(alpha) + cy
                        ]
                    ]
        
    def extractMatrix(self,groups):
        """extract a,b,c,d,e,f from matrix(a b c d e f) pattern"""
        a = groups[0]
        b = groups[1]
        c = groups[2]
        d = groups[3]
        e = groups[4]
        f = groups[5]
        self.matrix=[[float(a),float(c),float(e)], [float(b),float(d),float(f)]]
        self.translateX = e
        self.translateY = f
        self.scaleX = math.sqrt(float(a)**2+float(c)**2)
        self.scaleY = math.sqrt(float(b)**2+float(d)**2)
        self.rotate = math.atan2(float(b),float(d))
        
    def rectToPath(self,node):
        """inspired from inkscape pathmodifier.py"""
        x = float(node['x'])
        y = float(node['y'])
        w = float(node['width'])
        h = float(node['height'])        
        rx = 0
        ry = 0
        if 'rx' in node:
            rx = float(node['rx'])
        if 'ry' in node:
            ry = float(node['ry'])

        if rx==0 or ry ==0:
            d ='M %f,%f '%(x,y)
            d+='L %f,%f '%(x+w,y)
            d+='L %f,%f '%(x+w,y+h)
            d+='L %f,%f '%(x,y+h)
            d+='L %f,%f '%(x,y)
        else:
            d ='M %f,%f '%(x+rx,y)
            d+='L %f,%f '%(x+w-rx,y)
            d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,x+w,y+ry)
            d+='L %f,%f '%(x+w,y+h-ry)
            d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,x+w-rx,y+h)
            d+='L %f,%f '%(x+rx,y+h)
            d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,x,y+h-ry)
            d+='L %f,%f '%(x,y+ry)
            d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,x+rx,y)
            
        return d

    def circleToPath(self,node):
        """inspired from inkscape pathmodifier.py"""
        cx = float(node['cx'])
        cy = float(node['cy'])
        r = 0
        if 'r' in node:
            r = float(node['r'])

        d ='M %f,%f '%(cx-r,cy)
        d+='A %f,%f 0 0 1 %f,%f'%(r,r,cx,cy-r)
        d+='A %f,%f 0 0 1 %f,%f'%(r,r,cx+r,cy)
        d+='A %f,%f 0 0 1 %f,%f'%(r,r,cx,cy+r)
        d+='A %f,%f 0 0 1 %f,%f'%(r,r,cx-r,cy)

        return d

    def ellipseToPath(self,node):
        """inspired from inkscape pathmodifier.py"""
        cx = float(node['cx'])
        cy = float(node['cy'])
        rx = 0
        ry = 0
        if 'rx' in node:
            rx = float(node['rx'])
        if 'ry' in node:
            ry = float(node['ry'])

        d ='M %f,%f '%(cx-rx,cy)
        d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,cx,cy-ry)
        d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,cx+rx,cy)
        d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,cx,cy+ry)
        d+='A %f,%f 0 0 1 %f,%f'%(rx,ry,cx-rx,cy)

        return d

    def applyTransformToPoint(self,mat,pt):
        x = mat[0][0]*pt[0] + mat[0][1]*pt[1] + mat[0][2]
        y = mat[1][0]*pt[0] + mat[1][1]*pt[1] + mat[1][2]
        pt[0]=x
        pt[1]=y

    def applyTransformToPath(self,mat,path):
        for comp in path:
            for ctl in comp:
                for pt in ctl:
                    self.applyTransformToPoint(mat,pt)
