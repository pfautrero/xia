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

    // Load datas in the accordion menu - only useful for themes debugging
    if ($("#accordion2").html() === "{{ACCORDION}}") {
        var menu = "";
        menu += '<div class="accordion-group">';
        menu += '<div class="accordion-heading">';
        menu += '<a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">'+scene.intro_title+'</a>';
        menu += '<div id="collapsecomment" class="accordion-body collapse">';
        menu += '<div class="accordion-inner">' + scene.intro_detail + '</div></div></div></div>';

        for (var i in details) {
            if (details[i].options.indexOf("direct-link") == -1) {
                if ((details[i].detail.indexOf("Réponse:") != -1) || (details[i].detail.indexOf("réponse:") != -1)) {
                    var question = details[i].detail.substr(0,details[i].detail.indexOf("Réponse:"));
                    var answer = details[i].detail.substr(details[i].detail.indexOf("Réponse:")+8);
                    menu += '<div class="accordion-group">';
                    menu += '<div class="accordion-heading">';
                    menu += '<a id="collapse'+i+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+i+'">'+details[i].title+'</a>';
                    menu += '<div id="collapse'+i+'" class="accordion-body collapse">';
                    menu += '<div class="accordion-inner">' + question + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+i+'">Réponse</a></div>' + '<div class="response" id="response_'+ i +'">' + answer + '</div>' + '</div></div></div></div>';
                }

                else {
                    menu += '<div class="accordion-group">';
                    menu += '<div class="accordion-heading">';
                    menu += '<a id="collapse'+i+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+i+'">'+details[i].title+'</a>';
                    menu += '<div id="collapse'+i+'" class="accordion-body collapse">';
                    menu += '<div class="accordion-inner">'+details[i].detail+'</div></div></div></div>';
                }
            }
        }
        $("#accordion2").html(menu);
        //$("#collapsecomment").collapse("show");
    }
    if ($("#title").html() === "{{TITLE}}") $("#title").html(scene.title);

};

/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.afterMainConstructor = function(mainScene, layers) {

    var that = this;
    $(".infos").on("click", function(){
        $("#overlay").show();
    });
    $("#popup_close").on("click", function(){
        $("#overlay").hide();
    });
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

    $(".accordion-toggle").on("click tap", function(){
        $('.accordion-body').removeClass("slidedown").addClass("collapse");
        $(this).parent().children(".accordion-body").removeClass("collapse").addClass("slidedown");              
    });

    $("#collapsecomment-heading").on('click tap',function(){
        if (mainScene.zoomActive === 0) {
            if ((mainScene.element !== 0) && (typeof(mainScene.element) !== 'undefined')) {
                for (var i in mainScene.element.kineticElement) {
                    mainScene.element.kineticElement[i].fillPriority('color');
                    mainScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    mainScene.element.kineticElement[i].setStroke('rgba(0, 0, 0, 0)');
                    mainScene.element.kineticElement[i].setStrokeWidth(0);                                         
                    mainScene.element.layer.draw();
                }
            }
            mainScene.element = that;
            layers[0].moveToBottom();
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
                    mainScene.element.kineticElement[0].fire("click");
                }
            }
            else if (mainScene.cursorState.indexOf("ZoomIn.cur") !== -1) {
                document.body.style.cursor = "default";
                mainScene.cursorState = "default";
                if (typeof(mainScene.element.kineticElement) != "undefined") {
                    mainScene.element.kineticElement[0].fire("mouseleave");
                }
            }
        }
    });    

};
/*
 *
 *  
 */
hooks.prototype.afterIaObjectConstructor = function(iaScene, idText, detail, iaObject) {

    /*
     *  manage accordion events related to this element
     */
    $("#" + idText + "-heading").on('click touchstart',function(){
      
        if ($('#' + idText).css("height") == "0px") {
            iaObject.kineticElement[0].fire("click");
        }
        else {
            iaObject.kineticElement[0].fire("mouseleave");
        }
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
    $('.accordion-body').removeClass("slidedown").addClass("collapse");
    $('#' + idText).parent().children(".accordion-body").removeClass("collapse").addClass("slidedown");
    $('#' + idText + " audio").each(function(){
        if ($(this).data("state") === "autostart") {
            $(this)[0].play();
        }
    }); 
};
