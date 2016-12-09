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

from xiaconverter.iaobject import iaObject
from xiaconverter.logger import Logger
from nose.tools import *
from xml.dom import minidom
import tempfile
import os

class LoggerMock(Logger):
    def display(self, msg):
        pass

class TestiaObject:

    def test_extractRaster(self):
        console = LoggerMock()
        ia = iaObject(console)
        # XIA logo 16x16
        originalRaster = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=='
        rasterExtracted = ia.extractRaster(originalRaster)
        assert_equal(rasterExtracted, originalRaster)

    def test_fixRaster(self):
        console = LoggerMock()
        ia = iaObject(console)
        # XIA logo 16x16
        originalRaster = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3gofDSYCgyL5zAAAAlVJREFUOMttk01IVFEUx3/3zodjZoVJWpuytDSS3kMSKneRRtuSdq2sUSGYje3aZNGHm9EyTRetIhUiCAkjC8KgFsJ7JBgKSUE5KpNo2TjOzLu3xczTl/hf3Xu+z/+cI8jBiFrYERMjalUC14CzQFlOPQOMAt12xJx0bQHEJud+oMkNKgN5qEwatMKDPjtihl0f4XEeB2pcK+2kmbrXSOn5VnYZ9WzCZ8AAtPRkrvFaqFSStYXv/By6zRaoBnrsiInM9dyEkCDkuoXOpEEIZF4+ybmvOKt/vHoBhI2oVe4rPdd8U0jfifmRHhIzFqG95TiJZaY7GtGZNCr5l/iHQeZHnyD9QQoOmt5KpDCi1rQM5ldMtNXirK6glQIBQvrwhQrYadSD1ixZI6hUkpKGq5Q0hEFrgIwwolYKCAgpmX3ZyeLH5zjJFQKFxRy99Q6dSWVr9geZvHGG/ZfvsK3MBHRW7gbIFiRZeP2Y2KtHHGkbJLTvMPGxARCC4rpLW5GJBL5tMCNI/44DkLfnAFopluwRZl90uCVvhiOBN+vMK8WOqjqEkMSGuxBScqi1n+r7n0CIbDtCeAP0SqB7468pqKhFKUV8bIBfY8/whQrxhbYTG+5i4vpJfgy1e8fZ6a5yH3DFla7NzfDl7gWklIhAELTOjlQpjrW/xV9YBNBrR8wW7ypbwPHskgicxDLx909ZHB9GSj9Fpy+y+1QjMhgCmAIq/zum3LsHCK+TKiUIX44fxz2qXjtitriJJeCeprYjZnMu8gMgoZVCO2m0k06g1UOgyusM8A8PqAKAYqQluwAAAABJRU5ErkJggg=='
        rasterFixed = ia.fixRaster(originalRaster, 16, 16)
        assert_equal(rasterFixed, originalRaster)
