# Cartographie statique de flux (ou de réseaux) spatiaux

## Description
Outils Python pour cartographier des interconnections spatiales. Nécessite une carte, la projection de cette carte au format EPSG, et un tableau de données relationnelles. Veuillez vous référer à l'exemple pour le format du tableau de données.

* Construit automatiquement des graphiques en bulles ou pointes de tartes (oû les couleurs des bulles représentent des catégories, et leurs tailles représentent la somme des effectifs des catégories);
* Échelles linéaires ou log (base 2 ou 10);
* Utilise une méthode de déplacement d'étiquettes utilisant un moteur de simulation d'objets physiques (débraillable);
* Calcule et déssine la légende de la carte automatiquement.

## Exemples de résultats
![alt text](https://github.com/AtelierCartographique/Cartographie-Statique-Flux-Spatiaux/blob/master/images/result.png)
![alt text](https://github.com/AtelierCartographique/Cartographie-Statique-Flux-Spatiaux/blob/master/images/NFootprint-Reasons_travel_EN_Size-0.008-0.04_Scale-Linear_Palette-Set2.jpg)
![alt text](https://github.com/AtelierCartographique/Cartographie-Statique-Flux-Spatiaux/blob/master/images/NFootprint_etudiants_EN_Size-0.01-0.05_Scale-Linear_Palette-Set2.jpg)

## Bibliothèques Python 3 requises
* Pyproj
* PIL
* Pymunk
* Geocoder
* Shapely
* Numpy

## À faire
* Choix dans les projections et étendues des cartes (adapter à des cartes non-globales)
* Échelle automatique
* Souplesse dans les choix de paramètres (format de données, couleurs/transparences, etc.)
* Contrôle plus serré de la simulation physique pour les déplacement d'étiquettes
