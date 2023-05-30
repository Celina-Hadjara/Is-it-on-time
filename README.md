# Projet Flight Time

## Présentation du projet
Bienvenue dans notre projet de prédiction des retards de vols, une solution innovante pour les voyageurs. Ce projet vise à faciliter la planification de voyage en fournissant des analyses détaillées et des prédictions précises des retards de vols. Notre objectif est d'aider les voyageurs à faire des choix éclairés et à éviter les désagréments causés par les retards de vols imprévus.

## Services

Notre application offre une gamme de services, notamment :

- Comparaison des compagnies aériennes : Des analyses détaillées et une comparaison des performances de différentes compagnies aériennes pour vous aider à faire le choix optimal pour votre voyage.

- Statistiques par ville et période : Un outil de comparaison qui analyse les tendances de vol par période et itinéraire, pour une planification de voyage optimale.

- Analyse des causes de retard : Une compréhension des causes spécifiques des retards de vols en fonction de votre itinéraire pour vous aider à anticiper les imprévus.

- Prédiction des retards de vols : Des prédictions précises des retards de vols pour minimiser les perturbations dues aux retards de vols imprévus.

## Lien vers le site de présentation
Pour accéder à notre site de présentation, veuillez visiter notre site web : https://flight.my.canva.site/flight-time

## Architecture 

![Architecture](https://github.com/Celina-Hadjara/Is-it-on-time/blob/41991f18576d58c778ea4c62d4fa1240136a4b8a/image.png)


## Comment lancer le projet

### Prérequis
Ce projet a été développé en utilisant Flask, un cadre de travail en Python pour développer des applications web. Pour pouvoir exécuter ce projet, vous aurez besoin de :

- Python 3.6 ou version ultérieure
- Flask 1.0 ou version ultérieure

Vous pouvez installer Flask à l'aide de pip, l'installateur de paquet Python :
 "pip install flask"
 
 Vous pouvez installer toutes les dépendances Python requises pour ce projet à partir du fichier requirements.txt inclus. Pour cela, utilisez la commande suivante :

 - ' pip install -r requirements.txt ' 
 
### Téléchargement des fichiers nécessaires

En raison de l'espace insuffisant de Git LFS, nous avons fait le choix de ne pas mettre les fichiers de modèle (PKL) et le dataset sur Git. Vous devrez donc télécharger ces fichiers séparément.

- Téléchargez le dossier contenant les fichiers de modèle et le dataset à partir du lien  Google Drive: https://drive.google.com/file/d/10UF_EiRaiWIaYPZYs9olFOBWvxUlaJ_v/view?usp=share_link  puis dézipper le.

- Placez les dossiers  "model_save" et "encoder"  dans le dossier "prediction".

### Lancer l'application
Après avoir installé les dépendances nécessaires et téléchargé les fichiers requis, vous pouvez lancer l'application Flask en utilisant la commande suivante depuis la ligne de commande :

- " flask run " 
Assurez-vous que vous êtes dans le répertoire racine du projet lorsque vous exécutez cette commande.

### Remarque
Si vous rencontrez des problèmes pour exécuter le projet ou avez des questions, n'hésitez pas à ouvrir une issue sur GitHub. Nous serons heureux de vous aider.

Nous espérons que vous trouverez notre projet utile et nous sommes ouverts à toute suggestion d'amélioration !
