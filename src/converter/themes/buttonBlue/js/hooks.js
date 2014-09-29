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
var hooks = function() {
    "use strict";
    this.dragwindow = false;
    this.popvisible = 0;
    this.deltaX = 0;
    this.deltaY = 0;
};

/*
 * @param array layers
 * @param iaScene mainScene
 */
hooks.prototype.beforeMainConstructor = function(mainScene, layers) {

    // Load datas - only useful for themes debugging
    var menu = "";
    var buttons = "<ul>";

    menu += '<article class="detail_content" id="general">';
    menu += '<h1>'+scene.intro_title+'</h1>';
    menu += '<p>' + scene.intro_detail + '</p>';
    menu += '</article>';
    for (var i in details) {
        if (details[i].options.indexOf("direct-link") == -1) {
            if ((details[i].detail.indexOf("Réponse:") != -1) || (details[i].detail.indexOf("réponse:") != -1)) {
                var question = details[i].detail.substr(0,details[i].detail.indexOf("Réponse:"));
                var answer = details[i].detail.substr(details[i].detail.indexOf("Réponse:")+8);
                menu += '<article class="detail_content" id="article-'+i+'">';
                menu += '<h1>'+details[i].title+'</h1>';
                menu += '<p>' + question + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+i+'">Réponse</a></div>' + '<div class="response" id="response_'+ i +'">' + answer + '</div>' + '</p>';
                menu += '</article>';            
            }

            else {
                menu += '<article class="detail_content" id="article-'+i+'">';
                menu += '<h1>'+details[i].title+'</h1>';
                menu += '<p>'+details[i].detail+'</p>';
                menu += '</article>';                        
            }
            buttons += '<li class="button-unselected button-li" id="li-article-' + i + '">' + (parseInt(i)+1) + '</li>';
        }
    }
    buttons += '</ul>';
    
    if ($("#content").html() === "{{CONTENT}}") {
        $("#content").html(menu);
    }
    $("#buttons").html(buttons);
    if ($("#title").html() === "{{TITLE}}") $("#title").html(scene.title);
};

/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.afterMainConstructor = function(mainScene, layers) {

    // some stuff to manage popin windows

    var viewportHeight = $(window).height();
    var that = this;
    
    $(".meta-doc").on("click", function(){
        $(".detail_content").hide();
        that.popvisible = "general";
        $("#content").show();
        $("#general").show();
        var general_border = $("#general").css("border-top-width").substr(0,$("#general").css("border-top-width").length - 2);
        var general_offset = $("#general").offset();
        var content_offset = $("#content").offset();
        $("#general").css({'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)});
        $('.buttons_container').show();
        $('.buttons_container').css({"top":$('#general').offset().top - 10});
        $('.buttons_container').css({"left": $('#general').offset().left + ($('#content').width() - $('.buttons_container').width()) / 2});   
    });

    $(".overlay").hide();

    $(".infos").on("click", function(){
        $("#rights").show();
    });
    $("#popup_close").on("click", function(){
        $("#rights").hide();
    });

    $("#article_close").on("click", function(){
        $(".buttons_container").hide();
        $(".detail_content").hide();
        $("#content").hide();
    });
    $("#article_move").on("mousedown", function(evt){
        that.dragwindow = true;
        that.deltaX = Math.abs(evt.pageX - $(".buttons_container").offset().left);
        that.deltaY = Math.abs(evt.pageY - $(".buttons_container").offset().top);
        $(".buttons_container").offset().top = $("#" + that.popvisible).offset().top;
        $(".buttons_container").offset().left = $("#" + that.popvisible).offset().left + $("#container").offset().left;
        // disable text selection
        return false;
    });
    $(document).on("mousemove", function(evt){
         if (that.dragwindow) {
            $("#" + that.popvisible).css({"top":evt.pageY});
            $("#" + that.popvisible).css({"left":evt.pageX - $("#container").offset().left - ($('#content').width() - $('.buttons_container').width()) / 2  - that.deltaX}); 
            $(".buttons_container").css({"top":evt.pageY - 10});
            $(".buttons_container").css({"left":evt.pageX - that.deltaX}); 
        }
    });
    $(document).on("mouseup", function(evt){
        that.dragwindow = false;
     });
    document.addEventListener("click", function(ev){
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
    });     
};

/*
 *
 *  
 */
hooks.prototype.afterIaObjectConstructor = function(iaScene, idText, detail, iaObject) {
    $("#li-" + idText).on("click", function(){
        $(".button-li").removeClass("button-selected").addClass("button-unselected");
        $(this).addClass("button-selected").removeClass("button-unselected");
        iaObject.kineticElement[0].fire("click");
    });
};

/*
 *
 *  
 */
hooks.prototype.afterIaObjectZoom = function(iaScene, idText, iaObject) {

};
    
/*
 *
 *  
 */
hooks.prototype.afterIaObjectFocus = function(iaScene, idText, iaObject) {
    var viewportHeight = $(window).height();
    var that = this;
    that.popvisible = idText;
    $("#content").show();
    $(".detail_content").hide();
    $('#' + idText).show();
    $('.buttons_container').show();
    $('.buttons_container').css({"top":$('#' + idText).offset().top - 10});
    $('.buttons_container').css({"left":$('#' + idText).offset().left + ($('#content').width() - $('.buttons_container').width()) / 2});
    $('#' + idText + " audio").each(function(){
        if ($(this).data("state") === "autostart") {
            $(this)[0].play();
        }
    });                
    var article_border = $('#' + idText).css("border-top-width").substr(0,$('#' + idText).css("border-top-width").length - 2);
    var article_offset = $('#' + idText).offset();
    var content_offset = $("#content").offset();
    $('#' + idText).css({'max-height':(viewportHeight - article_offset.top - content_offset.top - 2 * article_border)});
    $(".button-li").removeClass("button-selected").addClass("button-unselected");
    $("#li-" + idText).addClass("button-selected").removeClass("button-unselected");
};
