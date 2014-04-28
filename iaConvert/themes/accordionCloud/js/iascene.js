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
function iaScene(originalWidth, originalHeight) {
    "use strict";
    var that = this;
    //  canvas width
    this.width = 1000;
    
    // canvas height
    this.height = 800;  
    
    // default color used to fill shapes during mouseover
    var _colorOver = {red:66, green:133, blue:244, opacity:0.6};

    // Image ratio on the scene
    this.ratio = 0.65;  
    
    // padding-top in the canvas
    this.y = 0;

    // easing effect
    //this.easing = Kinetic.Easings.StrongEaseOut;

    // color used over background image during focus
    var _colorCache = {red:255, green:255, blue:255, opacity:0.6};
 
    // internal
    this.fullScreen = "off";
    this.backgroundCacheColor = 'rgba(' + _colorCache.red + ',' + _colorCache.green + ',' + _colorCache.blue + ',' + _colorCache.opacity + ')';
    this.overColor = 'rgba(' + _colorOver.red + ',' + _colorOver.green + ',' + _colorOver.blue + ',' + _colorOver.opacity + ')';    
    this.scale = 1;
    this.zoomActive = 0;
    this.element = 0;
    this.originalWidth = originalWidth;
    this.originalHeight = originalHeight;
    this.coeff = (this.width * this.ratio) / parseFloat(originalWidth);
    this.cursorState="";

}

/*
 * Scale entire scene
 *  
 */
iaScene.prototype.scaleScene = function(mainScene){
    var viewportWidth = $(window).width();
    var viewportHeight = $(window).height();
    var new_height = scene.height * mainScene.coeff + $('#canvas').offset().top - $('#container').offset().top;
    $('#container').css({"height": new_height + 'px'});
    $('#canvas').css({"height": mainScene.originalHeight * mainScene.coeff + 'px'});
    
    var resize = false;
    if ((this.fullScreen == "on") || (viewportWidth < 1000)) {
        resize = true;
    }
    if (resize) {
        mainScene.width = viewportWidth - mainScene.y;
        mainScene.coeff = (mainScene.width * mainScene.ratio) / parseFloat(mainScene.originalWidth);
        $('#container').css({"width": viewportWidth - mainScene.y});
    }
    if (viewportHeight < 755) {
        mainScene.height = viewportHeight - mainScene.y;
        $('#detect').css({"height": viewportHeight - mainScene.y});
    }
};

