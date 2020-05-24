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
 * Main
 * Initialization
 *
 * 1rst layer : div "detect" - if clicked, enable canvas events
 * 2nd layer : bootstrap accordion
 * 3rd layer : div "canvas" containing images and paths
 * 4th layer : div "disablearea" - if clicked, disable events canvas
 */

function Xia (params) {
  'use strict'
  this.params = params
  if (!('hooks' in this.params)) { this.params.hooks = {} }
  if (this.params.hooks == null) { this.params.hooks = {} }
  if ('duringXiaInit' in this.params.hooks) { this.params.hooks.duringXiaInit(this) }
  this.initKonva()
  this.addDocumentUndoEvents()
  this.start()
}

Xia.prototype.initKonva = function () {
  // fix bug in retina and amoled screens
  Konva.pixelRatio = 1
  if (!('setXiaParent' in Konva.Shape.prototype)) {
    Konva.Shape.prototype.setXiaParent = function (xiaparent) {
      this.xiaparent = xiaparent
    }
  }
  if (!('getXiaParent' in Konva.Shape.prototype)) {
    Konva.Shape.prototype.getXiaParent = function () {
      return this.xiaparent
    }
  }
  if (!('setIaObject' in Konva.Shape.prototype)) {
    Konva.Shape.prototype.setIaObject = function (iaobject) {
      this.iaobject = iaobject
    }
  }
  if (!('getIaObject' in Konva.Shape.prototype)) {
    Konva.Shape.prototype.getIaObject = function () {
      return this.iaobject
    }
  }
}

Xia.prototype.start = function () {
  this.canvas = document.getElementById(this.params.targetID)
  this.iaObjects = []
  this.focusedObj = null
  var loadBackground = new Promise(function (resolve, reject) {
    if (('path' in this.params.scene) && (this.params.scene.path !== '')) {
      var tempCanvas = this.convertPath2Image(this.params.scene)
      this.params.scene.image = tempCanvas.toDataURL()
      resolve(0)
    } else if ('group' in this.params.scene) {
      this.convertGroup2Image(this.params.scene, resolve)
    } else {
      resolve(0)
    }
  }.bind(this))

  loadBackground.then(function (value) {
    this.buildScene()
  }.bind(this))
}

Xia.prototype.buildScene = function () {
  // Load XiaElements when Background Image is loaded
  this.imageObj = new Image()
  // allowing images coming from another server
  this.imageObj.crossOrigin = "Anonymous"
  this.imageObj.src = this.params.scene.image
  this.imageObj.onload = function () {
    if (!('width' in this.params.scene) || !('height' in this.params.scene)) {
      this.params.scene.width = this.imageObj.width
      this.params.scene.height = this.imageObj.height
      this.params.scene.ratio = 1
    }
    var mainScene = new IaScene(
      this.params.scene.width,
      this.params.scene.height,
      this.params.scene.ratio
    )
    this.mainScene = mainScene
    if ('scaleScene' in this.params.hooks) {
      this.params.hooks.scaleScene(this)
    } else {
      this.mainScene.scaleScene(this)
    }
    var stage = new Konva.Stage({
      container: this.params.targetID,
      width: this.mainScene.width,
      height: this.mainScene.height
    })
    this.stage = stage
    // area containing image background
    var baseImage = new Konva.Image({
      x: 0,
      y: this.mainScene.y,
      width: this.params.scene.width,
      height: this.params.scene.height,
      scale: { x: this.mainScene.coeff, y: this.mainScene.coeff },
      image: this.imageObj
    })
    // cache used over background image
    // to darken it during detail focus
    var baseCache = new Konva.Rect({
      x: 0,
      y: this.mainScene.y,
      width: this.params.scene.width,
      height: this.params.scene.height,
      scale: { x: this.mainScene.coeff, y: this.mainScene.coeff },
      fill: this.mainScene.backgroundCacheColor
    })
    this.layers = {}
    this.layers.modalBackground = new Konva.Layer()
    this.layers.baseImage = new Konva.Layer()
    this.layers.mainLayer = new Konva.Layer()
    this.layers.modalBackground.add(baseCache)
    this.layers.baseImage.add(baseImage)

    stage.add(this.layers.modalBackground)
    stage.add(this.layers.baseImage)
    stage.add(this.layers.mainLayer)

    for (let i in this.params.details) {
      this.iaObjects[i] = new IaObject({
        parent: this,
        imageObj: this.imageObj,
        detail: this.params.details[i],
        layer: this.layers.mainLayer,
        idText: 'collapse' + i,
        baseImage: baseImage,
        iaScene: mainScene,
        background_layer: this.layers.baseImage,
        backgroundCache_layer: this.layers.modalBackground,
        myhooks: this.params.hooks
      })
    }
    this.addUndoEvents()
    if ('loaded' in this.params.hooks) this.params.hooks.loaded(this)
  }.bind(this)
}

Xia.prototype.reorderItems = function () {
  do {
    var swap = false
    for (let j = 0; j < this.iaObjects.length - 1; j++) {
      if (this.iaObjects[j].group.getZIndex() > this.iaObjects[j + 1].group.getZIndex()) {
        this.iaObjects[j].group.moveDown()
        swap = true
        break
      }
    }
  }
  while (swap)
}

Xia.prototype.addDocumentUndoEvents = function () {
  document.addEventListener('click', function () {
    var overBox = false
    var boxes = document.querySelectorAll(':hover')
    for (let i = 0; i < boxes.length; i++) {
      if (boxes[i].className === 'konvajs-content') overBox = true
    }
    if (!overBox) {
      if (!('mainScene' in this)) return
      if (this.mainScene.element === null) return
      for (let j in this.mainScene.element.xiaDetail) {
        if (this.mainScene.element === null) break
        var xiaDetail = this.mainScene.element.xiaDetail[j]
        if (this.mainScene.zoomActive === 0) {
          this.mainScene.cursorState = 'default'
          xiaDetail.kineticElement.fire('mouseleave')
        } else {
          xiaDetail.kineticElement.fire('click')
        }
      }
      this.mainScene.element = null
    }
  }.bind(this), false)
}

