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


/*
 * 
 * @param {type} imageObj
 * @param {type} detail
 * @param {type} layer
 * @param {type} idText
 * @param {type} baseImage
 * @param {type} iaScene
 * @constructor create image active object
 */
function iaObject(imageObj, detail, layer, idText, baseImage, iaScene, background_layer, backgroundCache_layer) {
    "use strict";
    var that = this;
    this.path = new Array();
    this.kineticElement = new Array();
    this.backgroundImage = new Array();
    this.backgroundImageOwnScaleX = new Array();
    this.backgroundImageOwnScaleY = new Array();    
    this.persistent = new Array();
    this.originalX = new Array();
    this.originalY = new Array();
    this.layer = layer;
    this.background_layer = background_layer;
    this.backgroundCache_layer = backgroundCache_layer;
    this.imageObj = imageObj;
    this.agrandissement = 0;
    this.zoomActive = 0;
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -10000;
    this.maxY = -10000;
    this.tween = new Array(); 
    this.tween_group = 0;
    this.group = 0;
    
    // Create kineticElements and include them in a group
   
    that.group = new Kinetic.Group();
    that.layer.add(that.group);
    
    if (typeof(detail.path) !== 'undefined') {
        that.includePath(detail, 0, that, iaScene, baseImage, idText);
    }
    else if (typeof(detail.image) !== 'undefined') {
        that.includeImage(detail, 0, that, iaScene, baseImage, idText);
    }
    else if (typeof(detail.group) !== 'undefined') {
        for (var i in detail.group) {
            if (typeof(detail.group[i].path) !== 'undefined') {
                that.includePath(detail.group[i], i, that, iaScene, baseImage, idText);
            }
            else if (typeof(detail.group[i].image) !== 'undefined') {
                that.includeImage(detail.group[i], i, that, iaScene, baseImage, idText);
            }
        }
        that.definePathBoxSize(detail, that);
    }
    else {
        console.log(detail);
    }

    this.defineTweens(this, iaScene);
    
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
                    //iaScene.element.kineticElement[i].fillPriority('color');
                    //iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    //iaScene.element.layer.draw();
                    
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
                        iaScene.element.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        iaScene.element.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                        iaScene.element.kineticElement[i].fillPatternImage(iaScene.element.backgroundImage[i]);                        
                    }                     
                    iaScene.element.layer.draw();
                }
                
            }
            var zoomable = true;
            if ((typeof(detail.fill) !== 'undefined') && 
                (detail.fill === "#000000")) {
                zoomable = false;
            }

            if (zoomable === true) {
                document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
            }            
            var cacheBackground = true;
            for (var i in that.kineticElement) {
                if (that.persistent[i] === "onImage") cacheBackground = false;
                that.kineticElement[i].fillPriority('pattern');
                that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);                
                that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
            }
            if (cacheBackground == true) {
                that.backgroundCache_layer.moveToTop();
            }

            iaScene.element = that;
            that.layer.moveToTop();
            that.layer.draw();				
            that.backgroundCache_layer.draw();
        }
    });
}

