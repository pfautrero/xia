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

function Xia(params) {
    "use strict";
    this.initKonva()
    this.initDetectArea()
    this.fullScreenAbility()
    this.start(params)
}

Xia.prototype.start = function(params) {
  this.params = params
  var myhooks = this.params.hooks
  this.canvas = document.getElementById(this.params.targetID)

  this.iaObjects = []
  this.backgroundLoaded = $.Deferred()
  this.backgroundLoaded.done(function(value){
    this.backgroundCallback()
  }.bind(this))

  if (this.params.scene.path !== "") {
    var tempCanvas = this.convertPath2Image(this.params.scene)
    this.params.scene.image = tempCanvas.toDataURL()
    this.backgroundLoaded.resolve(0)
  }
  else if ('group' in this.params.scene) {
    this.convertGroup2Image(this.params.scene)
  }
  else {
    this.backgroundLoaded.resolve(0)
  }
}

Xia.prototype.initKonva = function() {
  // fix bug in retina and amoled screens
  Konva.pixelRatio = 1;

  Konva.Shape.prototype.setXiaParent = function(xiaparent) {
      this.xiaparent = xiaparent;
  }
  Konva.Shape.prototype.getXiaParent = function() {
      return this.xiaparent;
  }
  Konva.Shape.prototype.setIaObject = function(iaobject) {
      this.iaobject = iaobject;
  }
  Konva.Shape.prototype.getIaObject = function() {
      return this.iaobject;
  }


}

Xia.prototype.initDetectArea = function() {
  // area located under the canvas. If mouse over is detected,
  // we must re-activate mouse events on canvas

  var detect = document.getElementById("detect")
  detect.addEventListener("mouseover", function()
  {
    this.canvas.style.pointerEvents="auto"
    if ((IaScene.element !== 0) && (typeof(IaScene.element) !== 'undefined')) {
      for (var i in IaScene.element.xiaDetail) {
        var xiaDetail = IaScene.element.xiaDetail[i]
        if ((xiaDetail.kineticElement.getClassName() == "Sprite") &&
          (xiaDetail.persistent == "off")) {
            xiaDetail.kineticElement.animation("hidden")
        }
        else {
          xiaDetail.kineticElement.fillPriority('color');
          xiaDetail.kineticElement.fill('rgba(0,0,0,0)');
        }
      }
    }
  }.bind(this), false);
  detect.addEventListener("touchstart", function()
  {
    this.canvas.style.pointerEvents="auto";
    if ((IaScene.element !== 0) && (typeof(IaScene.element) !== 'undefined')) {
      for (var i in IaScene.element.xiaDetail) {
        var xiaDetail = IaScene.element.xiaDetail[i]
        if ((xiaDetail.kineticElement.getClassName() == "Sprite") &&
          (xiaDetail.persistent == "off")) {
            xiaDetail.kineticElement.animation("hidden")
        }
        else {
          xiaDetail.kineticElement.fillPriority('color');
          xiaDetail.kineticElement.fill('rgba(0,0,0,0)');
        }
      }
    }
  }.bind(this), false);

}

Xia.prototype.backgroundCallback = function() {


  // Load XiaElements when Background Image is loaded

  this.imageObj = new Image()
  this.imageObj.src = this.params.scene.image
  this.imageObj.onload = function() {
      var mainScene = new IaScene(this.params.scene.width,this.params.scene.height, this.params.scene.ratio)
      mainScene.scaleScene()
      this.mainScene = mainScene

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
          scale: {x:this.mainScene.coeff,y:this.mainScene.coeff},
          image: this.imageObj
      })

      // cache used over background image
      var baseCache = new Konva.Rect({
          x: 0,
          y: this.mainScene.y,
          width: this.params.scene.width,
          height: this.params.scene.height,
          scale: {x:this.mainScene.coeff,y:this.mainScene.coeff},
          fill: this.mainScene.backgroundCacheColor
      })

      // define area to disable canvas events management when
      // mouse is over. Thus, we can reach div located under canvas
      var disableArea = new Konva.Rect({
          x: this.mainScene.width  * this.mainScene.ratio,
          y: this.mainScene.y,
          width: this.mainScene.width * (1 - this.mainScene.ratio),
          height: this.mainScene.height
      })

      disableArea.on('mouseover touchstart', function() {
          this.canvas.style.pointerEvents="none";
      }.bind(this))

      this.layers = {}
      this.layers.modalBackground = new Konva.Layer()
      this.layers.baseImage = new Konva.Layer()
      this.layers.disableArea = new Konva.Layer()
      this.layers.zoomLayer = new Konva.Layer()
      this.layers.mainLayer = new Konva.Layer()

      this.layers.modalBackground.add(baseCache)
      this.layers.baseImage.add(baseImage)
      this.layers.disableArea.add(disableArea)

      stage.add(this.layers.modalBackground);
      stage.add(this.layers.baseImage);
      stage.add(this.layers.disableArea);
      stage.add(this.layers.zoomLayer);
      stage.add(this.layers.mainLayer);

      myhooks.beforeMainConstructor(mainScene, this);
      for (var i in details) {
        this.iaObjects[i] = new IaObject({
          imageObj: this.imageObj,
          detail: details[i],
          layer: this.layers.mainLayer,
          idText: "collapse" + i,
          baseImage: baseImage,
          iaScene: mainScene,
          background_layer: this.layers.baseImage,
          backgroundCache_layer: this.layers.modalBackground,
          zoomLayer: this.layers.zoomLayer,
          myhooks: myhooks
        })
      }

      myhooks.afterMainConstructor(mainScene, this);

  }.bind(this);
}

