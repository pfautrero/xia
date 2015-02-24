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
 * @param {object} params
 * @constructor create image active object
 */
function IaObject(params) {
    "use strict";
    var that = this;
    this.xiaDetail = [];
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -10000;
    this.maxY = -10000;
    this.match = false;
    this.collisions = "on";
    this.mainScene = params.iaScene;
    this.layer = params.layer;
    this.imageObj = params.imageObj;
    this.idText = params.idText;
    this.myhooks = params.myhooks;

    // Create kineticElements and include them in a group
   
    //that.group = new Kinetic.Group();
    //that.layer.add(that.group);
    
    if (typeof(params.detail.path) !== 'undefined') {
        that.includePath(params.detail, 0, that, params.iaScene, params.baseImage, params.idText);
    }
    else if (typeof(params.detail.image) !== 'undefined') {
        that.includeImage(params.detail, 0, that, params.iaScene, params.baseImage, params.idText);
    }

    else if (typeof(params.detail.group) !== 'undefined') {
        that.group = new Kinetic.Group({
            id: params.detail.id
        });
        that.layer.add(that.group);

        for (var i in params.detail.group) {
            if (typeof(params.detail.group[i].path) !== 'undefined') {
                that.includePath(params.detail.group[i], i, that, params.iaScene, params.baseImage, params.idText);
            }
            else if (typeof(params.detail.group[i].image) !== 'undefined') {
                that.includeImage(params.detail.group[i], i, that, params.iaScene, params.baseImage, params.idText);
            }
        }
        //that.definePathBoxSize(params.detail, that);
    }
    else {
        console.log(params.detail);
    }
    //this.scaleBox(this, params.iaScene);
    this.myhooks.afterIaObjectConstructor(params.iaScene, params.idText, params.detail, this);
}

