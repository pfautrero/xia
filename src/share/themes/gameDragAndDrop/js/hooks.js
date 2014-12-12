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
 * @constructor init specific hooks
 */
function hooks() {
    "use strict";
}
/*
 * @param array layers
 * @param iaScene mainScene
 */
hooks.prototype.beforeMainConstructor = function(mainScene, layers) {

// a the very beginning, just before building objects

};

/*
 * @param iaScene mainScene
 * @param array layers
 */
hooks.prototype.afterMainConstructor = function(mainScene, layers) {

// after building objects, just before rendering scene
    
};
/*
 *
 *  
 */
hooks.prototype.afterIaObjectConstructor = function(mainScene, idText, detail, iaObject) {



};


/*
 *
 *
 */
hooks.prototype.afterXiaObjectCreation = function(mainScene, xiaDetail) {

/*
    define your own events on xiaDetails
    have a look at XiaDetail object for further informations

    example :

    xiaDetail.kineticElement.on('mousedown', function(){
        console.log("mousedown");

        // remove cache
        this.scale({x:1,y:1});
        this.clearCache();

        // add blue border
        this.stroke("blue");

        // enable cache
        this.cache({width:this.width(), height:this.height()});
        this.scale({x:mainScene.coeff,y:mainScene.coeff});
        this.drawHitFromCache();

        // redraw scene
        this.getIaObject().layer.draw();
    });

*/


};


/*
 *
 *  
 */
hooks.prototype.afterDragStart = function(mainScene, idText, kineticElement) {

// kineticElement.getXiaParent() -> get reference to xiaDetail object
// kineticElement.getIaObject() -> get reference to iaobject
// $('#' + idText) is the DOM element linked to kineticElement
};
/*
 *
 *  
 */
hooks.prototype.afterDragEnd = function(mainScene, idText, kineticElement) {

// kineticElement.getXiaParent() -> get reference to xiaDetail object
// kineticElement.getIaObject() -> get reference to iaobject
// $('#' + idText) is the DOM element linked to kineticElement

};

