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
// @author : pascal.fautrero@ac-versailles.fr


/*
 *
 * @param {object} params
 * @constructor create image active object
 */
function IaObject(params) {
    "use strict";
    var that = this;
    this.path = [];
    this.xiaDetail = [];
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -10000;
    this.maxY = -10000;
    this.group = 0;
    this.jsonSource = params.detail
    this.iaScene = params.iaScene

    this.layer = params.layer;
    this.background_layer = params.background_layer;
    this.imageObj = params.imageObj;
    this.idText = params.idText;
    this.myhooks = params.myhooks;
    // Create kineticElements and include them in a group

    this.group = new Kinetic.Group();
    this.layer.add(this.group);

    if (typeof(params.detail.path) !== 'undefined') {
        that.includePath(params.detail, 0, that, params.iaScene, params.baseImage, params.idText);
    }
    else if (typeof(params.detail.image) !== 'undefined') {
        var re = /sprite(.*)/i;
        if (params.detail.id.match(re)) {
            console.log('sprite detected')
            that.includeSprite(params.detail, 0, that, params.iaScene, params.baseImage, params.idText);
        }
        else {
            that.includeImage(params.detail, 0, that, params.iaScene, params.baseImage, params.idText);
        }
    }
    else if (typeof(params.detail.group) !== 'undefined') {
        for (var i in params.detail.group) {
            if (typeof(params.detail.group[i].path) !== 'undefined') {
                that.includePath(params.detail.group[i], i, that, params.iaScene, params.baseImage, params.idText);
            }
            else if (typeof(params.detail.group[i].image) !== 'undefined') {
                var re = /sprite(.*)/i;
                if (params.detail.group[i].id.match(re)) {
                    console.log('sprite detected')
                    that.includeSprite(params.detail.group[i], i, that, params.iaScene, params.baseImage, params.idText);
                }
                else {
                    that.includeImage(params.detail.group[i], i, that, params.iaScene, params.baseImage, params.idText);
                }
            }
        }
        that.definePathBoxSize(params.detail, that);
    }
    else {
        console.log(params.detail);
    }

    this.scaleBox(this, params.iaScene);
    this.myhooks.afterIaObjectConstructor(params.iaScene, params.idText, params.detail, this);
}

