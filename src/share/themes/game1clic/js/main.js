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
// @author : pascal.fautrero@ac-versailles.fr
// @version=xxx

/*
 * Main
 * Initialization
 *
 * 1rst layer : div "detect" - if clicked, enable canvas events
 * 2nd layer : bootstrap accordion
 * 3rd layer : div "canvas" containing images and paths
 * 4th layer : div "disablearea" - if clicked, disable events canvas
 */

function main(myhooks) {
    "use strict";
    var that=window;
    that.canvas = document.getElementById("canvas");

    this.backgroundLoaded = $.Deferred()

    this.backgroundLoaded.done(function(value){

      // fix bug in retina and amoled screens
      Kinetic.pixelRatio = 1;

      Kinetic.Util.addMethods(Kinetic.Path,{
          setIaObject: function(iaobject) {
              this.iaobject = iaobject;
          },
          getIaObject: function() {
              return this.iaobject;
          }
      });

      Kinetic.Util.addMethods(Kinetic.Image,{
          setIaObject: function(iaobject) {
              this.iaobject = iaobject;
          },
          getIaObject: function() {
              return this.iaobject;
          }
      });

      Kinetic.Util.addMethods(Kinetic.Sprite,{
          setIaObject: function(iaobject) {
              this.iaobject = iaobject;
          },
          getIaObject: function() {
              return this.iaobject;
          }
      });

      Kinetic.Util.addMethods(Kinetic.Path,{
          setXiaParent: function(xiaparent) {
              this.xiaparent = xiaparent;
          },
          getXiaParent: function() {
              return this.xiaparent;
          }
      });
      Kinetic.Util.addMethods(Kinetic.Image,{
          setXiaParent: function(xiaparent) {
              this.xiaparent = xiaparent;
          },
          getXiaParent: function() {
              return this.xiaparent;
          }
      });

      Kinetic.Util.addMethods(Kinetic.Sprite,{
          setXiaParent: function(xiaparent) {
              this.xiaparent = xiaparent;
          },
          getXiaParent: function() {
              return this.xiaparent;
          }
      });

      // Load background image

      that.imageObj = new Image();
      that.imageObj.src = scene.image;
      that.imageObj.onload = function() {

          var mainScene = new IaScene(scene.width,scene.height);
          mainScene.scale = 1;
          mainScene.scaleScene(mainScene);

          var stage = new Kinetic.Stage({
              container: 'canvas',
              width: mainScene.width,
              height: mainScene.height
          });
          stage.on("mouseout touchend", function(){
              var shape = Kinetic.shapes[mainScene.currentShape];
              if (typeof(shape) != "undefined") {
                  mainScene.mouseout(shape);
              }
              mainScene.currentShape = "";
          });

          stage.on("click tap", function(){
              mainScene.currentShape = "";
              if ((mainScene.currentShape == "") || (typeof(mainScene.currentShape) == "undefined")) {
                  var mousePos = this.getPointerPosition();
                  var imageDest = mainScene.completeImage.data;
                  var position1 = 0;
                  position1 = 4 * (Math.floor(mousePos.y) * Math.floor(mainScene.width) + Math.floor(mousePos.x));
                  mainScene.currentShape = "#" + Kinetic.Util._rgbToHex(imageDest[position1 + 0], imageDest[position1 + 1], imageDest[position1 + 2]);
              }

              var shape = Kinetic.shapes[mainScene.currentShape];
              if (typeof(shape) != "undefined") {
                if (typeof(shape.getXiaParent().imgData) !== "undefined") {
                    var pos = {
                        x : Math.floor((mousePos.x - shape.x()) / mainScene.coeff),
                        y : Math.floor((mousePos.y - shape.y()) / mainScene.coeff)
                    }
                    frameIndex = (typeof(shape.getXiaParent().timeLine) !== "undefined") ? shape.getXiaParent().timeLine[shape.frameIndex()] : 0
                    if (typeof(shape.getXiaParent().timeLine) !== "undefined") {
                        var index = Math.floor(pos.y * shape.getXiaParent().imgData[frameIndex].width + pos.x)
                        var imgDataArray = shape.getXiaParent().imgData[frameIndex].data;
                    }
                    else {
                        var index = Math.floor(pos.y * shape.getXiaParent().imgData.width + frameIndex * shape.getXiaParent().width + pos.x)
                        var imgDataArray = shape.getXiaParent().imgData.data;
                    }
                    if (imgDataArray[index*4+3] == 0) {
                        // sprite not touched (Alpha = 0)
                        var shapesArray = Object.keys(Kinetic.shapes)
                        for (var i = shapesArray.length - 1; i >= 1; i--) {
                            if (shapesArray[i] != mainScene.currentShape) {
                                shape = Kinetic.shapes[shapesArray[i]]
                                var pos = {
                                    x : Math.floor((mousePos.x - shape.x()) / mainScene.coeff),
                                    y : Math.floor((mousePos.y - shape.y()) / mainScene.coeff)
                                }
                                if ((mousePos.x > shape.x()) && (mousePos.x < shape.x() + shape.getXiaParent().width)) {
                                    if ((mousePos.y > shape.y()) && (mousePos.y < shape.y() + shape.getXiaParent().height)) {
                                        if (typeof(shape.getXiaParent().timeLine) !== "undefined") {
                                            var frameIndex = shape.getXiaParent().timeLine[shape.frameIndex()]
                                            var index = pos.y * shape.getXiaParent().imgData[frameIndex].width + pos.x
                                            var d = shape.getXiaParent().imgData[frameIndex].data;

                                            if (d[index*4+3] !== 0) {
                                                shape.stop()
                                                shape.hide()
                                                mainScene.click(shape, mousePos);
                                                break
                                            }
                                        }
                                        else {
                                            if (typeof(shape.getXiaParent().imgData) !== "undefined") {
                                                var index = pos.y * shape.getXiaParent().imgData.width + pos.x
                                                var d = shape.getXiaParent().imgData.data;
                                                if (d[index*4+3] != 0) {
                                                    mainScene.click(shape, mousePos);
                                                    break
                                                }
                                            }
                                            else {
                                                mainScene.click(shape, mousePos);
                                                break
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        return
                    }
                }
                if (typeof(shape.getXiaParent().timeLine) !== "undefined") {
                    shape.stop()
                    shape.hide()
                }
                mainScene.click(shape, mousePos);
              }
          });

          stage.on("mousemove touchstart", function(){
              var mousePos = this.getPointerPosition();
              var imageDest = mainScene.completeImage.data;
              var position1 = 0;
              position1 = 4 * (Math.floor(mousePos.y) * Math.floor(mainScene.width) + Math.floor(mousePos.x));
              var shape_id = Kinetic.Util._rgbToHex(imageDest[position1 + 0], imageDest[position1 + 1], imageDest[position1 + 2]);
              var shape = Kinetic.shapes["#" + shape_id];
              if (typeof(shape) != "undefined") {
                  if (shape.colorKey != mainScene.currentShape) {
                      if (mainScene.currentShape != "") {
                          var oldShape = Kinetic.shapes[mainScene.currentShape];
                          if (typeof(oldShape) != "undefined") {
                              mainScene.mouseout(oldShape);
                          }
                      }
                      mainScene.currentShape = shape.colorKey;
                      mainScene.mouseover(shape);
                  }
              }
              else {
                  var shape = Kinetic.shapes[mainScene.currentShape];
                  if (typeof(shape) != "undefined") {
                      mainScene.mouseout(shape);
                  }
                  mainScene.currentShape = "";
              }
          });
          // area containing image background
          var baseImage = new Kinetic.Image({
              x: 0,
              y: mainScene.y,
              width: scene.width,
              height: scene.height,
              scale: {x:mainScene.coeff,y:mainScene.coeff},
              image: that.imageObj
          });


          var layers = [];
          that.layers = layers;
          layers[0] = new Kinetic.FastLayer();
          layers[0].add(baseImage);
          stage.add(layers[0]);
          myhooks.beforeMainConstructor(mainScene, that.layers);
          var indice = 1;
          layers[indice] = new Kinetic.Layer();
          stage.add(layers[indice]);

          for (var i in details) {
              var iaObj = new IaObject({
                  imageObj: that.imageObj,
                  detail: details[i],
                  layer: layers[indice],
                  idText: "article-" + i,
                  baseImage: baseImage,
                  iaScene: mainScene,
                  background_layer: layers[0],
                  myhooks: myhooks
              });
          }

          var hitCanvas = layers[indice].getHitCanvas();
          mainScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));


          myhooks.afterMainConstructor(mainScene, that.layers);
          $("#splash").fadeOut("slow", function(){
                  $("#loader").hide();
          });
          var viewportHeight = $(window).height();
          if (scene.description != "") {
              $("#rights").show();
              var content_offset = $("#rights").offset();
              var message_height = $("#popup_intro").css('height').substr(0,$("#popup_intro").css("height").length - 2);
              $("#popup_intro").css({'top':(viewportHeight - content_offset.top - message_height)/ 2 - 40});
              $("#popup_intro").show();
              $("#popup").hide();
              $("#popup_close_intro").on("click", function(){
                  $("#rights").hide();
              });
          }
          // FullScreen ability
          // source code from http://blogs.sitepointstatic.com/examples/tech/full-screen/index.html
          var e = document.getElementById("title");
          var div_container = document.getElementById("image-active");
          e.onclick = function() {
              if (runPrefixMethod(document, "FullScreen") || runPrefixMethod(document, "IsFullScreen")) {
                  runPrefixMethod(document, "CancelFullScreen");
              }
              else {
                  runPrefixMethod(div_container, "RequestFullScreen");
              }
              mainScene.fullScreen = mainScene.fullScreen == "on" ? "off": "on";
          };

          var pfx = ["webkit", "moz", "ms", "o", ""];
          function runPrefixMethod(obj, method) {
              var p = 0, m, t;
              while (p < pfx.length && !obj[m]) {
                  m = method;
                  if (pfx[p] === "") {
                      m = m.substr(0,1).toLowerCase() + m.substr(1);
                  }
                  m = pfx[p] + m;
                  t = typeof obj[m];
                  if (t != "undefined") {
                      pfx = [pfx[p]];
                      return (t == "function" ? obj[m]() : obj[m]);
                  }
                  p++;
              }
          }

      };
    })

    if (scene.path !== "") {
      var tempCanvas = this.convertPath2Image(scene)
      scene.image = tempCanvas.toDataURL()
      this.backgroundLoaded.resolve(0)
    }
    else if (typeof(scene.group) !== "undefined") {
      this.convertGroup2Image(scene)
    }
    else {
      this.backgroundLoaded.resolve(0)
    }

}

/*
 * convert path to image if this path is used as background
 * transform scene.path to scene.image
 */
main.prototype.convertPath2Image = function(scene) {
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
main.prototype.convertGroup2Image = function(scene) {
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
              tempContext.drawImage(this, 0, 0, this.width, this.height, imageItem.x, imageItem.y, this.width, this.height)
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

myhooks = new hooks();
launch = new main(myhooks);
