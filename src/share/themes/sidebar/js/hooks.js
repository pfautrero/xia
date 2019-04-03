class MyApp {
  constructor(params){
    this.article = {
      wrapper : document.getElementById(params.wrapper),
      footer : params.footer,
      scrolldown_button : document.getElementById(params.scrolldown_button),
      template : `
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
  rescale(xiaObject){
    setTimeout(function(){
      this.mainScene.scaleScene(this)
      this.restart()
    }.bind(xiaObject), 200)
  }
  _fullScreenAbility(xiaObject) {
    document.getElementById(this.fullscreen).addEventListener("click", function() {
      this._toggleFullScreen()
    }.bind(this), false)
    document.addEventListener("fullscreenchange", function(){
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
    document.addEventListener("mozfullscreenchange", function(){
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
    document.addEventListener("webkitfullscreenchange", function(){
      this.rescale(xiaObject)
    }.bind(this, xiaObject), false)
  }
  _toggleFullScreen() {
    if (!document.fullscreenElement &&    // alternative standard method
      !document.mozFullScreenElement && !document.webkitFullscreenElement) {  // current working methods
      if (document.documentElement.requestFullscreen) {
        document.documentElement.requestFullscreen();
      } else if (document.documentElement.mozRequestFullScreen) {
        document.documentElement.mozRequestFullScreen();
      } else if (document.documentElement.webkitRequestFullscreen) {
        document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
      }
    } else {
      if (document.cancelFullScreen) {
        document.cancelFullScreen();
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen();
      }
    }
  }

  handle_question() {
    var button_click = function() {
      var target = this.dataset.target
      var password_hash = this.dataset.password
      var response = document.getElementById("response_" + target)
      var form = document.getElementById("form_" + target)
      if (response.style.display == "none") response.innerHTML = response.dataset.encrypted_content
      response.style.display = (response.style.display == "none") ? "block" : "none"

    }
    var unlock_input = function(e) {
      e.preventDefault()
      var entered_password = this.parentNode.querySelector('input[type=text]').value
      var hash_password = this.dataset.password
      var target = this.dataset.target
      var response = document.getElementById("response_" + target)
      var form = document.getElementById("form_" + target)
      var sha1Digest= new createJs(true)
      sha1Digest.update(entered_password.encode())
      var hash = sha1Digest.digest()
      if (hash == hash_password) {
        var encrypted_content = response.innerHTML
        response.dataset.encrypted_content = encrypted_content
        response.innerHTML = XORCipher.decode(entered_password, encrypted_content).decode()
        response.style.display = "block"
        form.style.display = "none"
      }
    };
    var buttons = document.querySelectorAll(".button")
    buttons.forEach(function(button){
      var password_hash = button.dataset.password
      if (password_hash) {
        var target = button.dataset.target
        var form = document.getElementById("form_" + target)
        form.style.display = "flex"
        var input = document.querySelector("#form_" + target + " input[type=text]")
        input.value=""
        input.focus()
      }
      else {
        button.addEventListener("click", button_click)
        button.addEventListener("touchstart", button_click)
      }

    })
    var unlock_buttons = document.querySelectorAll(".unlock input[type=submit]")
    unlock_buttons.forEach(function(unlock_button){
      unlock_button.addEventListener("click", unlock_input)
      unlock_button.addEventListener("touchstart", unlock_input)
    })
  }

  //
  // called during Zoom method
  // We show the article content
  // about zoomed detail
  //
  update_content(title, desc) {

    // remove child nodes
    // We suppose attached events are removed implicitly
    while (this.article.wrapper.firstChild)
      this.article.wrapper.removeChild(this.article.wrapper.firstChild)

    // retrieve title and description
    this.article.wrapper.innerHTML = this.article.template
      .replace('{TITLE}', title)
      .replace('{DESCRIPTION}', desc)

    // load iframes
    var iframes = document.querySelectorAll("[data-iframe]")
    iframes.forEach(function(item){
      var source = item.dataset.iframe
      var iframe = document.createElement("iframe")
      iframe.src = source
      item.append(iframe)
    })
    // handle questions
    this.handle_question()

    // show article
    this.article.wrapper.style.opacity = 1
    var box = this.article.wrapper.getBoundingClientRect()
    this.article.wrapper.scrollBy({
      top: box.height * (-1),
      behavior: 'auto'
    });

  }
  //
  // hook for Xia Mouseover
  //
  mouseover(el) {
    // for accessibility feature
    this.alert_mouseover.innerHTML = el.title
  }
  //
  // hook for Xia Zoom
  //
  zoom(el) {
    var delay = 0
    if (this.article.wrapper.style.opacity == 1) {
      this.article.wrapper.style.opacity = 0
      delay = 500
    }
    setTimeout(function(){
      this.update_content(el.title, el.desc)
      this.manage_scrolldown_button()
    }.bind(this), delay)
    //return false
  }
  //
  // hook for Xia Unzoom
  //
  unzoom(el) {
    this.article.scrolldown_button.style.opacity = 0
    //this.article.wrapper.style.opacity = 0
    //return false
  }
  //
  // called when clicking on arrow to scroll down article
  //
  scrolldown(event){
    var article = this.article.wrapper.getBoundingClientRect()
    this.article.wrapper.scrollBy({
      top: article.height / 2,
      behavior: 'smooth'
    });
    event.stopPropagation()
  }
  manage_scrolldown_button(){
    setTimeout(function(){
      var bottom = document.getElementById(this.article.footer).getBoundingClientRect()
      var article = this.article.wrapper.getBoundingClientRect()
      var sidebar = this.sidebar.getBoundingClientRect()
      if (article.height < bottom.top) {
        this.article.scrolldown_button.style.top = "{TOP}px"
          .replace("{TOP}", article.height - 40)
        this.article.scrolldown_button.style.left = "{LEFT}px"
          .replace("{LEFT}", sidebar.width / 2 - 15)
        this.article.scrolldown_button.style.opacity = 1
      }
    }.bind(this), 500)
  }
  //
  // hook for Xia Loaded
  //
  loaded(XiaObject) {
    // show title and main description
    this.update_content(
      XiaObject.params.scene.intro_title,
      XiaObject.params.scene.intro_detail)

    // Do not execute following code twice
    if (this.already_loaded) return
    this.already_loaded = true

    var container = XiaObject.stage.container()
    container.addEventListener('keydown', function (e) {
      if (e.shiftKey && (e.key === "Tab")) {
        if (XiaObject.mainScene.zoomActive == 1) {
          e.preventDefault()
          return
        }
        if (XiaObject.focusedObj !== null) {
          XiaObject.focusedObj--
          if (XiaObject.focusedObj >= 0) {
            XiaObject.iaObjects[XiaObject.focusedObj+1].xiaDetail[0].kineticElement.fire("mouseleave")
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("mouseover")
            e.preventDefault()
          }
          else {
            XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire("mouseleave")
            XiaObject.focusedObj = null;
          }
        }
        else {
          XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire("mouseover")
          e.preventDefault()
        }
      }
      else if (e.key === "Tab") {
        if (XiaObject.mainScene.zoomActive == 1) {
          e.preventDefault()
          return
        }
        if (XiaObject.focusedObj !== null) {
          XiaObject.focusedObj++
          if (XiaObject.focusedObj < XiaObject.iaObjects.length) {
            XiaObject.iaObjects[XiaObject.focusedObj-1].xiaDetail[0].kineticElement.fire("mouseleave")
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("mouseover")
            e.preventDefault()
          }
          else {
            XiaObject.iaObjects[XiaObject.iaObjects.length-1].xiaDetail[0].kineticElement.fire("mouseleave")
            XiaObject.focusedObj = null;
          }
        }
        else {
          XiaObject.iaObjects[0].xiaDetail[0].kineticElement.fire("mouseover")
          e.preventDefault()
        }
      }
      else if (e.key === "Enter") {
        if (XiaObject.focusedObj !== null) {
          var mouseover = false
          if (XiaObject.mainScene.zoomActive == 1) mouseover = true
          XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("click")
          if (mouseover) XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("mouseover")
        }
      }
      else if (e.key === "Escape") {
        e.preventDefault()
        if (XiaObject.focusedObj !== null) {
          if (XiaObject.mainScene.zoomActive == 1) {
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("click")
          }
          else {
            XiaObject.iaObjects[XiaObject.focusedObj].xiaDetail[0].kineticElement.fire("mouseleave")
          }
          XiaObject.focusedObj = null
        }
      }
    });


    this.manage_scrolldown_button()
    // Choose color background
    var quantizeImage = new Quantization()
    quantizeImage.setImage(XiaObject.imageObj)
    var dominant_color = quantizeImage.getDominantColor()
    document.getElementById(XiaObject.params.targetID).style.backgroundColor = 'rgba(RED, GREEN, BLUE, 255)'
      .replace('RED', dominant_color.red)
      .replace('GREEN', dominant_color.green)
      .replace('BLUE', dominant_color.blue)

    // binding events
    this._fullScreenAbility(XiaObject)
    document.getElementById(this.reload).addEventListener("click", function(e){
      this.restart()
      e.preventDefault()
    }.bind(XiaObject))
    this.article.scrolldown_button.addEventListener("click", this.scrolldown.bind(this))
    this.article.scrolldown_button.addEventListener("touchstart", this.scrolldown.bind(this))
    this.article.scrolldown_button.addEventListener("keypress", function(e){
      if (e.key == "Enter") this.scrolldown(e)
    }.bind(this))
  }
}
