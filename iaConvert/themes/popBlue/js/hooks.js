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
    var that = this;
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

    $(".infos").on("click", function(){
        $("#overlay").show();
    });
    $("#popup_close").on("click", function(){
        $("#overlay").hide();
    });

    $("#collapsecomment-heading").on('click touchstart',function(){
        console.log("test");
        if (mainScene.zoomActive === 0) {
            $('.collapse.in').each(function (index) {
                if ($(this).attr("id") !== "collapsecomment") $(this).collapse("toggle");
            });
            if ((mainScene.element !== 0) && (typeof(mainScene.element) !== 'undefined')) {
                for (var i in mainScene.element.kineticElement) {
                    mainScene.element.kineticElement[i].fillPriority('color');
                    mainScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    mainScene.element.layer.draw();
                }
            }
            mainScene.element = that;
            layers[0].moveToBottom();
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
        if (iaScene.zoomActive === 0) {
            $('.collapse.in').each(function (index) {
                if ($(this).attr("id") !== idText) $(this).collapse("toggle");
            });
            if ((iaScene.element !== 0) && 
                (typeof(iaScene.element) !== 'undefined')) {
                for (var i in iaScene.element.kineticElement) {
                   
                    if (iaScene.element.persistent[i] == "off") {
                        iaScene.element.kineticElement[i].fillPriority('color');
                        iaScene.element.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                    }
                    else if (iaScene.element.persistent[i] == "onPath") {
                        iaScene.element.kineticElement[i].fillPriority('color');
                        iaScene.element.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                    }
                    else if (iaScene.element.persistent[i] == "onImage") {
                        iaScene.element.kineticElement[i].fillPriority('pattern');
                        iaScene.element.kineticElement[i].fillPatternScaleX(iaObject.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        iaScene.element.kineticElement[i].fillPatternScaleY(iaObject.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        iaScene.element.kineticElement[i].fillPatternImage(iaScene.element.backgroundImage[i]);                        
                    }                     
                    iaScene.element.layer.draw();
                }
            }
            var zoomable = true;
            if ((typeof(detail.fill) !== 'undefined') && 
                (detail.fill == "#000000")) {
                zoomable = false;
            }

            if (zoomable === true) {
                document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
            }            
            var cacheBackground = true;
            for (var i in iaObject.kineticElement) {
                if (iaObject.persistent[i] === "onImage") cacheBackground = false;
                iaObject.kineticElement[i].fillPriority('pattern');
                iaObject.kineticElement[i].fillPatternScaleX(iaObject.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                iaObject.kineticElement[i].fillPatternScaleY(iaObject.backgroundImageOwnScaleY[i] * 1/iaScene.scale);               
                iaObject.kineticElement[i].fillPatternImage(iaObject.backgroundImage[i]);
            }
            if (cacheBackground == true) {
                iaObject.backgroundCache_layer.moveToTop();
            }

            iaScene.element = iaObject;
            iaObject.layer.moveToTop();
            iaObject.layer.draw();				
            iaObject.backgroundCache_layer.draw();
        }
    });
};
    
/*
 *
 *  
 */
hooks.prototype.afterIaObjectFocus = function(iaScene, idText, iaObject) {
    $('.collapse.in').each(function (index) {
            if ($(this).attr("id") !== idText) 
                $(this).collapse("toggle");
    });
    $('#' + idText).collapse("show");
    $('#' + idText + " audio").each(function(){
        if ($(this).data("state") === "autostart") {
            $(this)[0].play();
        }
    }); 
};
