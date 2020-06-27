Version 3.0-beta5 - xx/xx/2020
-------------------------------
- Use Konvajs 7.0.0


Version 3.0-beta4 - 23/06/2020
-------------------------------
- GameDrag&Drop: correctif sur les liens directs
- Sprites: les sprites sont désormais fonctionnels
- GameDrag&Drop: correctif sur les tooltips
- Images: les transformations affines sont opérationnelles
- Material: correctif sur les détourages trop épais et déplacement des boutons du bas
- Material: synchronisation de la popup et de l'image au moment de leur apparition
- Mise à jour de la documentation sur les images interactives
- Images interactives: correctif sur l'autostart des images et des videos
- Game1clic: correctif sur la zone de hitarea qui ne s'adaptait plus aux formes
- Game1clic: correctif sur la visibilité des sprites

Version 3.0-beta3 - 08/06/2020
-------------------------------
- scaling sur les sprites fixés sur les thèmes sidebar, material et game1clic
- ajout des sprites sur gameDragAndDrop
- angle de rotation d'une image fixé
- mise à jour des documentations

Version 3.0-beta2 - 06/06/2020
-------------------------------
- Changement de visuel de l'extension Inkscape pour être compatible MAC OS X Catalina
- Material : correctif sur le mouseover pour afficher les pointillés
- Pikipiki : Les images peuvent être des liens
- Xia Engine : Désactive le cache par défaut pour accepter les images de fond avec transparence
- Game1Click : fix un problème de scale sur les images quand elles sont redimensionnées

Version 3.0-beta1 - 01/06/2020
-------------------------------
- Compatibilité avec python3
- Compatibilité avec Inkscape 1
- Suppression des thèmes popBlue, popYellow, buttonBlue et audioBrown
- Ajout d'un nouveau thème orienté mobiles baptisé "sidebar"
- Les images interactives peuvent être intégrées dans une page web sans utiliser d'iframe
- Documentation pour les développeurs qui veulent intégrer une image interactive dans leurs pages web
- La qualité de l'image zoomée dans les images interactives a été grandement améliorée
- Ajout d'un nouveau type d'objet : les sprites (experimental)
- Suppression de la dépendance à jquery pour les images interactives
- Remplacement de la lib KineticJs par KonvaJs 6.0.0 pour les images interactives
- Accessibilité sur les thèmes d'images interactives (navigation clavier + aria)
- migration vers xia.funraiders.org
- Refonte de l'interface de génération
- Simplification de l'arborescence des fichiers sur l'export fichiers multiples

Version 2.2 - 21/03/2017
-------------------------------

- [Windows] : Correctif d'un bug qui empêchait la génération d'images interactives (depuis la dernière mise à jour de Windows en date de mi-mars 2017)
- Tous les thèmes : les images dans les popups sont désormais centrées et leurs dimensions sont adaptées.
- Tous les thèmes : L'apparence des titres obtenus avec la nouvelle syntaxe "# mon titre" a été améliorée
- Thème popBlue : Mise en place du scrolling sur la fenêtre popup de présentation générale
- Tous les thèmes : Un fichier audio intégré en "autostart" dans la description de l'image de fond est automatiquement démarré au lancement de l'image. Ceci permet de créer une musique d'ambiance ou une explication audio immédiatement après le chargement de l'image interactive.

Version 2.1 - 15/03/2017
-------------------------------

- Ajout des fichiers de langue portugais
- popBlue : Les images sont désormais centrées
- popBlue : Le scroll dans les popup ne concerne plus que le texte (le bouton quitter reste en haut)
- pikipiki : Les liens vers les PDF sont pris en compte
- pikipiki : Les titres markdown sont pris en compte

Version 2.0 - 12/12/2016
-------------------------------

