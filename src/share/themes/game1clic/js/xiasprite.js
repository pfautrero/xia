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
// @author : Pascal Fautrero


/*
 * 
 */
class XiaSprite extends XiaDetail {

    constructor(parent, idText){
        super(parent, idText)
        this.zoomable = false
        this.width = this.parent.jsonSource.width * this.parent.iaScene.scale
        this.height = this.parent.jsonSource.height * this.parent.iaScene.scale
        this.timeLine = JSON.parse("[" + this.parent.jsonSource.timeline + "]")
        this.idle = this.createTimeLine(this.timeLine)
        this.persistent = "hiddenSprite";
    }

    createTimeLine(timeLine) {
        "use strict"
        var idle = []
        for(var k = 0; k < timeLine.length; k++) {
            idle.push(timeLine[k] * this.parent.jsonSource.width, 0, this.parent.jsonSource.width, this.parent.jsonSource.height)
        }
        return idle
    }

    start() {
        var rasterObj = new Image();
        this.kineticElement = new Kinetic.Sprite({
          x: parseFloat(this.parent.jsonSource.x) * this.parent.iaScene.coeff,
          y: parseFloat(this.parent.jsonSource.y) * this.parent.iaScene.coeff + this.parent.iaScene.y,
          image: rasterObj,
          animation: 'idle',
          animations: {
            idle: this.idle,
            hidden : [
                this.timeLine.length * this.parent.jsonSource.width, 0,
                this.parent.jsonSource.width, this.parent.jsonSource.height
            ]
          },
          frameRate: this.parent.iaScene.frameRate,
          frameIndex: 0,
          scale: {x:this.parent.iaScene.coeff,y:this.parent.iaScene.coeff}
        });

        this.kineticElement.setXiaParent(this);
        this.kineticElement.setIaObject(this.parent);

        this.kineticElement.backgroundImage = rasterObj;
        this.kineticElement.tooltip = "";
        this.kineticElement.droparea = false;
        this.kineticElement.tooltip_area = false;

        var that = this
        rasterObj.onload = function() {

            that.kineticElement.backgroundImageOwnScaleX = that.parent.iaScene.scale * that.parent.jsonSource.width / that.width;
            that.kineticElement.backgroundImageOwnScaleY = that.parent.iaScene.scale * that.parent.jsonSource.height / that.height;

            that.parent.group.add(that.kineticElement);

            that.imgData = []
            for (var k = 0; k < Math.max.apply(null, that.timeLine) + 1; k++) {
                var canvas_source = document.createElement('canvas')
                canvas_source.setAttribute('width', that.parent.jsonSource.width)
                canvas_source.setAttribute('height', that.parent.jsonSource.height)
                var context_source = canvas_source.getContext('2d')

                context_source.drawImage(
                    rasterObj,
                    that.parent.jsonSource.width * k,
                    0,
                    that.parent.jsonSource.width,
                    that.parent.jsonSource.height,
                    0,
                    0,
                    that.parent.jsonSource.width,
                    that.parent.jsonSource.height
                )

                //document.body.appendChild(canvas_source)
                that.imgData[k] = context_source.getImageData(0,0,canvas_source.width,canvas_source.height)
            }

            that.kineticElement.animation('hidden')
            that.kineticElement.start();
            if ((typeof(that.parent.jsonSource.fill) !== 'undefined') &&
                (that.parent.jsonSource.fill == "#ffffff")) {
                that.persistent = "persistentSprite";
                that.kineticElement.animation('idle')
             }
            //that.parent.addEventsManagement(i,that.zoomable, that.parent, that.parent.iaScene, that.parent.baseImage, that.idText);
            that.manageDropAreaAndTooltips()
            that.parent.group.draw()
            var hitCanvas = that.parent.layer.getHitCanvas();
            that.parent.iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));
        };
        rasterObj.src = this.parent.jsonSource.image;

    }


}
