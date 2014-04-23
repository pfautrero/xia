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
// @author : pascal.fautrero@crdp.ac-versailles.fr

/**
 * 
 * @param {type} originalWidth
 * @param {type} originalHeight
 * @constructor create image active scene
 */
function iaScene(originalWidth, originalHeight) {
    "use strict";
    var that = this;
    //  canvas width
    this.width = 1000;
    // canvas height
    this.height = 800;  
    // default color used to fill shapes during mouseover
    this.overColor = 'rgba(66, 133, 244,0.4)';  
    // Image ratio on the scene
    this.ratio = 0.50;  
    // padding-top in the canvas
    this.y = 0;
    // easing effect
    this.easing = Kinetic.Easings.StrongEaseOut;
    
    // internal
    this.scale = 1;
    this.zoomActive = 0;
    this.element = 0;
    this.originalWidth = originalWidth;
    this.originalHeight = originalHeight;
    this.coeff = (this.width * this.ratio) / parseFloat(originalWidth);
    this.cursorState="";

}

/*
 * Scale entire scene
 *  
 */
iaScene.prototype.scaleScene = function(mainScene){
    var viewportWidth = $(window).width();
    var viewportHeight = $(window).height();
    var new_height = scene.height * mainScene.coeff + $('#canvas').offset().top - $('#container').offset().top;
    $('#container').css({"height": new_height + 'px'});
    $('#canvas').css({"height": mainScene.originalHeight * mainScene.coeff + 'px'});

    if (viewportWidth < 1000) {
        mainScene.width = viewportWidth - mainScene.y;
        mainScene.coeff = (mainScene.width * mainScene.ratio) / parseFloat(mainScene.originalWidth);
        $('#container').css({"width": viewportWidth - mainScene.y});
    }
    if (viewportHeight < 755) {
        mainScene.height = viewportHeight - mainScene.y;
        $('#detect').css({"height": viewportHeight - mainScene.y});
    }
};



/*
 * 
 * @param {type} imageObj
 * @param {type} detail
 * @param {type} layer
 * @param {type} idText
 * @param {type} baseImage
 * @param {type} iaScene
 * @constructor create image active object
 */
function iaObject(imageObj, detail, layer, idText, baseImage, iaScene, background_layer) {
    "use strict";
    var that = this;
    this.path = new Array();
    this.kineticElement = new Array();
    this.backgroundImage = new Array();
    this.originalX = new Array();
    this.originalY = new Array();
    this.layer = layer;
    this.background_layer = background_layer;
    this.imageObj = imageObj;
    this.agrandissement = 0;
    this.zoomActive = 0;
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -10000;
    this.maxY = -10000;
    this.tween = new Array(); 
    this.tween_group = 0;
    this.group = 0;

    // Create kineticElements and include them in a group
   
    that.group = new Kinetic.Group();
    that.layer.add(that.group);
    
    if (typeof(detail.path) !== 'undefined') {
        that.includePath(detail, 0, that, iaScene, baseImage, idText);
    }
    else if (typeof(detail.image) !== 'undefined') {
        that.includeImage(detail, 0, that, iaScene, baseImage, idText);
    }
    else if (typeof(detail.group) !== 'undefined') {
        for (var i in detail.group) {
            if (typeof(detail.group[i].path) !== 'undefined') {
                that.includePath(detail.group[i], i, that, iaScene, baseImage, idText);
            }
            else if (typeof(detail.group[i].image) !== 'undefined') {
                that.includeImage(detail.group[i], i, that, iaScene, baseImage, idText);
            }
        }
        that.definePathBoxSize(detail, that);
    }
    else {
        console.log(detail);
    }

    /*that.group.cache({
        width : iaScene.width,
        height : iaScene.height
    });*/

    this.defineTweens(this, iaScene);
    
    /*
     *  manage accordion events related to this element
     */
    $("#" + idText + "-heading").on('click touchstart',function(){
        if (iaScene.zoomActive === 0) {
            $('.collapse.in').each(function (index) {
                if ($(this).attr("id") !== idText) $(this).collapse("toggle");
            });
            if ((iaScene.element !== 0) && 
                (typeof(iaScene.element) !== 'undefined')) {
                for (var i in iaScene.element.kineticElement) {
                    iaScene.element.kineticElement[i].fillPriority('color');
                    iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    iaScene.element.layer.draw();
                }
            }
            var zoomable = true;
            if ((typeof(detail.fill) !== 'undefined') && 
                (detail.fill === "#000000")) {
                zoomable = false;
            }
            if (zoomable === true) {
                document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
            }            
            baseImage.opacity(0.3);
            for (var i in that.kineticElement) {
                that.kineticElement[i].fillPriority('pattern');
                that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
            }
            iaScene.element = that;
            that.layer.moveToTop();
            that.layer.draw();				
            that.background_layer.draw();
        }
    });
}

