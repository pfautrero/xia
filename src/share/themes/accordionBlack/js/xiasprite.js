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
 *
 */
class XiaSprite extends XiaDetail {

    constructor(parent, detail, idText){
        super(parent, detail, idText)
        this.width = this.detail.width * this.parent.iaScene.scale
        this.height = this.detail.height * this.parent.iaScene.scale
        this.persistent = (('fill' in this.detail) && (this.detail.fill === "#ffffff")) ? "on" : "off"
        this.path = this.detail.path
        this.tooltip = ""
        this.stroke = (('stroke' in this.detail) && (this.detail.stroke != 'none')) ? this.detail.stroke : 'rgba(0, 0, 0, 0)'
        this.strokeWidth = ('strokewidth' in this.detail) ? this.detail.strokewidth : '0'
        this.parent.group.zoomActive = 0
    }

    defineImageBoxSize() {
        if (this.parent.minX === -1) this.parent.minX = this.detail.x
        if (this.parent.maxY === 10000) this.parent.maxY = this.detail.y + this.detail.height
        if (this.parent.maxX === -1) this.parent.maxX = this.detail.x + this.detail.width
        if (this.parent.minY === 10000) this.parent.minY = this.detail.y

        if ((this.detail.x) < this.parent.minX) this.parent.minX = (this.detail.x)
        if ((this.detail.x) + (this.detail.width) > this.parent.maxX)
            this.parent.maxX = (this.detail.x) + (this.detail.width)
        if ((this.detail.y) < this.parent.minY) this.parent.minY = (this.detail.y)
        if ((this.detail.y) + (this.detail.height) > this.parent.maxY)
            this.parent.maxY = (this.detail.y) + (this.detail.height)
    }

    start() {
      this.defineImageBoxSize()
      var rasterObj = new Image();

      this.backgroundImage = rasterObj;
      var timeLine = JSON.parse("[" + this.detail.timeline + "]")

      var idle = []
      for(k=0;k<timeLine.length;k++) {
          idle.push(timeLine[k] * detail.width, 0, detail.width, detail.height)
      }
      this.kineticElement = new Konva.Sprite({
        x: this.detail.x * this.parent.iaScene.coeff,
        y: this.detail.y * this.parent.iaScene.coeff + this.parent.iaScene.y,
        image: this.backgroundImage,
        animation: 'idle',
        animations: {
          idle: idle,
          hidden : [timeLine.length * this.parent.detail.width, 0, this.parent.detail.width, this.parent.detail.height]
        },
        frameRate: 10,
        frameIndex: 0,
        scale: {x:this.parent.iaScene.coeff,y:this.parent.iaScene.coeff}
      });

      rasterObj.onload = function() {
          this.parent.group.add(this.kineticElement)
          this.kineticElement.animation('hidden')
          this.kineticElement.start();
          if (this.persistent == "on") {
              this.kineticElement.animation('idle')
           }
           this.addEventsManagement()
      }.bind(this)
      rasterObj.src = detail.image
    }
}
if (typeof module !== 'undefined' && module.exports != null) {
    exports.XiaSprite = XiaSprite
}
