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
// @author : pascal.fautrero@crdp.ac-versailles.fr

/**
 *
 * @param {type} originalWidth
 * @param {type} originalHeight
 * @constructor create image active scene
 */
function IaScene(originalWidth, originalHeight) {
    "use strict";
    var that = this;
    //  canvas width
    this.width = 1000;

    // canvas height
    this.height = 800;

    // default color used to fill shapes during mouseover
    var _colorOver = {red:0, green:0, blue:0, opacity:0.7};

    // default color used to fill stroke around shapes during mouseover
    var _colorOverStroke = {red:207, green:0, blue:15, opacity:1};

    // default color used to fill shapes if defined as cache
    this.colorPersistent = {red:124, green:154, blue:174, opacity:1};

    // Image ratio on the scene
    this.ratio = 1.00;

    // padding-top in the canvas
    this.y = 0;

    // Sprites frameRate
    this.frameRate = 10

    // internal
    this.score = 0;
    this.score2 = 0;

    this.currentShape = "";

    this.currentScore = 0;
    this.currentScore2 = 0;
    this.fullScreen = "off";
    this.overColor = 'rgba(' + _colorOver.red + ',' + _colorOver.green + ',' + _colorOver.blue + ',' + _colorOver.opacity + ')';
    this.overColorStroke = 'rgba(' + _colorOverStroke.red + ',' + _colorOverStroke.green + ',' + _colorOverStroke.blue + ',' + _colorOverStroke.opacity + ')';
    this.scale = 1;
    this.zoomActive = 0;
    this.element = 0;
    this.originalWidth = originalWidth;
    this.originalHeight = originalHeight;
    this.coeff = (this.width * this.ratio) / parseFloat(originalWidth);
    this.cursorState="";
    this.noPropagation = false;
}

/*
 * Scale entire scene
 *
 */
IaScene.prototype.scaleScene = function(mainScene){
    "use strict";
    var viewportWidth = $(window).width();
    var viewportHeight = $(window).height();

    var coeff_width = (viewportWidth * mainScene.ratio) / parseFloat(mainScene.originalWidth);
    var coeff_height = (viewportHeight) / (parseFloat(mainScene.originalHeight) + $('#canvas').offset().top + $('#container').offset().top);

    var canvas_border_left = parseFloat($("#canvas").css("border-left-width").substr(0,$("#canvas").css("border-left-width").length - 2));
    var canvas_border_right = parseFloat($("#canvas").css("border-right-width").substr(0,$("#canvas").css("border-right-width").length - 2));
    var canvas_border_top = parseFloat($("#canvas").css("border-top-width").substr(0,$("#canvas").css("border-top-width").length - 2));
    var canvas_border_bottom = parseFloat($("#canvas").css("border-bottom-width").substr(0,$("#canvas").css("border-bottom-width").length - 2));

    if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_width) && (viewportHeight >= ((parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_width))) {
        mainScene.width = viewportWidth - canvas_border_left - canvas_border_right;
        mainScene.coeff = (mainScene.width * mainScene.ratio) / parseFloat(mainScene.originalWidth);
        mainScene.height = parseFloat(mainScene.originalHeight) * mainScene.coeff;
    }
    else if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_height) && (viewportHeight >= (parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_height)) {
        mainScene.height = viewportHeight - $('#container').offset().top - $('#canvas').offset().top - canvas_border_top - canvas_border_bottom - 2;
        mainScene.coeff = (mainScene.height) / parseFloat(mainScene.originalHeight);
        mainScene.width = parseFloat(mainScene.originalWidth) * mainScene.coeff;
    }

    $('#container').css({"width": (mainScene.width + canvas_border_left + canvas_border_right) + 'px'});
    $('#container').css({"height": (mainScene.height + $('#canvas').offset().top - $('#container').offset().top + canvas_border_top + canvas_border_bottom) + 'px'});
    $('#canvas').css({"height": (mainScene.height) + 'px'});
    $('#canvas').css({"width": mainScene.width + 'px'});
    $('#detect').css({"height": (mainScene.height) + 'px'});
    $('#detect').css({"top": ($('#canvas').offset().top) + 'px'});
};

IaScene.prototype.mouseover = function(kineticElement) {
    if (this.cursorState.indexOf("ZoomOut.cur") !== -1) {

    }
    else if (this.cursorState.indexOf("ZoomIn.cur") !== -1) {

    }
    else if (this.cursorState.indexOf("HandPointer.cur") === -1) {
        if ((kineticElement.getXiaParent().options.indexOf("pointer") !== -1) && (!this.tooltip_area)) {
            document.body.style.cursor = "pointer";
        }
        this.cursorState = "url(img/HandPointer.cur),auto";

        // manage tooltips if present
        var tooltip = false;
        if ((typeof(kineticElement.getXiaParent().tooltip) !== "undefined") && (kineticElement.getXiaParent().tooltip != "")) {
            tooltip = true;
        }
        else if ($("#" + kineticElement.getXiaParent().idText).data("tooltip") != "") {
            var tooltip_id = $("#" + kineticElement.getXiaParent().idText).data("tooltip");
            kineticElement.getXiaParent().tooltip = kineticElement.getStage().find("#" + tooltip_id)[0];
            tooltip = true;
        }
        if (tooltip) {
            kineticElement.getXiaParent().tooltip.clearCache();
            kineticElement.getXiaParent().tooltip.fillPriority('pattern');
            if ((kineticElement.getXiaParent().tooltip.backgroundImageOwnScaleX != "undefined") &&
                    (kineticElement.getXiaParent().tooltip.backgroundImageOwnScaleY != "undefined")) {
                kineticElement.getXiaParent().tooltip.fillPatternScaleX(kineticElement.getXiaParent().tooltip.backgroundImageOwnScaleX * 1/this.scale);
                kineticElement.getXiaParent().tooltip.fillPatternScaleY(kineticElement.getXiaParent().tooltip.backgroundImageOwnScaleY * 1/this.scale);
            }
            kineticElement.getXiaParent().tooltip.fillPatternImage(kineticElement.getXiaParent().tooltip.backgroundImage);
            kineticElement.getXiaParent().tooltip.getParent().moveToTop();
            //that.group.draw();
            kineticElement.getXiaParent().tooltip.draw();
        }

        //kineticElement.getIaObject().layer.batchDraw();
        //kineticElement.draw();
    }


};