- plugin inkscape : changement d'arborescence, plugin accessible dans Export (Nouveauté)
- Une image avec une transparence de moins de 40% faisait planter xia (Nouveauté)
- Thème de jeu drag&drop : connecteurs entre éléments (Nouveauté)
- gamedragandrop : un élément déplaçable peut avoir plusieurs target (Nouveauté)
- gamedraganddrop : groupement de cibles (Nouveauté)
- Tous les thèmes : Un groupe peut être défini comme image de fond (Nouveauté)
- Tous les thèmes : Un path peut être défini comme image de fond (Nouveauté)
- Application : Nouveau thème "Material" (Nouveauté)
- Application : Interface utilisateur revue (Nouveauté)
- Application : Suppression de l'export Firefox OS (Nouveauté)
- Tous les thèmes : Thèmes relookés (Nouveauté)
- Application : Nom du fichier html d'export identique à celui du fichier svg (Nouveauté)
- Tous les thèmes : oembed flicker (Nouveauté)
- Prise en compte du oembed scolawebtv et webtv
- Paramètre score2 ajouté dans gameDrag&Drop
- Prise en compte du fond quand passage au plein écran
- Le mode console prend en compte la qualité ainsi que le type d'export
- Les exports uniques peuvent être intégrés dans des sites utilisant le https
- gamedraganddrop : attribut onfail=return permet de ramener l'élément à sa position d'origine si droppé sur la mauvaise zone
- progressbar de chargement
- popBlue : affichage de la popup en 1 seul clic
- Export fichier unique par défaut
- (correctif) Images dans groupes : translation sur un groupe répercutée sur les images de ce groupe

Version 1.1 - 23/03/2015
-------------------------------

- bugfix : chrome et chromium ne gérait pas correctement document.onload
- popBlue et popYellow : les popup s'affichent si la description ou le titre sont présents
- buttonBlue : le titre est désormais blanc
- tous les thèmes : respect de la superposition des détails au moment du survol ou du focus
- ajout des tests fonctionnels sur audioBrown, popBlue, popYellow, buttonBlue
- Correctifs sur la documentation + ajout d'une section sur firefox OS


Version 1.0 - 13/02/2015
-------------------------------

- bugfix : game1clic ne fonctionnait pas sur écrans retina et amoled
- amélioration : le focus sur un détail est verrouillé même lorsque le pointeur sort de la zone



Version 1.0-beta6 - 09/02/2015
-------------------------------

- nouveau : xia gère les ellipses et les cercles au sens SVG
- bugfix : une image était hardcodée dans les thèmes de jeu
- refactorisation de la documentation
- mise à jour de la documentation
- nouveau : documentation traduite en portugais
- amélioration : images de fond supprimées et remplacées par des fonds bicolores.
- amélioration : le moteur de wiki est compatible xhtml (préparation pour les exports epub3)
- amélioration : ajout d'un logger qui s'adapte à la console voulue
- amélioration : amélioration notoire des effets de zoom qui sont plus fluides et plus rapides
- nouveau : changement de l'interface de XIA en ajoutant des logos plus significatifs
- nouveau : simplification de l'interface paramètres
- mise à jour des tests fonctionnels
- amélioration : les thèmes de jeu ont été légèrement retouchés pour améliorer l'expérience utilisateur
- bugfix : suppression des contours des détails s'ils sont mentionnés comme "none" dans inkscape

Version 1.0-beta5 - 19/01/2015
-------------------------------

- bugfix : gestion des noms avec caractères accentués dans les sessions windows
- amélioration : suppression des zones transparentes inutiles sur les images
- gameDragAndDrop : si le clic est désactivé, le lien direct fonctionne encore
- développeurs : les fichiers hook.js peuvent être édités pour ajouter des fonctionnalités
- bugfix : suppression des détails qui contiennent des paramètres invalides
- pikipiki : insensible à la casse
- MAC OS X : PIL est utilisé de base.
- Amélioration : toutes les metadatas sont prises en compte
- IA 1 : prise en compte du facteur zoom sur les fichiers .xia
- Amélioration : les contours des détails sont définis dans le svg et ne sont donc plus rouges par défaut.
- bugfix : les chemins réseaux n'étaient pas gérés correctement

Version 1.0-beta4 - 21/11/2014
-------------------------------

- XIA est compatible avec les ressources issues de IA1
- Le mode "lier les images" d'inkscape n'a désormais plus d'incidence sur XIA
- bugfix : les mots de passe du module quiz peuvent comporter des caractères
accentués
- Les vidéos et les sons s'arrêtent à la fermeture des popups
- Si la description d'un détail est vide, la popup liée n'est plus visible
- AccordionBlack : l'accordéon laisse apparaître un ascenseur vertical s'il est
trop long
- Le moteur de zoom dans les images interactives est plus fluide et plus rapide
- gameDragAndDrop : la balise <magnet> existe maintenant aussi de manière
 globale. De plus, si elle est sur "on", toutes les zones de drop sont