Xia.prototype.addUndoEvents = function () {
// Events applyed on stage and document
// to unselect elements if user clicks out of scene
  this.stage.on('click touchstart', function (e) {
    if (!('event' in this)) this.event = null
    if (this.event !== null) {
      this.event.then(function (value) {
        this.manageStage()
      }.bind(this))
      this.event = null
    } else {
      this.manageStage()
    }
  }.bind(this))
}

Xia.prototype.manageStage = function () {
  var xiaDetail
  if (this.mainScene.zoomActive === 0) {
    var shape = this.layers.mainLayer.getIntersection(this.stage.getPointerPosition())
    if (this.mainScene.element === null) return
    if ((shape === null) && this.mainScene.element) {
      for (let j in this.mainScene.element.xiaDetail) {
        xiaDetail = this.mainScene.element.xiaDetail[j]
        this.mainScene.cursorState = 'default'
        xiaDetail.kineticElement.fire('mouseleave')
      }
    } else if (shape !== null) {
      if (shape.getXiaParent().parent !== this.mainScene.element) {
        for (let j in this.mainScene.element.xiaDetail) {
          xiaDetail = this.mainScene.element.xiaDetail[j]
          this.mainScene.cursorState = 'default'
          xiaDetail.kineticElement.fire('mouseleave')
        }
        this.mainScene.element = null
      }
    }
  } else {
    if (!this.mainScene.element) return
    if (this.mainScene.element.group.scaleX().toFixed(5) === (this.mainScene.element.agrandissement).toFixed(5)) {
      for (let j in this.mainScene.element.xiaDetail) {
        if (this.mainScene.element == null) break // used to stop firing events on grouped Konva shapes
        xiaDetail = this.mainScene.element.xiaDetail[j]
        xiaDetail.kineticElement.fire('click')
      }
    }
  }
}

Xia.prototype.stop = function () {
  var params = this.params
  // remove all Konva events
  for (let j in this.iaObjects) {
    for (let i in this.iaObjects[j].xiaDetail) {
      if (this.iaObjects[j].xiaDetail[i].kineticElement) {
        this.iaObjects[j].xiaDetail[i].kineticElement.off('mouseover')
        this.iaObjects[j].xiaDetail[i].kineticElement.off('mouseleave')
        this.iaObjects[j].xiaDetail[i].kineticElement.off('click touchstart')
      }
    }
  }
  // remove Konva objects
  if (typeof this.stage === 'object') this.stage.destroy()
  // remove iaScene objects
  delete this.mainScene.element
  // remove Xia objects
  Object.keys(this).forEach(function (key) {
    delete this[key]
  }.bind(this))
  this.params = params
}

Xia.prototype.restart = function () {
  this.stop()
  this.start()
}

/*
 * convert path to image if this path is used as background
 * transform scene.path to scene.image
 */
Xia.prototype.convertPath2Image = function (scene) {
  var tempCanvas = document.createElement('canvas')
  tempCanvas.setAttribute('width', scene.width)
  tempCanvas.setAttribute('height', scene.height)
  var tempContext = tempCanvas.getContext('2d')
  // Arghh...forced to remove single quotes from scene.path...
  var currentPath = new Path2D(scene.path.replace(/'/g, ''))
  tempContext.beginPath()
  tempContext.fillStyle = scene.fill
  tempContext.fill(currentPath)
  tempContext.strokeStyle = scene.stroke
  tempContext.lineWidth = scene.strokewidth
  tempContext.stroke(currentPath)
  // scene.image = tempCanvas.toDataURL()
  return tempCanvas
}

Xia.prototype.convertGroup2Image = function (scene, resolve) {
  var nbImages = 0
  var nbImagesLoaded = 0
  var tempCanvas = document.createElement('canvas')
  tempCanvas.setAttribute('width', scene.width)
  tempCanvas.setAttribute('height', scene.height)
  var tempContext = tempCanvas.getContext('2d')
  tempContext.beginPath()
  for (let i in scene['group']) {
    if (typeof scene['group'][i].image !== 'undefined') {
      nbImages++
    }
  }
  for (let i in scene['group']) {
    if (typeof scene['group'][i].path !== 'undefined') {
      // Arghh...forced to remove single quotes from scene.path...
      var currentPath = new Path2D(scene['group'][i].path.replace(/'/g, ''))
      tempContext.fillStyle = scene['group'][i].fill
      tempContext.fill(currentPath)
      tempContext.strokeStyle = scene['group'][i].stroke
      tempContext.lineWidth = scene['group'][i].strokewidth
      tempContext.stroke(currentPath)
    } else if (typeof scene['group'][i].image !== 'undefined') {
      var tempImage = new Image()
      tempImage.onload = (function (main, imageItem) {
        tempContext.drawImage(
          this,
          0,
          0,
          this.width,
          this.height,
          imageItem.x,
          imageItem.y,
          this.width,
          this.height
        )
        nbImagesLoaded++
        if (nbImages === nbImagesLoaded) {
          scene.image = tempCanvas.toDataURL()
          resolve(0)
        }
      })(this, scene['group'][i])

      tempImage.src = scene['group'][i].image
    }
  }
  if (nbImages === 0) {
    scene.image = tempCanvas.toDataURL()
    resolve(0)
  }
}