IaScene.prototype.mouseout = function(kineticElement) {

    if ((this.cursorState.indexOf("ZoomOut.cur") !== -1) ||
            (this.cursorState.indexOf("ZoomIn.cur") !== -1)){

    }
    else {

        var mouseXY = kineticElement.getStage().getPointerPosition();
        if (typeof(mouseXY) == "undefined") {
            mouseXY = {x:0,y:0};
        }
        //if ((kineticElement.getStage().getIntersection(mouseXY) != kineticElement)) {

            // manage tooltips if present
            var tooltip = false;
            if ((typeof(kineticElement.getXiaParent().tooltip) !== "undefined") && (kineticElement.getXiaParent().tooltip != "")) {
                tooltip = true;
            }
            else if ($("#" + kineticElement.getXiaParent().idText).data("tooltip") != "") {
                var tooltip_id = $("#" + kineticElement.getXiaParent().idText).data("tooltip");
                kineticElement.getXiaParent().tooltip = kineticElement.getStage().find("#" + tooltip_id)[0];
                tooltip = true;
            }
            if (tooltip) {
                kineticElement.getXiaParent().tooltip.fillPriority('color');
                kineticElement.getXiaParent().tooltip.fill('rgba(0, 0, 0, 0)');
                kineticElement.getXiaParent().tooltip.getParent().moveToBottom();
                kineticElement.getXiaParent().tooltip.draw();
                kineticElement.getIaObject().layer.draw();
            }

            document.body.style.cursor = "default";
            this.cursorState = "default";

        //}
        document.body.style.cursor = "default";
    }

};

IaScene.prototype.click = function(kineticElement, mousePos) {

    if (kineticElement.getXiaParent().click == "off") return;

    /*
     * if we click in this element, manage zoom-in, zoom-out
     */
    if (kineticElement.getXiaParent().options.indexOf("direct-link") !== -1) {
        location.href = kineticElement.getXiaParent().title;
    }
    else {

        this.noPropagation = true;
        var iaobject = kineticElement.getIaObject();
        for (var i in iaobject.xiaDetail) {
            if (iaobject.xiaDetail[i].persistent == "off") {
                if (iaobject.xiaDetail[i].kineticElement instanceof Kinetic.Image) {
                    iaobject.xiaDetail[i].kineticElement.fillPriority('pattern');
                    iaobject.xiaDetail[i].kineticElement.fillPatternScaleX(iaobject.xiaDetail[i].kineticElement.backgroundImageOwnScaleX * 1/this.scale);
                    iaobject.xiaDetail[i].kineticElement.fillPatternScaleY(iaobject.xiaDetail[i].kineticElement.backgroundImageOwnScaleY * 1/this.scale);
                    iaobject.xiaDetail[i].kineticElement.fillPatternImage(iaobject.xiaDetail[i].kineticElement.backgroundImage);
                }
                else {
                    iaobject.xiaDetail[i].kineticElement.fillPriority('color');
                    iaobject.xiaDetail[i].kineticElement.fill(this.overColor);
                    iaobject.xiaDetail[i].kineticElement.scale(this.coeff);
                    iaobject.xiaDetail[i].kineticElement.stroke(this.overColorStroke);
                    iaobject.xiaDetail[i].kineticElement.strokeWidth(2);
                }

            }
            else if (iaobject.xiaDetail[i].persistent == "onPath") {
                iaobject.xiaDetail[i].kineticElement.fillPriority('color');
                iaobject.xiaDetail[i].kineticElement.fill('rgba(' + this.colorPersistent.red + ',' + this.colorPersistent.green + ',' + this.colorPersistent.blue + ',' + this.colorPersistent.opacity + ')');
            }
            else if (iaobject.xiaDetail[i].persistent == "onImage") {
                iaobject.xiaDetail[i].kineticElement.fillPriority('pattern');
                iaobject.xiaDetail[i].kineticElement.fillPatternScaleX(iaobject.xiaDetail[i].kineticElement.backgroundImageOwnScaleX * 1/this.scale);
                iaobject.xiaDetail[i].kineticElement.fillPatternScaleY(iaobject.xiaDetail[i].kineticElement.backgroundImageOwnScaleY * 1/this.scale);
                iaobject.xiaDetail[i].kineticElement.fillPatternImage(iaobject.xiaDetail[i].kineticElement.backgroundImage);
            }
            else if ((iaobject.xiaDetail[i].persistent == "persistentSprite") || (iaobject.xiaDetail[i].persistent == "hiddenSprite")) {
                iaobject.xiaDetail[i].kineticElement.animation('idle')
                iaobject.xiaDetail[i].kineticElement.frameIndex(0)
            }
            //iaobject.xiaDetail[i].kineticElement.moveToTop();
            iaobject.xiaDetail[i].kineticElement.draw();
        }

        //iaobject.group.moveToTop();
        //iaobject.layer.draw();
        this.element = iaobject;
        iaobject.myhooks.afterIaObjectFocus(this, kineticElement.getXiaParent().idText, iaobject, kineticElement);
        iaobject.layer.getStage().completeImage = "redefine";

    }

};
