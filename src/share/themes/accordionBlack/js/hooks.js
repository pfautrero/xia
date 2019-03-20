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
 * @constructor init specific hooks
 */
function hooks() {
    "use strict";
    this.beforeDone = false
    this.afterDone = false
}

hooks.prototype._fullScreenAbility = function(xiaObject) {
  var e = document.getElementById("title")
  e.onclick = function() {
    this._toggleFullScreen()
  }.bind(this)
  document.addEventListener("fullscreenchange", function () {
    setTimeout(function(){
      this.params.hooks.scaleScene(this)
      this.restart()
    }.bind(this), 100)
  }.bind(xiaObject), false);

  document.addEventListener("mozfullscreenchange", function () {
    setTimeout(function(){
      this.params.hooks.scaleScene(this)
      this.restart()
    }.bind(this), 100)
  }.bind(xiaObject), false);

  document.addEventListener("webkitfullscreenchange", function () {
    setTimeout(function(){
      this.params.hooks.scaleScene(this)
      this.restart()
    }.bind(this), 100)
  }.bind(xiaObject), false);

}

hooks.prototype._toggleFullScreen = function() {
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

/*
 * @param array layers
 * @param iaScene mainScene
 */
hooks.prototype.duringXiaInit = function(xiaObject) {
  // This function is not re-entrant !
  if (this.beforeDone) return
  this.beforeDone = true

  // area located under the canvas. If mouse over is detected,
  // we must re-activate mouse events on canvas
  var detect = document.getElementById("detect")
  detect.addEventListener("mouseover", function()
  {
    this.canvas.style.pointerEvents="auto"
    if (this.mainScene.element) {
      for (var i in this.mainScene.element.xiaDetail) {
        var xiaDetail = this.mainScene.element.xiaDetail[i]
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
  }.bind(xiaObject), false);
  detect.addEventListener("touchstart", function()
  {
    this.canvas.style.pointerEvents="auto";
    if (this.mainScene.element) {
      for (var i in this.mainScene.element.xiaDetail) {
        var xiaDetail = this.mainScene.element.xiaDetail[i]
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
  }.bind(xiaObject), false);

  this._fullScreenAbility(xiaObject)

  // Script used to load youtube resource after main page
  // otherwise, Chrome fails to start the page

  $(".videoWrapper16_9").each(function(){
      var source = $(this).data("iframe");
      var iframe = document.createElement("iframe");
      iframe.src = source;
      $(this).append(iframe);
      $(this).data("iframe", "");
  });

  $(".videoWrapper4_3").each(function(){
      var source = $(this).data("iframe");
      var iframe = document.createElement("iframe");
      iframe.src = source;
      $(this).append(iframe);
      $(this).data("iframe", "");
  });
  $(".flickr_oembed").each(function(){
      var source = $(this).data("oembed");
      var that = $(this);
      $.ajax({
          url: "http://www.flickr.com/services/oembed/?format=json&callback=?&jsoncallback=xia&url=" + source,
          dataType: 'jsonp',
          jsonpCallback: 'xia',
          success: function (data) {
              var url = data.url;
              var newimg = document.createElement("img");
              newimg.src = url;
              that.append(newimg);
          }
      });
  });

}
hooks.prototype.scaleScene = function(xiaObject) {
  var mainScene = xiaObject.mainScene
  if ($(window).width() >= '768') {
    mainScene.ratio = 0.50;
  }
  else {
    mainScene.ratio = 1.00;
  }
  var viewportWidth = $(window).width() * 0.9;
  var viewportHeight = $(window).height();

  var coeff_width = (viewportWidth * mainScene.ratio) / parseFloat(mainScene.originalWidth);
  var coeff_height = (viewportHeight) / (parseFloat(mainScene.originalHeight) + $('#canvas').offset().top + $('#container').offset().top);
  if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_width) && (viewportHeight >= ((parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_width))) {
      mainScene.width = viewportWidth * mainScene.ratio;
      mainScene.coeff = (mainScene.width) / parseFloat(mainScene.originalWidth);
      mainScene.height = parseFloat(mainScene.originalHeight) * mainScene.coeff;
  }
  else if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_height) && (viewportHeight >= (parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_height)) {
      mainScene.height = viewportHeight - $('#container').offset().top - $('#canvas').offset().top -5;
      mainScene.coeff = (mainScene.height) / parseFloat(mainScene.originalHeight);
      mainScene.width = parseFloat(mainScene.originalWidth) * mainScene.coeff;
  }

  mainScene.width = mainScene.width / mainScene.ratio;
  $('#container').css({"width": mainScene.width + 'px'});
  $('#container').css({"height": (mainScene.height + $('#canvas').offset().top - $('#container').offset().top) + 'px'});
  $('#canvas').css({"height": (mainScene.height) + 'px'});
  $('#canvas').css({"width": mainScene.width + 'px'});
  $('#detect').css({"height": (mainScene.height) + 'px'});
  $('#accordion2').css({"max-height": (mainScene.height - $('#accordion2').offset().top) + 'px'});
  $('#detect').css({"top": ($('#canvas').offset().top - $('#container').offset().top) + 'px'});
}
/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.loaded = function(xiaObject) {

    // This function is not re-entrant !
    // because some events are handled here
    if (this.afterDone) return
    this.afterDone = true

    var mainScene = xiaObject.mainScene
    
    $("#splash").fadeOut("slow", function(){
      $("#loader").hide()
    })

    $('#collapsecomment audio').each(function(){
      if ($(this).data("state") === "autostart") {
        $(this)[0].play()
      }
    })

    $(".infos").on("click", function(){
      $("#overlay").show()
    })
    $("#popup_close").on("click", function(){
      $("#overlay").hide()
    })
    var button_click = function() {
      var target = $(this).data("target")
      if ($("#response_" + target).is(":hidden")) {
        if ($(this).data("password")) {
          $("#form_" + target).toggle()
          $("#form_" + target + " input[type=text]").val("")
          $("#form_" + target + " input[type=text]").focus()
        }
        else {
          $("#response_" + target).toggle()
        }
      }
      else {
        if ($(this).data("password")) {
          $("#response_" + target).html($("#response_" + target).data("encrypted_content"));
        }
        $("#response_" + target).toggle();
      }
    }
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

    $(".accordion-toggle").on("click tap", function(){
      $('.accordion-body').removeClass("slidedown").addClass("collapse");
      $(this).parent().children(".accordion-body").removeClass("collapse").addClass("slidedown");
    });

    $("#collapsecomment-heading").on('click tap',function(){
      if (mainScene.zoomActive === 0) {
        if (mainScene.element) {
          for (var i in mainScene.element.xiaDetail) {
            mainScene.element.xiaDetail[i].kineticElement.fillPriority('color');
            mainScene.element.xiaDetail[i].kineticElement.fill('rgba(0,0,0,0)');
            mainScene.element.xiaDetail[i].kineticElement.setStroke('rgba(0, 0, 0, 0)');
            mainScene.element.xiaDetail[i].kineticElement.setStrokeWidth(0);
            mainScene.element.layer.draw();
          }
          mainScene.element = null
        }
        xiaObject.layers.modalBackground.moveToBottom();
      }
    })
    document.addEventListener("click", function(ev){
      if (mainScene.noPropagation) {
        mainScene.noPropagation = false;
      }
      else {
        if (mainScene.zoomActive === 1) {
          if (mainScene.element) {
            mainScene.element.xiaDetail[0].kineticElement.fire("click");
          }
        }
        else if ((mainScene.cursorState.indexOf("ZoomIn.cur") !== -1) ||
          (mainScene.cursorState.indexOf("ZoomFocus.cur") !== -1)) {
            document.body.style.cursor = "default";
            mainScene.cursorState = "default";
            if (typeof(mainScene.element.xiaDetail) != "undefined") {
              mainScene.element.xiaDetail[0].kineticElement.fire("mouseleave");
            }
        }
      }
    })

};
/*
 *
 *
 */
hooks.prototype.afterIaObjectConstructor = function(iaScene, idText, detail, iaObject) {

    // first disable events (to make this function re-entrant)
    $("#" + idText + "-heading").off('click touchstart')

    // then add click event on accordion entries
    $("#" + idText + "-heading").on('click touchstart',function(){

        if ($('#' + idText).css("height") == "0px") {
            iaObject.xiaDetail[0].kineticElement.fire("click");
        }
        else {
            iaObject.xiaDetail[0].kineticElement.fire("mouseleave");
        }
    });
};
/*
 *
 *
 */
hooks.prototype.zoom = function(XiaObject) {

}
/*
 *
 *
 */
hooks.prototype.mouseover = function(XiaObject) {

}
/*
 *
 *
 */
hooks.prototype.unzoom = function(XiaObject) {
  $('#' + XiaObject.parent.idText + " audio").each(function(){
      $(this)[0].pause();
  })
  $('#' + XiaObject.parent.idText + " video").each(function(){
      $(this)[0].pause();
  })
};
/*
 *
 *
 */
hooks.prototype.focus = function(XiaObject) {
  var idText = XiaObject.parent.idText
  if (XiaObject.parent.iaScene.element) {
    $('#ID audio'.replace('ID', XiaObject.parent.iaScene.element.idText)).each(function(){
        $(this)[0].pause()
    })
    $('#ID video'.replace('ID', XiaObject.parent.iaScene.element.idText)).each(function(){
        $(this)[0].pause()
    })
  }

  $('.accordion-body').removeClass("slidedown").addClass("collapse");
  $('#' + idText).parent().children(".accordion-body").removeClass("collapse").addClass("slidedown");
  $('#' + idText + " audio").each(function(){
      if ($(this).data("state") === "autostart") {
          $(this)[0].play();
      }
  });
};
