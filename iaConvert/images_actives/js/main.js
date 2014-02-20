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
    this.zoomActive = 0;
    this.minX = 0;
    this.minY = 0;
    this.maxX = 0;
    this.maxY = 0;
    
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
        if (that.minX == 0) that.minX = point.x;
        if (that.minY == 0) that.minY = point.y;
        if (that.maxX == 0) that.maxX = point.x;
        if (that.maxY == 0) that.maxY = point.y;
        for (var percent =0; percent<1000;percent++) {
            var point = element.getPointAtLength( len * percent/1000 );
            if (point.x < that.minX) that.minX = point.x;
            if (point.x > that.maxX) that.maxX = point.x;
            if (point.y < that.minY) that.minY = point.y;
            if (point.y > that.maxY) that.maxY = point.y;			
        }        
    }
    
    /*
     * 
     * @param {type} index
     * @returns {undefined}
     */
    var defineImageBoxSize = function(index) {
        "use strict";
        that.minX = parseFloat(detail.x);
        that.minY = parseFloat(detail.y) + parseFloat(detail.height);
        that.maxX = parseFloat(detail.x) + parseFloat(detail.width);
        that.maxY = parseFloat(detail.y);
    }    
    
    
    
    // Find paths and details
    
    if (typeof(detail.path) != 'undefined') {
        for (var i in detail.path) {
            this.path[i] = detail.path[i];
            this.backgroundImage[i] = imageObj;
            this.kineticElement[i] = new Kinetic.Path({
                data: this.path[i],
                y: 50,
                fill: 'rgba(0, 0, 0, 0)',
                stroke: '',
                strokeWidth: 0
            });
            that.kineticElement[i].scale({x:iaScene.coeff,y:iaScene.coeff});
            definePathBoxSize(i);

            /*
             * if mouse is over element, fill the element with semi-transparency
             */
            this.kineticElement[i].on('mouseover', function() {
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
            this.kineticElement[i].on('click touchstart', function() {
                // let's zoom
                if ((iaScene.cursorState.indexOf("ZoomIn.cur") != -1) && (iaScene.element == that)) {
                    iaScene.zoomActive = 1;
                    document.body.style.cursor = "url(img/ZoomOut.cur),auto";
                    iaScene.cursorState = "url(img/ZoomOut.cur),auto";
                    var largeur = (that.maxX - that.minX) * 1;
                    var hauteur = (that.maxY - that.minY) * 1;                
                    if (hauteur > largeur) {
                        that.agrandissement = iaScene.height / hauteur;
                    }
                    else {
                        that.agrandissement = iaScene.width / largeur;
                    }
                    for (var i in that.kineticElement) {
                        that.kineticElement[i].zoomActive = 1;
                        that.kineticElement[i].scale({x:that.agrandissement,y:that.agrandissement});
                        that.originalX[i] = that.kineticElement[i].x();
                        that.originalY[i] = that.kineticElement[i].y();
                        if (hauteur > largeur) {
                            that.kineticElement[i].x(((iaScene.width-largeur*that.agrandissement)/2 - that.minX*that.agrandissement) * 1);
                            that.kineticElement[i].y((that.kineticElement[i].y() - that.minY*that.agrandissement) * 1);
                        }
                        else {
                            that.kineticElement[i].y(((iaScene.height-hauteur*that.agrandissement)/2 - that.minY*that.agrandissement) * 1);
                            that.kineticElement[i].x((that.kineticElement[i].x() - that.minX*that.agrandissement) * 1);					
                        }
                    }
                    that.layer.draw();
                }
                // let's unzoom
                else if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {
                    for (var i in that.kineticElement) {
                        if (that.kineticElement[i].zoomActive == 1) {
                            iaScene.zoomActive = 0;
                            that.kineticElement[i].zoomActive = 0;
                            that.kineticElement[i].scale({x:iaScene.coeff,y:iaScene.coeff});
                            that.kineticElement[i].x(that.originalX[i]);
                            that.kineticElement[i].y(that.originalY[i]);

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
                            that.kineticElement[i].fillPatternImage(imageObj);
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
            this.kineticElement[i].on('mouseleave', function() {
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

            this.layer.add(this.kineticElement[i]);
        }
    }
    
    // path not found, default is image
    
    else {
        var rasterObj = new Image();
        this.backgroundImage[0] = rasterObj;
        rasterObj.onload = function() {
            that.kineticElement[0] = new Kinetic.Rect({
                    x: (parseFloat(detail.x))*iaScene.coeff,
                    y: parseFloat(detail.y)*iaScene.coeff+50,
                    width: detail.width,
                    height: detail.height,
                    scale: {x:iaScene.coeff,y:iaScene.coeff},
                    fill: 'rgba(0, 0, 0, 0)',
                    stroke: '',
                    strokeWidth: 0	
            });


            defineImageBoxSize();
            
            var i = 0;
            that.kineticElement[i].on('mouseover', function() {
                if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {

                }
                else {
                    document.body.style.cursor = "url(img/HandPointer.cur),auto";
                    iaScene.cursorState = "url(img/HandPointer.cur),auto";
                    for (var i in that.kineticElement) {
                        that.kineticElement[i].fillPriority('pattern');
                        that.kineticElement[i].fillPatternImage(that.backgroundImage[i]);
                        that.kineticElement[i].fillPatternOffset({x:0, y:0});
                    }
                    that.layer.draw();
                }
            });
            that.kineticElement[i].on('click touchstart', function() {
                // let's zoom
                if ((iaScene.cursorState.indexOf("ZoomIn.cur") != -1) && (iaScene.element == that)) {
                    iaScene.zoomActive = 1;
                    document.body.style.cursor = "url(img/ZoomOut.cur),auto";
                    iaScene.cursorState = "url(img/ZoomOut.cur),auto";
                    var largeur = (that.maxX - that.minX) * 1;
                    var hauteur = (that.maxY - that.minY) * 1;                
                    console.log("LARGEUR = " + largeur + " - " + "HAUTEUR = " + hauteur);
                    if (hauteur > largeur) {
                        that.agrandissement = iaScene.height / hauteur;
                    }
                    else {
                        that.agrandissement = iaScene.width / largeur;
                    }
                    for (var i in that.kineticElement) {
                        that.kineticElement[i].zoomActive = 1;
                        that.kineticElement[i].scale({x:that.agrandissement,y:that.agrandissement});
                        that.originalX[i] = that.kineticElement[i].x();
                        that.originalY[i] = that.kineticElement[i].y();
                        console.log("AGRANDISSEMENT = " + that.agrandissement + " X = " + that.kineticElement[i].x() + " - " + "Y = " + that.kineticElement[i].y());                        
                        if (hauteur > largeur) {
                            that.kineticElement[i].x(((iaScene.width-largeur)/2 - that.minX)  * iaScene.coeff);
                            that.kineticElement[i].y((that.kineticElement[i].y() - that.minY)  * iaScene.coeff);
                        }
                        else {
                            that.kineticElement[i].y(((iaScene.height-hauteur)/2 - that.minY)  * iaScene.coeff);
                            that.kineticElement[i].x((that.kineticElement[i].x() - that.minX)  * iaScene.coeff);					
                        }
                        console.log("X = " + that.kineticElement[i].x() + " - " + "Y = " + that.kineticElement[i].y());                        
                    }
                    that.layer.draw();
                }
                // let's unzoom
                else if (iaScene.cursorState.indexOf("ZoomOut.cur") != -1) {
                    for (var i in that.kineticElement) {
                        if (that.kineticElement[i].zoomActive == 1) {
                            iaScene.zoomActive = 0;
                            that.kineticElement[i].zoomActive = 0;
                            that.kineticElement[i].scale({x:iaScene.coeff,y:iaScene.coeff});
                            that.kineticElement[i].x(that.originalX[i]);
                            that.kineticElement[i].y(that.originalY[i]);

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

            that.layer.add(that.kineticElement[0]);
            that.layer.draw();
        };
        rasterObj.src = detail.image;        
    }
    
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
// Load datas in the accordion menu
/*var menu = "";
menu += '<div class="accordion-group">';
menu += '<div class="accordion-heading">';
menu += '<a id="collapsecomment-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapsecomment">'+scene.intro_title+'</a>';
menu += '<div id="collapsecomment" class="accordion-body collapse">';
menu += '<div class="accordion-inner">'+scene.intro_detail+'</div></div></div></div>';
for (var i in details) {
    if ((details[i].detail.indexOf("Réponse:") != -1) || (details[i].detail.indexOf("réponse:") != -1))  {
        var question = details[i].detail.substr(0,details[i].detail.indexOf("Réponse:"));
        var answer = details[i].detail.substr(details[i].detail.indexOf("Réponse:")+8);
        menu += '<div class="accordion-group">';
        menu += '<div class="accordion-heading">';
        menu += '<a id="collapse'+i+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+i+'">'+details[i].title+'</a>';
        menu += '<div id="collapse'+i+'" class="accordion-body collapse">';
        menu += '<div class="accordion-inner">' + question + '<div style="margin-top:5px;margin-bottom:5px;"><a class="button" href="#response_'+i+'">Réponse</a></div>' + '<div class="response" id="response_'+ i +'">' + answer + '</div>' + '</div></div></div></div>';                        

    }
    else {
        menu += '<div class="accordion-group">';
        menu += '<div class="accordion-heading">';
        menu += '<a id="collapse'+i+'-heading" class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse'+i+'">'+details[i].title+'</a>';
        menu += '<div id="collapse'+i+'" class="accordion-body collapse">';
        menu += '<div class="accordion-inner">'+details[i].detail+'</div></div></div></div>';                        
    }

}	
$("#accordion2").html(menu);*/


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