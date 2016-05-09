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
 * 1rst layer : div "detect" - if clicked, enable canvas events
 * 2nd layer : bootstrap accordion
 * 3rd layer : div "canvas" containing images and paths
 * 4th layer : div "disablearea" - if clicked, disable events canvas
 */

function main(myhooks) {
    "use strict";
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

        // cache used over background image
        var baseCache = new Kinetic.Rect({
            x: 0,
            y: mainScene.y,
            width: scene.width,
            height: scene.height,
            scale: {x:mainScene.coeff,y:mainScene.coeff},
            fill: mainScene.backgroundCacheColor
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
        var layers = [];
        that.layers = layers;
        layers[0] = new Kinetic.FastLayer();
        layers[1] = new Kinetic.FastLayer();
        layers[2] = new Kinetic.Layer();
        layers[3] = new Kinetic.Layer();
        layers[4] = new Kinetic.Layer();

        layers[0].add(baseCache);
        layers[1].add(baseImage);
        layers[2].add(disableArea);
        stage.add(layers[0]);
        stage.add(layers[1]);
        stage.add(layers[2]);
        stage.add(layers[3]);
        stage.add(layers[4]);
        myhooks.beforeMainConstructor(mainScene, that.layers);

        for (var i in details) {
            var iaObj = new IaObject({
                imageObj: that.imageObj,
                detail: details[i],
                layer: layers[4],
                idText: "article-" + i,
                baseImage: baseImage,
                iaScene: mainScene,
                background_layer: layers[1],
                backgroundCache_layer: layers[0],
                zoomLayer: layers[3],
                myhooks: myhooks
            });
        }

        myhooks.afterMainConstructor(mainScene, that.layers);

        $("#splash").fadeOut("slow", function(){
                $("#loader").hide();
        });
        
    };
}

myhooks = new hooks();
launch = new main(myhooks);
