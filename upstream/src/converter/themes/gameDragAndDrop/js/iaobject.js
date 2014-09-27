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
 * @param {type} backgroundCache_layer
 * @constructor create image active object
 */
function IaObject(imageObj, detail, layer, idText, baseImage, iaScene, background_layer, backgroundCache_layer, myhooks) {
    "use strict";
    var that = this;
    this.title = [];
    this.path = [];
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
    this.idText = idText;
    this.myhooks = myhooks;
    this.match = false;
    this.collisions = "on";
    // Create kineticElements and include them in a group
   
    that.group = new Kinetic.Group();
    that.layer.add(that.group);
    
    if (typeof(detail.path) !== 'undefined') {
        that.includePath(detail, 0, that, iaScene, baseImage, idText);
    }
    else if (typeof(detail.image) !== 'undefined') {
        that.includeImage(detail, 0, that, iaScene, baseImage, idText);
    }
    // actually, groups are not allowed because of boxsize restriction
    
    /*else if (typeof(detail.group) !== 'undefined') {
        for (var i in detail.group) {
            if (typeof(detail.group[i].path) !== 'undefined') {
                that.includePath(detail.group[i], i, that, iaScene, baseImage, idText);
            }
            else if (typeof(detail.group[i].image) !== 'undefined') {
                that.includeImage(detail.group[i], i, that, iaScene, baseImage, idText);
            }
        }
        that.definePathBoxSize(detail, that);
    }*/
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

    var that = this;
    if ((typeof(detail.options) !== 'undefined')) {
        that.options[i] = detail.options;
    }   
    var draggable_object = true;
    if (that.options[i].indexOf("disable-click") != -1) {
        draggable_object = false;
    };  
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }    
    that.defineImageBoxSize(detail, that);
    var rasterObj = new Image();
    rasterObj.src = detail.image;       
    that.title[i] = detail.title;
    that.backgroundImage[i] = rasterObj;
    that.kineticElement[i] = new Kinetic.Image({
        id: detail.id,
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        draggable: draggable_object
     
    });
    
    
    var collision_state = $("#" + idText).data("collisions");
    that.collisions = collision_state;
    var global_collision_state = $("#message_success").data("collisions");
    if (global_collision_state == "on" && collision_state != "off") {
        that.kineticElement[i].dragBoundFunc(function(pos) {
            var x_value = pos.x;
            var y_value = pos.y;
            var len = iaScene.shapes.length;
            var getAbsolutePosition = {
                x : this.getAbsolutePosition().x,
                y : this.getAbsolutePosition().y,
            }    

            for(var i=0; i< len; i++) {
                if (that != iaScene.shapes[i] && iaScene.shapes[i].collisions == "on") {

                    var shape = {
                        maxX : iaScene.shapes[i].maxX,
                        maxY : iaScene.shapes[i].maxY,
                        minX : iaScene.shapes[i].minX - (that.maxX - that.minX),
                        minY : iaScene.shapes[i].minY - (that.maxY - that.minY)
                    };                    
                    var pos_y = (getAbsolutePosition.y < shape.maxY - 10) &&
                          (getAbsolutePosition.y > shape.minY + 10);
                    var pos_x = (getAbsolutePosition.x < shape.maxX - 10) &&
                          (getAbsolutePosition.x > shape.minX + 10);

                    if (pos.x <= shape.maxX && 
                            pos_y && 
                            getAbsolutePosition.x >= shape.maxX - 10) {
                        if (x_value == pos.x) {
                            x_value = shape.maxX;
                        }
                        else {
                            x_value = Math.max(shape.maxX, x_value);
                        }
                    }

                    if (pos.x >= shape.minX && 
                            pos_y && 
                            getAbsolutePosition.x <= shape.minX + 10) {
                        if (x_value == pos.x) {
                            x_value = shape.minX;
                        }
                        else {
                            x_value = Math.min(shape.minX, x_value);
                        }
                    }
                    if (pos.y <= shape.maxY && 
                            pos_x && 
                            getAbsolutePosition.y >= shape.maxY -10) {
                        if (y_value == pos.y) {
                            y_value = shape.maxY;
                        }
                        else {
                            y_value = Math.max(shape.maxY, y_value);
                        }
                    }                    

                    if (pos.y >= shape.minY && 
                            pos_x && 
                            getAbsolutePosition.y <= 10 + shape.minY) {
                        if (y_value == pos.y) {
                            y_value = shape.minY;
                        }
                        else {
                            y_value = Math.min(shape.minY, y_value);
                        }
                    }
                }
            }

            return {
              x: x_value,
              y: y_value
            };
        
        });
       
    }
    
    
    that.kineticElement[i].setIaObject(that);

    rasterObj.onload = function() {
        that.backgroundImageOwnScaleX[i] = iaScene.scale * detail.width / this.width;
        that.backgroundImageOwnScaleY[i] = iaScene.scale * detail.height / this.height;
        var zoomable = true;

        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }

        detail.fill = '#ffffff';    // force image to be displayed - must refactor if it is a good idea !

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
        // =============================================================
        that.rasterObj = rasterObj;

        that.kineticElement[i].cache();
        that.kineticElement[i].scale({x:iaScene.coeff,y:iaScene.coeff});
        that.kineticElement[i].drawHitFromCache();
        that.kineticElement[i].draw();

    };

};    