Xia.prototype.toggleFullScreen = function() {
    if (!document.fullscreenElement &&    // alternative standard method
        !document.mozFullScreenElement && !document.webkitFullscreenElement) {  // current working methods
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }
}

Xia.prototype.restart = function() {
  var params = this.params
  // remove all Konva events
  for (var j in this.iaObjects) {
    for (var i in this.iaObjects[j].xiaDetail) {
      this.iaObjects[j].xiaDetail[i].kineticElement.off("mouseover")
      this.iaObjects[j].xiaDetail[i].kineticElement.off("mouseleave")
      this.iaObjects[j].xiaDetail[i].kineticElement.off("click touchstart")
    }
  }

  // remove Konva objects
  if (typeof this.stage === "object") this.stage.destroy()

  // remove iaScene objects
  delete this.mainScene.element

  // remove Xia objects
  Object.keys(this).forEach(function(key) {
      delete this[key]
  }.bind(this))

  // restart Xia
  this.start(params)
}

Xia.prototype.fullScreenAbility = function() {
  var e = document.getElementById("title")
  e.onclick = function() {
    this.toggleFullScreen()
  }.bind(this)
  document.addEventListener("fullscreenchange", function () {
    this.mainScene.scaleScene()
    this.restart()
  }.bind(this), false);

  document.addEventListener("mozfullscreenchange", function () {
    this.mainScene.scaleScene()
    this.restart()
  }.bind(this), false);

  document.addEventListener("webkitfullscreenchange", function () {
    this.mainScene.scaleScene()
    this.restart()
  }.bind(this), false);

}
/*
 * convert path to image if this path is used as background
 * transform scene.path to scene.image
 */
Xia.prototype.convertPath2Image = function(scene) {
  var tempCanvas = document.createElement('canvas')
  tempCanvas.setAttribute('width', scene.width)
  tempCanvas.setAttribute('height', scene.height)
  var tempContext = tempCanvas.getContext('2d')
  // Arghh...forced to remove single quotes from scene.path...
  var currentPath = new Path2D(scene.path.replace(/'/g, ""))
  tempContext.beginPath()
  tempContext.fillStyle = scene.fill
  tempContext.fill(currentPath)
  tempContext.strokeStyle = scene.stroke
  tempContext.lineWidth = scene.strokewidth
  tempContext.stroke(currentPath)
  //scene.image = tempCanvas.toDataURL()
  return tempCanvas
}

Xia.prototype.convertGroup2Image = function(scene) {
  var nbImages = 0
  var nbImagesLoaded = 0
  var tempCanvas = document.createElement('canvas')
  tempCanvas.setAttribute('width', scene.width)
  tempCanvas.setAttribute('height', scene.height)
  var tempContext = tempCanvas.getContext('2d')
  tempContext.beginPath()
  for (var i in scene['group']) {
    if (typeof(scene['group'][i].image) != "undefined") {
      nbImages++
    }
  }
  for (var i in scene['group']) {
      if (typeof(scene['group'][i].path) != "undefined") {
        // Arghh...forced to remove single quotes from scene.path...
        var currentPath = new Path2D(scene['group'][i].path.replace(/'/g, ""))
        tempContext.fillStyle = scene['group'][i].fill
        tempContext.fill(currentPath)
        tempContext.strokeStyle = scene['group'][i].stroke
        tempContext.lineWidth = scene['group'][i].strokewidth
        tempContext.stroke(currentPath)
      }
      else if (typeof(scene['group'][i].image) != "undefined") {
        var tempImage = new Image()
        tempImage.onload = (function(main, imageItem){
          return function(){
              tempContext.drawImage(this,
                0, 0, this.width, this.height,
                imageItem.x, imageItem.y, this.width, this.height)
              nbImagesLoaded++
              if (nbImages == nbImagesLoaded) {
                  scene.image = tempCanvas.toDataURL()
                  main.backgroundLoaded.resolve(0)
              }
          }
        })(this, scene['group'][i])

        tempImage.src = scene['group'][i].image
      }
  }
  if (nbImages == 0) {
    scene.image = tempCanvas.toDataURL()
    this.backgroundLoaded.resolve(0)
  }
}
