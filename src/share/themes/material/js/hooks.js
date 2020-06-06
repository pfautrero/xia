class CroppedImage {
  constructor (params) {


    this.src = params.src
    this.id = params.id
    this.scale = params.scale
    this.left = params.left
    this.top = params.top

    this.origin = {
      top: this.top,
      left: this.left,
      scale: this.scale
    }

    var cropedImage = new Image()
    cropedImage.onload = function() {
      this.origin.height = cropedImage.naturalHeight
      this.origin.width = cropedImage.naturalWidth
      this.width = cropedImage.naturalWidth * this.scale
      this.height = cropedImage.naturalHeight * this.scale
      var newImage = document.createElement('img')
      newImage.setAttribute('id', this.id)
      newImage.classList.add('popup_material_image')
      newImage.classList.add('hidden_image')
      newImage.setAttribute('src', this.src)
      newImage.setAttribute('style', 'transform: scale({SCALE}); left: {LEFT}px; top: {TOP}px;'
        .replace('{SCALE}', this.scale)
        .replace('{LEFT}', this.left)
        .replace('{TOP}', this.top)
      )
      this.domElement = newImage
      document.getElementById('popup_material_image_background').appendChild(newImage)
    }.bind(this)
    cropedImage.src = this.src
    this.img = cropedImage

  }
  setVisible(){
    //var visibleImage = document.getElementById(this.id)
    //visibleImage.classList.remove('hidden_image')
    this.domElement.classList.remove('hidden_image')
  }
  moveTo(params){
    //var visibleImage = document.getElementById(this.id)
    //var section = visibleImage.parentNode.parentNode

    this.domElement.setAttribute('style',
      'top:{TOP}px;left:{LEFT}px;transform: scale({SCALE});'
      .replace('{TOP}', params.top)
      .replace('{LEFT}', params.left)
      .replace('{SCALE}', params.scale)
    )
    this.width = this.origin.width * params.scale
    this.height = this.origin.height * params.scale

  }
  reset(){
    //var visibleImage = document.getElementById(this.id)
    this.domElement.setAttribute('style',
      'top:{TOP}px;left:{LEFT}px;transform: scale({SCALE});'
      .replace('{TOP}', this.origin.top)
      .replace('{LEFT}', this.origin.left)
      .replace('{SCALE}', this.origin.scale)
    )
    this.width = this.origin.width * this.origin.scale
    this.height = this.origin.height * this.origin.scale
  }
}