/*
 * 
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
iaObject.prototype.includeImage = function(detail, i, that, iaScene, baseImage, idText) {
    that.defineImageBoxSize(detail, that);
    var rasterObj = new Image();
    rasterObj.src = detail.image;                
    that.backgroundImage[i] = rasterObj;
    that.kineticElement[i] = new Kinetic.Rect({
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        width: detail.width,
        height: detail.height,
        scale: {x:iaScene.coeff,y:iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)'	
    });
    rasterObj.onload = function() {

        var zoomable = true;
        if ((typeof(detail.fill) !== 'undefined') && 
            (detail.fill === "#000000")) {
            zoomable = false;
        }
        that.addEventsManagement(i,zoomable, that, iaScene, baseImage, idText);
        that.group.add(that.kineticElement[i]);

        // buggy on kinetic 5.1.0
        //that.kineticElement[i].cache();
        //that.kineticElement[i].drawHitFromCache();
        that.group.draw();        
    };

};    


/*
 * 
 * @param {type} path
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
iaObject.prototype.includePath = function(detail, i, that, iaScene, baseImage, idText) {
    that.path[i] = detail.path;
    //that.backgroundImage[i] = imageObj;

    that.kineticElement[i] = new Kinetic.Path({
        data: detail.path,
        x: parseFloat(detail.x) * iaScene.coeff,
        y: parseFloat(detail.y) * iaScene.coeff + iaScene.y,
        scale: {x:iaScene.coeff,y:iaScene.coeff},
        fill: 'rgba(0, 0, 0, 0)'
    });
    that.definePathBoxSize(detail, that);
    // crop background image to suit shape box
    that.cropCanvas = document.createElement('canvas');
    that.cropCanvas.setAttribute('width', parseFloat(detail.maxX) - parseFloat(detail.minX));
    that.cropCanvas.setAttribute('height', parseFloat(detail.maxY) - parseFloat(detail.minY));
    var cropCtx = that.cropCanvas.getContext('2d');
    var cropX = Math.max(parseFloat(detail.minX), 0);
    var cropY = Math.max(parseFloat(detail.minY), 0);
    var cropWidth = (Math.min(parseFloat(detail.maxX) - parseFloat(detail.minX), Math.floor(parseFloat(iaScene.originalWidth) * iaScene.scale)));
    var cropHeight = (Math.min(parseFloat(detail.maxY) - parseFloat(detail.minY), Math.floor(parseFloat(iaScene.originalHeight) * iaScene.scale)));

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
    cropedImage.src = dataUrl;
    cropedImage.onload = function() {
        that.backgroundImage[i] = cropedImage;
        that.kineticElement[i].fillPatternRepeat('no-repeat');
        that.kineticElement[i].fillPatternX(detail.minX);
        that.kineticElement[i].fillPatternY(detail.minY);
        that.kineticElement[i].draw();
    };

    var zoomable = true;
    if ((typeof(detail.fill) !== 'undefined') && 
        (detail.fill === "#000000")) {
        zoomable = false;
    }
    that.addEventsManagement(i, zoomable, that, iaScene, baseImage, idText);

    that.group.add(that.kineticElement[i]);
    that.group.draw();
};

/*
 * 
 * @param {type} index
 * @returns {undefined}
 */
