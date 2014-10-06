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

from src.xiaconverter.ctm import CurrentTransformation
from nose.tools import *
import math

import xiaconverter.cubicsuperpath

class TestCurrentTransformation:

    def test_analyze_translate(self):
        ctm = CurrentTransformation();
        ctm.analyze("translate( 10   )")
        assert_equal(ctm.translateX, "10")
        assert_equal(ctm.translateY, "10")
        assert_equal(ctm.matrix, [[1.0, 0.0, 10.0], [0.0, 1.0, 10.0]])

        ctm.analyze("translate(10   20)")
        assert_equal(ctm.translateX, "10")
        assert_equal(ctm.translateY, "20")
        assert_equal(ctm.matrix, [[1.0, 0.0, 10.0], [0.0, 1.0, 20.0]])

        ctm.analyze("translate(10   , -10)")
        assert_equal(ctm.translateX, "10")
        assert_equal(ctm.translateY, "-10")
        assert_equal(ctm.matrix, [[1.0, 0.0, 10.0], [0.0, 1.0, -10.0]])		


    def test_analyze_scale(self):
        ctm = CurrentTransformation();
        ctm.analyze("scale(10)")
        assert_equal(ctm.scaleX, "10")
        assert_equal(ctm.scaleY, "10")
        assert_equal(ctm.matrix, [[10, 0.0, 0.0], [0.0, 10, 0.0]])

        ctm.analyze("scale(10 20)")
        assert_equal(ctm.scaleX, "10")
        assert_equal(ctm.scaleY, "20")
        assert_equal(ctm.matrix, [[10, 0.0, 0.0], [0.0, 20, 0.0]])

        ctm.analyze("scale(10,-10)")
        assert_equal(ctm.scaleX, "10")
        assert_equal(ctm.scaleY, "-10")
        assert_equal(ctm.matrix, [[10, 0.0, 0.0], [0.0, -10, 0.0]])		

    def test_analyze_rotate(self):
        ctm = CurrentTransformation();
        ctm.analyze("rotate(10 20 -30)")
        assert_equal(ctm.rotate, "10")
        assert_equal(ctm.rX, "20")
        assert_equal(ctm.rY, "-30")		
        assert_equal(ctm.matrix, 
            [ 
                [
                    math.cos(10), 
                    -math.sin(10), 
                    -20 * math.cos(10) - 30 * math.sin(10) + 20
                ], 
                [
                    math.sin(10), 
                    math.cos(10), 
                    -20 * math.sin(10) + 30 * math.cos(10) - 30
                ]
            ])

        ctm.analyze("rotate(10)")
        assert_equal(ctm.rotate, "10")
        assert_equal(ctm.rX, "0")
        assert_equal(ctm.rY, "0")		
        assert_equal(ctm.matrix, 
            [ 
                [
                    math.cos(10), 
                    -math.sin(10), 
                    0
                ], 
                [
                    math.sin(10), 
                    math.cos(10), 
                    0
                ]
            ])

    def test_analyze_matrix(self):
        ctm = CurrentTransformation();
        ctm.analyze("matrix(1 2 3 4 5 6)")
        assert_equal(ctm.translateX, "5")
        assert_equal(ctm.translateY, "6")
        assert_equal(ctm.scaleX, math.sqrt(float(1)**2+float(3)**2))
        assert_equal(ctm.scaleY, math.sqrt(float(2)**2+float(4)**2))
        assert_equal(ctm.rotate, math.atan2(float(2),float(4)))                
        # @TODO assert_equal(ctm.rX, ??)
        # @TODO assert_equal(ctm.rY, ??)		
        assert_equal(ctm.matrix, [[1.0,3.0,5.0],[2.0,4.0,6.0]])

    def test_analyze_rectToPath(self):
        ctm = CurrentTransformation();
        rect = {
            'x' : 10,
            'y' : 20,
            'width' : 50,
            'height' : 30
        }
        path = ctm.rectToPath(rect)
        assert_equal(path, "M 10.000000,20.000000 L 60.000000,20.000000 L 60.000000,50.000000 L 10.000000,50.000000 L 10.000000,20.000000 ")

        rect = {
            'x' : 10,
            'y' : 20,
            'width' : 50,
            'height' : 30,
            'rx' : 5,
            'ry' : 10
        }
        path = ctm.rectToPath(rect)
        assert_equal(path, "M 15.000000,20.000000 L 55.000000,20.000000 A 5.000000,10.000000 0 0 1 60.000000,30.000000L 60.000000,40.000000 A 5.000000,10.000000 0 0 1 55.000000,50.000000L 15.000000,50.000000 A 5.000000,10.000000 0 0 1 10.000000,40.000000L 10.000000,30.000000 A 5.000000,10.000000 0 0 1 15.000000,20.000000")

        rect = {
            'x' : 10,
            'y' : 10,
            'width' : 40,
            'height' : 40,
            'rx' : 20,
            'ry' : 20
        }
        path = ctm.rectToPath(rect)
        assert_equal(path, "M 30.000000,10.000000 L 30.000000,10.000000 A 20.000000,20.000000 0 0 1 50.000000,30.000000L 50.000000,30.000000 A 20.000000,20.000000 0 0 1 30.000000,50.000000L 30.000000,50.000000 A 20.000000,20.000000 0 0 1 10.000000,30.000000L 10.000000,30.000000 A 20.000000,20.000000 0 0 1 30.000000,10.000000")


    def test_analyze_applyTransformToPath(self):
        matrix = [[1,2,3],[4,5,6]]
        ctm = CurrentTransformation()
        path = "M 10,20 L 60,20 L 60,50 L 10,50 L 10,20"
        path_modified = "M53.0 146.0C53.0 146.0 103.0 346.0 103.0 346.0C103.0 346.0 163.0 496.0 163.0 496.0C163.0 496.0 113.0 296.0 113.0 296.0C113.0 296.0 53.0 146.0 53.0 146.0"
        p = xiaconverter.cubicsuperpath.parsePath(path)
        ctm.applyTransformToPath(matrix,p)
        path_calculated = xiaconverter.cubicsuperpath.formatPath(p)
        assert_equal(path_calculated,path_modified)