/*
 *
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includeSprite = function(detail, i, that, iaScene, baseImage, idText) {
    this.defineImageBoxSize(detail, this);
    this.xiaDetail[i] = new XiaSprite(this, idText)
    this.xiaDetail[i].start(i)
};

/*
 *
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includeImage = function(detail, i, that, iaScene, baseImage, idText) {
    that.defineImageBoxSize(detail, that);

    that.xiaDetail[i] = new XiaDetail(that, idText);

    var rasterObj = new Image();


    that.xiaDetail[i].kineticElement = new Kinetic.Image({
        id: detail.id,
        name: detail.title,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        scale: {x:iaScene.coeff,y:iaScene.coeff}
    });
    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    that.xiaDetail[i].kineticElement.setIaObject(that);

    that.xiaDetail[i].kineticElement.backgroundImage = rasterObj;
    that.xiaDetail[i].kineticElement.tooltip = "";

    that.xiaDetail[i].kineticElement.droparea = false;
    that.xiaDetail[i].kineticElement.tooltip_area = false;

    rasterObj.onload = function() {

        that.xiaDetail[i].width = detail.width * iaScene.scale
        that.xiaDetail[i].height = detail.height * iaScene.scale

        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX = iaScene.scale * detail.width / this.width;
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY = iaScene.scale * detail.height / this.height;
        var zoomable = true;

        if ((typeof(detail.fill) !== 'undefined') &&
            (detail.fill === "#000000")) {
            zoomable = false;
        }

        that.xiaDetail[i].persistent = "off";
        if ((typeof(detail.fill) !== 'undefined') &&
            (detail.fill === "#ffffff")) {
            that.xiaDetail[i].persistent = "onImage";
            that.xiaDetail[i].kineticElement.fillPriority('pattern');
            that.xiaDetail[i].kineticElement.fillPatternScaleX(that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX * 1/iaScene.scale);
            that.xiaDetail[i].kineticElement.fillPatternScaleY(that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY * 1/iaScene.scale);
            that.xiaDetail[i].kineticElement.fillPatternImage(that.xiaDetail[i].kineticElement.backgroundImage);
            zoomable = false;
        }
        that.group.add(that.xiaDetail[i].kineticElement);

        // define hit area excluding transparent pixels

        var cropX = Math.max(parseFloat(detail.minX), 0);
        var cropY = Math.max(parseFloat(detail.minY), 0);
        var cropWidth = (Math.min(parseFloat(detail.maxX) - parseFloat(detail.minX), Math.floor(parseFloat(iaScene.originalWidth) * 1)));
        var cropHeight = (Math.min(parseFloat(detail.maxY) - parseFloat(detail.minY), Math.floor(parseFloat(iaScene.originalHeight) * 1)));
        if (cropX + cropWidth > iaScene.originalWidth * 1) {
            cropWidth = Math.abs(iaScene.originalWidth * 1 - cropX * 1);
        }
        if (cropY * 1 + cropHeight > iaScene.originalHeight * 1) {
            cropHeight = Math.abs(iaScene.originalHeight * 1 - cropY * 1);
        }

	      var hitCanvas = that.layer.getHitCanvas();
        iaScene.completeImage = hitCanvas.getContext().getImageData(0,0,Math.floor(hitCanvas.width),Math.floor(hitCanvas.height));

        /*var canvas_source = document.createElement('canvas');
        canvas_source.setAttribute('width', cropWidth * iaScene.coeff);
        canvas_source.setAttribute('height', cropHeight * iaScene.coeff);
        var context_source = canvas_source.getContext('2d');
        context_source.drawImage(rasterObj,0,0, Math.floor(cropWidth * iaScene.coeff), Math.floor(cropHeight * iaScene.coeff));
        */

        var canvas_source = document.createElement('canvas');
        canvas_source.setAttribute('width', detail.width);
        canvas_source.setAttribute('height', detail.height);
        var context_source = canvas_source.getContext('2d');
        context_source.drawImage(rasterObj,0,0, (detail.width), (detail.height));
        //document.body.appendChild(canvas_source)
        that.xiaDetail[i].imgData = context_source.getImageData(0,0,canvas_source.width,canvas_source.height);

        /*imageDataSource = context_source.getImageData(0, 0, Math.floor(cropWidth * iaScene.coeff), Math.floor(cropHeight * iaScene.coeff));

        (function(imageDataSource){
            that.xiaDetail[i].kineticElement.hitFunc(function(context) {
                var imageData = imageDataSource.data;
                var imageDest = iaScene.completeImage.data;
                var position1 = 0;
                var position2 = 0;
                var maxWidth = Math.floor(cropWidth * iaScene.coeff);
                var maxHeight = Math.floor(cropHeight * iaScene.coeff);
                var startY = Math.floor(cropY * iaScene.coeff);
                var startX = Math.floor(cropX * iaScene.coeff);
                var hitCanvasWidth = Math.floor(that.layer.getHitCanvas().width);
                var rgbColorKey = Kinetic.Util._hexToRgb(this.colorKey);
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
                context.putImageData(iaScene.completeImage, 0, 0);
            });
        })(imageDataSource);*/


      /* that.xiaDetail[i].kineticElement.sceneFunc(function(context) {
            var yo = that.layer.getHitCanvas().getContext().getImageData(0,0,iaScene.width, iaScene.height);
            context.putImageData(yo, 0,0);
        });*/
        //that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);
        that.xiaDetail[i].manageDropAreaAndTooltips()
        that.group.draw();
    };
    rasterObj.src = detail.image;

};