/*
 * 
 * @param {type} path
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includePath = function(detail, i, that, iaScene, baseImage, idText) {
    var that = this;

    if ((typeof(detail.options) !== 'undefined')) {
        that.options[i] = detail.options;
    }   
    
    var draggable_object = true;
    if (that.options[i].indexOf("disable-click") != -1) {
        draggable_object = false;
    };

    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }
    
    
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
        fill: 'rgba(0, 0, 0, 0)',
        draggable : draggable_object
    });
    
    var collision_state = $("#" + idText).data("collisions");
    that.collisions = collision_state;    
    var global_collision_state = $("#message_success").data("collisions");
    if (global_collision_state == "on" && collision_state != "off") {

        that.kineticElement[i].dragBoundFunc(function(pos) {
            var x_value = pos.x;
            var y_value = pos.y;
            var len = iaScene.shapes.length;
            var getAbsolutePosition = {
                x : this.getAbsolutePosition().x,
                y : this.getAbsolutePosition().y,
            }    

            for(var i=0; i< len; i++) {
                if (that != iaScene.shapes[i] && iaScene.shapes[i].collisions == "on") {

                    var shape = {
                        maxX : iaScene.shapes[i].maxX,
                        maxY : iaScene.shapes[i].maxY,
                        minX : iaScene.shapes[i].minX - (that.maxX - that.minX),
                        minY : iaScene.shapes[i].minY - (that.maxY - that.minY)
                    };                    
                    var pos_y = (getAbsolutePosition.y < shape.maxY - 10) &&
                          (getAbsolutePosition.y > shape.minY + 10);
                    var pos_x = (getAbsolutePosition.x < shape.maxX - 10) &&
                          (getAbsolutePosition.x > shape.minX + 10);

                    if (pos.x <= shape.maxX && 
                            pos_y && 
                            getAbsolutePosition.x >= shape.maxX - 10) {
                        if (x_value == pos.x) {
                            x_value = shape.maxX;
                        }
                        else {
                            x_value = Math.max(shape.maxX, x_value);
                        }
                    }

                    if (pos.x >= shape.minX && 
                            pos_y && 
                            getAbsolutePosition.x <= shape.minX + 10) {
                        if (x_value == pos.x) {
                            x_value = shape.minX;
                        }
                        else {
                            x_value = Math.min(shape.minX, x_value);
                        }
                    }
                    if (pos.y <= shape.maxY && 
                            pos_x && 
                            getAbsolutePosition.y >= shape.maxY -10) {
                        if (y_value == pos.y) {
                            y_value = shape.maxY;
                        }
                        else {
                            y_value = Math.max(shape.maxY, y_value);
                        }
                    }                    

                    if (pos.y >= shape.minY && 
                            pos_x && 
                            getAbsolutePosition.y <= 10 + shape.minY) {
                        if (y_value == pos.y) {
                            y_value = shape.minY;
                        }
                        else {
                            y_value = Math.min(shape.minY, y_value);
                        }
                    }
                }
            }

            return {
              x: x_value,
              y: y_value
            };
              
        
        });
        
        
        
    }

    that.kineticElement[i].setIaObject(that);
    that.definePathBoxSize(detail, that);
    // crop background image to suit shape box


    
    if (that.options[i].indexOf("disable-click") == -1) {
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
        };
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
    that.layer.draw();
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

    var that=this;

    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        return;
    }
    
    if (that.options[i].indexOf("disable-click") != -1) return;

    if (that.options[i].indexOf("direct-link") != -1) {
        that.kineticElement[i].on('click touchstart', function(e) {
            location.href = that.title[i];
        });
    }
    else {
        that.kineticElement[i].on('dragstart', function(e) {
            iaScene.element = that;
            that.myhooks.afterIaObjectDragStart(iaScene, idText, that);
            that.layer.moveToTop();
            Kinetic.draggedshape = this;
        });
        
        that.kineticElement[i].on('dragend', function(e) {
            iaScene.element = that;
            Kinetic.draggedshape = null;
            that.myhooks.afterIaObjectDragEnd(iaScene, idText, that, e);
            that.layer.draw();
        });    
    }

    that.kineticElement[i].on('mouseover', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            document.body.style.cursor = "url(img/HandPointer.cur),auto";
            iaScene.cursorState = "url(img/HandPointer.cur),auto";
        }
    });

    /*
     * if we leave this element, just clear the scene
     */
    that.kineticElement[i].on('mouseleave', function() {
        if ((iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) ||
                (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1)){

        }
        else {
            var mouseXY = that.layer.getStage().getPointerPosition();
            if ((that.layer.getStage().getIntersection(mouseXY) != this)) {
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
        }
    });       
    
      
};