iaObject.prototype.defineImageBoxSize = function(detail, that) {
    "use strict";

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
iaObject.prototype.definePathBoxSize = function(detail, that) {
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
 * Define zoom rate and define tween effect for each group
 * @returns {undefined}
 */
iaObject.prototype.defineTweens = function(that, iaScene) {

    that.minX = that.minX * iaScene.coeff;
    that.minY = that.minY * iaScene.coeff;
    that.maxX = that.maxX * iaScene.coeff;
    that.maxY = that.maxY * iaScene.coeff;    

    var largeur = that.maxX - that.minX;
    var hauteur = that.maxY - that.minY;
    that.agrandissement1  = (iaScene.height - iaScene.y) / hauteur;   // beta
    that.agrandissement2  = iaScene.width / largeur;    // alpha

    if (hauteur * that.agrandissement2 > iaScene.height) {
        that.agrandissement = that.agrandissement1;
        that.tweenX = (0 - (that.minX)) * that.agrandissement + (iaScene.width - largeur * that.agrandissement) / 2;
        that.tweenY = (0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y;
    }
    else {
        that.agrandissement = that.agrandissement2;
        that.tweenX = (0 - (that.minX)) * that.agrandissement;
        that.tweenY = 1 * ((0 - iaScene.y - (that.minY)) * that.agrandissement + iaScene.y + (iaScene.height - hauteur * that.agrandissement) / 2);
    }

};

/*
 * Define mouse events on the current KineticElement
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
   
iaObject.prototype.addEventsManagement = function(i, zoomable, that, iaScene, baseImage, idText) {

    /*
     * if mouse is over element, fill the element with semi-transparency
     */
    that.kineticElement[i].on('mouseover', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else if (iaScene.cursorState.indexOf("HandPointer.cur") === -1) {
            //that.group.clearCache();
            document.body.style.cursor = "url(img/HandPointer.cur),auto";
            iaScene.cursorState = "url(img/HandPointer.cur),auto";
            for (var i in that.kineticElement) {
                that.kineticElement[i].fill(iaScene.overColor);
                that.kineticElement[i].scale(iaScene.coeff);
            }
            /*that.group.cache({
                width : iaScene.width,
                height : iaScene.height
            });*/
            that.layer.batchDraw();
        }
    });
    /*
     * if we click in this element, manage zoom-in, zoom-out
     */
    that.kineticElement[i].on('click touchstart', function() {
        // let's zoom
        if ((iaScene.cursorState.indexOf("ZoomIn.cur") !== -1) && 
            (iaScene.element === that)) {
            iaScene.zoomActive = 1;
            document.body.style.cursor = "url(img/ZoomOut.cur),auto";
            iaScene.cursorState = "url(img/ZoomOut.cur),auto";
            that.layer.moveToTop();
            that.group.zoomActive = 1;
            that.originalX[0] = that.group.x();
            that.originalY[0] = that.group.y();
            /*that.tween_group = new Kinetic.Tween({
                node: that.group, 
                duration: 1,
                x: that.tweenX,
                y: that.tweenY,
                easing: iaScene.easing,
                scaleX: that.agrandissement,
                scaleY: that.agrandissement
            });*/                
            //that.tween_group.play();
            that.alpha = 0;
            that.step = 0.05;
            var personalTween = function() {
                // linear
                var tempX = that.originalX[0] + that.alpha.toFixed(2) * (that.tweenX - that.originalX[0]);
                var tempY = that.originalY[0] + that.alpha.toFixed(2) * (that.tweenY - that.originalY[0]);
                var tempScale = 1 + that.alpha.toFixed(2) * (that.agrandissement - 1);
                if (that.alpha.toFixed(2) <= 1) {
                    that.alpha = that.alpha + that.step;
                    that.group.x(tempX);
                    that.group.y(tempY);
                    that.group.scaleX(tempScale);
                    that.group.scaleY(tempScale);
                    that.layer.draw();
                    var t = setTimeout(personalTween, 20);
                }
                else {
                    clearTimeout(t);
                }
            };
            var t = setTimeout(personalTween, 20);
        }
        // let's unzoom
        else if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {

            if ((that.group.zoomActive == 1) && 
                (that.group.scaleX().toFixed(5) == (that.agrandissement).toFixed(5))) {
                iaScene.zoomActive = 0;
                that.group.zoomActive = 0;
                that.group.scaleX(1);
                that.group.scaleY(1);
                that.group.x(that.originalX[0]);
                that.group.y(that.originalY[0]);
                //that.group.clearCache();
                //that.tween_group.reset();
                //that.tween_group.destroy();
                //delete that.tween_group;

                baseImage.opacity(1);
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";

                for (var i in that.kineticElement) {
                    that.kineticElement[i].fillPriority('color');
                    that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                }                    
                that.layer.draw();
                that.background_layer.draw();
            }
        }
        // let's focus
        else {
            if (iaScene.zoomActive === 0) {
                if ((iaScene.element !== 0) && 
                    (typeof(iaScene.element) !== 'undefined')) {
                    //iaScene.element.group.clearCache();
                    for (var i in iaScene.element.kineticElement) {
                        iaScene.element.kineticElement[i].fillPriority('color');
                        iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                    }
                }                    
                if (zoomable === true) {
                    document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                    iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
                }
                $('.collapse.in').each(function (index) {
                        if ($(this).attr("id") !== idText) 
                            $(this).collapse("toggle");
                });
                $('#' + idText).collapse("show");
                baseImage.opacity(0.3);
                that.background_layer.draw();
                //that.group.clearCache();
                for (var i in that.kineticElement) {
                    that.kineticElement[i].fillPriority('pattern');
                    that.kineticElement[i].fillPatternScaleX(1/iaScene.scale);
                    that.kineticElement[i].fillPatternScaleY(1/iaScene.scale);
                    that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
                }
                /*that.group.cache({
                    width : iaScene.width,
                    height : iaScene.height
                });*/

                that.layer.draw(); 
                iaScene.element = that;
            }
        }
    });
    /*
     * if we leave this element, just clear the scene
     */
    that.kineticElement[i].on('mouseleave', function() {
        if (iaScene.cursorState.indexOf("ZoomOut.cur") !== -1) {

        }
        else {
            //that.group.clearCache();
            baseImage.opacity(1);
            that.background_layer.draw();
            for (var i in that.kineticElement) {
                that.kineticElement[i].fillPriority('color');
                that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
            }
            document.body.style.cursor = "default";
            iaScene.cursorState = "default";
            that.layer.draw();						
        }
    });        
};



/*
 * Main
 * Initialization
 * 
 * 1rst layer : div "detect" - if clicked, enable canvas events
 * 2nd layer : bootstrap accordion
 * 3rd layer : div "canvas" containing images and paths
 * 4th layer : div "disablearea" - if clicked, disable events canvas  
 */

function main() {
    "use strict";
    var that=this;

    that.canvas = document.getElementById("canvas");

    // area located under the canvas. If mouse over is detected, 
    // we must re-activate mouse events on canvas
    var detect = document.getElementById("detect");
    detect.addEventListener("mouseover", function()
        {
            that.canvas.style.pointerEvents="auto";

            if ((iaScene.element !== 0) && (typeof(iaScene.element) !== 'undefined')) {
                for (var i in iaScene.element.kineticElement) {
                    iaScene.element.kineticElement[i].fillPriority('color');
                    iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                }
            }
        }, false);			
    detect.addEventListener("touchstart", function()
        {   
            that.canvas.style.pointerEvents="auto";

            if ((iaScene.element !== 0) && (typeof(iaScene.element) !== 'undefined')) {
                for (var i in iaScene.element.kineticElement) {
                    iaScene.element.kineticElement[i].fillPriority('color');
                    iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                }
            }
        }, false);	

    $("#collapsecomment").collapse("show");


    // Load background image

    that.imageObj = new Image();
    that.imageObj.src = scene.image;
    that.imageObj.onload = function() {
        // define the maximum number of pixels allowed in the image
        // iPad can't manage images up to 5MB pixels
        var maxNumberPixels = 1 * 1024 * 1024;
        var ratio = 1;
        if (parseFloat(scene.width) * parseFloat(scene.height) >= maxNumberPixels) {
            ratio = Math.sqrt(maxNumberPixels/(parseFloat(scene.width) * parseFloat(scene.height)));
            console.log("Background Image is resized on the fly with ratio = " + ratio.toString());
        }
        else {
            console.log("Background Image is used without being resized");
        }
        //console.log(ratio);
        that.newwidth = parseFloat(scene.width) * ratio;
        that.newheight = parseFloat(scene.height) * ratio;
        that.scaleCanvas = document.createElement('canvas');
        that.scaleCanvas.setAttribute('width', that.newwidth);
        that.scaleCanvas.setAttribute('height', that.newheight);
        that.scaleCtx = that.scaleCanvas.getContext('2d');
        that.scaleCtx.drawImage(
            that.imageObj, 
            0, 
            0,
            that.newwidth,
            that.newheight
        );
        //document.body.appendChild(this.scaleCanvas);
        var dataUrl = that.scaleCanvas.toDataURL();
        delete that.scaleCanvas;
        delete that.imageObj;
        var scaledImage = new Image();
        scaledImage.src = dataUrl;
        scaledImage.onload = function() {

            //scene.width = that.newwidth;
            //scene.height = that.newheight;
            var mainScene = new iaScene(scene.width,scene.height);
            mainScene.scale = that.newwidth / scene.width; 
            mainScene.scaleScene(mainScene);

            var stage = new Kinetic.Stage({
                container: 'canvas',
                width: mainScene.width,
                height: mainScene.height
            });

            // area containing image background    
            var baseImage = new Kinetic.Image({
                x: 0,
                y: mainScene.y,
                width: scene.width,
                height: scene.height,
                scale: {x:mainScene.coeff,y:mainScene.coeff},
                image: scaledImage
            });

            // define area to disable canvas events management when
            // mouse is over. Thus, we can reach div located under canvas 
            var disableArea = new Kinetic.Rect({
                x: mainScene.width  * mainScene.ratio,
                y: mainScene.y,
                width: mainScene.width * (1 - mainScene.ratio),
                height: mainScene.height
            });		
            disableArea.on('mouseover touchstart', function() {
                canvas.style.pointerEvents="none";
            });
            var layers = new Array();
            layers[0] = new Kinetic.FastLayer();	
            layers[1] = new Kinetic.Layer();

            layers[0].add(baseImage);
            layers[1].add(disableArea);	
            stage.add(layers[0]);
            stage.add(layers[1]);

            for (var i in details) {
                var indice = parseInt(i+2);
                layers[indice] = new Kinetic.Layer();
                stage.add(layers[indice]);
                var iaObj = new iaObject(scaledImage, details[i], layers[indice], "collapse" + i, baseImage, mainScene, layers[0]);
            }

            $("#collapsecomment-heading").on('click touchstart',function(){
                if (mainScene.zoomActive === 0) {
                    $('.collapse.in').each(function (index) {
                        if ($(this).attr("id") !== "collapsecomment") $(this).collapse("toggle");
                    });
                    if ((mainScene.element !== 0) && (typeof(mainScene.element) !== 'undefined')) {
                        for (var i in mainScene.element.kineticElement) {
                            mainScene.element.kineticElement[i].fillPriority('color');
                            mainScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                            mainScene.element.layer.draw();
                        }
                    }
                    baseImage.opacity(1);
                    mainScene.element = that;
                    layers[0].draw();
                }
            });

            // FullScreen ability
            // source code from http://blogs.sitepointstatic.com/examples/tech/full-screen/index.html
            var e = document.getElementById("title");
            var div_container = document.getElementById("container");
            e.onclick = function() {
                if (RunPrefixMethod(document, "FullScreen") || RunPrefixMethod(document, "IsFullScreen")) {
                    RunPrefixMethod(document, "CancelFullScreen");
                }
                else {
                    RunPrefixMethod(div_container, "RequestFullScreen");
                }
            };

            var pfx = ["webkit", "moz", "ms", "o", ""];
            function RunPrefixMethod(obj, method) {
                var p = 0, m, t;
                while (p < pfx.length && !obj[m]) {
                    m = method;
                    if (pfx[p] == "") {
                        m = m.substr(0,1).toLowerCase() + m.substr(1);
                    }
                    m = pfx[p] + m;
                    t = typeof obj[m];
                    if (t != "undefined") {
                        pfx = [pfx[p]];
                        return (t == "function" ? obj[m]() : obj[m]);
                    }
                    p++;
                }
            };

        };

    };    
    
}

launch = new main();


