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
        this.zoomable = true
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

        var that = this
        rasterObj.onload = function() {

            that.kineticElement.backgroundImageOwnScaleX = that.parent.iaScene.scale * that.detail.width / that.width;
            that.kineticElement.backgroundImageOwnScaleY = that.parent.iaScene.scale * that.detail.height / that.height;
            that.parent.group.add(that.kineticElement)

            if ((typeof(that.parent.jsonSource.fill) !== 'undefined') &&
                (that.parent.jsonSource.fill === "#000000")) {
                that.zoomable = false;
            }

            if ((typeof(that.parent.jsonSource.fill) !== 'undefined') &&
                (that.parent.jsonSource.fill === "#ffffff")) {
                that.persistent = "onImage";
                that.kineticElement.fillPriority('pattern');
                that.kineticElement.fillPatternScaleX(that.kineticElement.backgroundImageOwnScaleX * 1/that.parent.iaScene.scale);
                that.kineticElement.fillPatternScaleY(that.kineticElement.backgroundImageOwnScaleY * 1/that.parent.iaScene.scale);
                that.kineticElement.fillPatternImage(that.kineticElement.backgroundImage);
                that.zoomable = false;
            }


            // define hit area excluding transparent pixels

            var cropX = Math.max(parseFloat(that.detail.minX), 0);
            var cropY = Math.max(parseFloat(that.detail.minY), 0);
            var cropWidth = (Math.min(parseFloat(that.detail.maxX) - parseFloat(that.detail.minX), Math.floor(parseFloat(that.parent.iaScene.originalWidth) * 1)));
            var cropHeight = (Math.min(parseFloat(that.detail.maxY) - parseFloat(that.detail.minY), Math.floor(parseFloat(that.parent.iaScene.originalHeight) * 1)));
            if (cropX + cropWidth > that.parent.iaScene.originalWidth * 1) {
                cropWidth = Math.abs(that.parent.iaScene.originalWidth * 1 - cropX * 1);
            }
            if (cropY * 1 + cropHeight > that.parent.iaScene.originalHeight * 1) {
                cropHeight = Math.abs(that.parent.iaScene.originalHeight * 1 - cropY * 1);
            }

            var hitCanvas = that.parent.layer.getHitCanvas();
            that.parent.iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));

            var canvas_source = document.createElement('canvas');
            canvas_source.setAttribute('width', that.detail.width);
            canvas_source.setAttribute('height', that.detail.height);
            var context_source = canvas_source.getContext('2d');
            context_source.drawImage(rasterObj,0,0, (that.detail.width), (that.detail.height));
            //document.body.appendChild(canvas_source)
            that.imgData = context_source.getImageData(0,0,canvas_source.width,canvas_source.height);

            /* that.xiaDetail[i].kineticElement.sceneFunc(function(context) {
                var yo = that.layer.getHitCanvas().getContext().getImageData(0,0,iaScene.width, iaScene.height);
                context.putImageData(yo, 0,0);
            });*/
            //that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);
            that.manageDropAreaAndTooltips()
            that.parent.group.draw();

        };
        rasterObj.src = this.detail.image;

    }
}
if (typeof module !== 'undefined' && module.exports != null) {
     exports.XiaImage = XiaImage
}