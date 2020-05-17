# Utiliser XIA 3

## 1. Exemple basique.
**xiajs** est une bibliothèque JavaScript basée sur la lib KonvaJS qui permet de créer des images interactives. Pour premier exemple, voici comment créer une image interactive issue d'une image disponible sur le web :

```
var XiaInstance = new Xia({
    'targetID' : 'my_div',
    'scene' : {
      'image' : './test/fortnite.jpg'
    },
    'details' : [
      {
        path : "M 1050,1050 1250,1050 1250,1250 1050,1250 Z"
      }
    ]
  })
```
Ici, nous appelons l'objet **XIA** auquel nous passons 3 paramètres obligatoires :
- le **targetID** : Il s'agit de l'id de la DIV qui va recevoir l'image interactive. XIA va y insérer l'image de façon optimale. Ceci signifie que la div de départ doit déjà être dimensionnée pour recevoir l'image.
- la **scene** : C'est un objet au format json qui doit au moins contenir l'attribut **image** qui pointe vers l'image qui va servir de base
- les **details** : C'est un tableau qui va contenir l'ensemble des détails zoomables. Dans notre exemple, nous ne définissons qu'un seul détail défini par son **path** au format SVG. (il s'agit d'un rectangle)

Voici le code source complet d'une page qui implémente une instance de XIA :

```
<!doctype html>
<html>
 <head>
   <meta charset="utf-8">
   <title>XIA 3</title>
   <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/konva/3.1.7/konva.min.js"></script>
   <script type="text/javascript" src="https://xia.dane.ac-versailles.fr/network/delivery/xia30/xia.js"></script>
 </head>
 <body>
  <div id="my_div" style="width:500px;height:300px;margin:0 auto;"></div>
  <script>
    var XiaInstance = new Xia({
      'targetID' : 'my_div',
      'scene' : {
        'image' : './test/fortnite.jpg'
      },
      'details' : [
        {
          path : "M 1050,1050 1250,1050 1250,1250 1050,1250 Z"
        }
      ]
    })
  </script>
 </body>
</html>
```

## 2. Exemples plus complexes
