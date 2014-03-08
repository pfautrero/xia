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
    /*
     *  define scene dimensions on the page
     */
    this.width = 1000;
    this.height = 755;
    
    this.zoomActive = 0;
    this.element = 0;
    this.originalWidth = originalWidth;
    this.originalHeight = originalHeight;
    this.coeff = (this.width / 2) / parseFloat(originalWidth);
    this.cursorState=""
}

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
function iaObject(imageObj, detail, layer, idText, baseImage, iaScene) {
    "use strict";
    var that = this;
    this.path = new Array();
    this.kineticElement = new Array();
    this.backgroundImage = new Array();
    this.originalX = new Array();
    this.originalY = new Array();
    this.layer = layer;
    this.imageObj = imageObj;
    this.agrandissement = 0;
    this.zoomActive = 0;
    this.minX = 10000;
    this.minY = 10000;
    this.maxX = -1;
    this.maxY = -1;
    this.tween = new Array();    

    /*
     * 
     * @param {type} index
     * @returns {undefined}
     */
    var definePathBoxSize = function(index) {
        "use strict";
        var element = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        element.setAttribute('d', that.path[index]);
        var len = element.getTotalLength();
        var point = element.getPointAtLength(0);
        if (that.minX == -1) that.minX = point.x;
        if (that.minY == -1) that.minY = point.y;
        if (that.maxX == -1) that.maxX = point.x;
        if (that.maxY == -1) that.maxY = point.y;
        for (var percent =0; percent<1000;percent++) {
            var point = element.getPointAtLength( len * percent/1000 );
            if (point.x < that.minX) that.minX = point.x;
            if (point.x > that.maxX) that.maxX = point.x;
            if (point.y < that.minY) that.minY = point.y;
            if (point.y > that.maxY) that.maxY = point.y;			
        }        
        //that.minY += 50;
        //that.maxY += 50;
//
//        var aux = that.minY;
//        that.minY= that.maxY;
//        that.maxY = aux;


    }
    
    /*
     * 
     * @param {type} index
     * @returns {undefined}
     */
    var defineImageBoxSize = function(detail) {
        "use strict";
       
        if (that.minX == -1) that.minX = (parseFloat(detail.x));
        if (that.maxY == 10000) that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
        if (that.maxX == -1) that.maxX = (parseFloat(detail.x) + parseFloat(detail.width));
        if (that.minY == 10000) that.minY = (parseFloat(detail.y));

        if (parseFloat(detail.x) < that.minX) that.minX = parseFloat(detail.x);
        if (parseFloat(detail.x) + parseFloat(detail.width) > that.maxX) that.maxX = parseFloat(detail.x) + parseFloat(detail.width);
        if (parseFloat(detail.y) < that.minY) that.miny = parseFloat(detail.y);        
        if (parseFloat(detail.y) + parseFloat(detail.height) > that.maxY) that.maxY = parseFloat(detail.y) + parseFloat(detail.height);
 

    }    
    /*
     * Define mouse events on the current KineticElement
     * @param {type} i KineticElement index
     * @returns {undefined}
     */
    
    var addEventsManagement = function(i) {

        /*
         * if mouse is over element, fill the element with semi-transparency
         */
        that.kineticElement[i].on('mouseover', function() {
            if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {

            }
            else {
                document.body.style.cursor = "url(img/HandPointer.cur),auto";
                iaScene.cursorState = "url(img/HandPointer.cur),auto";
                for (var i in that.kineticElement) {
                        that.kineticElement[i].fill('rgba(0, 221, 255, 0.4)');
                }
                that.layer.draw();
            }
        });
        /*
         * if we click in this element, manage zoom-in, zoom-out
         */
        that.kineticElement[i].on('click touchstart', function() {
            // let's zoom
            if ((iaScene.cursorState.indexOf("ZoomIn.cur") != -1) && (iaScene.element == that)) {
                iaScene.zoomActive = 1;
                document.body.style.cursor = "url(img/ZoomOut.cur),auto";
                iaScene.cursorState = "url(img/ZoomOut.cur),auto";
                for (var i in that.kineticElement) {
                    that.kineticElement[i].zoomActive = 1;
                    that.kineticElement[i].setZIndex(1000);
                    that.originalX[i] = that.kineticElement[i].x();
                    that.originalY[i] = that.kineticElement[i].y();
                    that.tween[i].play();
                }
                that.layer.draw();
            }
            // let's unzoom
            else if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {
                for (var i in that.kineticElement) {
                    if ((that.kineticElement[i].zoomActive == 1) && (that.kineticElement[i].scaleX().toFixed(10) == (that.agrandissement * iaScene.coeff).toFixed(10))) {
                        iaScene.zoomActive = 0;
                        that.kineticElement[i].zoomActive = 0;
                        that.kineticElement[i].scale({x:iaScene.coeff,y:iaScene.coeff});
                        that.kineticElement[i].setZIndex(100);
                        that.kineticElement[i].x(that.originalX[i]);
                        that.kineticElement[i].y(that.originalY[i]);
                        that.tween[i].reset();
                        that.kineticElement[i].fillPriority('color');
                        baseImage.opacity(1);
                        that.kineticElement[i].setFill('rgba(0, 0, 0, 0)');
                        document.body.style.cursor = "default";
                        iaScene.cursorState = "default";
                        that.layer.draw();										
                    }
                }
            }
            // let's focus
            else {
                if (iaScene.zoomActive == 0) {
                    if ((iaScene.element != 0) && (typeof(iaScene.element) != 'undefined')) {
                        for (var i in iaScene.element.kineticElement) {
                            iaScene.element.kineticElement[i].fillPriority('color');
                            iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
                        }
                    }                    
                    document.body.style.cursor = 'url("img/ZoomIn.cur"),auto';
                    iaScene.cursorState = 'url("img/ZoomIn.cur"),auto';
                    $('.collapse.in').each(function (index) {
                            if ($(this).attr("id") != idText) $(this).collapse("toggle");
                    });
                    $('#' + idText).collapse("show");
                    baseImage.opacity(0.3);
                    for (var i in that.kineticElement) {
                        that.kineticElement[i].fillPriority('pattern');
                        that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
                        that.kineticElement[i].fillPatternOffset({x:0, y:0});
                    }
                    iaScene.element = that;
                    that.layer.draw();
                }
            }
        });
        /*
         * if we leave this element, just clear the scene
         */
        that.kineticElement[i].on('mouseleave', function() {
            if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {

            }
            else {
                baseImage.opacity(1);
                for (var i in that.kineticElement) {
                    that.kineticElement[i].fillPriority('color');
                    that.kineticElement[i].fill('rgba(0, 0, 0, 0)');
                }
                document.body.style.cursor = "default";
                iaScene.cursorState = "default";
                that.layer.draw();						
            }
        });        
    }
    
    /*
     * 
     * @param {type} path
     * @param {type} i KineticElement index
     * @returns {undefined}
     */
    var includePath = function(path, i) {
        that.path[i] = path;
        that.backgroundImage[i] = imageObj;
        that.kineticElement[i] = new Kinetic.Path({
            data: path,
            y: 50,
            x: 0,
            scale: {x:iaScene.coeff,y:iaScene.coeff},
            fill: 'rgba(0, 0, 0, 0)',
            stroke: '',
            strokeWidth: 0
        });
        definePathBoxSize(i);
        addEventsManagement(i);
        that.layer.add(that.kineticElement[i]);
    };

    /*
     * 
     * @param {type} detail
     * @param {type} i KineticElement index
     * @returns {undefined}
     */
    var includeImage = function(detail, i) {
//        definePathBoxSize(i);
        defineImageBoxSize(detail);
        var rasterObj = new Image();
        rasterObj.src = detail.image;                
        that.backgroundImage[i] = rasterObj;
        that.kineticElement[i] = new Kinetic.Rect({
            x: (parseFloat(detail.x))*iaScene.coeff,
            y: parseFloat(detail.y)*iaScene.coeff+50,
            width: detail.width,
            height: detail.height,
            scale: {x:iaScene.coeff,y:iaScene.coeff},
            fill: 'rgba(0, 0, 0, 0)',
            stroke: '',
            strokeWidth: 0	
        });
        addEventsManagement(i);
        that.layer.add(that.kineticElement[i]);
        that.layer.draw();

    }    
    
    if (typeof(detail.path) !== 'undefined') {
        includePath(detail.path, 0);
        //console.log("PATH1 : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
        //console.log("PATH2 : " + that.kineticElement[0].x() + " " + that.kineticElement[0].y());        
    }
    else if (typeof(detail.image) !== 'undefined') {
        includeImage(detail, 0);
        //console.log("IMAGE1 : " + that.minX + " " + (that.minY) + " " + that.maxX + " " + (that.maxY));
        //console.log("IMAGE2 : " + that.kineticElement[0].x() + " " + that.kineticElement[0].y());
    }
    else if (typeof(detail.group) !== 'undefined') {
        for (var i in detail.group) {
            if (typeof(detail.group[i].path) != 'undefined') {
                includePath(detail.group[i].path, i);
        //console.log("GPATH1 : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
        //console.log("GPATH2 : " + that.kineticElement[i].x() + " " + that.kineticElement[i].y());        

            }
            else if (typeof(detail.group[i].image) != 'undefined') {
                includeImage(detail.group[i], i);
        //console.log("GIMAGE1 : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
        //console.log("GIMAGE2 : " + that.kineticElement[i].x() + " " + that.kineticElement[i].y());

            }
        }
        //console.log("GROUP1 : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
    }
    else {
        console.log(detail);
    }

    that.minX = that.minX * iaScene.coeff;
    that.minY = (that.minY) * iaScene.coeff;
    that.maxX = that.maxX * iaScene.coeff;
    that.maxY = (that.maxY) * iaScene.coeff;    

    var largeur = (that.maxX - that.minX) * 1;
    var hauteur = (that.maxY - that.minY) * 1;
    that.agrandissement1  = iaScene.height / hauteur;   // beta
    that.agrandissement2  = iaScene.width / largeur;    // alpha
    
    if (hauteur * that.agrandissement2 > iaScene.height) {
        //console.log("hauteur > largeur");
        that.agrandissement = that.agrandissement1;
         for (var i in that.kineticElement) {
            var new_x = (that.kineticElement[i].x() - (that.minX)) * that.agrandissement + (iaScene.width - largeur * that.agrandissement) / 2;
            var new_y = (that.kineticElement[i].y() - 50 - (that.minY))*that.agrandissement + 50;
            that.tween[i] = new Kinetic.Tween({
              node: that.kineticElement[i], 
              duration: 1,
              x: new_x,
              y: new_y,
                easing: Kinetic.Easings.BackEaseIn,
                scaleX: that.agrandissement * iaScene.coeff,
                scaleY: that.agrandissement * iaScene.coeff                
              

            });
            //console.log(i.toString() + " new_x = " + new_x.toString());
            //console.log(i.toString() + " new_y = " + new_y.toString());            
            //console.log("largeur = " + largeur.toString());
            //console.log("hauteur = " + hauteur.toString());                        
            //console.log("min - max : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
        }
    }
    else {
        //console.log("hauteur < largeur");
        that.agrandissement = that.agrandissement2;
        for (var i in that.kineticElement) {
            var new_x = (that.kineticElement[i].x() - (that.minX))*that.agrandissement;
            var new_y = 1 * ((that.kineticElement[i].y() - 50 - (that.minY)) * that.agrandissement + 50 + (iaScene.height-hauteur*that.agrandissement)/2);
            that.tween[i] = new Kinetic.Tween({
              node: that.kineticElement[i], 
              duration: 1,
                x: new_x,
                y: new_y,
                easing: Kinetic.Easings.BackEaseIn,
                scaleX: that.agrandissement * iaScene.coeff,
                scaleY: that.agrandissement * iaScene.coeff
            });
            //console.log("new_x = " + new_x.toString());
            //console.log("new_y = " + new_y.toString());            
            //console.log("largeur = " + largeur.toString());
            //console.log("hauteur = " + hauteur.toString());                        
            //console.log("min - max : " + that.minX + " " + that.minY + " " + that.maxX + " " + that.maxY);
        }
    }
    //console.log("agrandissement = " + that.agrandissement);
    //    console.log("agrandissement * largeur = " + that.agrandissement*largeur);
    //    console.log("agrandissement * hauteur = " + that.agrandissement*hauteur);
    
    /*
     *  manage accordion events related to this element
     */
    $("#" + idText + "-heading").on('click touchstart',function(){
        $('.collapse.in').each(function (index) {
            if ($(this).attr("id") != idText) $(this).collapse("toggle");
        });
        if ((iaScene.element != 0) && (typeof(iaScene.element) != 'undefined')) {
            for (var i in iaScene.element.kineticElement) {
                iaScene.element.kineticElement[i].fillPriority('color');
                iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
            }
        }
        baseImage.opacity(0.3);
        for (var i in that.kineticElement) {
            that.kineticElement[i].fillPriority('pattern');
            that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
            that.kineticElement[i].fillPatternOffset({x:0, y:0});
        }
        iaScene.element = that;
        that.layer.draw();				
    });
}
/*
 * Main
 * Initialization
 * 
 * 1rst layer : div "detect" - if clicked, enable canvas events
 * 2nd layer : bootstrap accordion
 * 3rd layer : div "canvas" containing images and paths
 * 4th layer : div "disablearea" - if clicked, disable events canvas  
 */