aimantées pour tous les détails.
- bugfix : les transformations du plan appliquées sur des groupes imbriqués
fonctionnent désormais comme prévu.
- Mise en place des nouveaux logos xia
- gameclic : grosse amélioration de la vitesse de détection des zones de survol
- Export fichier unique disponible
- Export firefox os en option
- moteur de wiki : les liens relatifs sont autorisés dans les hyperliens
- Système de double-scoring disponible dans gameclic
- mise à jour de la documentation
- développement des tests fonctionnels en cours

Version 1.0-beta3 - 29/10/2014
-------------------------------

- XIA est disponible en mode console.
- LibreOffice Draw : XIA peut lire les sorties svg issues de libreoffice draw
(sauf pour le thème gameDragAndDrop)
- Système de "double-scoring" disponible sur game1clic
- hotfix : amélioration de la gestion de la mémoire dans les thèmes des
images interactives
- Dans gameDragAndDrop, les zones de drop peuvent maintenant déclencher
l'ouverture d'une nouvelle page au moment du drop.
- Chemins relatifs disponibles dans les liens entre crochets
- Les listes à puces sont désormais "formattables".
- hotfix : bug sur le module quiz avec un mot de passe.

Version 1.0-beta2 - 23/10/2014
-------------------------------

- XIA est compatible Inkscape 0.47 en tant qu'extension
- Mise à jour de la documentation + internationalisation
- Système de réponse générique avec mot de passe possible
- Correctif : bug dans kinetic bloquant pour IE11 sur gameDrag&Drop

Version 1.0-beta1 - 12/10/2014
-------------------------------

- Correctif : les bandes sons ne s'arrêtaient pas lorsqu'on changeait de détail
- Mise à jour des documentations + refactorisation du code
- Ajout de la documentation en anglais
- Reconstruction de la procédure de build
- Correctif : les tests unitaires ne passaient plus à cause d'un chemin erroné
- Suppression de la dépendance avec bootstrap dans les thèmes accordion
- Ajout d'informations plus explicites dans les infos-bulles

Version 1.0-alpha9 - 05/10/2014
-------------------------------

- Correction d'une regression sur les détourages dans game1clic
- Echappement des titres quand ils contiennent des double quotes

Version 1.0-alpha8 - 01/10/2014
-------------------------------

- Séparation du package debian et du code source
- Ajout de la fonctionnalité info-bulles sur les 2 thèmes de jeu
- Les zones de drop dans gameDragAndDrop sont cliquables si leur
titre est une url
- soumis à évaluation : limitation de la largeur des jeux gameDragAndDrop à
1000 pixels de large max pour éviter des problèmes de performance sur des grands écrans.
- Refactorisation du code des thèmes de jeu.
- Refactorisation du code pour respecter la "debian policy"

Version 1.0-alpha7 - 29/09/2014
-------------------------------

- Doc : mise à jour des docs de prise en main
- Bouton de bascule ajouté sur les messages de succès dans les thèmes game\*
- hotfix : les balises vidéos plantaient les zooms
- hotfix : les détails "chemin" hors image de fond crashaient l'application html5
- Ergonomie : amélioration du visuel de la popup d'introduction

Version 1.0-alpha6 - 25/09/2014
-------------------------------

- Doc : mise à jour des docs de prise en main
- Correctif : reprise du manifest firefox OS
- Ergonomie : sur gameDragAndDrop, les images n'ont plus besoin d'être sur fond
blanc
- Ergonomie : sur popBlue, lors d'une clic sur un détail, le pointeur ne se
transforme plus en loupe.
- Ergonomie : sur gameDragAndDrop, les zones de drop sont par défaut insensibles
au clic
- Correctif : gameDragAndDrop -> régression sur les popup

Version 1.0-alpha5 - 23/09/2014
-------------------------------

