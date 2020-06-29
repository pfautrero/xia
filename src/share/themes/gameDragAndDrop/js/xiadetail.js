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
// @author : pascal.fautrero@gmail.com


/*
 * XiaDetail is a wrapper of a Kinetic Node to store xia specific informations
 */
class XiaDetail {

    constructor(parent, detail, idText) {
        "use strict";

        // observers are used to manage lines connectors
        this.observers = new ObserverList();
        this.title = detail.title;
        this.parent = parent
        this.detail = detail
        this.onfailreturn = false;
        this.path = "";
        this.kineticElement = null;
        this.persistent = "";
        this.options = "";
        this.backgroundImage = null;
        this.tooltip = "";
        this.draggable_object = true;
        this.target_id = null;
        this.magnet_state = null;
        this.droparea = false;
        this.idText = idText;
        // if this detail is a connector line, keep references to the start object and the end object
        this.connectionStart = null;
        this.connectionEnd = null;
        this.connectorStart = null;
        this.connectorEnd = null;
        this.style= "";
        this.stroke=null;
        this.strokeWidth=null;
        this.lastDragPos = {x:0, y:0};
        // used to force details to go home if onfailreturn is specified when dropped onwrong drop area
        this.originalCoords = {x:0,y:0};
        this.minX = 10000;
        this.minY = 10000;
        this.maxX = -10000;
        this.maxY = -10000;
        // match is used to know if current detail has been dropped over the right drop area
        this.match = false;
        // delta is used to remember delta between real coordinates and min,max ones. (only useful for paths)
        this.delta = {x:0, y:0};

        // retrieve options
        if ((typeof(this.detail.options) !== 'undefined')) {
            this.options = this.detail.options
        }

        var onfail_state = $("#" + idText).data("onfail");
        if (onfail_state == "return") {
            this.onfailreturn = true
        }
        // retrieve styles
        if ((typeof(detail.style) !== 'undefined')) {
            this.style = detail.style;
            var stroke = this.style.match("stroke:(.*?);")
            if (stroke) this.stroke = stroke[1];

            var strokeWidth = this.style.match("stroke-width:(.*?);")
            if (strokeWidth) this.strokeWidth = strokeWidth[1]
        }

        // retrieve connection if exists
        if ((typeof(detail.connectionStart) !== 'undefined')) {
            this.connectionStart = detail.connectionStart;
            this.connectionEnd = detail.connectionEnd;
            this.options += " disable-click ";
        }

        if (this.options.indexOf("disable-click") != -1) {
            this.draggable_object = false
        }
        if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
            this.draggable_object = false
        }
        if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
            this.draggable_object = false
        }

        this.target_id = $('#' + idText).data("target")
        this.magnet_state = $("#" + idText).data("magnet")

        if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
            this.droparea = true;

        }


    }
    addObserver(observer) {
        this.observers.add( observer )
    }
    removeObserver(observer) {
        this.observers.removeAt( this.observers.indexOf( observer, 0 ) )
    }
    notify() {
        var observerCount = this.observers.count();
        for(var i=0; i < observerCount; i++){
            this.observers.get(i).update();
        }
    }
    update() {
        // redraw connector
        var coeff = (1/this.kineticElement.getIaObject().mainScene.coeff);
        xStart = this.connectorStart.x() * coeff+ this.connectorStart.width() / 2;
        yStart = this.connectorStart.y() * coeff+ this.connectorStart.height() / 2;
        xEnd = this.connectorEnd.x() * coeff + this.connectorEnd.width() / 2;
        yEnd = this.connectorEnd.y() * coeff + this.connectorEnd.height() / 2;

        this.kineticElement.data("M" + (xStart) + "," + (yStart) + " " + (xEnd) + "," + (yEnd) + " z");

    }

    addEventsManagement(that, iaScene, idText) {

        //var that=this;

        this.kineticElement.tooltip_area = false;
        // tooltip must be at the bottom
        this.parent.myhooks.afterXiaObjectCreation(iaScene, this)

        if ($('article[data-tooltip="' + $("#" + this.idText).data("kinetic_id") + '"]').length != 0) {
            this.kineticElement.moveToBottom();
            this.kineticElement.tooltip_area = true;
            this.options += " disable-click ";
            return
        }

        this.kineticElement.on('mouseenter touchstart', function() {
            if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

            }
            else if (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) {

            }
            else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
                if ((!this.kineticElement.getXiaParent().droparea) && (!this.tooltip_area)  &&
                   (this.kineticElement.getXiaParent().options.indexOf("disable-click") == -1)) {
                    document.body.style.cursor = "pointer";
                }
                iaScene.cursorState = "url(img/HandPointer.cur),auto";
                // manage tooltips if present
                var tooltip = false;
                if (this.tooltip !== "") {
                    tooltip = true;
                }
                else if ($("#" + idText).data("tooltip") != "") {
                    var tooltip_id = $("#" + idText).data("tooltip");
                    this.tooltip = this.kineticElement.getStage().find("#" + tooltip_id)[0];
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
                    this.kineticElement.getIaObject().layer.draw();
                }

            }
        }.bind(this));

        this.kineticElement.on('click touchstart', function(e) {

          $('#' + idText + " audio").each(function(){
              if ($(this).data("state") === "autostart") {
                  $(this)[0].play();
              }
          });

        });

        /*
         * if we leave this element, just clear the scene
         */
        this.kineticElement.on('mouseout', function() {
            if ((iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) ||
              (iaScene.cursorState.indexOf("ZoomIn.cur") !== -1)){
            }
            else {
              var mouseXY = this.kineticElement.getIaObject().layer.getStage().getPointerPosition();
              if ((this.kineticElement.getIaObject().layer.getStage().getIntersection(mouseXY) != this)) {
                // manage tooltips if present
                var tooltip = false;
                if (this.tooltip != "") {
                    tooltip = true;
                }
                else if ($("#" + idText).data("tooltip") != "") {
                    var tooltip_id = $("#" + idText).data("tooltip");
                    this.tooltip = this.kineticElement.getStage().find("#" + tooltip_id)[0];
                    tooltip = true;
                }
                if (tooltip) {
                    this.tooltip.fillPriority('color');
                    this.tooltip.fill('rgba(0, 0, 0, 0)');
                    this.tooltip.moveToBottom();
                    this.tooltip.draw();
                }
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                this.kineticElement.getIaObject().layer.draw();
              }
            }
        }.bind(this));


        if (this.options.indexOf("disable-click") != -1) {
            return;
        }
        else {
            if (this.options.indexOf("direct-link") != -1) {
                this.kineticElement.on('mouseup touchend', function(e) {
                    //location.href = that.title[i];
                    location.href = this.title;
                }.bind(this));
            }

            if (!this.droparea) {
                this.kineticElement.on('dragstart', function(e) {
                    if (this.getXiaParent().type == "sprite") this.stop()
                    iaScene.element = this.getIaObject()
                    this.fire("click")
                    this.getIaObject().afterDragStart(iaScene, idText, this);
                    this.getIaObject().myhooks.afterDragStart(iaScene, idText, this);
                    this.moveToTop();
                    Kinetic.draggedshape = this;
                });

                this.kineticElement.on('dragend', function(e) {
                    
                    iaScene.element = this.getIaObject()

                    Kinetic.draggedshape = null;

                    var match = false
                    var onfailreturn = false
                    var all_elements = this.getIaObject().xiaDetail
                    for (var i = 0;i < all_elements.length;i++) {

                        var target_id = all_elements[i].kineticElement.getXiaParent().target_id
                        var target_object = this.getStage().find("#" + target_id)[0]
                        if (target_object instanceof Kinetic.Group) {
                            var xiaDetailsTarget = target_object.getIaObject().xiaDetail
                            for (var j=0;j < xiaDetailsTarget.length;j++) {
                                e.target = all_elements[i].kineticElement
                                this.getIaObject().afterDragEnd(iaScene, all_elements[i].idText, e, all_elements[i].kineticElement, xiaDetailsTarget[j])
                                this.getIaObject().myhooks.afterDragEnd(iaScene, all_elements[i].idText, all_elements[i].kineticElement)
                            }
                        }
                        else {
                            e.target = all_elements[i].kineticElement
                            var target_id = all_elements[i].kineticElement.getXiaParent().target_id
                            var target_object = all_elements[i].kineticElement.getStage().find("#" + target_id)
                            if (typeof(target_object[0]) != "undefined") {
                                var targetObj = target_object[0].getXiaParent()
                            }
                            else {
                                var targetObj = null
                            }
                            this.getIaObject().afterDragEnd(iaScene, all_elements[i].idText, e, all_elements[i].kineticElement, targetObj)
                            this.getIaObject().myhooks.afterDragEnd(iaScene, all_elements[i].idText, all_elements[i].kineticElement)
                        }
                        if (all_elements[i].match) match = true
                        if (all_elements[i].onfailreturn) onfailreturn = true
                    }
                    if (this.getXiaParent().type == "sprite") {
                        let coeff = this.getXiaParent().parent.mainScene.coeff
                        let translate = {
                            'x': (this.getXiaParent().frames[0]['x'] *  coeff - this.x()) / coeff,
                            'y': (this.getXiaParent().frames[0]['y'] *  coeff - this.y()) / coeff
                        }
                        for (let k = 0; k < this.getXiaParent().frames.length; k++) {
                            this.getXiaParent().frames[k]['x'] = this.getXiaParent().frames[k]['x'] - translate['x']
                            this.getXiaParent().frames[k]['y'] = this.getXiaParent().frames[k]['y'] - translate['y']
                        }
                        this.start()
                    }

                    // force draggable shape to come back home if option onfailreturn is active
                    if (!match && onfailreturn) {
                        var XiaDetails = this.getIaObject().xiaDetail;
                        for (var i =0; i < XiaDetails.length; i++) {
                            XiaDetails[i].kineticElement.x(XiaDetails[i].originalCoords.x);
                            XiaDetails[i].kineticElement.y(XiaDetails[i].originalCoords.y);
                            XiaDetails[i].lastDragPos.x = XiaDetails[i].originalCoords.x;
                            XiaDetails[i].lastDragPos.y = XiaDetails[i].originalCoords.y;
                            var width = XiaDetails[i].maxX - XiaDetails[i].minX;
                            var height = XiaDetails[i].maxY - XiaDetails[i].minY;
                            XiaDetails[i].minX = XiaDetails[i].kineticElement.x() - XiaDetails[i].delta.x;
                            XiaDetails[i].minY = XiaDetails[i].kineticElement.y() - XiaDetails[i].delta.y;
                            XiaDetails[i].maxX = XiaDetails[i].minX + width;
                            XiaDetails[i].maxY = XiaDetails[i].minY + height;
                            XiaDetails[i].kineticElement.getXiaParent().notify();
                            XiaDetails[i].kineticElement.drawScene();
                        }
                    }

                    // Kinetic hacking - speed up _getIntersection (for linux)
                    this.getStage().completeImage = "redefine"
                    this.getIaObject().layer.draw()
                });
                //if (this.connectionStart) {
                    this.kineticElement.on('dragmove', function(e) {
                        var other_elements = this.getIaObject().xiaDetail;
                        if (other_elements.length > 1) {
                            var delta = {x:this.x() - this.getXiaParent().lastDragPos.x,
                                y:this.y() - this.getXiaParent().lastDragPos.y};
                            for (var i=0;i<other_elements.length;i++) {
                                if (other_elements[i].kineticElement != this) {
                                    other_elements[i].kineticElement.move(delta)
                                    other_elements[i].lastDragPos.x = other_elements[i].kineticElement.x()
                                    other_elements[i].lastDragPos.y = other_elements[i].kineticElement.y()
                                }
                            }
                            this.getXiaParent().lastDragPos.x = this.x()
                            this.getXiaParent().lastDragPos.y = this.y()
                        }
                        this.getXiaParent().notify()
                        this.drawScene()
                    });
                //}
            }
        }

    }

    /*
     * Detect AABB collisions
     * @pos {object} current object expected position
     * @kineticElement dragged object
     * @returns {object} the new object position
     */
    dragCollisions(pos, kineticElement) {
        "use strict"
        var iaScene = kineticElement.getIaObject().mainScene
        var x_value = pos.x
        var y_value = pos.y
        var len = iaScene.shapes.length;
        var getAbsolutePosition = {
            x : kineticElement.getAbsolutePosition().x,
            y : kineticElement.getAbsolutePosition().y,
        }
        var objectWidth = kineticElement.getXiaParent().maxX - kineticElement.getXiaParent().minX
        var objectHeight = kineticElement.getXiaParent().maxY - kineticElement.getXiaParent().minY
        for (var i = 0; i < len; i++) {
            if (kineticElement.getIaObject() != iaScene.shapes[i] && iaScene.shapes[i].collisions == "on") {

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
                        bottomLeft: (getAbsolutePosition.x <= shape.minX + 10) &&
                          (getAbsolutePosition.y >= shape.maxY - 10),
                        topLeft: (getAbsolutePosition.x <= shape.minX + 10) &&
                          (getAbsolutePosition.y <= shape.minY + 10),
                        topRight: (getAbsolutePosition.x >= shape.maxX - 10) &&
                          (getAbsolutePosition.y <= shape.minY + 10),
                        bottomRight: (getAbsolutePosition.x >= shape.maxX - 10) &&
                          (getAbsolutePosition.y >= shape.maxY - 10)

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

    }



}

if (typeof module !== 'undefined' && module.exports != null) {
    exports.XiaDetail = XiaDetail
}
