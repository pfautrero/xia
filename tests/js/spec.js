import {XiaDetail} from './../../build/share/themes/game1clic/js/xia.js'

describe("Check XiaDetail init", function() {
    var iaObject = {
        jsonSource : {
            title : "A small path",
            options : "disable-click",
            fill : "#000000"
        },
    }
    var myDetail = new XiaDetail(iaObject, iaObject.jsonSource, "id of associated DOM ELEMENT")

    it("check title", function() {
        expect(myDetail.title).toBe("A small path")
    })
    it("check disable click", function() {
        expect(myDetail.click).toBe("off")
    })
    it("check disable zoom", function() {
        expect(myDetail.zoomable).toBe(false)
    })
    it("check idText", function() {
        expect(myDetail.idText).toBe("id of associated DOM ELEMENT")
    })
});