/*
 * 
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
iaObject.prototype.includeImage = function(detail, i, that, iaScene, baseImage, idText) {
    that.defineImageBoxSize(detail, that);
    var rasterObj = new Image();
    rasterObj.src = detail.image;                
    that.backgroundImage[i] = rasterObj;
    that.kineticElement[i] = new Kinetic.Image({
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        scale: {x:iaScene.coeff,y:iaScene.coeff}
        //fill: 'rgba(0, 0, 0, 0)'	
    });

    rasterObj.onload = function() {
        that.backgroundImageOwnScaleX[i] = detail.width / this.width;
        that.backgroundImageOwnScaleY[i] = detail.height / this.height;
        var zoomable = true;
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }

        that.persistent[i] = "off";
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#ffffff")) {
            that.persistent[i] = "onImage";
            that.kineticElement[i].fillPriority('pattern');
            that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
            that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);                
            that.kineticElement[i].fillPatternImage(that.backgroundImage[i]); 
            zoomable = false;
        }
        
        
        that.group.add(that.kineticElement[i]);
        that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);

        // define hit area excluding transparent pixels

        /*detail.minX = parseFloat(detail.x);
        detail.minY = parseFloat(detail.y);
        detail.maxX = parseFloat(detail.x) + parseFloat(detail.width);
        detail.maxY = parseFloat(detail.y) + parseFloat(detail.height);
        var cropX = Math.max(parseFloat(detail.minX), 0);
        var cropY = Math.max(parseFloat(detail.minY), 0);
        var cropWidth = (Math.min(parseFloat(detail.maxX) - parseFloat(detail.minX), Math.floor(parseFloat(iaScene.originalWidth) * 1)));
        var cropHeight = (Math.min(parseFloat(detail.maxY) - parseFloat(detail.minY), Math.floor(parseFloat(iaScene.originalHeight) * 1)));


        that.kineticElement[i].hitFunc(function(context) {
            var canvas_source = document.createElement('canvas');
            canvas_source.setAttribute('width', cropWidth * iaScene.coeff);
            canvas_source.setAttribute('height', cropHeight * iaScene.coeff);
            var context_source = canvas_source.getContext('2d');
            context_source.drawImage(rasterObj,0,0, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);
            var imageDataSource = context_source.getImageData(0, 0, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);            
            len = imageDataSource.data.length;
            
            var imageDataDestination = context.getImageData(cropX, cropY, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);
            rgbColorKey = Kinetic.Util._hexToRgb(this.colorKey);
       
            for(j = 0; j < len; j += 4) {

                imageDataDestination.data[j + 0] = rgbColorKey.r;
                imageDataDestination.data[j + 1] = rgbColorKey.g;
                imageDataDestination.data[j + 2] = rgbColorKey.b;
                imageDataDestination.data[j + 3] = imageDataSource.data[j + 3];

            }
            context.putImageData(imageDataDestination, cropX * iaScene.coeff, cropY * iaScene.coeff);     
            this.scaleX(iaScene.coeff);

        });        

        that.kineticElement[i].sceneFunc(function(context) {
            var yo = that.layer.getHitCanvas().getContext().getImageData(0,0,iaScene.width, iaScene.height);
            context.putImageData(yo, 0,0);  
        });*/

        that.group.draw();        
    };

};    


/*
 * 
 * @param {type} path
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
iaObject.prototype.includePath = function(detail, i, that, iaScene, baseImage, idText) {
    that.path[i] = detail.path;
    //that.backgroundImage[i] = imageObj;

    that.kineticElement[i] = new Kinetic.Path({
        data: detail.path,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        scale: {x:iaScene.coeff,y:iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)'
    });
    that.definePathBoxSize(detail, that);
    // crop background image to suit shape box
    that.cropCanvas = document.createElement('canvas');
    that.cropCanvas.setAttribute('width', parseFloat(detail.maxX) - parseFloat(detail.minX));
    that.cropCanvas.setAttribute('height', parseFloat(detail.maxY) - parseFloat(detail.minY));
    var cropCtx = that.cropCanvas.getContext('2d');
    var cropX = Math.max(parseFloat(detail.minX), 0);
    var cropY = Math.max(parseFloat(detail.minY), 0);
    var cropWidth = (Math.min(parseFloat(detail.maxX) - parseFloat(detail.minX), Math.floor(parseFloat(iaScene.originalWidth) * iaScene.scale)));
    var cropHeight = (Math.min(parseFloat(detail.maxY) - parseFloat(detail.minY), Math.floor(parseFloat(iaScene.originalHeight) * iaScene.scale)));

    cropCtx.drawImage(
        that.imageObj,
        cropX * iaScene.scale,
        cropY * iaScene.scale,
        cropWidth,
        cropHeight,
        0,
        0,
        cropWidth,
        cropHeight
    );
    var dataUrl = that.cropCanvas.toDataURL();
    delete that.cropCanvas;
    var cropedImage = new Image();
    cropedImage.src = dataUrl;
    cropedImage.onload = function() {
        that.backgroundImage[i] = cropedImage;
        that.backgroundImageOwnScaleX[i] = 1;
        that.backgroundImageOwnScaleY[i] = 1;        
        that.kineticElement[i].fillPatternRepeat('no-repeat');
        that.kineticElement[i].fillPatternX(detail.minX);
        that.kineticElement[i].fillPatternY(detail.minY);
        //that.kineticElement[i].draw();
    };

    var zoomable = true;
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#000000")) {
        zoomable = false;
    }
    that.persistent[i] = "off";
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#ffffff")) {
        that.persistent[i] = "onPath";
        that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
    }    
    that.addEventsManagement(i, zoomable, that, iaScene, baseImage, idText);

    that.group.add(that.kineticElement[i]);
    that.group.draw();
};

/*
 * 
 * @param {type} index
 * @returns {undefined}
 */
