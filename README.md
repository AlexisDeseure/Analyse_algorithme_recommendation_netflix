# Projet IC05 : Analyse de l'algorithme de recommandation de Netflix

Ce dépôt contient les fichiers de scripts et de résultats obtenus dans le cadre d'un projet réalisé pour l'UV IC05 intitulée "Analyse critique des données
numériques" à l'UTC.
Notre étude s'est articulée autour de l'algorithme de recommandation  de Netflix, et principalement autour de la proportion de programmes issues d'une production originale par la plateforme. Pour cela, notre projet consiste au scrapping (utilisant la bibliothèque Selenium sur python) des programmes présentés sur la page d'accueil de Netflix sur différents types de profils : 
* 1 profil témoin qui ne réalisera aucune action durant le parcours,
* 2 profils test dont :
    1. un "fan" des productions originales, il mettra des "like" sur tous les programmes originaux proposés sur la page d'accueil et appliquera des "dislike" au reste,
    2. un "hostile" qui fera l'inverse pour chacun des programmes proposés sur la page d'accueil.

Vous trouverez dans ce dépôt trois dossiers dont le détail de leur contenu est décrit ci-dessous.

## Analyse et représentations

Ce dossier contient :
* un rapport détaillé de notre projet : notre méthode utilisée, les résultats obtenus et leur interprétation
* le fichier source de la représentation des données sur Gephi (en .gephi)
* les exportations des différents graphes obtenus que nous avons exploités dans l'analyse

## Bases_csv_finales

Vous trouverez, pour chacun des trois profils de notre expérience, les bases de données dans le format CSV obtenues après le scrapping ainsi que celles adaptées pour une exploitation sur le logiciel Gephi.

## Sources

Ce dossier contient :
1. le script python permettant de lancer le scrapping en 2 étapes d'un profil type
2. le script python permettant de convertir le fichier du scrapping obtenu, en 2 fichiers .csv exploitables sur Gephi

Pour le programme destiné au scrapping, notez qu'il vous faudra au préalable :
* un compte premium Netflix fonctionnel
* cloner le dépôt Github sur votre machine en utilisant le lien associé
* créer un fichier "variables_de_connexion.env" dans le répertoire courant du script python ou à la racine de votre projet, dans lequel il faudra écrire précisément (en remplaçant par les bonnes valeurs) :

MOT_DE_PASSE=votre_mot_de_passe_netflix<br>
IDENTIFIANT=votre_identifiant_netflix<br>
TOKEN=le_token_associée_au_profil_test<br>

Pour exemple, on trouve le token comme sur la photo ci-dessous : 

![Capture d'écran pour trouver le token d'un profil Netflix](/token_profil_netflix_readme_screenshot.png)

* installer les bibliothèques python nécessaire au programme

Pour ce point, il vous faudra python installé sur votre machine et il suffira de copier coller et d'exécuter le script ci-dessous dans votre terminal pour installer les modules :

pip install selenium<br>
pip install BeautifulSoup4<br>
pip install pandas<br>
pip install python-dotenv<br>
pip install opencv-python<br>
pip install numpy<br>
pip install requests<br>

* changer la valeur du paramètre "objectif" de l'appel de la fonction "parcourt_titres_informations" dans la fonction "main" du fichier "netflix_scrapping.py" pour intervertir les actions et correspondre au profil témoin/"fan"/"hostile"
