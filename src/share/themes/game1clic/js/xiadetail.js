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
 */
class XiaDetail {
  constructor(parent, detail, idText) {
    this.parent = parent
    this.detail = detail
    this.idText = idText
    this.click = "on"
    this.title = this.parent.jsonSource.title
    this.path = ""
    this.kineticElement = null
    this.persistent = ""
    this.options = ""
    this.backgroundImage = null
    this.tooltip = ""
    this.zoomable = true

    if ((typeof(this.parent.jsonSource.options) !== 'undefined')) {
        this.options = this.parent.jsonSource.options
    }
    if (this.options.indexOf("disable-click") !== -1) {
        this.click = "off"
    }
    if ((typeof(this.parent.jsonSource.fill) !== 'undefined') &&
        (this.parent.jsonSource.fill === "#000000")) {
        this.zoomable = false;
    }
  }

  manageDropAreaAndTooltips() {
    // tooltip must be at the bottom
    if ($('article[data-tooltip="' + $("#" + this.idText).data("kinetic_id") + '"]').length != 0) {
        this.kineticElement.getParent().moveToBottom();
        this.options += " disable-click ";
        this.kineticElement.tooltip_area = true;
        // disable hitArea for tooltip
        this.kineticElement.hitFunc(function(context){
            context.beginPath();
            context.rect(0,0,0,0);
            context.closePath();
            context.fillStrokeShape(this);
        });
    }
  }
}

if (typeof module !== 'undefined' && module.exports != null) {
    exports.XiaDetail = XiaDetail
}
