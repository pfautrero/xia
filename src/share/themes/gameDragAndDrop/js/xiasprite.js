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
  constructor (parent, detail, idText) {
    super(parent, detail, idText)
    this.width = this.detail.width * this.parent.mainScene.scale
    this.height = this.detail.height * this.parent.mainScene.scale
    this.persistent = (('fill' in this.detail) && (this.detail.fill === '#ffffff')) ? 'on' : 'off'
    this.path = this.detail.path
    this.tooltip = ''
    this.stroke = (('stroke' in this.detail) && (this.detail.stroke !== 'none')) ? this.detail.stroke : 'rgba(0, 0, 0, 0)'
    this.strokeWidth = ('strokewidth' in this.detail) ? this.detail.strokewidth : '0'
    this.parent.group.zoomActive = 0
  }

  defineImageBoxSize () {
    var timeLine = JSON.parse('[' + this.detail.timeline + ']')
    this.parent.minX = (this.parent.minX) ? Math.min(this.detail.x, this.parent.minX) : this.detail.x
    this.parent.minY = (this.parent.minY) ? Math.min(this.detail.y, this.parent.minY) : this.detail.y
    this.parent.maxX = (this.parent.maxX) ? Math.max(this.detail.x + this.detail.width / timeLine.length, this.parent.maxX) : this.detail.x + this.detail.width / timeLine.length
    this.parent.maxY = (this.parent.maxY) ? Math.max(this.detail.y + this.detail.height, this.parent.maxY) : this.detail.y + this.detail.height
  }

  start () {
    //this.defineImageBoxSize()
    var rasterObj = new Image()

    this.backgroundImage = rasterObj
    var timeLine = JSON.parse('[' + this.detail.timeline + ']')

    rasterObj.onload = function () {

      var ratioRaster = rasterObj.naturalHeight / this.detail.height
      var idle = []
      for (let k = 0; k < timeLine.length; k++) {
        idle.push(timeLine[k] * this.detail.width * ratioRaster, 0, this.detail.width * ratioRaster, this.detail.height * ratioRaster)
      }
      this.kineticElement = new Kinetic.Sprite({
        x: this.detail.x * this.parent.mainScene.coeff,
        y: this.detail.y * this.parent.mainScene.coeff + this.parent.mainScene.y,
        image: this.backgroundImage,
        animation: 'idle',
        animations: {
          idle: idle,
          hidden: [timeLine.length * this.detail.width * ratioRaster, 0, this.detail.width * ratioRaster, this.detail.height * ratioRaster]
        },
        frameRate: 10,
        frameIndex: 0,
        draggable: this.draggable_object,
        scale: { x: this.parent.mainScene.coeff / ratioRaster, y: this.parent.mainScene.coeff / ratioRaster}
      })
      this.parent.layer.add(this.kineticElement)
      this.kineticElement.animation('hidden')
      this.kineticElement.start()
      if (this.persistent === 'on') { this.kineticElement.animation('idle') }
      this.addEventsManagement(this, this.parent.mainScene, this.idText)
      this.kineticElement.setXiaParent(this)
      this.kineticElement.setIaObject(this.parent)
      this.parent.nbElements--
      if (this.parent.nbElements === 0) this.parent.resolve('All elements created')
    }.bind(this)
    rasterObj.crossOrigin = "Anonymous"
    rasterObj.src = this.detail.image
  }
}
if (typeof module !== 'undefined' && module.exports != null) {
  exports.XiaSprite = XiaSprite
}
