# Cartographie statique de flux (ou de réseaux) spatiaux

## Description
Outils Python pour cartographier des interconnections spatiales. Nécessite une carte, la projection de cette carte au format EPSG, et un tableau de données relationnelle. Veuillez vous référer à l'exemple pour le format du tableau de données.

## Caractéristiques
* Construit automatiquement des graphiques en bulles ou pointes de tartes (la ou les couleurs représentes des catégories, et la taille représente la somme des effectifs des catégories)
* Échelles log base 2, base 10 ou linéraires
* Utilise une méthode expérimentale de déplacement d'étiquettes fondée sur un moteur de simulation d'objets physiques (débraillable)
* Calcul et déssine la légende de la carte automatiquement

## Exemple de résultat
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
