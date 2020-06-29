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

    constructor(parent, detail, idText){
        super(parent, detail, idText)
        this.zoomable = false
        this.width = this.parent.jsonSource.width * this.parent.iaScene.scale
        this.height = this.parent.jsonSource.height * this.parent.iaScene.scale
        this.timeLine = JSON.parse("[" + this.parent.jsonSource.timeline + "]")
        this.frames = JSON.parse(this.detail.frames.replace(/'/g, '"')) // replacement fixes xiapy weird json encoding 
        this.persistent = "hiddenSprite";
    }

    createTimeLine(timeLine, ratioRaster) {
        "use strict"
        var idle = []
        for(var k = 0; k < timeLine.length; k++) {
            idle.push(timeLine[k] * this.parent.jsonSource.width * ratioRaster, 0, this.parent.jsonSource.width * ratioRaster, this.parent.jsonSource.height * ratioRaster)
        }
        return idle
    }

    frameChange () {
        this.kineticElement.x(this.frames[this.kineticElement.frameIndex()]['x'] *  this.parent.iaScene.coeff)
        this.kineticElement.y(this.frames[this.kineticElement.frameIndex()]['y'] *  this.parent.iaScene.coeff)
    }

    start() {
        var rasterObj = new Image();
        //var that = this
        rasterObj.onload = function() {

          var ratioRaster = rasterObj.naturalHeight / this.parent.jsonSource.height
          this.idle = this.createTimeLine(this.timeLine, ratioRaster)
          this.kineticElement = new Kinetic.Sprite({
            x: parseFloat(this.parent.jsonSource.x) * this.parent.iaScene.coeff,
            y: parseFloat(this.parent.jsonSource.y) * this.parent.iaScene.coeff + this.parent.iaScene.y,
            image: rasterObj,
            animation: 'idle',
            animations: {
              idle: this.idle,
              hidden : [
                  this.timeLine.length * this.parent.jsonSource.width * ratioRaster, 0,
                  this.parent.jsonSource.width * ratioRaster, this.parent.jsonSource.height * ratioRaster
              ]
            },
            frameRate: this.parent.iaScene.frameRate,
            frameIndex: 0,
            scale: {x:this.parent.iaScene.coeff / ratioRaster,y:this.parent.iaScene.coeff / ratioRaster}
          });

          this.kineticElement.setXiaParent(this);
          this.kineticElement.setIaObject(this.parent);

          this.kineticElement.backgroundImage = rasterObj;
          this.tooltip = "";
          this.kineticElement.droparea = false;
          this.kineticElement.tooltip_area = false;

          this.kineticElement.backgroundImageOwnScaleX = this.parent.iaScene.scale * this.parent.jsonSource.width / this.width;
          this.kineticElement.backgroundImageOwnScaleY = this.parent.iaScene.scale * this.parent.jsonSource.height / this.height;

          this.parent.group.add(this.kineticElement);

          this.imgData = []
          for (var k = 0; k < Math.max.apply(null, this.timeLine) + 1; k++) {
              var canvas_source = document.createElement('canvas')
              canvas_source.setAttribute('width', this.parent.jsonSource.width * ratioRaster)
              canvas_source.setAttribute('height', this.parent.jsonSource.height * ratioRaster)
              var context_source = canvas_source.getContext('2d')

              context_source.drawImage(
                  rasterObj,
                  this.parent.jsonSource.width * k,
                  0,
                  this.parent.jsonSource.width,
                  this.parent.jsonSource.height,
                  0,
                  0,
                  this.parent.jsonSource.width,
                  this.parent.jsonSource.height
              )

              //document.body.appendChild(canvas_source)
              this.imgData[k] = context_source.getImageData(0,0,canvas_source.width,canvas_source.height)
          }

          this.kineticElement.animation('hidden')
          this.kineticElement.start();
          if ((typeof(this.parent.jsonSource.fill) !== 'undefined') &&
              (this.parent.jsonSource.fill == "#ffffff")) {
              this.persistent = "persistentSprite";
              this.kineticElement.animation('idle')
           }
          //this.parent.addEventsManagement(i,this.zoomable, this.parent, this.parent.iaScene, this.parent.baseImage, this.idText);
          this.manageDropAreaAndTooltips()
          this.kineticElement.on('frameIndexChange', this.frameChange.bind(this))
          this.parent.group.draw()
          var hitCanvas = this.parent.layer.getHitCanvas();
          this.parent.iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));
        }.bind(this)
        rasterObj.src = this.parent.jsonSource.image;

    }
}
if (typeof module !== 'undefined' && module.exports != null) {
     exports.XiaSprite = XiaSprite
}
