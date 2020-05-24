# Utiliser XIA 3

## 1. Exemple basique.
**xiajs** est une bibliothèque JavaScript basée sur la lib KonvaJS qui permet de créer des images interactives. Pour premier exemple, voici comment créer une image interactive issue d'une image disponible sur le web :

```
var XiaInstance = new Xia({
    'targetID' : 'my_div',
    'scene' : {
      'image' : 'https://xia.funraiders.org/img/3614686.jpg'
    },
    'details' : [
      {
        path : "m 2300,1200 h 1000 v 1000 H 2300 Z"
      }
    ]
  })
```
Ici, nous appelons l'objet **XIA** auquel nous passons 3 paramètres obligatoires :
- le **targetID** : Il s'agit de l'id de la DIV qui va recevoir l'image interactive. XIA va y insérer l'image de façon optimale. Ceci signifie que la div de départ doit déjà être dimensionnée pour recevoir l'image.
- la **scene** : C'est un objet au format json qui doit au moins contenir l'attribut **image** qui pointe vers l'image qui va servir de base
- les **details** : C'est un tableau qui va contenir l'ensemble des détails zoomables. Dans notre exemple, nous ne définissons qu'un seul détail défini par son **path** au format SVG. (il s'agit d'un rectangle)

Voici le code source complet d'une page qui implémente une instance de XIA (image issue de freepik https://fr.freepik.com/photos-vecteurs-libre/nourriture) :

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
        'image' : 'https://xia.funraiders.org/img/3614686.jpg'
      },
      'details' : [
        {
          path : "m 2300,1200 h 1000 v 1000 H 2300 Z"
        }
      ]
    })
  </script>
 </body>
</html>
```

## 2. Exemples plus complexes

Dans cet exemple, nous pouvons afficher une description de l'objet zoomé. Pour cela, nous devons passer à l'objet XIA un paramètre supplémentaire *'hooks'* qui permet de hooker les événements suivants:
- le zoom
- le unzoom
- le mouseover
- le focus
- le mouseleave

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
  <div id="desc">Select an item...</div>
  <div id="my_div" style="width:100%;height:500px;"></div>
  <script>
    var XiaInstance = new Xia({
      'hooks' : {
        'zoom': function(el) {
          document.getElementById('desc').innerHTML = el.desc
          return true
        },
        'unzoom': function(el) {
          document.getElementById('desc').innerHTML = "Select an item..."
          return true
        }
      },
      'targetID' : 'my_div',
      'scene' : {
        'image' : 'https://xia.funraiders.org/img/3614686.jpg'
      },
      'details' : [
        {
          path : "m 2300,1200 h 1000 v 1000 H 2300 Z",
          desc : "this is an apple"
        }
      ]
    })
  </script>
 </body>
</html>

```
