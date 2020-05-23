//   This program is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//   You should have received a copy of the GNU General Public License
//   along with this program.  If not, see <http://www.gnu.org/licenses/>
//
//
// @author : pascal.fautrero@gmail.com

/**
 *
 * @param {type} originalWidth
 * @param {type} originalHeight
 * @constructor create image active scene
 */
function IaScene (originalWidth, originalHeight, ratio) {
  'use strict'

  //  canvas width
  this.width = 1000

  // canvas height
  this.height = 800

  // w2 = w1 * originalRatio
  this.originalRatio = ratio

  // default color used to fill shapes during mouseover
  var _colorOver = { red: 66, green: 133, blue: 244, opacity: 0.6 }

  // default color used to fill stroke around shapes during mouseover
  var _colorOverStroke = { red: 255, green: 0, blue: 0, opacity: 1 }

  // default color used to fill shapes if defined as cache
  this.colorPersistent = { red: 124, green: 154, blue: 174, opacity: 1 }
  var _colorPersistent = { red: 124, green: 154, blue: 174, opacity: 1 }

  // color used over background image during focus
  var _colorCache = { red: 0, green: 0, blue: 0, opacity: 0.8 }

  // Image ratio on the scene
  // Warning : hack to suit css media-queries rules !!
  this.ratio = 1
  // padding-top in the canvas
  this.y = 0

  // internal
  this.fullScreen = 'off'
  this.backgroundCacheColor = this.getRGBAColor(_colorCache)
  this.cacheColor = this.getRGBAColor(_colorPersistent)
  this.overColor = this.getRGBAColor(_colorOver)
  this.overColorStroke = this.getRGBAColor(_colorOverStroke)
  this.scale = 1
  this.zoomActive = 0
  this.element = null
  this.originalWidth = originalWidth
  this.originalHeight = originalHeight
  this.coeff = (this.width * this.ratio) / parseFloat(originalWidth)
  this.cursorState = ''
  this.noPropagation = false
}
IaScene.prototype.getRGBAColor = function (jsonColor) {
  return 'rgba(RED, GREEN, BLUE, OPACITY)'
    .replace('RED', jsonColor.red)
    .replace('GREEN', jsonColor.green)
    .replace('BLUE', jsonColor.blue)
    .replace('OPACITY', jsonColor.opacity)
}

IaScene.prototype.scaleScene = function (xiaObject) {
  var mainScene = xiaObject.mainScene
  var viewportWidth = document.getElementById(xiaObject.params.targetID).offsetWidth
  var viewportHeight = document.getElementById(xiaObject.params.targetID).offsetHeight

  var coeffWidth = viewportWidth / mainScene.originalWidth
  var coeffHeight = viewportHeight / mainScene.originalHeight
  if ((parseFloat(viewportWidth.toFixed(5)) >= parseFloat((mainScene.originalWidth * coeffWidth).toFixed(5))) &&
    (parseFloat(viewportHeight.toFixed(5)) >= parseFloat((mainScene.originalHeight * coeffWidth).toFixed(5)))) {
    mainScene.width = viewportWidth
    mainScene.coeff = mainScene.width / mainScene.originalWidth
    mainScene.height = mainScene.originalHeight * mainScene.coeff
  } else if ((parseFloat(viewportWidth.toFixed(5)) >= parseFloat((mainScene.originalWidth * coeffHeight).toFixed(5))) &&
    (parseFloat(viewportHeight.toFixed(5)) >= parseFloat((mainScene.originalHeight * coeffHeight).toFixed(5)))) {
    mainScene.height = viewportHeight
    mainScene.coeff = mainScene.height / mainScene.originalHeight
    mainScene.width = mainScene.originalWidth * mainScene.coeff
  }
}
