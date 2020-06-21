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

/*
 *
 * @param {object} params
 * @constructor create image active object
 */
function IaObject (params) {
  'use strict'
  this.parent = params.parent
  this.xiaDetail = []
  this.jsonSource = params.detail
  this.layer = params.layer
  this.background_layer = params.background_layer
  this.backgroundCache_layer = params.backgroundCache_layer
  this.imageObj = params.imageObj
  this.myhooks = params.myhooks
  this.idText = params.idText
  this.zoomLayer = params.zoomLayer
  this.iaScene = params.iaScene
  this.backgroundCache_layer.draw()
  this.agrandissement = 0
  this.zoomActive = 0
  this.index = params.index
  // Bounding Area is defined by details
  this.minX = null
  this.minY = null
  this.maxX = null
  this.maxY = null
  this.tween_group = 0
  this.group = 0
  // Create kineticElements and include them in a group
  this.group = new Konva.Group()
  this.layer.add(this.group)
  var allElementsCreated = new Promise(function (resolve) {
    this.resolve = resolve
    if ('group' in params.detail) {
      this.nbElements = params.detail.group.length
      for (let i in params.detail.group) {
        this.xiaDetail[i] = this.createXiaElement(params.detail.group[i], this.idText)
      }
      this.definePathBoxSize(params.detail, this)
    } else {
      this.nbElements = 1
      this.xiaDetail[0] = this.createXiaElement(params.detail, this.idText)
    }
  }.bind(this))
  allElementsCreated.then(function (value) {
    this.defineTweens(this, params.iaScene)
    if ('afterIaObjectConstructor' in this.myhooks) {
      this.myhooks.afterIaObjectConstructor(
        params.iaScene,
        params.idText,
        params.detail,
        this
      )
    }
  }.bind(this))
}

IaObject.prototype.createXiaElement = function (jsonDetail, idDOMElement) {
  var xiaDetail = null
  if ('path' in jsonDetail) {
    xiaDetail = this.includePath(jsonDetail, idDOMElement)
  } else if ('image' in jsonDetail) {
    var re = /sprite(.*)/i
    if (('id' in jsonDetail) && (jsonDetail.id.match(re))) {
      xiaDetail = this.includeSprite(jsonDetail, idDOMElement)
    } else {
      xiaDetail = this.includeImage(jsonDetail, idDOMElement)
    }
  }
  return xiaDetail
}

IaObject.prototype.includePath = function (detail, idDOMElement) {
  var xiaPath = new XiaPath(this, detail, idDOMElement)
  xiaPath.start()
  return xiaPath
}

IaObject.prototype.includeImage = function (detail, idDOMElement) {
  var xiaImage = new XiaImage(this, detail, idDOMElement)
  xiaImage.start()
  return xiaImage
}

IaObject.prototype.includeSprite = function (detail, idDOMElement) {
  var xiaSprite = new XiaSprite(this, detail, idDOMElement)
  xiaSprite.start()
  return xiaSprite
}

/*
 *
 * @param {type} index
 * @returns {undefined}
 */
IaObject.prototype.definePathBoxSize = function (detail, that) {
  'use strict'
  if (
    (typeof detail.minX !== 'undefined') &&
    (typeof detail.minY !== 'undefined') &&
    (typeof detail.maxX !== 'undefined') &&
    (typeof detail.maxY !== 'undefined')) {
    that.minX = detail.minX
    that.minY = detail.minY
    that.maxX = detail.maxX
    that.maxY = detail.maxY
  } else {
    console.log('definePathBoxSize failure')
  }
}

/*
 * Define zoom rate and define tween effect for each group
 * @returns {undefined}
 */
IaObject.prototype.defineTweens = function (that, iaScene) {
  that.minX = that.minX * iaScene.coeff
  that.minY = that.minY * iaScene.coeff
  that.maxX = that.maxX * iaScene.coeff
  that.maxY = that.maxY * iaScene.coeff
  var largeur = that.maxX - that.minX
  var hauteur = that.maxY - that.minY
  that.agrandissement1 = (iaScene.height - iaScene.y) / hauteur // beta
  that.agrandissement2 = iaScene.width / largeur // alpha

  if (hauteur * that.agrandissement2 > iaScene.height) {
    that.agrandissement = that.agrandissement1
    that.tweenX = (0 - (that.minX)) * that.agrandissement + (iaScene.width - largeur * that.agrandissement) / 2
    that.tweenY = (0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y
  } else {
    that.agrandissement = that.agrandissement2
    that.tweenX = (0 - (that.minX)) * that.agrandissement
    that.tweenY = 1 * ((0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y + (iaScene.height - hauteur * that.agrandissement) / 2)
  }
}
