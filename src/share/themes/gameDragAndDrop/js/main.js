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
// @version=xxx

/*
 * Main
 * Initialization
 *
 */

function main(myhooks) {
    "use strict";

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

    Kinetic.Util.addMethods(Kinetic.Group,{
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
    Kinetic.Util.addMethods(Kinetic.Sprite,{
        setXiaParent: function(xiaparent) {
            this.xiaparent = xiaparent;
        },
        getXiaParent: function() {
            return this.xiaparent;
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
    Kinetic.Util.addMethods(Kinetic.Image,{
        setXiaParent: function(xiaparent) {
            this.xiaparent = xiaparent;
        },
        getXiaParent: function() {
            return this.xiaparent;
        }    });

    Kinetic.draggedshape = null;

    //var that=window;
    //var this=this;
    this.canvas = document.getElementById("canvas");

    this.backgroundLoaded = $.Deferred()

    this.backgroundLoaded.done(function(value){

      // Load background image

      this.imageObj = new Image();
      this.imageObj.src = scene.image;
      this.imageObj.onload = function() {

          var mainScene = new IaScene(scene.width,scene.height);
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
              image: this.imageObj
          });

          var layers = [];
          this.layers = layers;
          layers[0] = new Kinetic.FastLayer();
          layers[0].add(baseImage);
          stage.add(layers[0]);

          myhooks.beforeMainConstructor(mainScene, this.layers);

          var indice = 1;
          layers[indice] = new Kinetic.Layer();
          stage.add(layers[indice]);

          for (var i in details) {
              var iaObj = new IaObject({
                  imageObj: this.imageObj,
                  detail: details[i],
                  layer: layers[indice],
                  idText: "article-" + i,
                  baseImage: baseImage,
                  iaScene: mainScene,
                  myhooks: myhooks
              });
              mainScene.shapes.push(iaObj);
          }

          this.afterMainConstructor(mainScene, this.layers);
          myhooks.afterMainConstructor(mainScene, this.layers);

          $("#loader").hide();

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


      }.bind(this)
    }.bind(this))

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
main.prototype.afterMainConstructor = function(mainScene, layers) {

    // some stuff to manage popin windows

    var viewportHeight = $(window).height();

    var button_click = function() {
        var target = $(this).data("target");
        if ($("#response_" + target).is(":hidden")) {
            if ($(this).data("password")) {
                $("#form_" + target).toggle();
                $("#form_" + target + " input[type=text]").val("");
                $("#form_" + target + " input[type=text]").focus();
            }
            else {
                $("#response_" + target).toggle();
            }
        }
        else {
            if ($(this).data("password")) {
                $("#response_" + target).html($("#response_" + target).data("encrypted_content"));
            }
            $("#response_" + target).toggle();
        }

    };
    var unlock_input = function(e) {
        e.preventDefault();
        var entered_password = $(this).parent().children("input[type=text]").val();
        var sha1Digest= new createJs(true);
        sha1Digest.update(entered_password.encode());
        var hash = sha1Digest.digest();
        if (hash == $(this).data("password")) {
            var target = $(this).data("target");
            var encrypted_content = $("#response_" + target).html();
            $("#response_" + target).data("encrypted_content", encrypted_content);
            $("#response_" + target).html(XORCipher.decode(entered_password, encrypted_content).decode());
            $("#response_" + target).show();
            $("#form_" + target).hide();
            $(".button").off("click");
            $(".button").on("click", button_click);
            $(".unlock input[type=submit]").off("click");
            $(".unlock input[type=submit]").on("click", unlock_input);
        }
    };
    $(".button").on("click", button_click);
    $(".unlock input[type=submit]").on("click", unlock_input);


    mainScene.score = $("#message_success").data("score");
    if ((mainScene.score == mainScene.currentScore) && (mainScene.score != "0")) {
        $("#content").show();
        $("#message_success").show();
        var general_border = $("#message_success").css("border-top-width").substr(0,$("#message_success").css("border-top-width").length - 2);
        var general_offset = $("#message_success").offset();
        var content_offset = $("#content").offset();
        $("#message_success").css({
            'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)
        });
    }

    mainScene.score2 = $("#message_success2").data("score");
    if ((mainScene.score2 == mainScene.currentScore2) && (mainScene.score2 != "0")) {
        $("#content").show();
        $("#message_success2").show();
        var general_border = $("#message_success2").css("border-top-width").substr(0,$("#message_success2").css("border-top-width").length - 2);
        var general_offset = $("#message_success2").offset();
        var content_offset = $("#content").offset();
        $("#message_success2").css({
            'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)
        });
    }


    $(".overlay").hide();

    $(".infos").on("click", function(){
        $("#rights").show();
        $("#popup").show();
        $("#popup_intro").hide();
    });
    $("#popup_close").on("click", function(){
        $("#rights").hide();
    });
    $("#popup_toggle").on("click", function(){
        $("#message_success_content").toggle();

        var strSource = $(this).attr('src')
        if (strSource.indexOf('hide.png') !== -1) {
            strSource = strSource.replace('hide.png', 'show.png')
        }
        else {
            strSource = strSource.replace('show.png', 'hide.png')
        }
        $(this).attr('src', strSource)

    });
    $("#popup_toggle2").on("click", function(){
        $("#message_success_content2").toggle();

        var strSource = $(this).attr('src')
        if (strSource.indexOf('hide.png') !== -1) {
            strSource = strSource.replace('hide.png', 'show.png')
        }
        else {
            strSource = strSource.replace('show.png', 'hide.png')
        }
        $(this).attr('src', strSource)

    });
};

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
