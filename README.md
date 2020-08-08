# XIA

This tool is used to generate html5 resources.
Thanks to it, you can generate three kinds of resources :
- first ones : interactives images. Simple images on which we can make a focus on some details by zooming and adding descriptions.
- second ones : games using what we call the "1 click with scoring".
- third ones : games using what we call the "drag and drop with scoring" and "drag and drop without scoring"

Just have a look here to see samples :

[XIA Examples](https://xia.funraiders.org/exemples.html)

XIA comes with a set of tools:
- An Inkscape extension to transform inkscape svg files to preformatted XIA html5 resources
- A standalone application to transform svg files to preformatted XIA html5 resource (usable in commandline too)
- A JS library which is the heart of XIA used to animate your html5 resources

# 1. How to use Inkscape extension?

see the dedicated french documentation [using inkscape extension](./doc/xia-fr.md)
see the dedicated english documentation [using inkscape extension](./doc/xia-en.md)

# 2. How to use xiajs?

This is the developer corner. **xiajs** is a javascript library based on KonvaJS for building interactives images. Here a first example:

```
var XiaInstance = new Xia({
    'targetID' : 'my_div',
    'scene' : {
      'image' : 'img/background.png'
    },
    'details' : [
      {
        path : "m 50,50 h 100 v 100 H 100 Z"
      }
    ]
  })
```
Here, we call Xia object giving these 3 mandatories parameters:
- the **targetID** : This is the id of HTML element where we want to display the interactive image. XIA will insert the resource calculating the best ratio. That means this HTML element must have its proper dimensions.
- the **scene** : This is a json object where we define the background image
- the **details** : This is an array of json objects called details. Each detail becomes a clickable/zoomable element. In this example, we draw a 100x100 rectangle at (50,50)

Here is a complete example:

```
<!doctype html>
<html>
 <head>
   <meta charset="utf-8">
   <title>XIA 3</title>
   <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/konva/3.1.7/konva.min.js"></script>
   <script type="text/javascript" src="https://xia.funraiders.org/cdn/xia30/js/xia.js"></script>
 </head>
 <body style="width:50%;margin:0 auto;">
  <h1>Example XIA</h1>
  <div id="my_div" style="width:100%;height:500px;"></div>
  <script>
    var XiaInstance = new Xia({
      'targetID' : 'my_div',
      'scene' : {
        'image' : 'img/background.png'
      },
      'details' : [
        {
          path : "m 50,50 h 100 v 100 H 100 Z"
        }
      ]
    })
  </script>
 </body>
</html>
```

more complex examples there: [dev corner](./doc/xia-fr-dev.md)

## How to build

See de dedicated documentation [Building xia](./BUILD.md)
