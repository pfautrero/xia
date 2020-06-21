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
class XiaImage extends XiaDetail {
  constructor (parent, detail, idText) {
    super(parent, detail, idText)
    this.width = this.detail.width * this.parent.iaScene.scale
    this.height = this.detail.height * this.parent.iaScene.scale
    this.persistent = (('fill' in this.detail) && (this.detail.fill === '#ffffff')) ? 'on' : 'off'
    this.path = this.detail.path
    this.tooltip = ''
    this.stroke = (('stroke' in this.detail) && (this.detail.stroke !== 'none')) ? this.detail.stroke : 'rgba(0, 0, 0, 0)'
    this.strokeWidth = ('strokewidth' in this.detail) ? this.detail.strokewidth : '0'
    this.parent.group.zoomActive = 0
    this.type = "image"
  }

  defineImageBoxSize (rasterObj) {
    if (!('width' in this.detail)) {
      this.detail.width = rasterObj.width
      this.detail.height = rasterObj.height
    }
    if (!('minX' in this.detail)) {
      this.detail.minX = this.detail.x
      this.detail.minY = this.detail.y
      this.detail.maxX = this.detail.x + this.detail.width
      this.detail.maxY = this.detail.y + this.detail.height
    }
    this.parent.minX = (this.parent.minX) ? Math.min(this.detail.x, this.parent.minX) : this.detail.x
    this.parent.minY = (this.parent.minY) ? Math.min(this.detail.y, this.parent.minY) : this.detail.y
    this.parent.maxX = (this.parent.maxX) ? Math.max(this.detail.x + this.detail.width, this.parent.maxX) : this.detail.x + this.detail.width
    this.parent.maxY = (this.parent.maxY) ? Math.max(this.detail.y + this.detail.height, this.parent.maxY) : this.detail.y + this.detail.height
  }

  start () {
    var rasterObj = new Image()
    rasterObj.onload = function () {
      this.defineImageBoxSize(rasterObj)
      this.backgroundImage = rasterObj
      this.kineticElement = new Konva.Image({
        id: this.detail.id,
        name: this.title,
        x: this.detail.x * this.parent.iaScene.coeff,
        y: this.detail.y * this.parent.iaScene.coeff + this.parent.iaScene.y,
        width: this.detail.width,
        height: this.detail.height,
        scale: { x: this.parent.iaScene.coeff, y: this.parent.iaScene.coeff }
      })
      this.kineticElement.backgroundImage = this.backgroundImage
      this.kineticElement.backgroundImageOwnScaleX = this.detail.width / this.width
      this.kineticElement.backgroundImageOwnScaleY = this.detail.height / this.height
      if (this.persistent === 'on') {
        this.kineticElement.setImage(this.kineticElement.backgroundImage)
      }
      this.parent.group.add(this.kineticElement)
      this.addEventsManagement()
      this.defineHitArea()
      /* that.kineticElement[i].sceneFunc(function(context) {
          var yo = that.layer.getHitCanvas().getContext().getImageData(0,0,iaScene.width, iaScene.height);
          context.putImageData(yo, 0,0);
      }); */
      this.kineticElement.setXiaParent(this)
      this.kineticElement.setIaObject(this.parent)
      this.parent.group.draw()
      this.parent.nbElements--
      if (this.parent.nbElements === 0) this.parent.resolve('All elements created')
    }.bind(this)
    rasterObj.crossOrigin = "Anonymous"
    rasterObj.src = this.detail.image
  }

  defineHitArea () {
    // define hit area excluding transparent pixels
    // =============================================================
    var cropper = {
      'x': Math.max(this.detail.minX, 0),
      'y': Math.max(this.detail.minY, 0),
      'width': Math.min(
        this.detail.maxX - this.detail.minX,
        Math.floor(this.parent.iaScene.originalWidth)),
      'height': Math.min(
        this.detail.maxY - this.detail.minY,
        Math.floor(this.parent.iaScene.originalHeight))
    }

    if (cropper.x + cropper.width > this.parent.iaScene.originalWidth * 1) {
      cropper.width = Math.abs(this.parent.iaScene.originalWidth * 1 - cropper.x * 1)
    }
    if (cropper.y * 1 + cropper.height > this.parent.iaScene.originalHeight * 1) {
      cropper.height = Math.abs(this.parent.iaScene.originalHeight * 1 - cropper.y * 1)
    }
    var hitCanvas = this.parent.layer.getHitCanvas()
    this.parent.iaScene.completeImage = hitCanvas
      .getContext()
      .getImageData(
        0,
        0,
        Math.floor(hitCanvas.width),
        Math.floor(hitCanvas.height)
      )

    var canvas_source = document.createElement('canvas')
    canvas_source.setAttribute('width', cropper.width * this.parent.iaScene.coeff)
    canvas_source.setAttribute('height', cropper.height * this.parent.iaScene.coeff)
    var context_source = canvas_source.getContext('2d')
    context_source.drawImage(
      this.kineticElement.backgroundImage,
      0,
      0,
      cropper.width * this.parent.iaScene.coeff,
      cropper.height * this.parent.iaScene.coeff
    )
    var imageDataSource = context_source
      .getImageData(
        0,
        0,
        Math.floor(cropper.width * this.parent.iaScene.coeff),
        Math.floor(cropper.height * this.parent.iaScene.coeff)
      )
    var len = imageDataSource.data.length;

    (function (len, imageDataSource, currentDetail, cropper) {
      currentDetail.kineticElement.hitFunc(function (context) {
        if (currentDetail.parent.iaScene.zoomActive === 0) {
          var imageData = imageDataSource.data
          var imageDest = currentDetail.parent.iaScene.completeImage.data
          var position1 = 0
          var position2 = 0
          var maxWidth = Math.floor(cropper.width * currentDetail.parent.iaScene.coeff)
          var maxHeight = Math.floor(cropper.height * currentDetail.parent.iaScene.coeff)
          var startY = Math.floor(cropper.y * currentDetail.parent.iaScene.coeff)
          var startX = Math.floor(cropper.x * currentDetail.parent.iaScene.coeff)
          var hitCanvasWidth = Math.floor(currentDetail.parent.layer.getHitCanvas().width)
          var rgbColorKey = Konva.Util._hexToRgb(this.colorKey)
          for (var varx = 0; varx < maxWidth; varx += 1) {
            for (var vary = 0; vary < maxHeight; vary += 1) {
              position1 = 4 * (vary * maxWidth + varx)
              position2 = 4 * ((vary + startY) * hitCanvasWidth + varx + startX)
              if (imageData[position1 + 3] > 100) {
                imageDest[position2 + 0] = rgbColorKey.r
                imageDest[position2 + 1] = rgbColorKey.g
                imageDest[position2 + 2] = rgbColorKey.b
                imageDest[position2 + 3] = 255
              }
            }
          }
          context.putImageData(currentDetail.parent.iaScene.completeImage, 0, 0)
        } else {
          context.beginPath()
          context.rect(0, 0, this.width(), this.height())
          context.closePath()
          context.fillStrokeShape(this)
        }
      })
    })(len, imageDataSource, this, cropper)
  }
}
if (typeof module !== 'undefined' && module.exports != null) {
  exports.XiaImage = XiaImage
}
