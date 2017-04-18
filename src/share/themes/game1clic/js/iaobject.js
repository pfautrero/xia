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

    this.jsonSource.maxX = parseFloat(this.jsonSource.maxX)
    this.jsonSource.minX = parseFloat(this.jsonSource.minX)
    this.jsonSource.maxY = parseFloat(this.jsonSource.maxY)
    this.jsonSource.minY = parseFloat(this.jsonSource.minY)

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
        that.includePath(params.detail, 0, params.idText);
    }
    else if (typeof(params.detail.image) !== 'undefined') {
        var re = /sprite(.*)/i;
        if (params.detail.id.match(re)) {
            that.includeSprite(params.detail, 0, params.idText);
        }
        else {
            that.includeImage(params.detail, 0, params.idText);
        }
    }
    else if (typeof(params.detail.group) !== 'undefined') {
        for (var i in params.detail.group) {
            if (typeof(params.detail.group[i].path) !== 'undefined') {
                that.includePath(params.detail.group[i], i, params.idText);
            }
            else if (typeof(params.detail.group[i].image) !== 'undefined') {
                var re = /sprite(.*)/i;
                if (params.detail.group[i].id.match(re)) {
                    that.includeSprite(params.detail.group[i], i, params.idText);
                }
                else {
                    that.includeImage(params.detail.group[i], i, params.idText);
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
IaObject.prototype.includeSprite = function(detail, i, idDOMElement) {

    this.defineImageBoxSize(detail, this);
    this.xiaDetail[i] = new XiaSprite(this, detail, idDOMElement)
    this.xiaDetail[i].start()

};

/*
 *
 * @param {type} detail
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includeImage = function(detail, i, idDOMElement) {

    this.defineImageBoxSize(detail, this);
    this.xiaDetail[i] = new XiaImage(this, detail, idDOMElement)
    this.xiaDetail[i].start()

};


/*
 *
 * @param {type} path
 * @param {type} i KineticElement index
 * @returns {undefined}
 */
IaObject.prototype.includePath = function(detail, i, idDOMElement) {

    this.definePathBoxSize(detail, this);
    this.xiaDetail[i] = new XiaPath(this, detail, idDOMElement)
    this.xiaDetail[i].start()

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

