* version alpha 2 - 04/30/2014

- L'outil standalone est packagé pour debian (François Lafont)
- Grosse optimisation du moteur html5 pour qu'il gère les images actives de grande taille (pb signalé par Patrice Raynaud et Isabelle Perucho)
- Un nouveau thème "AccordionCloud" est disponible (Wahid Mendil) 
- Pour ajouter un nouveau thème à partir d'un existant, il suffit de dupliquer un thème dans le répertoire iaConvert/themes
- Les chemins utilisés sont désormais persistants
- Ajout de la notion de puce: Par convention, une image définie avec un fond blanc est considérée comme une puce. De plus, un détourage sur fond blanc devient persistant. (signalé par Marie Persiaux)
- Les images liées ou incorporées dans InkScape sont traitées de la même façon (pb signalé par Isabelle Perucho sur MAC OS X 10.6)
- Un splash screen s'affiche durant la génération (feature demandée par Louis-Maurice De Sousa)
- Réglage d'un problème de zindex sur les détails (pb signalé par Isabelle Perucho)
- expérimental : ajout du fullscreen en cliquant sur le titre d'une image active
- Effet de zoom optimisé pour éviter le memory leaking sur Firefox et Iceweasel
- Prise en compte des images dans les descriptions (demandé par Aurélie Chauvet)
- Prise en compte des iframes dans les descriptions (demandé par Marie Persiaux pour vidéos youtube - fonctionne aussi avec les vidéos de la scolawebtv)
- Prise en compte des liens wiki de la forme [http(s)://link key_word] (demandé par Serge Raynaud)