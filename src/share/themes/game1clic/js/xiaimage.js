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
class XiaImage extends XiaDetail {

    constructor(parent, detail, idText){
        super(parent, detail, idText)
        //this.zoomable = true
        this.width = this.detail.width * this.parent.iaScene.scale
        this.height = this.detail.height * this.parent.iaScene.scale
        this.persistent = "off"
    }

    start() {
        var rasterObj = new Image()

        this.kineticElement = new Kinetic.Image({
            id: this.parent.jsonSource.id,
            name: this.parent.jsonSource.title,
            x: parseFloat(this.detail.x) * this.parent.iaScene.coeff,
            y: parseFloat(this.detail.y) * this.parent.iaScene.coeff + this.parent.iaScene.y,
            width: this.detail.width,
            height: this.detail.height,
            scale: {x:this.parent.iaScene.coeff,y:this.parent.iaScene.coeff}
        })

        this.kineticElement.setXiaParent(this)
        this.kineticElement.setIaObject(this.parent)

        this.kineticElement.backgroundImage = rasterObj
        this.tooltip = ""

        this.kineticElement.droparea = false
        this.kineticElement.tooltip_area = false


        rasterObj.onload = function() {
            var currentRatio = rasterObj.naturalWidth / this.detail.width
            this.kineticElement.backgroundImageOwnScaleX = (this.detail.width / this.width) / currentRatio
            this.kineticElement.backgroundImageOwnScaleY = (this.detail.height / this.height) / currentRatio
            this.parent.group.add(this.kineticElement)

            if ((typeof(this.parent.jsonSource.fill) !== 'undefined') &&
                (this.parent.jsonSource.fill === "#000000")) {
                this.zoomable = false;
            }

            if ((typeof(this.parent.jsonSource.fill) !== 'undefined') &&
                (this.parent.jsonSource.fill === "#ffffff")) {
                this.persistent = "onImage";
                this.kineticElement.fillPriority('pattern');
                this.kineticElement.fillPatternScaleX(this.kineticElement.backgroundImageOwnScaleX * 1/this.parent.iaScene.scale);
                this.kineticElement.fillPatternScaleY(this.kineticElement.backgroundImageOwnScaleY * 1/this.parent.iaScene.scale);
                this.kineticElement.fillPatternImage(this.kineticElement.backgroundImage);
                this.zoomable = false;
            }


            // define hit area excluding transparent pixels

            var cropX = Math.max(parseFloat(this.detail.minX), 0);
            var cropY = Math.max(parseFloat(this.detail.minY), 0);
            var cropWidth = (Math.min(parseFloat(this.detail.maxX) - parseFloat(this.detail.minX), Math.floor(parseFloat(this.parent.iaScene.originalWidth) * 1)));
            var cropHeight = (Math.min(parseFloat(this.detail.maxY) - parseFloat(this.detail.minY), Math.floor(parseFloat(this.parent.iaScene.originalHeight) * 1)));
            if (cropX + cropWidth > this.parent.iaScene.originalWidth * 1) {
                cropWidth = Math.abs(this.parent.iaScene.originalWidth * 1 - cropX * 1);
            }
            if (cropY * 1 + cropHeight > this.parent.iaScene.originalHeight * 1) {
                cropHeight = Math.abs(this.parent.iaScene.originalHeight * 1 - cropY * 1);
            }

            var hitCanvas = this.parent.layer.getHitCanvas();
            this.parent.iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));
/*
            var canvas_source = document.createElement('canvas');
            canvas_source.setAttribute('width', this.detail.width);
            canvas_source.setAttribute('height', this.detail.height);
            var context_source = canvas_source.getContext('2d');
            context_source.drawImage(rasterObj,0,0, (this.detail.width), (this.detail.height));
            //document.body.appendChild(canvas_source)
            this.imgData = context_source.getImageData(0,0,canvas_source.width,canvas_source.height);
*/

            var canvas_source = document.createElement('canvas');
            canvas_source.setAttribute('width', cropWidth * this.parent.iaScene.coeff);
            canvas_source.setAttribute('height', cropHeight * this.parent.iaScene.coeff);
            var context_source = canvas_source.getContext('2d');
            context_source.drawImage(rasterObj,0,0, Math.floor(cropWidth * this.parent.iaScene.coeff), Math.floor(cropHeight * this.parent.iaScene.coeff));

            var that = this
            var imageDataSource = context_source.getImageData(0, 0, Math.floor(cropWidth * this.parent.iaScene.coeff), Math.floor(cropHeight * this.parent.iaScene.coeff));

            (function(el, imageDataSource){
                el.kineticElement.hitFunc(function(context) {
                    var imageData = imageDataSource.data;
                    var imageDest = this.parent.iaScene.completeImage.data;
                    var position1 = 0;
                    var position2 = 0;
                    var maxWidth = Math.floor(cropWidth * this.parent.iaScene.coeff);
                    var maxHeight = Math.floor(cropHeight * this.parent.iaScene.coeff);
                    var startY = Math.floor(cropY * this.parent.iaScene.coeff);
                    var startX = Math.floor(cropX * this.parent.iaScene.coeff);
                    var hitCanvasWidth = Math.floor(this.parent.layer.getHitCanvas().width);
                    var rgbColorKey = Kinetic.Util._hexToRgb(this.kineticElement.colorKey);
                    for(var varx = 0; varx < maxWidth; varx +=1) {
                        for(var vary = 0; vary < maxHeight; vary +=1) {
                            position1 = 4 * (vary * maxWidth + varx);
                            position2 = 4 * ((vary + startY) * hitCanvasWidth + varx + startX);
                            if (imageData[position1 + 3] > 100) {
                               imageDest[position2 + 0] = rgbColorKey.r;
                               imageDest[position2 + 1] = rgbColorKey.g;
                               imageDest[position2 + 2] = rgbColorKey.b;
                               imageDest[position2 + 3] = 255;
                            }
                        }
                    }
                    context.putImageData(this.parent.iaScene.completeImage, 0, 0);
                }.bind(el));
            })(this, imageDataSource)

            /* this.xiaDetail[i].kineticElement.sceneFunc(function(context) {
                var yo = this.layer.getHitCanvas().getContext().getImageData(0,0,iaScene.width, iaScene.height);
                context.putImageData(yo, 0,0);
            });*/
            //this.addEventsManagement(i,zoomable, this, iaScene, baseImage, idText);
            this.manageDropAreaAndTooltips()
            this.parent.group.draw();

        }.bind(this)
        rasterObj.src = this.detail.image;

    }
}
if (typeof module !== 'undefined' && module.exports != null) {
     exports.XiaImage = XiaImage
}
