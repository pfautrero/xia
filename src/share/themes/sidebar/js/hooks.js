class MyApp {
  constructor (params) {
    this.article = {
      wrapper: document.getElementById(params.wrapper),
      footer: params.footer,
      scrolldown_button: document.getElementById(params.scrolldown_button),
      template: `
        <header id='{ID_HEADER}' aria-label='titre'>{TITLE}</header>
        <section id='{ID_CONTENT}' aria-label='description'>{DESCRIPTION}</section>
        <footer id='{ID_FOOTER}'></footer>
        `
        .replace('{ID_HEADER}', params.header)
        .replace('{ID_CONTENT}', params.content)
        .replace('{ID_FOOTER}', params.footer)
    }
    this.sidebar = document.getElementById(params.sidebar)
    this.alert_mouseover = document.getElementById(params.alert_mouseover)
    this.fullscreen = params.fullscreen
    this.reload = params.reload
    this.already_loaded = false
  }
  rescale (xiaObject) {
    setTimeout(function () {
      this.mainScene.scaleScene(this)
      this.restart()
    }.bind(xiaObject), 200)
  }
  _fullScreenAbility (xiaObject) {
    document.getElementById(this.fullscreen).addEventListener('click', function () {
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
    if (!document.fullscreenElement && // alternative standard method
      !document.mozFullScreenElement && !document.webkitFullscreenElement) { // current working methods
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen()
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen()
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT)
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

  applyFilter (params) {
    var targetPattern = params.target
    var handler = params.handler
    var targets = document.querySelectorAll(targetPattern)
    targets.forEach(function (target) {
      handler(target)
    })
  }

  //
  // called during Zoom method
  // We show the article content
  // about zoomed detail
  //

  buttonClick () {
    var target = this.dataset.target
    // var password_hash = this.dataset.password
    var response = document.getElementById('response_' + target)
    // var form = document.getElementById('form_' + target)
    //if (response.style.display === 'none') response.innerHTML = response.dataset.encrypted_content
    response.style.display = (response.style.display === 'none') ? 'block' : 'none'
  }
  unlockInput (e) {
    e.preventDefault()
    var enteredPassword = this.parentNode.querySelector('input[type=text]').value
    var hashPassword = this.dataset.password
    var target = this.dataset.target
    var response = document.getElementById('response_' + target)
    var form = document.getElementById('form_' + target)
    var sha1Digest = new createJs(true)
    sha1Digest.update(enteredPassword.encode())
    var hash = sha1Digest.digest()
    if (hash === hashPassword) {
      var encryptedContent = response.innerHTML
      response.dataset.encrypted_content = encryptedContent
      response.innerHTML = XORCipher.decode(enteredPassword, encryptedContent).decode()
      response.style.display = 'block'
      form.style.display = 'none'
    }
  }

  updateContent (title, desc) {
    // remove child nodes
    // We suppose attached events are removed implicitly
    while (this.article.wrapper.firstChild) {
      this.article.wrapper.removeChild(this.article.wrapper.firstChild)
    }

    // retrieve title and description
    this.article.wrapper.innerHTML = this.article.template
      .replace('{TITLE}', title)
      .replace('{DESCRIPTION}', desc)

    // this.load_embed_contents()
    this.applyFilter({
      target: '[data-iframe]',
      handler: function (target) {
        var source = target.dataset.iframe
        var iframe = document.createElement('iframe')
        iframe.src = source
        target.append(iframe)
      }
    })

    this.applyFilter({
      target: '.flickr_oembed',
      handler: function (target) {
        var source = target.dataset.oembed
        var jsonpHandler = function (data) {
          var url = data.url
          var newimg = document.createElement('img')
          newimg.src = url
          target.append(newimg)
        }
        var script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = 'https://www.flickr.com/services/oembed/?jsoncallback=jsonpHandler&format=json&url=' + source
        document.getElementsByTagName('head')[0].appendChild(script)
      }
    })

    this.applyFilter({
      target: '.button',
      handler: function (button) {
        var passwordHash = button.dataset.password
        if (passwordHash) {
          var target = button.dataset.target
          var form = document.getElementById('form_' + target)
          form.style.display = 'flex'
          var input = document.querySelector('#form_' + target + ' input[type=text]')
          input.value = ''
          input.focus()
        } else {
          button.addEventListener('click', this.buttonClick)
          button.addEventListener('touchstart', this.buttonClick)
        }
      }.bind(this)
    })

    this.applyFilter({
      target: '.unlock input[type=submit]',
      handler: function (unlockButton) {
        unlockButton.addEventListener('click', this.unlockInput)
        unlockButton.addEventListener('touchstart', this.unlockInput)
      }.bind(this)
    })

    // this.handle_question()
    // show article
    this.article.wrapper.style.opacity = 1
    var box = this.article.wrapper.getBoundingClientRect()
    this.article.wrapper.scrollBy({
      top: box.height * (-1),
      behavior: 'auto'
    })
  }
  //
  // hook for Xia Mouseover
  //
  mouseover (el) {
    // for accessibility feature
    this.alert_mouseover.innerHTML = el.title
  }
  //
  // hook for Xia Zoom
  //
  zoom (el) {
    var delay = 0
    if (this.article.wrapper.style.opacity === 1) {
      this.article.wrapper.style.opacity = 0
      delay = 500
    }
    setTimeout(function () {
      this.updateContent(el.title, el.desc)
      this.manageScrolldownButton()
    }.bind(this), delay)
    // return false
  }
  //
  // hook for Xia Unzoom
  //
  unzoom (el) {
    this.article.scrolldown_button.style.opacity = 0
    this.updateContent(
      el.parent.parent.params.scene.intro_title,
      el.parent.parent.params.scene.intro_detail)
    // this.article.wrapper.style.opacity = 0
    // return false
  }
  //
  // called when clicking on arrow to scroll down article
  //
  scrolldown (event) {
    var article = this.article.wrapper.getBoundingClientRect()
    this.article.wrapper.scrollBy({
      top: article.height / 2,
      behavior: 'smooth'
    })
    event.stopPropagation()
  }
  manageScrolldownButton () {
    setTimeout(function () {
      var bottom = document.getElementById(this.article.footer).getBoundingClientRect()
      var article = this.article.wrapper.getBoundingClientRect()
      var sidebar = this.sidebar.getBoundingClientRect()
      if (article.height < bottom.top) {
        this.article.scrolldown_button.style.top = '{TOP}px'
          .replace('{TOP}', article.height - 40)
        this.article.scrolldown_button.style.left = '{LEFT}px'
          .replace('{LEFT}', sidebar.width / 2 - 15)
        this.article.scrolldown_button.style.opacity = 1
      }
    }.bind(this), 500)
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

  /*
   * Stop events bubbling if you click in the sidebar
   * to avoid unzoom effect
   */
  stopPropagation() {
    document.getElementById('sidebar').addEventListener('click', function (e) {
      e.stopPropagation()
    })
  }

  //
  // hook for Xia Loaded
  //
  loaded (XiaObject) {
    // show title and main description
    this.updateContent(
      XiaObject.params.scene.intro_title,
      XiaObject.params.scene.intro_detail)

    // Do not execute following code twice
    if (this.already_loaded) return
    this.already_loaded = true

    this.stopPropagation()
    this.manageKeydownEvent(XiaObject)
    this.manageScrolldownButton()
    // Choose color background
    var quantizeImage = new Quantization()
    quantizeImage.setImage(XiaObject.imageObj)
    var dominantColor = quantizeImage.getDominantColor()
    document.getElementById(XiaObject.params.targetID).style.backgroundColor = 'rgba(RED, GREEN, BLUE, 255)'
      .replace('RED', dominantColor.red)
      .replace('GREEN', dominantColor.green)
      .replace('BLUE', dominantColor.blue)

    // binding events
    this._fullScreenAbility(XiaObject)
    document.getElementById(this.reload).addEventListener('click', function (e) {
      this.restart()
      e.preventDefault()
    }.bind(XiaObject))
    this.article.scrolldown_button.addEventListener('click', this.scrolldown.bind(this))
    this.article.scrolldown_button.addEventListener('touchstart', this.scrolldown.bind(this))
    this.article.scrolldown_button.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') this.scrolldown(e)
    }.bind(this))
  }
}
