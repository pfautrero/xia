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
 * @param {type} imageObj
 * @param {type} detail
 * @param {type} layer
 * @param {type} idText
 * @param {type} baseImage
 * @param {type} iaScene
 * @constructor create image active object
 */
function IaObject(imageObj, detail, layer, idText, baseImage, iaScene, background_layer, backgroundCache_layer, myhooks) {
    "use strict";
    var that = this;
    this.path = [];
    this.title = [];      
    this.kineticElement = [];
    this.backgroundImage = [];
    this.backgroundImageOwnScaleX = [];
    this.backgroundImageOwnScaleY = [];    
    this.persistent = [];
    this.originalX = [];
    this.originalY = [];
    this.options = [];    
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
    this.tween = []; 
    this.tween_group = 0;
    this.group = 0;
    this.myhooks = myhooks;
    this.idText = idText;    
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
    this.myhooks.afterIaObjectConstructor(iaScene, idText, detail, this);

}

/*
 * 
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includeImage = function(detail, i, that, iaScene, baseImage, idText) {
    that.defineImageBoxSize(detail, that);
    var rasterObj = new Image();
    rasterObj.src = detail.image;    
    that.title[i] = detail.title;    
    that.backgroundImage[i] = rasterObj;
    that.kineticElement[i] = new Kinetic.Image({
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        scale: {x:iaScene.coeff,y:iaScene.coeff}
        //fill: 'rgba(0, 0, 0, 0)'	
    });

    rasterObj.onload = function() {
        that.backgroundImageOwnScaleX[i] = iaScene.scale * detail.width / this.width;
        that.backgroundImageOwnScaleY[i] = iaScene.scale * detail.height / this.height;
        var zoomable = true;
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }
        if ((typeof(detail.options) !== 'undefined')) {
            that.options[i] = detail.options;
        }
        that.persistent[i] = "off-image";
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

        var cropX = Math.max(parseFloat(detail.minX), 0);
        var cropY = Math.max(parseFloat(detail.minY), 0);
        var cropWidth = (Math.min(parseFloat(detail.maxX) - parseFloat(detail.minX), Math.floor(parseFloat(iaScene.originalWidth) * 1)));
        var cropHeight = (Math.min(parseFloat(detail.maxY) - parseFloat(detail.minY), Math.floor(parseFloat(iaScene.originalHeight) * 1)));
        if (cropX + cropWidth > iaScene.originalWidth * 1) {
            cropWidth = iaScene.originalWidth * 1 - cropX * 1;
        }
        if (cropY * 1 + cropHeight > iaScene.originalHeight * 1) {
            cropHeight = iaScene.originalHeight * 1 - cropY * 1;
        }

        var canvas_source = document.createElement('canvas');
        canvas_source.setAttribute('width', cropWidth * iaScene.coeff);
        canvas_source.setAttribute('height', cropHeight * iaScene.coeff);
        var context_source = canvas_source.getContext('2d');
        context_source.drawImage(rasterObj,0,0, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);
        imageDataSource = context_source.getImageData(0, 0, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);            
        len = imageDataSource.data.length;
        that.group.zoomActive = 0;
       
        (function(len, imageDataSource){
        that.kineticElement[i].hitFunc(function(context) {
            if (that.group.zoomActive == 0) {
                rgbColorKey = Kinetic.Util._hexToRgb(this.colorKey);
                //detach from the DOM
                var imageData = imageDataSource.data;
                // just replace scene colors by hit colors - alpha remains unchanged
                for(j = 0; j < len; j += 4) {
                   imageData[j + 0] = rgbColorKey.r;
                   imageData[j + 1] = rgbColorKey.g;
                   imageData[j + 2] = rgbColorKey.b;
                   // imageData[j + 3] = imageDataSource.data[j + 3];
                } 
                // reatach to the DOM
                imageDataSource.data = imageData;

                context.putImageData(imageDataSource, cropX * iaScene.coeff, cropY * iaScene.coeff);     
            }
            else {
                context.beginPath();
                context.rect(0,0,this.width(),this.height());
                context.closePath();
                context.fillStrokeShape(this);					
            }
        });        
        })(len, imageDataSource);
        /*that.kineticElement[i].sceneFunc(function(context) {
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
IaObject.prototype.includePath = function(detail, i, that, iaScene, baseImage, idText) {
    that.path[i] = detail.path;
    //that.backgroundImage[i] = imageObj;
    that.title[i] = detail.title;
    // if detail is out of background, hack maxX and maxY
    if (parseFloat(detail.maxX) < 0) detail.maxX = 1;
    if (parseFloat(detail.maxY) < 0) detail.maxY = 1;        
    that.kineticElement[i] = new Kinetic.Path({
        name: detail.title,
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
    var cropWidth = (Math.min((parseFloat(detail.maxX) - cropX) * iaScene.scale, Math.floor(parseFloat(iaScene.originalWidth) * iaScene.scale)));
    var cropHeight = (Math.min((parseFloat(detail.maxY) - cropY) * iaScene.scale, Math.floor(parseFloat(iaScene.originalHeight) * iaScene.scale)));
    if (cropX * iaScene.scale + cropWidth > iaScene.originalWidth * iaScene.scale) {
	cropWidth = iaScene.originalWidth * iaScene.scale - cropX * iaScene.scale;
    }
    if (cropY * iaScene.scale + cropHeight > iaScene.originalHeight * iaScene.scale) {
	cropHeight = iaScene.originalHeight * iaScene.scale - cropY * iaScene.scale;
    }
    var posX = 0;
    var posY = 0;
    if (parseFloat(detail.minX) < 0) posX = parseFloat(detail.minX) * (-1);
    if (parseFloat(detail.minY) < 0) posY = parseFloat(detail.minY) * (-1);
    cropCtx.drawImage(
        that.imageObj,
        cropX * iaScene.scale,
        cropY * iaScene.scale,
        cropWidth,
        cropHeight,
        posX,
        posY,
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
    if ((typeof(detail.options) !== 'undefined')) {
        that.options[i] = detail.options;
    }    
    that.persistent[i] = "off";
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#ffffff")) {
        that.persistent[i] = "onPath";
        that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
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
IaObject.prototype.defineImageBoxSize = function(detail, that) {
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
IaObject.prototype.definePathBoxSize = function(detail, that) {
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
IaObject.prototype.defineTweens = function(that, iaScene) {

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
   
IaObject.prototype.addEventsManagement = function(i, zoomable, that, iaScene, baseImage, idText) {

    if (that.options[i].indexOf("disable-click") !== -1) return;
    
    /*
     * if mouse is over element, fill the element with semi-transparency
     */
    that.kineticElement[i].on('mouseover', function() {
        var k = 0;
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {
            
        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            document.body.style.cursor = "url(img/HandPointer.cur),auto";
            iaScene.cursorState = "url(img/HandPointer.cur),auto";
            for (k in that.kineticElement) {
                if (that.persistent[k] == "off") {
                    that.kineticElement[k].fillPriority('color');
                    that.kineticElement[k].fill(iaScene.overColor);
                    that.kineticElement[k].scale(iaScene.coeff);
                    that.kineticElement[k].stroke(iaScene.overColorStroke);
                    that.kineticElement[k].strokeWidth(2);                    
                }
                else if (that.persistent[k] == "onPath") {
                    that.kineticElement[k].fillPriority('color');
                    that.kineticElement[k].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                }
                else if ((that.persistent[i] == "onImage") || (that.persistent[i] == "off-image")) {
                    that.kineticElement[k].fillPriority('pattern');
                    that.kineticElement[k].fillPatternScaleX(that.backgroundImageOwnScaleX[k] * 1/iaScene.scale);
                    that.kineticElement[k].fillPatternScaleY(that.backgroundImageOwnScaleY[k] * 1/iaScene.scale);
                    that.kineticElement[k].fillPatternImage(that.backgroundImage[k]);                        
                }                
            }
            that.layer.batchDraw();
        }
    });
    /*
     * if we click in this element, manage zoom-in, zoom-out
     */
    if (that.options[i].indexOf("direct-link") !== -1) {
        that.kineticElement[i].on('click touchstart', function(e) {
            location.href = that.title[i];
        });
    }
    else {    
        that.kineticElement[i].on('click touchstart', function() {
            // let's zoom
            var k = 0;
            iaScene.noPropagation = true;
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
                for (k in that.kineticElement) {
                   that.kineticElement[k].setStrokeWidth(parseFloat(6 / that.agrandissement));
                }            
                var personalTween = function() {
                    // linear
                    var tempX = that.originalX[0] + that.alpha.toFixed(2) * (that.tweenX - that.originalX[0]);
                    var tempY = that.originalY[0] + that.alpha.toFixed(2) * (that.tweenY - that.originalY[0]);
                    var tempScale = 1 + that.alpha.toFixed(2) * (that.agrandissement - 1);
                    var t = null;                    
                    if (that.alpha.toFixed(2) <= 1) {
                        that.alpha = that.alpha + that.step;

                        that.group.x(tempX);
                        that.group.y(tempY);
                        that.group.scaleX(tempScale);
                        that.group.scaleY(tempScale);

                        that.layer.draw();
                        t = setTimeout(personalTween, 30);
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

                    for (k in that.kineticElement) {
                        if (that.persistent[k] == "off") {
                            that.kineticElement[k].fillPriority('color');
                            that.kineticElement[k].fill('rgba(0, 0, 0, 0)');
                        }
                        else if (that.persistent[k] == "onPath") {
                            that.kineticElement[k].fillPriority('color');
                            that.kineticElement[k].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                        }
                        else if (that.persistent[k] == "onImage") {
                            that.kineticElement[k].fillPriority('pattern');
                            that.kineticElement[k].fillPatternScaleX(that.backgroundImageOwnScaleX[k] * 1/iaScene.scale);
                            that.kineticElement[k].fillPatternScaleY(that.backgroundImageOwnScaleY[k] * 1/iaScene.scale);
                            that.kineticElement[k].fillPatternImage(that.backgroundImage[k]);                        
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

                        for (k in iaScene.element.kineticElement) {
                            iaScene.element.kineticElement[k].fillPriority('color');
                            iaScene.element.kineticElement[k].fill('rgba(0,0,0,0)');
                            iaScene.element.kineticElement[k].setStroke('rgba(0, 0, 0, 0)');
                            iaScene.element.kineticElement[k].setStrokeWidth(0);                         
                        }
                        iaScene.element.layer.draw();
                    }                    
                    if (zoomable === true) {
                        document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                        iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
                    }

                    var cacheBackground = true;
                    for (k in that.kineticElement) {
                        if (that.persistent[k] === "onImage") cacheBackground = false;
                        that.kineticElement[k].fillPriority('pattern');
                        that.kineticElement[k].fillPatternScaleX(that.backgroundImageOwnScaleX[k] * 1/iaScene.scale);
                        that.kineticElement[k].fillPatternScaleY(that.backgroundImageOwnScaleY[k] * 1/iaScene.scale);
                        that.kineticElement[k].fillPatternImage(that.backgroundImage[k]);
                        that.kineticElement[k].stroke(iaScene.overColorStroke);
                        that.kineticElement[k].strokeWidth(2); 
                        that.kineticElement[k].moveToTop();
                    }
                    if (cacheBackground === true) that.backgroundCache_layer.moveToTop();
                    that.layer.moveToTop();
                    that.layer.draw(); 
                    iaScene.element = that;
                    that.myhooks.afterIaObjectFocus(iaScene, idText, that);
                }
            }
        });
    }
    /*
     * if we leave this element, just clear the scene
     */
    that.kineticElement[i].on('mouseleave', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else {
            var mouseXY = that.layer.getStage().getPointerPosition();
            if (typeof(mouseXY) == "undefined") {
		mouseXY = {x:0,y:0};
            }            
            if ((that.layer.getStage().getIntersection(mouseXY) != this)) {
                that.backgroundCache_layer.moveToBottom();
                for (var i in that.kineticElement) {
                    if ((that.persistent[i] == "off") || (that.persistent[i] == "off-image")) {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                        that.kineticElement[i].stroke('rgba(0, 0, 0, 0)');
                        that.kineticElement[i].strokeWidth(0);                         
                    }
                    else if (that.persistent[i] == "onPath") {
                        that.kineticElement[i].fillPriority('color');
                        that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                        that.kineticElement[i].stroke('rgba(0, 0, 0, 0)');
                        that.kineticElement[i].strokeWidth(0);                        

                    }
                    else if (that.persistent[i] == "onImage") {
                        that.kineticElement[i].fillPriority('pattern');
                        that.kineticElement[i].fillPatternScaleX(that.backgroundImageOwnScaleX[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternScaleY(that.backgroundImageOwnScaleY[i] * 1/iaScene.scale);
                        that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);                        
                        that.kineticElement[i].stroke('rgba(0, 0, 0, 0)');
                        that.kineticElement[i].strokeWidth(0);                        

                    }                    
                }
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
        }
    });        
};

