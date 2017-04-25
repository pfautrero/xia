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

/*
 * Main
 * Initialization
 *
 */

function main(myhooks) {
    "use strict";
    var that=window
    that.canvas = document.getElementById("canvas")

    this.backgroundLoaded = $.Deferred()

    this.backgroundLoaded.done(function(value){
      var newImage = document.createElement('img')
      $("#popup_material_image_background").after(newImage)
      $(newImage).attr("id", "popup_material_image_general")
      $(newImage).addClass("popup_material_image")
      $(newImage).attr("src", scene.image).load(function(){
          $("#popup_material_image_general").css({
            'position' : 'absolute',
            'display' : 'block',
            //'top' : iaObject.minY + 'px',
            'top' : '2000px',
            'left' : '0px',
            'transition' : '0s',
            'cursor' : 'pointer'
          })
      })

      // Load background image

      that.imageObj = new Image()
      that.imageObj.src = scene.image
      that.imageObj.onload = function() {

          var mainScene = new IaScene(scene.width,scene.height);
          $(".meta-doc").on("click tap", function(){
            mainScene.cursorState = 'url("img/ZoomOut.cur"),auto'
            var popupMaterialTopOrigin = ($("#popup_material_background").height() - $("#popup_material").height()) / 2
            var popupMaterialLeftOrigin = ($("#popup_material_background").width() - $("#popup_material").width()) / 2

            var backgroundWidth = Math.min($("#popup_material_title").height(), $("#popup_material").width() / 2)
            var backgroundHeight = $("#popup_material_title").height()
            var imageWidth = scene.width
            var imageHeight = scene.height
            var a = Math.min(
                    backgroundWidth / imageWidth,
                    backgroundHeight / imageHeight)

            var x = popupMaterialLeftOrigin
            var y = ((backgroundHeight - a * imageHeight) / 2) + popupMaterialTopOrigin

            $.easing.custom = function (x, t, b, c, d) {
              return c*(t/=d)*t*t*t*t + b;
            }
            $("#popup_material_content").hide()
            $("#content article").hide()
            $("#popup_material").animate({
              'top': (popupMaterialTopOrigin) + 'px',
            },{
              duration : 500,
              easing : "custom",
              queue : false,
              complete : function(){
                $("#general").show()
                $("#popup_material_content").fadeIn()
              }
            })
            $("#popup_material_image_general").css({
              'transition' : '0s'
            })
            $("#popup_material_image_general").animate({
              'top' : y + 'px',
              'left' : x + 'px',
              'height' : (a * imageHeight) + 'px',
              'width' : (a * imageWidth) + 'px'

            },{
              duration : 500,
              easing : "custom",
              queue : false
            })

            $("#popup_material_title_text").css({
              "margin-left" : (a * imageWidth) + 'px'
            })
            $("#popup_material_title h1").html($("#general h1").html())
          })
          $("#popup_material_image_general").on("click tap", function(ev){
            // let's zoom the image
            if (mainScene.cursorState.indexOf("ZoomOut.cur") != -1) {
              mainScene.cursorState = 'url("img/ZoomImage.cur"),auto'
              var backgroundWidth = $("#popup_material_background").width()
              var backgroundHeight = $("#popup_material_background").height()
              var imageWidth = $("#popup_material_image_general").width()
              var imageHeight = $("#popup_material_image_general").height()
              var a = Math.min(
                      3,
                      backgroundWidth / imageWidth,
                      backgroundHeight / imageHeight)

              var x = (backgroundWidth - a * imageWidth) / 2
              var y = (backgroundHeight - a * imageHeight) / 2
              $("#popup_material_image_background").fadeIn()
              $(this).css({
                "position": "absolute",
                "top": y + 'px',
                "left" : x + "px",
                "height" : (a * imageHeight) + 'px',
                "width" : (a * imageWidth) + 'px',
                "transition" : "top 1s, left 1s, height 1s, width 1s"
              });
            }
            // let's unzoom the image
            else {
              mainScene.cursorState = 'url("img/ZoomOut.cur"),auto'
              var popupMaterialTopOrigin = ($("#popup_material_background").height() - $("#popup_material").height()) / 2
              var popupMaterialLeftOrigin = ($("#popup_material_background").width() - $("#popup_material").width()) / 2

              var backgroundWidth = Math.min($("#popup_material_title").height(), $("#popup_material").width() / 2)
              var backgroundHeight = $("#popup_material_title").height()
              var imageWidth = $(this).width()
              var imageHeight = $(this).height()
              var a = Math.min(
                      backgroundWidth / imageWidth,
                      backgroundHeight / imageHeight)

              var x = popupMaterialLeftOrigin
              var y = ((backgroundHeight - a * imageHeight) / 2) + popupMaterialTopOrigin

              $("#popup_material_image_background").fadeOut()
              $(this).css({
                'position' : 'absolute',
                'display' : 'block',
                'top' : y + 'px',
                'left' : x + 'px',
                'height' : (a * imageHeight) + 'px',
                'width' : (a * imageWidth) + 'px',
                'transition' : 'top 1s, left 1s, height 1s, width 1s'
              })
            }
          })

          mainScene.scale = 1;
          mainScene.scaleScene(mainScene);

          var stage = new Kinetic.Stage({
              container: 'canvas',
              width: mainScene.width,
              height: mainScene.height
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

          // cache used over background image
          var baseCache = new Kinetic.Rect({
              x: 0,
              y: mainScene.y,
              width: scene.width,
              height: scene.height,
              scale: {x:mainScene.coeff,y:mainScene.coeff},
              fill: mainScene.backgroundCacheColor
          });

          var layers = [];
          that.layers = layers;
          layers[0] = new Kinetic.FastLayer();
          layers[1] = new Kinetic.FastLayer();

          layers[3] = new Kinetic.Layer();
          layers[4] = new Kinetic.Layer();

          layers[0].add(baseCache);
          layers[1].add(baseImage);

          stage.add(layers[0]);
          stage.add(layers[1]);

          stage.add(layers[3]);
          stage.add(layers[4]);
          myhooks.beforeMainConstructor(mainScene, that.layers);
          mainScene.nbDetails = 0
          for (var i in details) {
            if (typeof(details[i].group) !== 'undefined') {
              mainScene.nbDetails+=details[i].group.length
            }
            else {
              mainScene.nbDetails++
            }
          }
          mainScene.nbDetailsLoaded = 0
          mainScene.allDetailsLoaded = $.Deferred()
          mainScene.allDetailsLoaded.done(function(value){
            myhooks.afterMainConstructor(mainScene, that.layers);
            $("#splash").fadeOut("slow", function(){
                    $("#loader").hide();
            });
          })
          if (details.length == 0) mainScene.allDetailsLoaded.resolve(0)
          for (var i in details) {
              var iaObj = new IaObject({
                  imageObj: that.imageObj,
                  detail: details[i],
                  layer: layers[4],
                  idText: "article-" + i,
                  baseImage: baseImage,
                  iaScene: mainScene,
                  background_layer: layers[1],
                  backgroundCache_layer: layers[0],
                  zoomLayer: layers[3],
                  myhooks: myhooks
              })
              mainScene.shapes.push(iaObj);
          }

          if (0 in mainScene.shapes) mainScene.element = mainScene.shapes[0]

      }
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
