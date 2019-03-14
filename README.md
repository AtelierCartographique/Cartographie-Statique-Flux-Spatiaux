# Cartographie statique de flux (ou de réseaux) spatiaux

## Description
Outils Python pour cartographier des interconnections spatiales. Nécessite une carte, la projection de cette carte au format EPSG, et un tableau de données relationnelle. Veuillez vous référer à l'exemple pour le format du tableau de données.

Cet outil utilise une méthode expérimentale de déplacement d'étiquettes fondée sur un moteur de simulation d'objets physiques.

## Exemple de résultat
![alt text](https://github.com/AtelierCartographique/Cartographie-Statique-Flux-Spatiaux/blob/master/images/result.png)
![alt text](https://github.com/AtelierCartographique/Cartographie-Statique-Flux-Spatiaux/blob/master/images/NFootprint-Reasons_travel_EN_Size-0.008-0.04_Scale-Linear_Palette-Set2.jpg)

## Bibliothèques Python 3 requises
* Pyproj
* PIL
* Pymunk
* Geocoder
* Shapely
* Numpy

## À faire
* Légende automatique
* Échelle automatique
* Souplesse dans les choix de paramètres (format de données, couleurs/transparences, etc.)
* Contrôle plus serré de la simulation physique pour les déplacement d'étiquettes