/*
 * 
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includeImage = function(detail, i, that, iaScene, baseImage, idText) {

    var that = this;
    that.xiaDetail[i] = new XiaDetail(detail, idText);

    that.defineImageBoxSize(detail, that.xiaDetail[i]);
    that.scaleBox(that.xiaDetail[i], iaScene);
    var rasterObj = new Image();
    
    rasterObj.src = detail.image;
    
    that.xiaDetail[i].kineticElement = new Kinetic.Image({
        id: detail.id,
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        draggable: that.xiaDetail[i].draggable_object
     
    });

    that.layer.add(that.xiaDetail[i].kineticElement);
    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    that.xiaDetail[i].kineticElement.setIaObject(that);
    that.xiaDetail[i].backgroundImage = rasterObj;
    that.xiaDetail[i].kineticElement.tooltip = "";
    that.xiaDetail[i].lastDragPos.x = that.xiaDetail[i].kineticElement.x();
    that.xiaDetail[i].lastDragPos.y = that.xiaDetail[i].kineticElement.y();
    
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
            var objectWidth = this.getXiaParent().maxX - this.getXiaParent().minX;
            var objectHeight = this.getXiaParent().maxY - this.getXiaParent().minY;
            for(var i=0; i< len; i++) {
                if (that != iaScene.shapes[i] && iaScene.shapes[i].collisions == "on") {

                    for (var j=0; j< iaScene.shapes[i].xiaDetail.length;j++) {
                        var shape = {
                            maxX : iaScene.shapes[i].xiaDetail[j].maxX,
                            maxY : iaScene.shapes[i].xiaDetail[j].maxY,
                            minX : iaScene.shapes[i].xiaDetail[j].minX - objectWidth,
                            minY : iaScene.shapes[i].xiaDetail[j].minY - objectHeight
                        };

                        var objectLocatedAt = {
                            horizontal: (getAbsolutePosition.y < shape.maxY - 10) &&
                              (getAbsolutePosition.y > shape.minY + 10),
                            vertical: (getAbsolutePosition.x < shape.maxX - 10) &&
                              (getAbsolutePosition.x > shape.minX + 10),
                            bottomLeft: getAbsolutePosition.x <= shape.minX + 10 &&
                              getAbsolutePosition.y >= shape.maxY - 10,
                            topLeft: getAbsolutePosition.x <= shape.minX + 10 &&
                              getAbsolutePosition.y <= shape.minY + 10,
                            topRight: getAbsolutePosition.x >= shape.maxX - 10 &&
                              getAbsolutePosition.y <= shape.minY + 10,
                            bottomRight: getAbsolutePosition.x >= shape.maxX - 10 &&
                              getAbsolutePosition.y >= shape.maxY - 10

                        };
                        if (objectLocatedAt.horizontal) {
                            if (pos.x <= shape.maxX &&
                              getAbsolutePosition.x >= shape.maxX - 10) {
                                if (x_value == pos.x) {
                                    x_value = shape.maxX;
                                }
                                else {
                                    x_value = Math.max(shape.maxX, x_value);
                                }
                            }
                            if (pos.x >= shape.minX &&
                              getAbsolutePosition.x <= shape.minX + 10) {
                                if (x_value == pos.x) {
                                    x_value = shape.minX;
                                }
                                else {
                                    x_value = Math.min(shape.minX, x_value);
                                }
                            }
                        }
                        if (objectLocatedAt.vertical) {
                            if (pos.y <= shape.maxY &&
                              getAbsolutePosition.y >= shape.maxY -10) {
                                if (y_value == pos.y) {
                                    y_value = shape.maxY;
                                }
                                else {
                                    y_value = Math.max(shape.maxY, y_value);
                                }
                            }

                            if (pos.y >= shape.minY &&
                              getAbsolutePosition.y <= 10 + shape.minY) {
                                if (y_value == pos.y) {
                                    y_value = shape.minY;
                                }
                                else {
                                    y_value = Math.min(shape.minY, y_value);
                                }
                            }
                        }
                        var delta = 15;
                        if (pos.x >= shape.minX + delta &&
                          pos.y <= shape.maxY - delta &&
                          objectLocatedAt.bottomLeft
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.minX;
                            }
                            else {
                                x_value = Math.min(shape.minX, x_value);
                            }

                        }
                        if (pos.x >= shape.minX + delta &&
                          pos.y >= shape.minY + delta &&
                          objectLocatedAt.topLeft
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.minX;
                            }
                            else {
                                x_value = Math.min(shape.minX, x_value);
                            }

                        }
                        if (pos.x <= shape.maxX - delta &&
                          pos.y >= shape.minY + delta &&
                          objectLocatedAt.topRight
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.maxX;
                            }
                            else {
                                x_value = Math.max(shape.maxX, x_value);
                            }

                        }
                        if (pos.x <= shape.maxX - delta &&
                          pos.y <= shape.maxY - delta &&
                          objectLocatedAt.bottomRight
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.maxX;
                            }
                            else {
                                x_value = Math.max(shape.maxX, x_value);
                            }

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
    
    
    rasterObj.onload = function() {
        
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX = iaScene.scale * detail.width / this.width;
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY = iaScene.scale * detail.height / this.height;        

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
        }
        

        that.addEventsManagement(i, that, iaScene, baseImage, idText);
        
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
    that.xiaDetail[i] = new XiaDetail(detail, idText);

    that.xiaDetail[i].path = detail.path;
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
        draggable : that.xiaDetail[i].draggable_object
    });
    that.layer.add(that.xiaDetail[i].kineticElement);
    that.xiaDetail[i].kineticElement.setIaObject(that);
    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    that.xiaDetail[i].kineticElement.tooltip = "";


    var collision_state = $("#" + idText).data("collisions");
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        collision_state = "off";
    }
    that.collisions = collision_state;


    if(that.xiaDetail[i].connectionStart) {
        that.xiaDetail[i].kineticElement.moveToBottom();
        that.xiaDetail[i].connectorStart = that.xiaDetail[i].kineticElement.getStage().find(that.xiaDetail[i].connectionStart)[0];
        that.xiaDetail[i].connectorEnd = that.xiaDetail[i].kineticElement.getStage().find(that.xiaDetail[i].connectionEnd)[0];
        that.xiaDetail[i].connectorStart.getXiaParent().addObserver(that.xiaDetail[i]);
        that.xiaDetail[i].connectorEnd.getXiaParent().addObserver(that.xiaDetail[i]);
        detail.fill = "#ffffff";
        if (that.xiaDetail[i].stroke) {
            that.xiaDetail[i].kineticElement.stroke(that.xiaDetail[i].stroke);
        }
        else {
            that.xiaDetail[i].kineticElement.stroke("black");
        }
        if (that.xiaDetail[i].strokeWidth) {
            that.xiaDetail[i].kineticElement.strokeWidth(that.xiaDetail[i].strokeWidth);
        }
        else {
            that.xiaDetail[i].kineticElement.strokeWidth(5);
        }
    }

    var global_collision_state = $("#message_success").data("collisions");

    if (global_collision_state == "on" && collision_state != "off") {


        that.xiaDetail[i].kineticElement.dragBoundFunc(function(pos) {
            pos.x = pos.x + this.getXiaParent().delta.x;
            pos.y = pos.y + this.getXiaParent().delta.y;
            var x_value = pos.x;
            var y_value = pos.y;
            var len = iaScene.shapes.length;
            var getAbsolutePosition = {
                x : this.getAbsolutePosition().x + this.getXiaParent().delta.x,
                y : this.getAbsolutePosition().y + this.getXiaParent().delta.y
            }

            var objectWidth = this.getXiaParent().maxX - this.getXiaParent().minX;
            var objectHeight = this.getXiaParent().maxY - this.getXiaParent().minY;
            for(var i=0; i< len; i++) {
                if (that != iaScene.shapes[i] && iaScene.shapes[i].collisions == "on") {

                    for (var j=0; j< iaScene.shapes[i].xiaDetail.length;j++) {
                        var shape = {
                            maxX : iaScene.shapes[i].xiaDetail[j].maxX,
                            maxY : iaScene.shapes[i].xiaDetail[j].maxY,
                            minX : iaScene.shapes[i].xiaDetail[j].minX - objectWidth,
                            minY : iaScene.shapes[i].xiaDetail[j].minY - objectHeight
                        };

                        var objectLocatedAt = {
                            horizontal: (getAbsolutePosition.y < shape.maxY - 10) &&
                              (getAbsolutePosition.y > shape.minY + 10),
                            vertical: (getAbsolutePosition.x < shape.maxX - 10) &&
                              (getAbsolutePosition.x > shape.minX + 10),
                            bottomLeft: getAbsolutePosition.x <= shape.minX + 10 &&
                              getAbsolutePosition.y >= shape.maxY - 10,
                            topLeft: getAbsolutePosition.x <= shape.minX + 10 &&
                              getAbsolutePosition.y <= shape.minY + 10,
                            topRight: getAbsolutePosition.x >= shape.maxX - 10 &&
                              getAbsolutePosition.y <= shape.minY + 10,
                            bottomRight: getAbsolutePosition.x >= shape.maxX - 10 &&
                              getAbsolutePosition.y >= shape.maxY - 10

                        };
                        if (objectLocatedAt.horizontal) {
                            if (pos.x <= shape.maxX &&
                              getAbsolutePosition.x >= shape.maxX - 10) {
                                if (x_value == pos.x) {
                                    x_value = shape.maxX;
                                }
                                else {
                                    x_value = Math.max(shape.maxX, x_value);
                                }
                            }
                            if (pos.x >= shape.minX &&
                              getAbsolutePosition.x <= shape.minX + 10) {
                                if (x_value == pos.x) {
                                    x_value = shape.minX;
                                }
                                else {
                                    x_value = Math.min(shape.minX, x_value);
                                }
                            }
                        }
                        if (objectLocatedAt.vertical) {
                            if (pos.y <= shape.maxY &&
                              getAbsolutePosition.y >= shape.maxY -10) {
                                if (y_value == pos.y) {
                                    y_value = shape.maxY;
                                }
                                else {
                                    y_value = Math.max(shape.maxY, y_value);
                                }
                            }

                            if (pos.y >= shape.minY &&
                              getAbsolutePosition.y <= 10 + shape.minY) {
                                if (y_value == pos.y) {
                                    y_value = shape.minY;
                                }
                                else {
                                    y_value = Math.min(shape.minY, y_value);
                                }
                            }
                        }
                        var delta = 15;
                        if (pos.x >= shape.minX + delta &&
                          pos.y <= shape.maxY - delta &&
                          objectLocatedAt.bottomLeft
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.minX;
                            }
                            else {
                                x_value = Math.min(shape.minX, x_value);
                            }

                        }
                        if (pos.x >= shape.minX + delta &&
                          pos.y >= shape.minY + delta &&
                          objectLocatedAt.topLeft
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.minX;
                            }
                            else {
                                x_value = Math.min(shape.minX, x_value);
                            }

                        }
                        if (pos.x <= shape.maxX - delta &&
                          pos.y >= shape.minY + delta &&
                          objectLocatedAt.topRight
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.maxX;
                            }
                            else {
                                x_value = Math.max(shape.maxX, x_value);
                            }

                        }
                        if (pos.x <= shape.maxX - delta &&
                          pos.y <= shape.maxY - delta &&
                          objectLocatedAt.bottomRight
                            ) {

                            if (x_value == pos.x) {
                                x_value = shape.maxX;
                            }
                            else {
                                x_value = Math.max(shape.maxX, x_value);
                            }

                        }
                    }
                }
            }

            return {
              x: x_value - this.getXiaParent().delta.x,
              y: y_value - this.getXiaParent().delta.y
            };

        });

    }

    that.definePathBoxSize(detail, that.xiaDetail[i]);
    that.scaleBox(that.xiaDetail[i], iaScene);
    that.xiaDetail[i].lastDragPos.x = that.xiaDetail[i].kineticElement.x();
    that.xiaDetail[i].lastDragPos.y = that.xiaDetail[i].kineticElement.y();
    that.xiaDetail[i].delta = {
        x:that.xiaDetail[i].minX - that.xiaDetail[i].kineticElement.x(),
        y:that.xiaDetail[i].minY - that.xiaDetail[i].kineticElement.y()
    };
    // crop background image to suit shape box

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
        if (cropWidth <= 0) cropWidth = 1;
        if (cropHeight <= 0) cropHeight = 1;
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

    that.xiaDetail[i].persistent = "off";
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#ffffff")) {
        that.xiaDetail[i].persistent = "onPath";
        that.xiaDetail[i].kineticElement.fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
    }    
    that.addEventsManagement(i, that, iaScene, baseImage, idText);

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
        that.minY = parseFloat(detail.y);
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
   
IaObject.prototype.addEventsManagement = function(i, that, iaScene, baseImage, idText) {

    var that=this;

    that.xiaDetail[i].kineticElement.tooltip_area = false;
    // tooltip must be at the bottom
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.xiaDetail[i].kineticElement.moveToBottom();
        that.xiaDetail[i].kineticElement.tooltip_area = true;
        that.xiaDetail[i].options += " disable-click ";
    }

    that.myhooks.afterXiaObjectCreation(iaScene, that.xiaDetail[i]);

    that.xiaDetail[i].kineticElement.on('mouseenter', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            if ((!this.getXiaParent().droparea) && (!this.tooltip_area)  &&
               (this.getXiaParent().options.indexOf("disable-click") == -1)) {
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
    
    if (that.xiaDetail[i].options.indexOf("direct-link") != -1) {
        that.xiaDetail[i].kineticElement.on('click touchstart', function(e) {
            //location.href = that.title[i];
            location.href = that.xiaDetail[i].title;
        });
    }
    else if (that.xiaDetail[i].options.indexOf("disable-click") != -1) {
        return;
    }
    else {

        if (!that.xiaDetail[i].droparea) {
            that.xiaDetail[i].kineticElement.on('dragstart', function(e) {
                iaScene.element = that;
                that.afterDragStart(iaScene, idText, this);
                that.myhooks.afterDragStart(iaScene, idText, this);
                this.moveToTop();
                Kinetic.draggedshape = this;
            });

            that.xiaDetail[i].kineticElement.on('dragend', function(e) {
                iaScene.element = that;

                Kinetic.draggedshape = null;
                // Kinetic hacking - speed up _getIntersection (for linux)
                var all_elements = this.getIaObject().xiaDetail;
                for (var i = 0;i < all_elements.length;i++) {

                    var target_id = all_elements[i].kineticElement.getXiaParent().target_id;
                    var target_object = all_elements[i].kineticElement.getStage().find("#" + target_id);
                    if (target_object instanceof Kinetic.Group) {
                        var xiaDetailsTarget = target_object.getIaObject.xiaDetail;
                        for (var j=0;j < xiaDetailsTarget.length;j++) {
                            e.target = all_elements[i].kineticElement;
                            that.afterDragEnd(iaScene, all_elements[i].idText, e, all_elements[i].kineticElement, xiaDetailsTarget[j]);
                            that.afterDragEnd(iaScene, all_elements[i].idText, e, all_elements[i].kineticElement);
                            that.myhooks.afterDragEnd(iaScene, all_elements[i].idText, all_elements[i].kineticElement);
                        }
                    }
                    else {
                        e.target = all_elements[i].kineticElement;
                        var target_id = all_elements[i].kineticElement.getXiaParent().target_id;
                        var target_object = all_elements[i].kineticElement.getStage().find("#" + target_id);
                        that.afterDragEnd(iaScene, all_elements[i].idText, e, all_elements[i].kineticElement, target_object);
                        that.myhooks.afterDragEnd(iaScene, all_elements[i].idText, all_elements[i].kineticElement);
                    }
                }

                this.getStage().completeImage = "redefine";

                that.layer.draw();
            });
            //if (that.xiaDetail[i].connectionStart) {
                that.xiaDetail[i].kineticElement.on('dragmove', function(e) {
                    var other_elements = this.getIaObject().xiaDetail;
                    if (other_elements.length > 1) {
                        var delta = {x:this.x() - this.getXiaParent().lastDragPos.x,
                            y:this.y() - this.getXiaParent().lastDragPos.y};
                        for (var i=0;i<other_elements.length;i++) {
                            if (other_elements[i].kineticElement != this) {
                                other_elements[i].kineticElement.move(delta);
                                other_elements[i].lastDragPos.x = other_elements[i].kineticElement.x();
                                other_elements[i].lastDragPos.y = other_elements[i].kineticElement.y();
                            }
                        }
                        this.getXiaParent().lastDragPos.x = this.x();
                        this.getXiaParent().lastDragPos.y = this.y();
                    }
                    this.getXiaParent().notify();
                    this.drawScene();
                });
            //}
        }
    }

};

IaObject.prototype.afterDragStart = function(iaScene, idText, kineticElement) {

    $('#' + idText + " audio").each(function(){
        if ($(this).data("state") === "autostart") {
            $(this)[0].play();
        }
    });
};
/*
 *
 *
 */
