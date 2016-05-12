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
 *
 * @constructor init specific hooks
 */
function hooks() {
    "use strict";
}
/*
 * @param array layers
 * @param iaScene mainScene
 */
hooks.prototype.beforeMainConstructor = function(mainScene, layers) {


};

/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.afterMainConstructor = function(mainScene, layers) {

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

    $(".meta-doc").on("click", function(){
        $("#content").show();
        $("#general").show();
        var general_border = $("#general").css("border-top-width").substr(0,$("#general").css("border-top-width").length - 2);
        var general_offset = $("#general").offset();
        var content_offset = $("#content").offset();
        $("#general").css({'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)});
    });

    $(".overlay").hide();

    $(".infos").on("click", function(){
        $("#rights").show();
    });
    $("#popup_close").on("click", function(){
        $("#rights").hide();
    });

    $(".article_close").on("click", function(){
        $(this).parent().hide();
        $("#content").hide();
        $(this).parent().children("audio").each(function(){
            $(this)[0].pause();
        });
        $(this).parent().children("video").each(function(){
            $(this)[0].pause();
        });
    });
    /*document.addEventListener("click", function(ev){
        if (mainScene.noPropagation) {
            mainScene.noPropagation = false;
        }
        else {
            if (mainScene.zoomActive === 1) {
                if ((mainScene.element !== 0) &&
                (typeof(mainScene.element) !== 'undefined')) {
                    mainScene.element.kineticElement[0].fire("click");
                }
            }
            else if (mainScene.cursorState.indexOf("ZoomIn.cur") !== -1) {
                document.body.style.cursor = "default";
                mainScene.cursorState = "default";
                mainScene.element.kineticElement[0].fire("mouseleave");
            }
        }
    })*/

    var popupMaterialTopOrigin = ($("#popup_material_background").height() - $("#popup_material").height()) / 2
    var popupMaterialLeftOrigin = ($("#popup_material_background").width() - $("#popup_material").width()) / 2

    $("#popup_material").css({
      "position": "absolute",
      "top": (popupMaterialTopOrigin * 2 + $("#popup_material").height()) + 'px',
      "left" : popupMaterialLeftOrigin + "px",
      "transition" : "1s"
    });




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

    this.convertDetail2Image(0, mainScene)


}

/*
 *  fired once all images are loaded
 *
 */
hooks.prototype.convertDetail2Image = function(index, iaScene) {

  var iaObject = iaScene.shapes[index]
  var myhooks = this
  var newContainer = document.createElement('div')
  $(newContainer).attr("id", "stage_" + iaObject.idText)
  $(newContainer).css({"display" : "none"})
  $("#invisible").append(newContainer)

  var tempStage = new Kinetic.Stage({
      container: "stage_" + iaObject.idText,
      width: iaObject.maxX - iaObject.minX,
      height: iaObject.maxY - iaObject.minY
  })

  for (i in iaObject.kineticElement) {
    iaObject.kineticElement[i].fillPriority('pattern')
    iaObject.kineticElement[i].fillPatternScaleX(iaObject.backgroundImageOwnScaleX[i] * 1/iaScene.scale)
    iaObject.kineticElement[i].fillPatternScaleY(iaObject.backgroundImageOwnScaleY[i] * 1/iaScene.scale)
    iaObject.kineticElement[i].fillPatternImage(iaObject.backgroundImage[i])
    iaObject.kineticElement[i].x(iaObject.kineticElement[i].x() - iaObject.minX)
    iaObject.kineticElement[i].y(iaObject.kineticElement[i].y() - iaObject.minY)
    iaObject.kineticElement[i].moveToTop()
  }

  var layerClone = iaObject.layer.clone()
  tempStage.add(layerClone)
  layerClone.draw()

  var data = layerClone.toDataURL()

  var newImage = document.createElement('img')
  $("#popup_material_image_background").after(newImage)
  $(newImage).attr("id", "popup_material_image_" + iaObject.idText)
  $(newImage).addClass("popup_material_image")
  $(newImage).attr("src", data).load(function(){
    /*for (i in iaObject.kineticElement) {

    }*/

    for (i in iaObject.kineticElement) {
      iaObject.kineticElement[i].x(iaObject.kineticElement[i].x() + iaObject.minX)
      iaObject.kineticElement[i].y(iaObject.kineticElement[i].y() + iaObject.minY)
        if (iaObject.persistent[i] == "off") {
            iaObject.kineticElement[i].fillPriority('color');
            iaObject.kineticElement[i].fill('rgba(0, 0, 0, 0)');
        }
        else if (iaObject.persistent[i] == "onPath") {
            iaObject.kineticElement[i].fillPriority('color');
            iaObject.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
        }
        else if (iaObject.persistent[i] == "onImage") {
            iaObject.kineticElement[i].fillPriority('pattern');
            iaObject.kineticElement[i].fillPatternScaleX(iaObject.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
            iaObject.kineticElement[i].fillPatternScaleY(iaObject.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
            iaObject.kineticElement[i].fillPatternImage(iaObject.backgroundImage[i]);
        }
    }


    iaObject.layer.draw();
    (function(index){
      if ((index+1) in iaScene.shapes) myhooks.convertDetail2Image(index+1, iaScene)
    })(index)
  })

  var popupMaterialTopOrigin = ($("#popup_material_background").height() - $("#popup_material").height()) / 2

  $("#popup_material_image_" + iaObject.idText).css({
    'position' : 'absolute',
    'display' : 'block',
    //'top' : iaObject.minY + 'px',
    'top' : '2000px',
    'left' : iaObject.minX + 'px',
    'height' : (iaObject.maxY - iaObject.minY) + 'px',
    'width' : (iaObject.maxX - iaObject.minX) + 'px',
    'transition' : '0s'
  })

  $("#popup_material_image_" + iaObject.idText).on("click tap", function(ev){
    // let's zoom the image
    if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {
      iaScene.cursorState = 'url("img/ZoomImage.cur"),auto'
      var backgroundWidth = $("#popup_material_background").width()
      var backgroundHeight = $("#popup_material_background").height()
      var imageWidth = $("#popup_material_image_" + iaObject.idText).width()
      var imageHeight = $("#popup_material_image_" + iaObject.idText).height()
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
      iaScene.cursorState = 'url("img/ZoomOut.cur"),auto'
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




}


/*
 *  fired once all images are loaded
 *
 */
hooks.prototype.afterIaObjectConstructor = function(iaScene, idText, detail, iaObject) {


};

/*
 *
 *
 */
hooks.prototype.afterIaObjectFocus = function(iaScene, idText, iaObject) {
  if ($('#' + idText).data("state") != "void") {
      $("#popup_material_title h1").html($("#" + idText + " h1").html())
      $("#popup_material_content").html($("#" + idText + " div").html())
      $('#' + idText + " audio").each(function(){
          if ($(this).data("state") === "autostart") {
              $(this)[0].play();
          }
      });
  }
};


/*
 *
 *
 */
hooks.prototype.afterIaObjectZoom = function(iaScene, idText, iaObject) {

};