iaObject.prototype.defineImageBoxSize = function(detail, that) {
    "use strict";

    if (that.minX === -1)
        that.minX = (parseFloat(detail.x));
    if (that.maxY === 10000)
        that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
    if (that.maxX === -1)
        that.maxX = (parseFloat(detail.x) + parseFloat(detail.width));
    if (that.minY === 10000)
        that.minY = (parseFloat(detail.y));

    if (parseFloat(detail.x) < that.minX) that.minX = parseFloat(detail.x);
    if (parseFloat(detail.x) + parseFloat(detail.width) > that.maxX)
        that.maxX = parseFloat(detail.x) + parseFloat(detail.width);
    if (parseFloat(detail.y) < that.minY) 
        that.miny = parseFloat(detail.y);
    if (parseFloat(detail.y) + parseFloat(detail.height) > that.maxY) 
        that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
};    


/*
 * 
 * @param {type} index
 * @returns {undefined}
 */
iaObject.prototype.definePathBoxSize = function(detail, that) {
    "use strict";
    if (  (typeof(detail.minX) !== 'undefined') &&
          (typeof(detail.minY) !== 'undefined') &&
          (typeof(detail.maxX) !== 'undefined') &&
          (typeof(detail.maxY) !== 'undefined')) {
        that.minX = detail.minX;
        that.minY = detail.minY;
        that.maxX = detail.maxX;
        that.maxY = detail.maxY;
    }
    else {
        console.log('definePathBoxSize failure');
    }
};



/*
 * Define zoom rate and define tween effect for each group
 * @returns {undefined}
 */
