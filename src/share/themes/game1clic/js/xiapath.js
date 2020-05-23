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
class XiaPath extends XiaDetail {

    constructor(parent, detail, idText){
        super(parent, detail, idText)
        //this.zoomable = true
        this.width = this.detail.width * this.parent.iaScene.scale
        this.height = this.detail.height * this.parent.iaScene.scale
        this.persistent = "off"
        this.path = this.detail.path;
        this.tooltip = ""
    }

    start() {


        // if detail is out of background, hack maxX and maxY
        if (parseFloat(this.detail.maxX) < 0) this.detail.maxX = 1;
        if (parseFloat(this.detail.maxY) < 0) this.detail.maxY = 1;
        this.kineticElement = new Kinetic.Path({
            id: this.parent.jsonSource.id,
            name: this.parent.jsonSource.title,
            data: this.detail.path,
            x: parseFloat(this.detail.x) * this.parent.iaScene.coeff,
            y: parseFloat(this.detail.y) * this.parent.iaScene.coeff + this.parent.iaScene.y,
            scale: {x:this.parent.iaScene.coeff,y:this.parent.iaScene.coeff},
            fill: 'rgba(0, 0, 0, 0)'
        });
        this.kineticElement.droparea = false;
        this.kineticElement.tooltip_area = false;

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
        //document.body.appendChild(tempCanvas)



        this.kineticElement.setXiaParent(this);
        this.kineticElement.setIaObject(this.parent);
        this.tooltip = "";

        // crop background image to suit shape box
        this.parent.cropCanvas = document.createElement('canvas');
        this.parent.cropCanvas.setAttribute('width', parseFloat(this.detail.maxX) - parseFloat(this.detail.minX));
        this.parent.cropCanvas.setAttribute('height', parseFloat(this.detail.maxY) - parseFloat(this.detail.minY));
        var cropCtx = this.parent.cropCanvas.getContext('2d');
        var cropX = Math.max(parseFloat(this.detail.minX), 0);
        var cropY = Math.max(parseFloat(this.detail.minY), 0);
        var cropWidth = (Math.min((parseFloat(this.detail.maxX) - parseFloat(this.detail.minX)) * this.parent.iaScene.scale, Math.floor(parseFloat(this.parent.iaScene.originalWidth) * this.parent.iaScene.scale)));
        var cropHeight = (Math.min((parseFloat(this.detail.maxY) - parseFloat(this.detail.minY)) * this.parent.iaScene.scale, Math.floor(parseFloat(this.parent.iaScene.originalHeight) * this.parent.iaScene.scale)));
        if (cropX * this.parent.iaScene.scale + cropWidth > this.parent.iaScene.originalWidth * this.parent.iaScene.scale) {
             cropWidth = this.parent.iaScene.originalWidth * this.parent.iaScene.scale - cropX * this.parent.iaScene.scale;
        }
        if (cropY * this.parent.iaScene.scale + cropHeight > this.parent.iaScene.originalHeight * this.parent.iaScene.scale) {
             cropHeight = this.parent.iaScene.originalHeight * this.parent.iaScene.scale - cropY * this.parent.iaScene.scale;
        }
        // bad workaround to avoid null dimensions
        if (cropWidth <= 0) cropWidth = 1;
        if (cropHeight <= 0) cropHeight = 1;
        cropCtx.drawImage(
            this.parent.imageObj,
            cropX * this.parent.iaScene.scale,
            cropY * this.parent.iaScene.scale,
            cropWidth,
            cropHeight,
            0,
            0,
            cropWidth,
            cropHeight
        );
        var dataUrl = this.parent.cropCanvas.toDataURL();
        delete this.parent.cropCanvas;
        var cropedImage = new Image();


        var that = this
        cropedImage.onload = function() {
            that.kineticElement.backgroundImage = cropedImage;
            that.kineticElement.backgroundImageOwnScaleX = 1;
            that.kineticElement.backgroundImageOwnScaleY = 1;
            that.kineticElement.fillPatternRepeat('no-repeat');
            that.kineticElement.fillPatternX(that.detail.minX);
            that.kineticElement.fillPatternY(that.detail.minY);
        };
        cropedImage.src = dataUrl
        var zoomable = true
        if ((typeof(this.detail.fill) !== 'undefined') &&
            (this.detail.fill === "#000000")) {
            zoomable = false
        }
        this.persistent = "off"
        if ((typeof(this.detail.fill) !== 'undefined') &&
            (this.detail.fill === "#ffffff")) {
            this.persistent = "onPath"
            this.kineticElement.fill('rgba(' + this.parent.iaScene.colorPersistent.red + ',' + this.parent.iaScene.colorPersistent.green + ',' + this.parent.iaScene.colorPersistent.blue + ',' + this.parent.iaScene.colorPersistent.opacity + ')');
        }
        //that.addEventsManagement(i, zoomable, that, iaScene, baseImage, idText);
        this.manageDropAreaAndTooltips()

        this.parent.group.add(this.kineticElement)
        this.parent.group.draw()

    }
}
if (typeof module !== 'undefined' && module.exports != null) {
     exports.XiaPath = XiaPath
}
