import {XiaDetail} from './../../build/share/themes/game1clic/js/xia.js'
import {XiaImage} from './../../build/share/themes/game1clic/js/xia.js'
import {XiaSprite} from './../../build/share/themes/game1clic/js/xia.js'

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

describe("Check XiaImage init", function() {
    var iaScene = {
        scale : 2
    }

    var iaObject = {
        jsonSource : {
            title : "A small image",
            options : "disable-click",
            fill : "#000000",
            width : 200,
            height: 100
        },
        iaScene : iaScene
    }
    var myDetail = new XiaImage(iaObject, iaObject.jsonSource, "id of associated DOM ELEMENT")

    it("check title", function() {
        expect(myDetail.title).toBe("A small image")
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
    it("check dimensions", function() {
        expect(myDetail.width).toBe(400)
        expect(myDetail.height).toBe(200)
    })
    it("check persistent", function() {
        expect(myDetail.persistent).toBe("off")
    })
});

describe("Check XiaSprite init", function() {
    var iaScene = {
        scale : 2
    }

    var iaObject = {
        jsonSource : {
            title : "A small sprite",
            options : "disable-click",
            fill : "#000000",
            width : 200,
            height: 100,
            timeline : "0,1,2,3,1,2,2,2,2,2,2,3,3,3"
        },
        iaScene : iaScene
    }
    var myDetail = new XiaSprite(iaObject, iaObject.jsonSource, "id of associated DOM ELEMENT")

    it("check title", function() {
        expect(myDetail.title).toBe("A small sprite")
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
    it("check dimensions", function() {
        expect(myDetail.width).toBe(400)
        expect(myDetail.height).toBe(200)
    })
    it("check persistent", function() {
        expect(myDetail.persistent).toBe("hiddenSprite")
    })
    it("check timeline", function() {
        expect(myDetail.idle).toEqual([ 0, 0, 200, 100, 200, 0, 200, 100, 400, 0, 200, 100, 600, 0, 200, 100, 200, 0, 200, 100, 400, 0, 200, 100, 400, 0, 200, 100, 400, 0, 200, 100, 400, 0, 200, 100, 400, 0, 200, 100, 400, 0, 200, 100, 600, 0, 200, 100, 600, 0, 200, 100, 600, 0, 200, 100 ])
    })

});