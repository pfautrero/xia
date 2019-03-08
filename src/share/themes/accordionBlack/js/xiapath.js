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
class XiaPath extends XiaDetail {

    constructor(parent, detail, idText){
      super(parent, detail, idText)
      this.width = this.detail.width * this.parent.iaScene.scale
      this.height = this.detail.height * this.parent.iaScene.scale
      this.persistent = (('fill' in this.detail) && (this.detail.fill === "#ffffff")) ? "on" : "off"
      this.path = this.detail.path
      this.tooltip = ""
      this.stroke = (('stroke' in this.detail) && (this.detail.stroke != 'none')) ? this.detail.stroke : 'rgba(0, 0, 0, 0)'
      this.strokeWidth = ('strokewidth' in this.detail) ? this.detail.strokewidth : '0'
    }

    start() {
      if ((this.detail.maxX < 0) || (this.detail.maxY < 0)) return
      this.defineBoxSize()
      this.kineticElement = new Konva.Path({
        id: this.detail.id,
        name: this.parent.jsonSource.title,
        data: this.detail.path,
        x: this.detail.x * this.parent.iaScene.coeff,
        y: this.detail.y * this.parent.iaScene.coeff + this.parent.iaScene.y,
        scale: {x:this.parent.iaScene.coeff,y:this.parent.iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)'
      })

      this.defineHitArea()
      this.cropBackgroundImage()

      if (this.persistent == "on") {
        this.kineticElement.fill(this.parent.iaScene.cacheColor)
      }
      this.addEventsManagement()
      this.manageDropAreaAndTooltips()

      this.parent.group.add(this.kineticElement)
      this.parent.group.draw()
    }

    defineHitArea() {
      // create path in a standalone image
      // to manage hitArea if this detail is under sprite...
      var tempCanvas = document.createElement('canvas')
      tempCanvas.setAttribute('width', this.detail.width)
      tempCanvas.setAttribute('height', this.detail.height)
      var tempContext = tempCanvas.getContext('2d')
      // Arghh...forced to remove single quotes from scene.path...
      var currentPath = new Path2D(this.detail.path.replace(/'/g, ""))
      tempContext.translate((-1) * this.detail.minX, (-1) * this.detail.minY)
      tempContext.fillStyle = "rgba(255, 255, 255, 255)"
      tempContext.fill(currentPath)
      this.imgData = tempContext.getImageData(0,0,tempCanvas.width,tempCanvas.height);

      this.kineticElement.setXiaParent(this);
      this.kineticElement.setIaObject(this.parent);
    }

    defineBoxSize() {
      this.parent.minX = ('minX' in this.detail) ? this.detail.minX : 0
      this.parent.minY = ('minY' in this.detail) ? this.detail.minY : 0
      this.parent.maxX = ('maxX' in this.detail) ? this.detail.maxX : 0
      this.parent.maxY = ('maxY' in this.detail) ? this.detail.maxY : 0
    }

    cropBackgroundImage() {
      // crop background image to suit shape box
      var cropperCanvas = document.createElement('canvas')
      cropperCanvas.setAttribute('width', (this.detail.maxX - this.detail.minX) * this.parent.iaScene.coeff)
      cropperCanvas.setAttribute('height', (this.detail.maxY - this.detail.minY) * this.parent.iaScene.coeff)

      var source = {
       'x' : Math.max(this.detail.minX, 0) * this.parent.iaScene.originalRatio,
       'y' : Math.max(this.detail.minY, 0) * this.parent.iaScene.originalRatio,
       'width' : (this.detail.maxX - Math.max(this.detail.minX, 0)) * this.parent.iaScene.originalRatio,
       'height' : (this.detail.maxY - Math.max(this.detail.minY, 0)) * this.parent.iaScene.originalRatio
      }
      var target = {
       'x' : Math.max(this.detail.minX * (-1), 0),
       'y' : Math.max(this.detail.minY * (-1), 0),
       'width' : (this.detail.maxX - Math.max(this.detail.minX, 0)) * this.parent.iaScene.coeff,
       'height' : (this.detail.maxY - Math.max(this.detail.minY, 0)) * this.parent.iaScene.coeff
      }
      cropperCanvas.getContext('2d').drawImage(
          this.parent.imageObj,
          source.x,
          source.y,
          source.width,
          source.height,
          target.x,
          target.y,
          target.width,
          target.height
      )
      var cropedImage = new Image()
      cropedImage.src = cropperCanvas.toDataURL()
      cropedImage.onload = function() {
          this.kineticElement.backgroundImage = cropedImage
          this.kineticElement.backgroundImageOwnScaleX = 1 / this.parent.iaScene.coeff
          this.kineticElement.backgroundImageOwnScaleY = 1 / this.parent.iaScene.coeff
          this.kineticElement.fillPatternRepeat('no-repeat')
          this.kineticElement.fillPatternX(this.detail.minX)
          this.kineticElement.fillPatternY(this.detail.minY)
      }.bind(this)
    }
}
if (typeof module !== 'undefined' && module.exports != null) {
     exports.XiaPath = XiaPath
}
