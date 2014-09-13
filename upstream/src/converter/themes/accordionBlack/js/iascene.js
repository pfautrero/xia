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
    var _colorOver = {red:66, green:133, blue:244, opacity:0.6};

    // default color used to fill stroke around shapes during mouseover
    var _colorOverStroke = {red:255, green:0, blue:0, opacity:1};
    
    // default color used to fill shapes if defined as cache
    this.colorPersistent = {red:124, green:154, blue:174, opacity:1};

    // Image ratio on the scene
    this.ratio = 0.50;  
    
    // padding-top in the canvas
    this.y = 0;

    // color used over background image during focus
    var _colorCache = {red:0, green:0, blue:0, opacity:0.6};
 
    // internal
    this.fullScreen = "off";
    this.backgroundCacheColor = 'rgba(' + _colorCache.red + ',' + _colorCache.green + ',' + _colorCache.blue + ',' + _colorCache.opacity + ')';
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
    console.log("0");
    if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_width) && (viewportHeight >= ((parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_width))) {
        mainScene.width = viewportWidth * mainScene.ratio;
        console.log("1");
        mainScene.coeff = (mainScene.width) / parseFloat(mainScene.originalWidth);
        mainScene.height = parseFloat(mainScene.originalHeight) * mainScene.coeff;
    }
    else if ((viewportWidth >= parseFloat(mainScene.originalWidth) * coeff_height) && (viewportHeight >= (parseFloat(mainScene.originalHeight) + $('#canvas').offset().top) * coeff_height)) {
        console.log("2");
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
    $('#detect').css({"top": ($('#canvas').offset().top - $('#container').offset().top) + 'px'});    
 
};