imageObj = new Image();
canvas = document.getElementById("canvas");

// area located under the canvas. If mouse over is detected, we must re-activate mouse events on canvas
detect = document.getElementById("detect");
detect.addEventListener("mouseover", function()
    {
        canvas.style.pointerEvents="auto";

        if ((iaScene.element != 0) && (typeof(iaScene.element) != 'undefined')) {
            console.log(iaScene.element);
            for (var i in iaScene.element.kineticElement) {
                iaScene.element.kineticElement[i].fillPriority('color');
                iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
            }
        }
    }, false);			
detect.addEventListener("touchstart", function()
    {   
        canvas.style.pointerEvents="auto";

        if ((iaScene.element != 0) && (typeof(iaScene.element) != 'undefined')) {
            console.log(iaScene.element);
            for (var i in iaScene.element.kineticElement) {
                iaScene.element.kineticElement[i].fillPriority('color');
                iaScene.element.kineticElement[i].fill('rgba(0,0,0,0)');
            }
        }
    }, false);	

$("#collapsecomment").collapse("show");
$("#title").html(scene.title);

// Load background image

imageObj.onload = function() {
    var mainScene = new iaScene(scene.width,scene.height);
    
    var stage = new Kinetic.Stage({
            container: 'canvas',
            width: mainScene.width,
            height: mainScene.height
    });


    // area containing image background    
    var baseImage = new Kinetic.Rect({
            x: 0,
            y: 50,
            width: scene.width,
            height: scene.height,
            scale: {x:mainScene.coeff,y:mainScene.coeff},
            fillPatternImage: imageObj,
            stroke: '',
            strokeWidth: 0
    });
    // define area to disable canvas events management when
    // mouse is over. Thus, we can reach div located under canvas 
    var disableArea = new Kinetic.Rect({
            x: mainScene.width / 2,
            y: 50,
            width: mainScene.width / 2,
            height: mainScene.height,
            stroke: '',
            strokeWidth: 0
    });		
    disableArea.on('mouseover touchstart', function() {
        canvas.style.pointerEvents="none";
    });
    var layer = new Kinetic.Layer();	
    layer.add(disableArea);	
    layer.add(baseImage);
    for (var i in details) {
        iaObj = new iaObject(imageObj, details[i], layer, "collapse" + i, baseImage, mainScene);
    }
    layer.draw();
    stage.add(layer);

};
imageObj.src = scene.image;