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

    // Load datas - only useful for themes debugging
    if ($("#content").html() === "{{CONTENT}}") {
        var menu = "";
        menu += '<article class="message_success" id="message_success" data-score="14">';
        menu += '<p>Bravo !!</p>';
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
            }
        }        
        $("#content").html(menu);
    }
    if ($("#title").html() === "{{TITLE}}") $("#title").html(scene.title);

};

/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.afterMainConstructor = function(mainScene, layers) {

    // some stuff to manage popin windows

    var viewportHeight = $(window).height();

    mainScene.score = $("#message_success").data("score");
    if ((mainScene.score == mainScene.currentScore) && (mainScene.score != "0")) {
        $("#content").show();
        $("#message_success").show();
        var general_border = $("#message_success").css("border-top-width").substr(0,$("#message_success").css("border-top-width").length - 2);
        var general_offset = $("#message_success").offset();
        var content_offset = $("#content").offset();
        $("#message_success").css({'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)});        
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
        if ($(this).attr('src') == 'img/hide.png') {
            $(this).attr('src', 'img/show.png');
        }
        else {
            $(this).attr('src', 'img/hide.png');
        }
    });
    
    document.addEventListener("click", function(ev){
        if (mainScene.noPropagation) {
            mainScene.noPropagation = false;
        }
        else {
            if (mainScene.zoomActive === 1) {
                if ((mainScene.element !== 0) && 
                (typeof(mainScene.element) !== 'undefined')) {
                    console.log("yo");
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
    $('#' + idText + " audio").each(function(){
        if ($(this).data("state") === "autostart") {
            $(this)[0].play();
        }
    }); 
    
    var options = $('#' + idText).data("options");
    if (typeof(options) != "undefined") { 
        if (options.indexOf("disable-score") == -1) {
            iaScene.currentScore += 1;        
        }
    }
    if ((iaScene.score == iaScene.currentScore) && (iaScene.score != 0)) {
        $("#content").show();
        $("#message_success").show();
        var general_border = $("#message_success").css("border-top-width").substr(0,$("#message_success").css("border-top-width").length - 2);
        var general_offset = $("#message_success").offset();
        var content_offset = $("#content").offset();
        $("#message_success").css({'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)});        
    }
    if (iaScene.score != 0) {
        for (var i in iaObject.kineticElement) {    
            iaObject.kineticElement[i].off("click");
        }
    }
                
};