/*
 *
 * @param {type} path
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includePath = function(detail, i, that, iaScene, baseImage, idText) {

    var that=this;
    that.xiaDetail[i] = new XiaDetail(that, idText);

    that.path[i] = detail.path;
    // if detail is out of background, hack maxX and maxY
    if (parseFloat(detail.maxX) < 0) detail.maxX = 1;
    if (parseFloat(detail.maxY) < 0) detail.maxY = 1;
    that.xiaDetail[i].kineticElement = new Kinetic.Path({
        id: detail.id,
        name: detail.title,
        data: detail.path,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        scale: {x:iaScene.coeff,y:iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)'
    });
    that.xiaDetail[i].kineticElement.droparea = false;
    that.xiaDetail[i].kineticElement.tooltip_area = false;

    // create path in a standalone image
    // to manage hitArea if this detail is under sprite...
    var tempCanvas = document.createElement('canvas')
    tempCanvas.setAttribute('width', detail.width)
    tempCanvas.setAttribute('height', detail.height)
    var tempContext = tempCanvas.getContext('2d')
    // Arghh...forced to remove single quotes from scene.path...
    var currentPath = new Path2D(detail.path.replace(/'/g, ""))
    tempContext.translate((-1) * detail.minX, (-1) * detail.minY)
    tempContext.fillStyle = "rgba(255, 255, 255, 255)"
    tempContext.fill(currentPath)
    that.xiaDetail[i].imgData = tempContext.getImageData(0,0,tempCanvas.width,tempCanvas.height);
    //document.body.appendChild(tempCanvas)


    that.xiaDetail[i].kineticElement.setXiaParent(that.xiaDetail[i]);
    that.xiaDetail[i].kineticElement.setIaObject(that);
    that.xiaDetail[i].kineticElement.tooltip = "";
    that.definePathBoxSize(detail, that);
    // crop background image to suit shape box
    that.cropCanvas = document.createElement('canvas');
    that.cropCanvas.setAttribute('width', parseFloat(detail.maxX) - parseFloat(detail.minX));
    that.cropCanvas.setAttribute('height', parseFloat(detail.maxY) - parseFloat(detail.minY));
    var cropCtx = that.cropCanvas.getContext('2d');
    var cropX = Math.max(parseFloat(detail.minX), 0);
    var cropY = Math.max(parseFloat(detail.minY), 0);
    var cropWidth = (Math.min((parseFloat(detail.maxX) - parseFloat(detail.minX)) * iaScene.scale, Math.floor(parseFloat(iaScene.originalWidth) * iaScene.scale)));
    var cropHeight = (Math.min((parseFloat(detail.maxY) - parseFloat(detail.minY)) * iaScene.scale, Math.floor(parseFloat(iaScene.originalHeight) * iaScene.scale)));
    if (cropX * iaScene.scale + cropWidth > iaScene.originalWidth * iaScene.scale) {
	     cropWidth = iaScene.originalWidth * iaScene.scale - cropX * iaScene.scale;
    }
    if (cropY * iaScene.scale + cropHeight > iaScene.originalHeight * iaScene.scale) {
	     cropHeight = iaScene.originalHeight * iaScene.scale - cropY * iaScene.scale;
    }
    // bad workaround to avoid null dimensions
    if (cropWidth <= 0) cropWidth = 1;
    if (cropHeight <= 0) cropHeight = 1;
    cropCtx.drawImage(
        that.imageObj,
        cropX * iaScene.scale,
        cropY * iaScene.scale,
        cropWidth,
        cropHeight,
        0,
        0,
        cropWidth,
        cropHeight
    );
    var dataUrl = that.cropCanvas.toDataURL();
    delete that.cropCanvas;
    var cropedImage = new Image();
    that.xiaDetail[i].kineticElement.tooltip = "";
    cropedImage.onload = function() {
        that.xiaDetail[i].kineticElement.backgroundImage = cropedImage;
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleX = 1;
        that.xiaDetail[i].kineticElement.backgroundImageOwnScaleY = 1;
        that.xiaDetail[i].kineticElement.fillPatternRepeat('no-repeat');
        that.xiaDetail[i].kineticElement.fillPatternX(detail.minX);
        that.xiaDetail[i].kineticElement.fillPatternY(detail.minY);
    };
    cropedImage.src = dataUrl;
    var zoomable = true;
    if ((typeof(detail.fill) !== 'undefined') &&
        (detail.fill === "#000000")) {
        zoomable = false;
    }
    that.xiaDetail[i].persistent = "off";
    if ((typeof(detail.fill) !== 'undefined') &&
        (detail.fill === "#ffffff")) {
        that.xiaDetail[i].persistent = "onPath";
        that.xiaDetail[i].kineticElement.fill('rgba(' + iaScene.colorPersistent.red + ',' + iaScene.colorPersistent.green + ',' + iaScene.colorPersistent.blue + ',' + iaScene.colorPersistent.opacity + ')');
    }
    //that.addEventsManagement(i, zoomable, that, iaScene, baseImage, idText);
    that.xiaDetail[i].manageDropAreaAndTooltips()

    that.group.add(that.xiaDetail[i].kineticElement);
    that.group.draw();
};

/*
 *
 * @param {type} index
 * @returns {undefined}
 */
