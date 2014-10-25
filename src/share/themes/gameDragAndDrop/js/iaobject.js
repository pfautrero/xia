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
function IaObject(imageObj, detail, layer, idText, baseImage, iaScene, myhooks) {
    "use strict";
    var that = this;
    this.xiaDetail = [];
    this.layer = layer;
    this.imageObj = imageObj;
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -10000;
    this.maxY = -10000;
    //this.group = 0;
    this.idText = idText;
    this.myhooks = myhooks;
    this.match = false;
    this.collisions = "on";
    // Create kineticElements and include them in a group
   
    //that.group = new Kinetic.Group();
    //that.layer.add(that.group);
    
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
    this.scaleBox(this, iaScene);
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
    that.xiaDetail[i] = new XiaDetail();
    
    if ((typeof(detail.options) !== 'undefined')) {
        //that.options[i] = detail.options;
        that.xiaDetail[i].options = detail.options;
    }   
    var draggable_object = true;
    if (that.xiaDetail[i].options.indexOf("disable-click") != -1) {
        draggable_object = false;
    };  
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }    
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }  
    that.defineImageBoxSize(detail, that);
    var rasterObj = new Image();
    
    rasterObj.src = detail.image;   
    
    //that.title[i] = detail.title;
    that.xiaDetail[i].title = detail.title;
    
    that.xiaDetail[i].kineticElement = new Kinetic.Image({
        id: detail.id,
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        draggable: draggable_object
     
    });
    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    that.xiaDetail[i].backgroundImage = rasterObj;
    that.xiaDetail[i].kineticElement.tooltip = "";
    
    var collision_state = $("#" + idText).data("collisions");
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        collision_state = "off";
    }    
    that.collisions = collision_state;
    var global_collision_state = $("#message_success").data("collisions");
    if (global_collision_state == "on" && collision_state != "off") {
        that.xiaDetail[i].kineticElement.dragBoundFunc(function(pos) {
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
    
    
    that.xiaDetail[i].kineticElement.setIaObject(that);

    rasterObj.onload = function() {
        
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX = iaScene.scale * detail.width / this.width;
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY = iaScene.scale * detail.height / this.height;        
        var zoomable = true;

        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }

        if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length == 0) {
            detail.fill = '#ffffff';    // force image to be displayed - must refactor if it is a good idea !
        }
        that.xiaDetail[i].persistent = "off";
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#ffffff")) {
            that.xiaDetail[i].persistent = "onImage";
            that.xiaDetail[i].kineticElement.fillPriority('pattern');
            that.xiaDetail[i].kineticElement.fillPatternScaleX(that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX * 1/iaScene.scale);
            that.xiaDetail[i].kineticElement.fillPatternScaleY(that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY * 1/iaScene.scale);                
            that.xiaDetail[i].kineticElement.fillPatternImage(that.xiaDetail[i].backgroundImage); 
            zoomable = false;
        }
        
        that.layer.add(that.xiaDetail[i].kineticElement);
        that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);
        
        // define hit area excluding transparent pixels
        // =============================================================
        that.rasterObj = rasterObj;

        that.xiaDetail[i].kineticElement.cache();
        that.xiaDetail[i].kineticElement.scale({x:iaScene.coeff,y:iaScene.coeff});
        that.xiaDetail[i].kineticElement.drawHitFromCache();
        that.xiaDetail[i].kineticElement.draw();
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
    that.xiaDetail[i] = new XiaDetail();
    
    if ((typeof(detail.options) !== 'undefined')) {
        that.xiaDetail[i].options = detail.options;
    }   
    
    var draggable_object = true;
    if (that.xiaDetail[i].options.indexOf("disable-click") != -1) {
        draggable_object = false;
    };

    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        draggable_object = false;
    }      
    

    
    //that.path[i] = detail.path;
    that.xiaDetail[i].path = detail.path;
    that.xiaDetail[i].title = detail.title;
    //that.title[i] = detail.title;
    // if detail is out of background, hack maxX and maxY
    if (parseFloat(detail.maxX) < 0) detail.maxX = 1;
    if (parseFloat(detail.maxY) < 0) detail.maxY = 1;        
    that.xiaDetail[i].kineticElement = new Kinetic.Path({
        id: detail.id,
        name: detail.title,
        data: detail.path,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        scale: {x:iaScene.coeff,y:iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)',
        draggable : draggable_object
    });
    
    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    
    var collision_state = $("#" + idText).data("collisions");
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        collision_state = "off";
    }
    that.collisions = collision_state;

    var global_collision_state = $("#message_success").data("collisions");

    if (global_collision_state == "on" && collision_state != "off") {


        that.xiaDetail[i].kineticElement.dragBoundFunc(function(pos) {
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

    that.xiaDetail[i].kineticElement.setIaObject(that);
    that.definePathBoxSize(detail, that);
    // crop background image to suit shape box
    that.xiaDetail[i].kineticElement.tooltip = "";
    if (that.xiaDetail[i].options.indexOf("disable-click") == -1) {
        var cropCanvas = document.createElement('canvas');
        cropCanvas.setAttribute('width', parseFloat(detail.maxX) - parseFloat(detail.minX));
        cropCanvas.setAttribute('height', parseFloat(detail.maxY) - parseFloat(detail.minY));
        var cropCtx = cropCanvas.getContext('2d');
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
        var dataUrl = cropCanvas.toDataURL();
        var cropedImage = new Image();
        cropedImage.src = dataUrl;
        cropedImage.onload = function() {
            that.xiaDetail[i].backgroundImage = cropedImage;
            that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX = 1;
            that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY = 1;            
            that.xiaDetail[i].kineticElement.fillPatternRepeat('no-repeat');
            that.xiaDetail[i].kineticElement.fillPatternX(detail.minX);
            that.xiaDetail[i].kineticElement.fillPatternY(detail.minY);
        };
    }



    var zoomable = true;
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#000000")) {
        zoomable = false;
    }
    that.xiaDetail[i].persistent = "off";
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#ffffff")) {
        that.xiaDetail[i].persistent = "onPath";
        that.xiaDetail[i].kineticElement.fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
    }    
    that.addEventsManagement(i, zoomable, that, iaScene, baseImage, idText);

    that.layer.add(that.xiaDetail[i].kineticElement);
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
 * Rescale box
 * @returns {undefined}
 */
IaObject.prototype.scaleBox = function(that, iaScene) {
    that.minX = that.minX * iaScene.coeff;
    that.minY = that.minY * iaScene.coeff;
    that.maxX = that.maxX * iaScene.coeff;
    that.maxY = that.maxY * iaScene.coeff;    
};


/*
 * Define mouse events on the current KineticElement
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
   
IaObject.prototype.addEventsManagement = function(i, zoomable, that, iaScene, baseImage, idText) {

    var that=this;

    that.xiaDetail[i].kineticElement.droparea = false;
    that.xiaDetail[i].kineticElement.tooltip_area = false;
    // if current detail is a drop area, disable drag and drop
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.xiaDetail[i].kineticElement.droparea = true;
        
    }
    // tooltip must be at the bottom
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.xiaDetail[i].kineticElement.moveToBottom();
        that.xiaDetail[i].kineticElement.tooltip_area = true;
        that.xiaDetail[i].options += " disable-click ";
    }

    that.xiaDetail[i].kineticElement.on('mouseenter', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            if ((!this.droparea) && (!this.tooltip_area)) {
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
                this.tooltip.fillPatternImage(this.tooltip.getXiaParent().backgroundImage); 

                this.tooltip.moveToTop();
                this.tooltip.draw();
                that.layer.draw();
            }
            
        }
    });
 
    /*
     * if we leave this element, just clear the scene
     */
    that.xiaDetail[i].kineticElement.on('mouseout', function() {
    
        
        if ((iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) ||
                (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1)){

        }
        else {
            var mouseXY = that.layer.getStage().getPointerPosition();
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
                    this.tooltip.draw();
                }                
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
        }
    });       
    
    if (that.xiaDetail[i].options.indexOf("disable-click") != -1) return;

    if (that.xiaDetail[i].options.indexOf("direct-link") != -1) {
        that.xiaDetail[i].kineticElement.on('click touchstart', function(e) {
            //location.href = that.title[i];
            location.href = that.xiaDetail[i].title;
        });
    }
    else {
        if (!that.xiaDetail[i].kineticElement.droparea) {
            that.xiaDetail[i].kineticElement.on('dragstart', function(e) {
                iaScene.element = that;
                that.myhooks.afterIaObjectDragStart(iaScene, idText, that);
                this.moveToTop();
                Kinetic.draggedshape = this;
            });

            that.xiaDetail[i].kineticElement.on('dragend', function(e) {
                iaScene.element = that;
                Kinetic.draggedshape = null;
                // Kinetic hacking - speed up _getIntersection (for linux)
                this.getStage().completeImage = "redefine";
                that.myhooks.afterIaObjectDragEnd(iaScene, idText, that, e);
                that.layer.draw();
            });    
        }
    }
};