iaObject.prototype.defineTweens = function(that, iaScene) {

    that.minX = that.minX * iaScene.coeff;
    that.minY = that.minY * iaScene.coeff;
    that.maxX = that.maxX * iaScene.coeff;
    that.maxY = that.maxY * iaScene.coeff;    

    var largeur = that.maxX - that.minX;
    var hauteur = that.maxY - that.minY;
    that.agrandissement1  = (iaScene.height - iaScene.y) / hauteur;   // beta
    that.agrandissement2  = iaScene.width / largeur;    // alpha

    if (hauteur * that.agrandissement2 > iaScene.height) {
        that.agrandissement = that.agrandissement1;
        that.tweenX = (0 - (that.minX)) * that.agrandissement + (iaScene.width - largeur * that.agrandissement) / 2;
        that.tweenY = (0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y;
    }
    else {
        that.agrandissement = that.agrandissement2;
        that.tweenX = (0 - (that.minX)) * that.agrandissement;
        that.tweenY = 1 * ((0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y + (iaScene.height - hauteur * that.agrandissement) / 2);
    }
};

/*
 * Define mouse events on the current KineticElement
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
   
iaObject.prototype.addEventsManagement = function(i, zoomable, that, iaScene, baseImage, idText) {

    /*
     * if mouse is over element, fill the element with semi-transparency
     */
    that.kineticElement[i].on('mouseover', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {
            
        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            document.body.style.cursor = "url(img/HandPointer.cur),auto";
            iaScene.cursorState = "url(img/HandPointer.cur),auto";
            for (var i in that.kineticElement) {
                if (that.persistent[i] == "off") {
                    that.kineticElement[i].fillPriority('color');
                    that.kineticElement[i].fill(iaScene.overColor);
                    that.kineticElement[i].scale(iaScene.coeff);
                }
                else if (that.persistent[i] == "onPath") {
                    that.kineticElement[i].fillPriority('color');
                    that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                }
                else if (that.persistent[i] == "onImage") {
                    that.kineticElement[i].fillPriority('pattern');
                    that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                    that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                    that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);                        
                }                
            }
            that.layer.batchDraw();
        }
    });
    /*
     * if we click in this element, manage zoom-in, zoom-out
     */
    that.kineticElement[i].on('click touchstart', function() {
        // let's zoom
        if ((iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) && 
            (iaScene.element === that)) {
            
            iaScene.zoomActive = 1;
            document.body.style.cursor = "url(img/ZoomOut.cur),auto";
            iaScene.cursorState = "url(img/ZoomOut.cur),auto";
            that.layer.moveToTop();
            that.group.zoomActive = 1;
            that.originalX[0] = that.group.x();
            that.originalY[0] = that.group.y();
            /*that.tween_group = new Kinetic.Tween({
                node: that.group, 
                duration: 1,
                x: that.tweenX,
                y: that.tweenY,
                easing: iaScene.easing,
                scaleX: that.agrandissement,
                scaleY: that.agrandissement
            });*/                
            //that.tween_group.play();
            that.alpha = 0;
            that.step = 0.1;
            var personalTween = function() {
                // linear
                var tempX = that.originalX[0] + that.alpha.toFixed(2) * (that.tweenX - that.originalX[0]);
                var tempY = that.originalY[0] + that.alpha.toFixed(2) * (that.tweenY - that.originalY[0]);
                var tempScale = 1 + that.alpha.toFixed(2) * (that.agrandissement - 1);
                if (that.alpha.toFixed(2) <= 1) {
                    that.alpha = that.alpha + that.step;
                    that.group.x(tempX);
                    that.group.y(tempY);
                    that.group.scaleX(tempScale);
                    that.group.scaleY(tempScale);
                    that.layer.draw();
                    var t = setTimeout(personalTween, 30);
                }
                else {
                    clearTimeout(t);
                }
            };
            var t = setTimeout(personalTween, 30);
            
            
            
            
            
            
        }
        // let's unzoom
        else if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {

            if ((that.group.zoomActive == 1) && 
                (that.group.scaleX().toFixed(5) == (that.agrandissement).toFixed(5))) {
                iaScene.zoomActive = 0;
                that.group.zoomActive = 0;
                that.group.scaleX(1);
                that.group.scaleY(1);
                that.group.x(that.originalX[0]);
                that.group.y(that.originalY[0]);
                //that.group.clearCache();
                //that.tween_group.reset();
                //that.tween_group.destroy();
                //delete that.tween_group;

                that.backgroundCache_layer.moveToBottom();
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";

                for (var i in that.kineticElement) {
                    if (that.persistent[i] == "off") {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                    }
                    else if (that.persistent[i] == "onPath") {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                    }
                    else if (that.persistent[i] == "onImage") {
                        that.kineticElement[i].fillPriority('pattern');
                        that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);                        
                    }
                }                    
                that.layer.draw();
                that.backgroundCache_layer.draw();
            }
        }
        // let's focus
        else {
            if (iaScene.zoomActive === 0) {
                if ((iaScene.element !== 0) && 
                    (typeof(iaScene.element) !== 'undefined')) {
                    
                    for (var i in iaScene.element.kineticElement) {
                        iaScene.element.kineticElement[i].fillPriority('color');
                        iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    }
                }                    
                if (zoomable === true) {
                    document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                    iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
                }
                $('.collapse.in').each(function (index) {
                        if ($(this).attr("id") !== idText) 
                            $(this).collapse("toggle");
                });
                $('#' + idText).collapse("show");

                var cacheBackground = true;
                for (var i in that.kineticElement) {
                    if (that.persistent[i] === "onImage") cacheBackground = false;
                    that.kineticElement[i].fillPriority('pattern');
                    that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                    that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                    that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
                }
                if (cacheBackground === true) that.backgroundCache_layer.moveToTop();
                that.layer.moveToTop();
                that.layer.draw(); 
                iaScene.element = that;
            }
        }
    });
    /*
     * if we leave this element, just clear the scene
     */
    that.kineticElement[i].on('mouseleave', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else {
            var mouseXY = that.layer.getStage().getPointerPosition();
            if ((that.layer.getStage().getIntersection(mouseXY) != this)) {
                that.backgroundCache_layer.moveToBottom();
                for (var i in that.kineticElement) {
                    if (that.persistent[i] == "off") {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                    }
                    else if (that.persistent[i] == "onPath") {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                    }
                    else if (that.persistent[i] == "onImage") {
                        that.kineticElement[i].fillPriority('pattern');
                        that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);                        
                    }                    
                }
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
        }
    });        
};