IaObject.prototype.defineImageBoxSize = function(detail, that) {
    "use strict";
    var that = this;
    if (that.minX === -1)
        that.minX = (parseFloat(detail.x));
    if (that.maxY === 10000)
        that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
    if (that.maxX === -1)
        that.maxX = (parseFloat(detail.x) + parseFloat(detail.width));
    if (that.minY === 10000)
        that.minY = (parseFloat(detail.y));

    if (parseFloat(detail.x) < that.minX) that.minX = parseFloat(detail.x);
    if (parseFloat(detail.x) + parseFloat(detail.width) > that.maxX)
        that.maxX = parseFloat(detail.x) + parseFloat(detail.width);
    if (parseFloat(detail.y) < that.minY)
        that.miny = parseFloat(detail.y);
    if (parseFloat(detail.y) + parseFloat(detail.height) > that.maxY)
        that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
};


/*
 *
 * @param {type} index
 * @returns {undefined}
 */
IaObject.prototype.definePathBoxSize = function(detail, that) {
    "use strict";
    if (  (typeof(detail.minX) !== 'undefined') &&
          (typeof(detail.minY) !== 'undefined') &&
          (typeof(detail.maxX) !== 'undefined') &&
          (typeof(detail.maxY) !== 'undefined')) {
        that.minX = detail.minX;
        that.minY = detail.minY;
        that.maxX = detail.maxX;
        that.maxY = detail.maxY;
    }
    else {
        console.log('definePathBoxSize failure');
    }
};


/*
 *
 */
IaObject.prototype.scaleBox = function(that, iaScene) {

    that.minX = that.minX * iaScene.coeff;
    that.minY = that.minY * iaScene.coeff;
    that.maxX = that.maxX * iaScene.coeff;
    that.maxY = that.maxY * iaScene.coeff;

};

/*
 * Define mouse events on the current KineticElement
 * @param {type} i KineticElement index
 * @returns {undefined}
 */

IaObject.prototype.addEventsManagement = function(i, zoomable, that, iaScene, baseImage, idText) {

    var that=this;
    // if current detail is a drop area, disable drag and drop
    if ($('article[data-target="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.xiaDetail[i].kineticElement.droparea = true;
    }
    // tooltip must be at the bottom
    if ($('article[data-tooltip="' + $("#" + idText).data("kinetic_id") + '"]').length != 0) {
        that.xiaDetail[i].kineticElement.getParent().moveToBottom();
        that.xiaDetail[i].options += " disable-click ";
        that.xiaDetail[i].kineticElement.tooltip_area = true;
        // disable hitArea for tooltip
        that.xiaDetail[i].kineticElement.hitFunc(function(context){
            context.beginPath();
            context.rect(0,0,0,0);
            context.closePath();
            context.fillStrokeShape(this);
	});
    }
};
