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
 * Main
 * Initialization
 * 
 */

function main(myhooks) {
    "use strict";

    Kinetic.Util.addMethods(Kinetic.Path,{
        setIaObject: function(iaobject) {
            this.iaobject = iaobject;
        },
        getIaObject: function() {
            return this.iaobject;
        }
    });    
    
    Kinetic.Util.addMethods(Kinetic.Image,{
        setIaObject: function(iaobject) {
            this.iaobject = iaobject;
        },
        getIaObject: function() {
            return this.iaobject;
        }
    });

    Kinetic.Util.addMethods(Kinetic.Path,{
        setXiaParent: function(xiaparent) {
            this.xiaparent = xiaparent;
        },
        getXiaParent: function() {
            return this.xiaparent;
        }
    });    
    
    Kinetic.Util.addMethods(Kinetic.Image,{
        setXiaParent: function(xiaparent) {
            this.xiaparent = xiaparent;
        },
        getXiaParent: function() {
            return this.xiaparent;
        }    });    
    
    Kinetic.draggedshape = null;
    
    var that=window;
    that.canvas = document.getElementById("canvas");

    // Load background image

    that.imageObj = new Image();
    that.imageObj.src = scene.image;
    that.imageObj.onload = function() {

        var mainScene = new IaScene(scene.width,scene.height);
        mainScene.scale = 1; 
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
            image: that.imageObj
        });

        var layers = [];
        that.layers = layers;
        layers[0] = new Kinetic.FastLayer();	
        layers[0].add(baseImage);
        stage.add(layers[0]);

        myhooks.beforeMainConstructor(mainScene, that.layers);

        var indice = 1;
        layers[indice] = new Kinetic.Layer();
        stage.add(layers[indice]);

        for (var i in details) {
            var iaObj = new IaObject(that.imageObj, details[i], layers[indice], "article-" + i, baseImage, mainScene, myhooks);
            mainScene.shapes.push(iaObj);
        }
        myhooks.afterMainConstructor(mainScene, that.layers);             
        $("#loader").hide();

        var viewportHeight = $(window).height();
        if (scene.description != "") {
            $("#rights").show();
            var content_offset = $("#rights").offset();
            var message_height = $("#popup_intro").css('height').substr(0,$("#popup_intro").css("height").length - 2);
            $("#popup_intro").css({'top':(viewportHeight - content_offset.top - message_height)/ 2 - 40});
            $("#popup_intro").show();
            $("#popup").hide();
            $("#popup_close_intro").on("click", function(){
                $("#rights").hide();
            });            
        }


        // FullScreen ability
        // source code from http://blogs.sitepointstatic.com/examples/tech/full-screen/index.html
        var e = document.getElementById("title");
        var div_container = document.getElementById("image-active");
        e.onclick = function() {
            if (runPrefixMethod(document, "FullScreen") || runPrefixMethod(document, "IsFullScreen")) {
                runPrefixMethod(document, "CancelFullScreen");
            }
            else {
                runPrefixMethod(div_container, "RequestFullScreen");
            }
            mainScene.fullScreen = mainScene.fullScreen == "on" ? "off": "on";
        };

        var pfx = ["webkit", "moz", "ms", "o", ""];
        function runPrefixMethod(obj, method) {
            var p = 0, m, t;
            while (p < pfx.length && !obj[m]) {
                m = method;
                if (pfx[p] === "") {
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
        }       
        
        
    };    
}

myhooks = new hooks();
launch = new main(myhooks);