IaObject.prototype.afterDragEnd = function(iaScene, idText, event, kineticElement, target_object) {
    //var target_id = $('#' + idText).data("target");
    var target_id = kineticElement.getXiaParent().target_id;
    var target_object = kineticElement.getStage().find("#" + target_id);
    var iaObject_width = kineticElement.getXiaParent().maxX - kineticElement.getXiaParent().minX;
    var iaObject_height = kineticElement.getXiaParent().maxY - kineticElement.getXiaParent().minY;
    kineticElement.getXiaParent().minX = event.target.x();
    kineticElement.getXiaParent().minY = event.target.y();
    kineticElement.getXiaParent().maxX = event.target.x() + iaObject_width;
    kineticElement.getXiaParent().maxY = event.target.y() + iaObject_height;
    var middle_coords = {
      x: event.target.x() + (kineticElement.getXiaParent().maxX - kineticElement.getXiaParent().minX)/2,
      y:event.target.y() + (kineticElement.getXiaParent().maxY - kineticElement.getXiaParent().minY)/2
    };

    //var mouseXY = kineticElement.getStage().getPointerPosition();
    //var droparea = kineticElement.getStage().getIntersection(mouseXY);
    var droparea = kineticElement.getStage().getIntersection(middle_coords);
    var over_droparea = false;
    if (droparea) {
        if (droparea == kineticElement) {
            // element dropped on its own area
            // move current element out of stage, redraw the scene,
            // find the drop zone element
            // and move current element to its original position
            var old_x = kineticElement.x();
            kineticElement.x(2000);
            kineticElement.getXiaParent().notify();
            kineticElement.getLayer().drawHit();
            kineticElement.getStage().completeImage = "redefine";
            //droparea = kineticElement.getStage().getIntersection(mouseXY);
            droparea = kineticElement.getStage().getIntersection(middle_coords);
            if (droparea) {
                if (droparea != kineticElement) {
                    over_droparea = true;
                }
            }
            kineticElement.x(old_x);
            kineticElement.getXiaParent().notify();
            kineticElement.getLayer().drawHit();
        }
        else if (droparea.getXiaParent().droparea) {
            over_droparea = true;
        }
    }

    if (over_droparea) {
        // retrieve kineticElement drop zone
        // if center of dropped element is located in the drop zone
        // then drop !
        //var target_object = this.xiaDetail[0].kineticElement.getStage().find("#" + target_id);
        var target_iaObject = droparea.getXiaParent();
        if ((middle_coords.x > target_iaObject.minX) &
                (middle_coords.x < target_iaObject.maxX) &
                (middle_coords.y > target_iaObject.minY) &
                (middle_coords.y < target_iaObject.maxY)) {
            if (!this.match && droparea == target_object[0]) {
                this.match = true;
                iaScene.currentScore += 1;
            }
            if (iaScene.global_magnet_enabled || droparea.getXiaParent().magnet_state=="on") {
                kineticElement.x(target_iaObject.minX - (iaObject_width / 2) + (target_iaObject.maxX - target_iaObject.minX) / 2);
                kineticElement.y(target_iaObject.minY - (iaObject_height / 2) + (target_iaObject.maxY - target_iaObject.minY) / 2);
            }
        }
        else {
            if (this.match) {
                this.match = false;
                iaScene.currentScore -= 1;
            }
        }
        kineticElement.getXiaParent().notify();
        kineticElement.drawScene();
        if (droparea.getXiaParent().options.indexOf("direct-link") != -1) {
            location.href = droparea.getXiaParent().title;
        }

        var viewportHeight = $(window).height();
        if ((iaScene.score == iaScene.currentScore) && (iaScene.score != 0)) {
            $("#content").show();
            $("#message_success").show();
            var general_border = $("#message_success").css("border-top-width").substr(0,$("#message_success").css("border-top-width").length - 2);
            var general_offset = $("#message_success").offset();
            var content_offset = $("#content").offset();
            $("#message_success").css({'max-height':(viewportHeight - general_offset.top - content_offset.top - 2 * general_border)});
        }
        $('#' + idText + " audio").each(function(){
            if ($(this).data("state") === "autostart") {
                $(this)[0].play();
            }
        });
    }
    else {
        if (this.match) {
            this.match = false;
            iaScene.currentScore -= 1;
        }
    }
};