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
class XiaImage extends XiaDetail {

    constructor(parent, detail, idText) {
        "use strict";
        super(parent, detail, idText)

    }

    start() {

        var rasterObj = new Image()

        this.kineticElement = new Kinetic.Image({
            id: this.detail.id,
            name: this.detail.title,
            x: parseFloat(this.detail.x) * this.parent.mainScene.coeff,
            y: parseFloat(this.detail.y) * this.parent.mainScene.coeff + this.parent.mainScene.y,
            width: this.detail.width,
            height: this.detail.height,
            draggable: this.draggable_object

        });

        this.parent.layer.add(this.kineticElement)
        this.kineticElement.setXiaParent(this)
        this.kineticElement.setIaObject(this.parent)
        this.backgroundImage = rasterObj
        this.kineticElement.tooltip = ""
        this.lastDragPos.x = this.kineticElement.x()
        this.lastDragPos.y = this.kineticElement.y()
        this.originalCoords.x = this.kineticElement.x()
        this.originalCoords.y = this.kineticElement.y()

        var collision_state = $("#" + this.idText).data("collisions")
        if ($('article[data-target="' + $("#" + this.idText).data("kinetic_id") + '"]').length != 0) {
            collision_state = "off"
        }
        if ($('article[data-tooltip="' + $("#" + this.idText).data("kinetic_id") + '"]').length != 0) {
            collision_state = "off"
        }
        this.collisions = collision_state
        var global_collision_state = $("#message_success").data("collisions");
        if (global_collision_state == "on" && collision_state != "off") {
            this.kineticElement.dragBoundFunc(function(pos) {
                var XiaElements = this.getIaObject().xiaDetail
                var delta = {x : 0, y : 0}
                var coords = {x : 0, y : 0}
                var delta_tmp = 0
                for (var i = 0;i < XiaElements.length; i++) {
                    coords = this.getXiaParent().dragCollisions(
                        {
                            x:pos.x - this.x() + XiaElements[i].kineticElement.x(),
                            y:pos.y - this.y() + XiaElements[i].kineticElement.y()
                        },
                        XiaElements[i].kineticElement
                    );
                    delta_tmp = coords.x - (pos.x - this.x() + XiaElements[i].kineticElement.x());
                    if (delta_tmp != 0) {
                        delta.x = Math.sign(delta_tmp) * Math.max(Math.abs(delta.x), Math.abs(delta_tmp))
                    }
                    delta_tmp = coords.y - (pos.y - this.y() + XiaElements[i].kineticElement.y())
                    if (delta_tmp != 0) {
                        delta.y = Math.sign(delta_tmp) * Math.max(Math.abs(delta.y), Math.abs(delta_tmp))
                    }
                }
                return {
                    x: delta.x + (pos.x),
                    y: delta.y + (pos.y)

                }
            })
        }

        var that = this
        rasterObj.onload = function() {

            that.kineticElement.backgroundImageOwnScaleX = that.parent.mainScene.scale * that.detail.width / this.width
            that.kineticElement.backgroundImageOwnScaleY = that.parent.mainScene.scale * that.detail.height / this.height

            if ($('article[data-tooltip="' + $("#" + that.idText).data("kinetic_id") + '"]').length == 0) {
                that.detail.fill = '#ffffff';    // force image to be displayed - must refactor if it is a good idea !
            }
            that.persistent = "off"
            if ((typeof(that.detail.fill) !== 'undefined') &&
                (that.detail.fill === "#ffffff")) {
                that.persistent = "onImage"
                that.kineticElement.fillPriority('pattern')
                that.kineticElement.fillPatternScaleX(that.kineticElement.backgroundImageOwnScaleX * 1 / that.parent.mainScene.scale)
                that.kineticElement.fillPatternScaleY(that.kineticElement.backgroundImageOwnScaleY * 1 / that.parent.mainScene.scale)
                that.kineticElement.fillPatternImage(that.backgroundImage)
            }

            that.addEventsManagement(that, that.parent.mainScene, that.idText);

            // define hit area excluding transparent pixels
            // =============================================================
            that.rasterObj = rasterObj;

            that.kineticElement.cache();
            that.kineticElement.scale(
                {
                    x : that.parent.mainScene.coeff,
                    y : that.parent.mainScene.coeff
                }
            )
            that.kineticElement.drawHitFromCache()
            that.kineticElement.draw()
        };

        rasterObj.src = this.detail.image


    }

}

if (typeof module !== 'undefined' && module.exports != null) {
    exports.XiaImage = XiaImage
}