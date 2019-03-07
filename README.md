# Cartographie statique de flux (ou de réseaux) spatiaux

## Description
Outils Python pour cartographier des interconnections spatiales. Nécessite une carte, la projection de cette carte au format EPSG, et un tableau de données relationnelle. Veuillez vous référer à l'exemple pour le format du tableau de données.

Cet outil utilise une méthode expérimentale de déplacement d'étiquettes fondée sur un moteur de simulation d'objets physiques.

## Exemple de résultat
![alt text](https://github.com/AtelierCartographique/CartoReseauxSpatiaux/result.png)

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