class MyApp {
  constructor (params) {
    this.article = {
      wrapper : params.wrapper,
      title : params.header
    }
    this.fullscreen = params.fullscreen
    this.reload = params.reload
    this.ripple = params.ripple
    this.already_loaded = false
    this.images = []
  }
  rescale (xiaObject) {
    setTimeout(function(){
      this.mainScene.scaleScene(this)
      this.restart()
    }.bind(xiaObject), 200)
  }
  _fullScreenAbility (xiaObject) {
    document.getElementById(this.fullscreen).addEventListener('click', function() {
      this._toggleFullScreen()
    }.bind(this), false)
    document.addEventListener('fullscreenchange', function () {
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
    document.addEventListener('mozfullscreenchange', function () {
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
    document.addEventListener('webkitfullscreenchange', function () {
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
  }
  _toggleFullScreen () {
    if (!document.fullscreenElement &&    // alternative standard method
      !document.mozFullScreenElement && !document.webkitFullscreenElement) {  // current working methods
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen()
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen()
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
      }
    } else {
      if (document.cancelFullScreen) {
        document.cancelFullScreen()
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen()
      } else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen()
      }
    }
  }

  apply_filter (params) {
    var target_pattern = params.target
    var handler = params.handler
    var targets = document.querySelectorAll(target_pattern)
    targets.forEach(function(target){
      handler(target)
    })
  }

  //
  // called during Zoom method
  // We show the article content
  // about zoomed detail
  //

  button_click () {
    var target = this.dataset.target
    var password_hash = this.dataset.password
    var response = document.getElementById('response_' + target)
    var form = document.getElementById('form_' + target)
    //if (response.style.display == 'none') response.innerHTML = response.dataset.encrypted_content
    response.style.display = (response.style.display == 'none') ? 'block' : 'none'
  }
  unlock_input (e) {
    e.preventDefault()
    var entered_password = this.parentNode.querySelector('input[type=text]').value
    var hash_password = this.dataset.password
    var target = this.dataset.target
    var response = document.getElementById('response_' + target)
    var form = document.getElementById('form_' + target)
    var sha1Digest= new createJs(true)
    sha1Digest.update(entered_password.encode())
    var hash = sha1Digest.digest()
    if (hash == hash_password) {
      var encrypted_content = response.innerHTML
      response.dataset.encrypted_content = encrypted_content
      response.innerHTML = XORCipher.decode(entered_password, encrypted_content).decode()
      response.style.display = 'block'
      form.style.display = 'none'
    }
  }


  //
  // Show popup
  //
  update_content(title, desc) {
    document.getElementById("popup_material").classList.add('visible')
    // remove child nodes
    // We suppose attached events are removed implicitly
    while (this.article.wrapper.firstChild)
      this.article.wrapper.removeChild(this.article.wrapper.firstChild)

    // retrieve title and description
    this.article.wrapper.innerHTML = desc
    this.article.title.innerHTML = title
    //this.load_embed_contents()
    this.apply_filter({
      target : '[data-iframe]',
      handler : function(target){
        var source = target.dataset.iframe
        var iframe = document.createElement('iframe')
        iframe.src = source
        target.append(iframe)
      }
    })

    this.apply_filter({
      target : '.flickr_oembed',
      handler : function(target){
        var source = target.dataset.oembed
        var jsonp_handler = function(data){
          var url = data.url
          var newimg = document.createElement('img')
          newimg.src = url
          target.append(newimg)
        }
        var script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = 'https://www.flickr.com/services/oembed/?jsoncallback=jsonp_handler&format=json&url=' + source
        document.getElementsByTagName('head')[0].appendChild(script)
      }
    })

    this.apply_filter({
      target : '.button',
      handler : function(button){
        var password_hash = button.dataset.password
        if (password_hash) {
          var target = button.dataset.target
          var form = document.getElementById('form_' + target)
          form.style.display = 'flex'
          var input = document.querySelector('#form_' + target + ' input[type=text]')
          input.value=""
          input.focus()
        }
        else {
          button.addEventListener('click', this.button_click)
          button.addEventListener('touchstart', this.button_click)
        }
      }.bind(this)
    })

    this.apply_filter({
      target : '.unlock input[type=submit]',
      handler : function(unlock_button){
        unlock_button.addEventListener('click', this.unlock_input)
        unlock_button.addEventListener('touchstart', this.unlock_input)
      }.bind(this)
    })
  }

  mouseover(el) {

    var zoomed = (el.parent.iaScene.cursorState.includes('ZoomOut.cur'))
    var focused_zoomable = (el.parent.iaScene.cursorState.includes('ZoomIn.cur'))
    var focused_unzoomable = (el.parent.iaScene.cursorState.includes('ZoomFocus.cur'))
    var overflown = (el.parent.iaScene.cursorState.includes('HandPointer.cur'))

    if (zoomed || focused_zoomable || focused_unzoomable || overflown) return

    document.body.style.cursor = 'pointer'
    el.parent.iaScene.cursorState = 'url(img/HandPointer.cur),auto'

    var cacheBackground = true
    for (let i in el.parent.xiaDetail) {
      var xiaDetail = el.parent.xiaDetail[i]
      var kineticElement = xiaDetail.kineticElement
      var objectType = kineticElement.getClassName()
      if (objectType === 'Sprite') {
        kineticElement.animation('idle')
        kineticElement.frameIndex(0)
        kineticElement.setAttrs({ opacity: 0 })
        kineticElement.to({ opacity: 1 })
      } else if (objectType === 'Image') {
        if (xiaDetail.persistent === 'on') cacheBackground = false
        kineticElement.setImage(kineticElement.backgroundImage)
        kineticElement.setAttrs({ opacity: 0 })
        kineticElement.to({ opacity: 1 })
      } else {
        kineticElement.fillPriority('color')
        kineticElement.stroke(xiaDetail.parent.iaScene.overColorStroke)
        kineticElement.strokeWidth(5) //xiaDetail.strokeWidth)
        kineticElement.dashEnabled()
        kineticElement.dash([10,10])
        kineticElement.setAttrs({ opacity: 1 })
        //kineticElement.to({ opacity: 1 })
      }
    }
    el.parent.layer.moveToTop()
    el.parent.layer.draw()
    el.parent.parent.focusedObj = el.parent.index

    return false
  }

  //
  // hook for Xia Zoom
  //
  zoom(el) {
    this.xiaObject = el.parent
    this.xiaDetail = el
    var container = document.getElementById('canvas').firstChild.getBoundingClientRect()
    var pointer = el.parent.layer.getStage().getPointerPosition()
    if (typeof(pointer) == "undefined") {
      pointer = {
        x: 0,
        y: 0
      }
    }
    var div = document.createElement('div')
    div.setAttribute('id', 'ripple-effect')
    div.setAttribute('style',
      'top:{TOP}px;left:{LEFT}px;'
      .replace('{TOP}', pointer.y - 25 + container.top)
      .replace('{LEFT}', pointer.x - 25 + container.left))
    this.ripple.appendChild(div)
    window.setTimeout(function(){
      this.ripple.removeChild(this.ripple.firstChild)
    }.bind(this), 1100)

    this.images[this.xiaObject.idText].setVisible()
    this.update_content(el.title, el.desc)
    return false
  }

  manageKeydownEvent(XiaObject) {
    var container = XiaObject.stage.container()
    container.addEventListener('keydown', function (e) {
      if (e.shiftKey && (e.key === 'Tab')) {
        if (XiaObject.mainScene.zoomActive === 1) {
          e.preventDefault()
          return
        }
        if (XiaObject.focusedObj !== null) {
          XiaObject.focusedObj--
          if (XiaObject.focusedObj >= 0) {
            XiaObject.iaObjects[XiaObject.focusedObj + 1].xiaDetail[0].kineticElement.fire('mouseleave')
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('mouseover')
            e.preventDefault()
          } else {
            XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire('mouseleave')
            XiaObject.focusedObj = null
          }
        } else {
          XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire('mouseover')
          e.preventDefault()
        }
      } else if (e.key === 'Tab') {
        if (XiaObject.mainScene.zoomActive === 1) {
          e.preventDefault()
          return
        }
        if (XiaObject.focusedObj !== null) {
          XiaObject.focusedObj++
          if (XiaObject.focusedObj < XiaObject.iaObjects.length) {
            XiaObject.iaObjects[XiaObject.focusedObj - 1].xiaDetail[0].kineticElement.fire('mouseleave')
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('mouseover')
            e.preventDefault()
          } else {
            XiaObject.iaObjects[XiaObject.iaObjects.length - 1].xiaDetail[0].kineticElement.fire('mouseleave')
            XiaObject.focusedObj = null
          }
        } else {
          XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire('mouseover')
          e.preventDefault()
        }
      } else if (e.key === 'Enter') {
        if (XiaObject.focusedObj !== null) {
          var mouseover = false
          if (XiaObject.mainScene.zoomActive === 1) mouseover = true
          XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('click')
          if (mouseover) XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('mouseover')
        }
      } else if (e.key === 'Escape') {
        e.preventDefault()
        document.getElementById("popup_material_delete").click()
        if (XiaObject.focusedObj !== null) {
          if (XiaObject.mainScene.zoomActive === 1) {
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('click')
          } else {
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire('mouseleave')
          }
          XiaObject.focusedObj = null
        }
      }
    })
  }

  createAboutButton(XiaObject) {
    var target = document.getElementById('canvas').firstChild
    var about = document.createElement('div')
    about.setAttribute('id', 'about')
    target.appendChild(about)
    var about_button = document.createElement('a')
    about_button.setAttribute('class', 'infos')
    about.appendChild(about_button)
    about.addEventListener('click', function(){
      this.update_content(document.getElementById("title").innerHTML, document.getElementById("metadata").innerHTML)
    }.bind(this))
  }

  createMetadocButton(XiaObject) {
    var target = document.getElementById('canvas').firstChild
    var metadoc = document.createElement('div')
    metadoc.setAttribute('id', 'general_infos')
    target.appendChild(metadoc)
    var metadoc_button = document.createElement('a')
    metadoc_button.setAttribute('class', 'meta-doc')
    metadoc.appendChild(metadoc_button)
    metadoc.addEventListener('click', function(){
      this.update_content(XiaObject.params.scene.title, XiaObject.params.scene.intro_detail)
    }.bind(this))
  }
  //
  // hook for Xia Loaded
  //
  loaded(XiaObject) {

    // Do not execute following code twice
    if (this.already_loaded) return
    this.already_loaded = true

    this.manageKeydownEvent(XiaObject)
    this.createAboutButton(XiaObject)
    this.createMetadocButton(XiaObject)

    //
    //  When user click on popup title
    //  Zoom image
    //

    document.getElementById('popup_material_title').addEventListener('click', function(){

      if (this.xiaObject == null) return
      var container = document.getElementById("popup_material_background")

      document.getElementById("popup_material_image_background").setAttribute('style',
        'background-color: black;pointer-events: auto;'
      )

      var current = {
        height: this.images[this.xiaObject.idText].height,
        width: this.images[this.xiaObject.idText].width,
        scale: this.images[this.xiaObject.idText].height / this.images[this.xiaObject.idText].origin.height
      }

      let target = {
        height: container.offsetHeight,
        width: container.offsetWidth
      }

      var minScale = Math.min(
        target.height / current.height,
        target.width / current.width
      )

      this.images[this.xiaObject.idText].moveTo({
        top: (target.height - minScale * current.height) / 2,
        left: (target.width - minScale * current.width) / 2,
        scale: minScale * current.scale
      })

    }.bind(this))

    //
    // Unzoom image
    // When user click on screen to unzoom image
    //
    document.getElementById('popup_material_image_background').addEventListener('click', function(event){
      document.getElementById('popup_material_image_background').setAttribute('style','background-color: none;pointer-events: none;')

      var popup_material = document.getElementById("popup_material")
      var popup_material_title = document.getElementById("popup_material_title")

      if (popup_material.offsetTop > document.getElementById(this.xiaObject.parent.params.targetID).offsetHeight) {
        this.images[this.xiaObject.idText].reset()
      } else {
        var currentHeight = this.images[this.xiaObject.idText].origin.height * this.xiaObject.iaScene.coeff
        var currentWidth = this.images[this.xiaObject.idText].origin.width * this.xiaObject.iaScene.coeff

        let target = {
          height: popup_material_title.offsetHeight,
          width: popup_material_title.offsetWidth / 4
        }

        var minScale = Math.min(
          target.height / currentHeight,
          target.width / currentWidth
        )

        this.images[this.xiaObject.idText].moveTo({
          top: ((target.height - minScale * currentHeight) / 2) + popup_material.offsetTop,
          left: ((target.width - minScale * currentWidth) / 2) + popup_material.offsetLeft,
          scale: this.xiaObject.iaScene.coeff * minScale
        })
      }

      event.stopPropagation()
    }.bind(this))

    //
    // When user click on top right corner cross of popup
    //Close popup
    //

    document.getElementById('popup_material_delete').addEventListener('click', function(event){
      document.getElementById("popup_material").classList.remove('visible')
      var targets = document.querySelectorAll('.popup_material_image')
      targets.forEach(function(target){
        target.classList.add('hidden_image')
      })
      if (this.xiaObject != null) {
        this.images[this.xiaObject.idText].reset()
        this.xiaObject.iaScene.zoomActive = 0
        this.xiaObject.group.zoomActive = 0
        this.xiaObject.group.scaleX(1)
        this.xiaObject.group.scaleY(1)
        this.xiaObject.group.x(this.originalX)
        this.xiaObject.group.y(this.originalY)
        this.xiaDetail.reset_state_all(this.xiaObject.xiaDetail)
        this.xiaObject.layer.draw()
        this.xiaObject.backgroundCache_layer.to({ opacity: 0 })
        this.xiaObject.iaScene.cursorState = 'default'
        this.xiaObject.iaScene.element = null
        document.body.style.cursor = 'default'
        this.xiaObject.parent.reorderItems()

      }
      event.stopPropagation()
    }.bind(this))

    //
    //  When popup appears
    //  Wait and finally move image to popup top left corner
    //

    document.getElementById("popup_material").addEventListener("transitionend", function(event) {
      if (this.xiaObject == null) return
      var popup_material = document.getElementById("popup_material")
      var popup_material_title = document.getElementById("popup_material_title")

      if (popup_material.offsetTop > document.getElementById(this.xiaObject.parent.params.targetID).offsetHeight) {
        this.images[this.xiaObject.idText].reset()
      } else {
        var currentHeight = this.images[this.xiaObject.idText].origin.height * this.xiaObject.iaScene.coeff
        var currentWidth = this.images[this.xiaObject.idText].origin.width * this.xiaObject.iaScene.coeff

        let target = {
          height: popup_material_title.offsetHeight,
          width: popup_material_title.offsetWidth / 4
        }

        var minScale = Math.min(
          target.height / currentHeight,
          target.width / currentWidth
        )


        this.images[this.xiaObject.idText].moveTo({
          top: ((target.height - minScale * currentHeight) / 2) + popup_material.offsetTop,
          left: ((target.width - minScale * currentWidth) / 2) + popup_material.offsetLeft,
          scale: this.xiaObject.iaScene.coeff * minScale
        })
     }

    }.bind(this), false);

  }

  //
  // hook for Xia Constructor
  //
  afterIaObjectConstructor(scene, id, jsonDetail, xiaGroup) {


    // workaround to fix size image for standalone images with ratio different than the bg one
    if ((xiaGroup.xiaDetail.length == 1) && (typeof(xiaGroup.xiaDetail[0].path) == "undefined")){
      let currentDetail = xiaGroup.xiaDetail[0]
      let currentRatio = currentDetail.backgroundImage.naturalWidth / (currentDetail.detail.maxX - currentDetail.detail.minX)

      var container = document.getElementById('canvas').firstChild.getBoundingClientRect()
      this.images[id] = new CroppedImage({
          id: 'popup_material_image_' + id,
          src: xiaGroup.xiaDetail[0].backgroundImage.currentSrc,
          scale: scene.coeff / currentRatio,
          left: container.left + xiaGroup.minX,
          top: container.top + xiaGroup.minY
      })
      xiaGroup.backgroundImage = this.images[id].img

    }
    // grouped elements
    else {
      let groupedImages = document.createElement('canvas')
      groupedImages.setAttribute('width', scene.originalRatio * (parseFloat(xiaGroup.maxX / scene.coeff) - parseFloat(xiaGroup.minX / scene.coeff)))
      groupedImages.setAttribute('height', scene.originalRatio * (parseFloat(xiaGroup.maxY / scene.coeff) - parseFloat(xiaGroup.minY / scene.coeff)))
      for (let i = 0; i < xiaGroup.xiaDetail.length; i++) {
        let currentDetail = xiaGroup.xiaDetail[i]

        let currentRatio = scene.originalRatio

        // Let's suppose it is an image - use its own ratio
      	if (typeof(currentDetail.path) == "undefined") {
      	  currentRatio = currentDetail.backgroundImage.naturalWidth / (currentDetail.detail.maxX - currentDetail.detail.minX)
      	}

        let source = {
          'x': 0,
          'y': 0,
          'width':  currentRatio * (currentDetail.detail.maxX - Math.max(currentDetail.detail.minX, 0)),
          'height':  currentRatio * (currentDetail.detail.maxY - Math.max(currentDetail.detail.minY, 0))
        }

        let target = {
          'x' :  scene.originalRatio * (currentDetail.detail.minX - (xiaGroup.minX / scene.coeff)),
          'y' :  scene.originalRatio * (currentDetail.detail.minY - (xiaGroup.minY / scene.coeff)),
          'width':  scene.originalRatio * (currentDetail.detail.maxX - Math.max(currentDetail.detail.minX, 0)),
          'height':  scene.originalRatio * (currentDetail.detail.maxY - Math.max(currentDetail.detail.minY, 0))
        }


        if (currentDetail.kineticElement) {
          groupedImages.getContext('2d').drawImage(
            currentDetail.kineticElement.backgroundImage,
            source.x,
            source.y,
            source.width,
            source.height,
            target.x,
            target.y,
            target.width,
            target.height
          )
        }
      }

      var container = document.getElementById('canvas').firstChild.getBoundingClientRect()
      this.images[id] = new CroppedImage({
        id: 'popup_material_image_' + id,
        src: groupedImages.toDataURL(),
        scale: scene.coeff / scene.originalRatio,
        left: container.left + xiaGroup.minX,
        top: container.top + xiaGroup.minY
      })
      xiaGroup.backgroundImage = this.images[id].img
    }
  }
}