- Correctif : Modification de l'internationalisation pour MAC OS X
- Ergonomie : Suppression de l'oeil sur tous les thèmes
- Ergonomie : Ajout d'une popup de démarrage sur game1clic et gameDragAndDrop pour
permettre l'affichage de consignes (champ description des metadonnées)
- Correctif : xia ne gérait pas (sic) les groupes de détails imbriqués !
- Correctif : xia plantait sur des images de taille bien précise.
- Ergonomie : il est désormais possible d'afficher un pointeur de sélection
au survol d'un détail dans game1clic (onmouseover=pointer)
- Optimisation : amélioration du système de détourage automatique
pour définir la zone de hit de chaque détail
- Correctif : Les propriétés des détails étaient propagées aux groupes qui les
contenaient (propagation de off par exemple)...à surveiller, risque de régression.

Version 1.0-alpha4 - 15/09/2014
-------------------------------

- Ajout de l'internationalisation
- Changement de nom de l'application
- relooking des boutons de l'interface de génération des IAs
- Ajout d'une fenêtre "paramètres" qui sera enrichie par la suite.
Actuellement, elle ne propose qu'une seule option. Vous pouvez contrôler
la qualité de l'image rendue.
- Réduction du Critical Rendering Path
- Minification des CSS et des JS.
- Désormais, les images de fond dans inkscape n'ont plus besoin d'être
alignées dans le coin supérieur gauche. La gestion des calques a
également été améliorée.
- Ajout d'une nouvelle fonctionnalité dans les images actives : les
LIENS DIRECTS. Pour cela, il suffit de mettre un lien absolu ou relatif
dans le titre du détail.
- Tous les fichiers utiles pour créer une app Firefox OS sont désormais
installés par défaut dans chaque IA générée
- Via les metadonnées opengraph, les IA générées peuvent être affichées
dans les réseaux sociaux (Facebook, twitter...)
- Grosse amélioration du drag and drop sur le thème gameDragAndDrop
- Les images dans game1clic réagissent uniquement sur les pixels opaques
(comme pour gameDrag&Drop)
- Mise en cache des images pour accélérer le traitement dans gameDragAndDrop et
game1clic
- ajout d'un lanceur executable pour Windows

Version 1.0-alpha3 - 02/07/2014
-------------------------------

- Ajout d'une popup durant la génération d'une image active
- L'image de fond n'est plus estompée durant la lecture de la description
générale
- L'image de fond est embarquée même si elle est liée dans Inkscape
- pikipiki : ajout des liens hypertexte
- Conservation des chemins vers source et destination pour génération des
images actives
- Améliorations importantes du packaging
- Images persistantes si elles ont un fond blanc
- Masquage des fichiers cachés lors de la recherche d'un fichier svg dans
le filesystem
- tests unitaires ajoutés
- tests fonctionnels sur les thèmes ajoutés
- Ajout de la gestion des metadonnées
- popup disponible dans les thèmes pour afficher les metadonnées
- Ajout des thèmes popBlue, popYellow, audioBlue, buttonBlue
- Ajout des bordures sur les détourages

Version 1.0-alpha2 - 30/04/2014
-------------------------------

- L'outil standalone est packagé pour debian (François Lafont)
- Grosse optimisation du moteur html5 pour qu'il gère les images actives de
grande taille (pb signalé par Patrice Raynaud et Isabelle Perucho)
- Un nouveau thème "AccordionCloud" est disponible (Wahid Mendil)
- Pour ajouter un nouveau thème à partir d'un existant, il suffit de dupliquer
un thème dans le répertoire iaConvert/themes
- Les chemins utilisés sont désormais persistants
- Ajout de la notion de puce: Par convention, une image définie avec un fond
blanc est considérée comme une puce. De plus, un détourage sur fond blanc
devient persistant. (signalé par Marie Persiaux)
- Les images liées ou incorporées dans InkScape sont traitées de la même
façon (pb signalé par Isabelle Perucho sur MAC OS X 10.6)
- Un splash screen s'affiche durant la génération (feature demandée par
Louis-Maurice De Sousa)
- Réglage d'un problème de zindex sur les détails (pb signalé par
Isabelle Perucho)
- expérimental : ajout du fullscreen en cliquant sur le titre d'une image active
- Effet de zoom optimisé pour éviter le memory leaking sur Firefox et Iceweasel
- Prise en compte des images dans les descriptions (demandé par Aurélie Chauvet)
- Prise en compte des iframes dans les descriptions (demandé par Marie
Persiaux pour vidéos youtube - fonctionne aussi avec les vidéos de la scolawebtv)
- Prise en compte des liens wiki de la forme [http(s)://link key_word]
(demandé par Serge Raynaud)
