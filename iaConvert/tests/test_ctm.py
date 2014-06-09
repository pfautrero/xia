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

from iaConvert.ia2.ctm import CurrentTransformation
from nose.tools import *
import math

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

