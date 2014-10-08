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
function IaObject(imageObj, detail, layer, idText, baseImage, iaScene, background_layer, myhooks) {
    "use strict";
    var that = this;
    this.path = [];
    this.title = [];      
    this.kineticElement = [];
    this.persistent = [];
    this.originalX = [];
    this.originalY = [];
    this.options = [];
    this.layer = layer;
    this.background_layer = background_layer;
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
    this.idText = idText;
    this.myhooks = myhooks;
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
    //that.backgroundImage[i] = rasterObj;
    that.kineticElement[i] = new Kinetic.Image({
        id: detail.id,
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        scale: {x:iaScene.coeff,y:iaScene.coeff}
    });

    that.kineticElement[i].backgroundImage = rasterObj;
    that.kineticElement[i].tooltip = "";
    
    rasterObj.onload = function() {
        
        that.kineticElement[i].backgroundImageOwnScaleX = iaScene.scale * detail.width / this.width;
        that.kineticElement[i].backgroundImageOwnScaleY = iaScene.scale * detail.height / this.height;           
        var zoomable = true;

        if ((typeof(detail.options) !== 'undefined')) {
            that.options[i] = detail.options;
        }
        else {
            that.options[i] = "";
        }

        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }

        that.persistent[i] = "off";
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#ffffff")) {
            that.persistent[i] = "onImage";
            that.kineticElement[i].fillPriority('pattern');
            that.kineticElement[i].fillPatternScaleX(that.kineticElement[i].backgroundImageOwnScaleX * 1/iaScene.scale);
            that.kineticElement[i].fillPatternScaleY(that.kineticElement[i].backgroundImageOwnScaleY * 1/iaScene.scale);                
            that.kineticElement[i].fillPatternImage(that.kineticElement[i].backgroundImage); 
            zoomable = false;
        }
        that.group.add(that.kineticElement[i]);

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
        
	var hitCanvas = that.layer.getHitCanvas();
        iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));

        var canvas_source = document.createElement('canvas');
        canvas_source.setAttribute('width', cropWidth * iaScene.coeff);
        canvas_source.setAttribute('height', cropHeight * iaScene.coeff);
        var context_source = canvas_source.getContext('2d');
        context_source.drawImage(rasterObj,0,0, cropWidth * iaScene.coeff, cropHeight * iaScene.coeff);

	imageDataSource = context_source.getImageData(0, 0, Math.floor(cropWidth * iaScene.coeff), Math.floor(cropHeight * iaScene.coeff));            
        len = imageDataSource.data.length;

        // just replace scene colors by hit colors - alpha remains unchanged
        //context_source.putImageData(imageDataSource, 0, 0);  

        (function(len, imageDataSource){
        that.kineticElement[i].hitFunc(function(context) {

            if (that.group.zoomActive == 0) {
                    var imageData = imageDataSource.data;
                    var imageDest = iaScene.completeImage.data;
                    var position1 = 0;
                    var position2 = 0;

                    var rgbColorKey = Kinetic.Util._hexToRgb(this.colorKey);
                    for(var varx = 0; varx < Math.floor(cropWidth * iaScene.coeff); varx +=1) {
                        for(var vary = 0; vary < Math.floor(cropHeight * iaScene.coeff); vary +=1) {
                                position1 = 4 * (vary * Math.floor(cropWidth * iaScene.coeff) + varx);
                                position2 = 4 * ((vary + Math.floor(cropY * iaScene.coeff)) * Math.floor(that.layer.getHitCanvas().width) + varx + Math.floor(cropX * iaScene.coeff));
                                if (imageData[position1 + 3] > 200) {
                                   imageDest[position2 + 0] = rgbColorKey.r;
                                   imageDest[position2 + 1] = rgbColorKey.g;
                                   imageDest[position2 + 2] = rgbColorKey.b;
                                   imageDest[position2 + 3] = 255;
                                }
                        }
                    } 
                    context.putImageData(iaScene.completeImage, 0, 0);     
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
        that.group.zoomActive = 0;
        that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);
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
    
    var that=this;
    
    that.path[i] = detail.path;
    that.title[i] = detail.title;
    // if detail is out of background, hack maxX and maxY
    if (parseFloat(detail.maxX) < 0) detail.maxX = 1;
    if (parseFloat(detail.maxY) < 0) detail.maxY = 1;        
    that.kineticElement[i] = new Kinetic.Path({
        id: detail.id,        
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
    var cropWidth = (Math.min((parseFloat(detail.maxX) - parseFloat(detail.minX)) * iaScene.scale, Math.floor(parseFloat(iaScene.originalWidth) * iaScene.scale)));
    var cropHeight = (Math.min((parseFloat(detail.maxY) - parseFloat(detail.minY)) * iaScene.scale, Math.floor(parseFloat(iaScene.originalHeight) * iaScene.scale)));
    if (cropX * iaScene.scale + cropWidth > iaScene.originalWidth * iaScene.scale) {
	cropWidth = iaScene.originalWidth * iaScene.scale - cropX * iaScene.scale;
    }
    if (cropY * iaScene.scale + cropHeight > iaScene.originalHeight * iaScene.scale) {
	cropHeight = iaScene.originalHeight * iaScene.scale - cropY * iaScene.scale;
    }
    // bad workaround to avoid null dimensions
    if (cropWidth == 0) cropWidth = 1;
    if (cropHeight == 0) cropHeight = 1;
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
    that.kineticElement[i].tooltip = "";
    cropedImage.onload = function() {
        that.kineticElement[i].backgroundImage = cropedImage;

        that.kineticElement[i].backgroundImage = cropedImage;
        that.kineticElement[i].backgroundImageOwnScaleX = 1;
        that.kineticElement[i].backgroundImageOwnScaleY = 1;
        that.kineticElement[i].fillPatternRepeat('no-repeat');
        that.kineticElement[i].fillPatternX(detail.minX);
        that.kineticElement[i].fillPatternY(detail.minY);
    };

    if ((typeof(detail.options) !== 'undefined')) {

        that.options[i] = detail.options;
    }
    else {
        that.options[i] = "";
    }

    var zoomable = true;
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#000000")) {
        zoomable = false;
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
    var that = this;
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

    var that=this;

    that.kineticElement[i].droparea = false;
    that.kineticElement[i].tooltip_area = false;
    // if current detail is a drop area, disable drag and drop
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.kineticElement[i].droparea = true;
    }
    // tooltip must be at the bottom
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.kineticElement[i].getParent().moveToBottom();
        that.options[i] += " disable-click ";
        that.kineticElement[i].tooltip_area = true;
        // disable hitArea for tooltip
        that.kineticElement[i].hitFunc(function(context){
            context.beginPath();
            context.rect(0,0,0,0);
            context.closePath();
            context.fillStrokeShape(this);	
	});        
    }
    /*
     * if mouse is over element, fill the element with semi-transparency
     */
    
    that.kineticElement[i].on('mouseover', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            if ((that.options[i].indexOf("pointer") !== -1) && (!this.tooltip_area)) {
                document.body.style.cursor = "pointer";
            }
            iaScene.cursorState = "url(img/HandPointer.cur),auto";   
            
            // manage tooltips if present
            var tooltip = false;
            if (this.tooltip != "") {
                tooltip = true;
            }
            else if ($("#" + idText).data("tooltip") != "") {
                var tooltip_id = $("#" + idText).data("tooltip");
                this.tooltip = this.getStage().find("#" + tooltip_id)[0];
                tooltip = true;
            }
            if (tooltip) {
                this.tooltip.clearCache();
                this.tooltip.fillPriority('pattern');
                if ((this.tooltip.backgroundImageOwnScaleX != "undefined") && 
                        (this.tooltip.backgroundImageOwnScaleY != "undefined")) {
                    this.tooltip.fillPatternScaleX(this.tooltip.backgroundImageOwnScaleX * 1/iaScene.scale);
                    this.tooltip.fillPatternScaleY(this.tooltip.backgroundImageOwnScaleY * 1/iaScene.scale);
                }
                this.tooltip.fillPatternImage(this.tooltip.backgroundImage);
                this.tooltip.getParent().moveToTop();
                //that.group.draw();
            }            

            that.layer.batchDraw();
        }
    });

    /*
     * if we leave this element, just clear the scene
     */
    that.kineticElement[i].on('mouseleave', function() {
        //iaScene.noPropagation = true;
        if ((iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) ||
                (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1)){

        }
        else {
            var mouseXY = that.layer.getStage().getPointerPosition();
            if (typeof(mouseXY) == "undefined") {
		mouseXY = {x:0,y:0};
            }            
            if ((that.layer.getStage().getIntersection(mouseXY) != this)) {

                // manage tooltips if present
                var tooltip = false;
                if (this.tooltip != "") {
                    tooltip = true;
                }
                else if ($("#" + idText).data("tooltip") != "") {
                    var tooltip_id = $("#" + idText).data("tooltip");
                    this.tooltip = this.getStage().find("#" + tooltip_id)[0];
                    tooltip = true;
                }                
                if (tooltip) {
                    this.tooltip.fillPriority('color');
                    this.tooltip.fill('rgba(0, 0, 0, 0)');
                    this.tooltip.getParent().moveToBottom();
                    this.tooltip.draw();
                }                     

                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
            document.body.style.cursor = "default";
        }
    }); 


    if (that.options[i].indexOf("disable-click") !== -1) return;
    
    /*
     * if we click in this element, manage zoom-in, zoom-out
     */
    if (that.options[i].indexOf("direct-link") !== -1) {
        that.kineticElement[i].on('click touchstart', function(e) {
            location.href = that.title[i];
        });
    }
    else {    
        that.kineticElement[i].on('click touchstart', function(evt) {

            iaScene.noPropagation = true;
                if (iaScene.zoomActive === 0) {
                    for (var i in that.kineticElement) {
                        if (that.persistent[i] == "off") {
                            if (that.kineticElement[i] instanceof Kinetic.Image) {
                                that.kineticElement[i].fillPriority('pattern');
                                that.kineticElement[i].fillPatternScaleX(that.kineticElement[i].backgroundImageOwnScaleX * 1/iaScene.scale);
                                that.kineticElement[i].fillPatternScaleY(that.kineticElement[i].backgroundImageOwnScaleY * 1/iaScene.scale); 
                                that.kineticElement[i].fillPatternImage(that.kineticElement[i].backgroundImage);                        
                            }
                            else {
                                that.kineticElement[i].fillPriority('color');
                                that.kineticElement[i].fill(iaScene.overColor);
                                that.kineticElement[i].scale(iaScene.coeff);
                                that.kineticElement[i].stroke(iaScene.overColorStroke);
                                that.kineticElement[i].strokeWidth(2);                                                
                            }

                        }
                        else if (that.persistent[i] == "onPath") {
                            that.kineticElement[i].fillPriority('color');
                            that.kineticElement[i].fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');                       
                        }
                        else if (that.persistent[i] == "onImage") {
                            that.kineticElement[i].fillPriority('pattern');
                            that.kineticElement[i].fillPatternScaleX(that.kineticElement[i].backgroundImageOwnScaleX * 1/iaScene.scale);
                            that.kineticElement[i].fillPatternScaleY(that.kineticElement[i].backgroundImageOwnScaleY * 1/iaScene.scale); 
                            that.kineticElement[i].fillPatternImage(that.kineticElement[i].backgroundImage);                        
                        }                
                        that.kineticElement[i].moveToTop();
                    }                

                    that.group.moveToTop();
                    that.layer.draw(); 
                    iaScene.element = that;
                    that.myhooks.afterIaObjectFocus(iaScene, idText, that);
                    this.getStage().completeImage = "redefine";

                }
            //}

        });
    }
       
};

