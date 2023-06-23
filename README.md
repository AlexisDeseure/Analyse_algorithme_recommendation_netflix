## Projet_IC05_Analyse_algorithme_recommendation_netflix

Ce dépôt contient les fichiers de scripts et de résultats obtenus dans le cadre d'un projet réalisé pour l'UV IC05 intitulée "Analyse critique des données
numériques" à l'UTC.
Notre étude s'est articulée autour de l'algorithme de recommendations de Netflix, et principalement autour de la proportion de programmes issues d'une production originale par la plateforme. Pour cela, notre projet conciste au scrapping (utilisant la bibliothèque Selenium sur python) des programmes présentés sur la page d'acceuil de Netflix sur différents types de profils : 
* 1 profil témoin qui ne réalisera aucune action durant le parcours,
* 2 profils test dont :
    1. un "fan" des productions originales, il mettra des "like" sur tous les programmes originaux proposés sur la page d'acceuil et appliquera des "dislike" au reste,
    2. un "hostile" qui fera l'inverse pour chacun des programmes proposés sur la page d'acceuil.

Vous trouverez dans ce dépôt trois dossier dont le détail de leur contenu est décrit ci-dessous.

# Analyse et représentations

Ce dossier contient :
* un rapport détaillé de notre projet : notre méthode utilisée, nos résultats obtenus et leur interprétation
* le fichier source de la représentation des données sur Gephi (en .gephi)
* les exportations des différents graphes obtenus que nous avons exploités dans l'analyse

# Bases_csv_finales

Vous trouverez, pour chacun des trois profils de notre expérience, les bases de données dans le format csv obtenues après le scrappping ainsi que celles adaptées pour une exploitation sur le logiciel Gephi.

# Sources

Ce dossier contient :
* le scripts python permettant de lancer le scrapping en 2 étapes d'un profil type
* le script python permettant de convertir le fichier du scrapping obtenu en 2 fichiers csv exploitables sur Gephi

Pour le programme destiné au scrapping, notez qu'il vous faudra au préalable :
* un compte premium Netflix fonctionnel
* cloner le dépôt github sur votre machine en utilisant le lien associé
* créer un fichier "variables_de_connexion.env" dans le répertoire courant du script python, dans lequel il faudra écrire précisément (en remplaçant par les bonnes valeurs) :

MOT_DE_PASSE=votre_mot_de_passe_netflix
IDENTIFIANT=votre_identifiant_netflix
TOKEN=le_token_associée_au_profil_test

Pour exemple, on trouve le token comme sur la photo ci-dessous : 

![Capture d'écran pour trouver le token d'un profil Netflix](/token_profil_netflix_readme_screenshot.png)

* installer les bibliothèques python nécessaire au programme

Pour ce point, il vous faudra python installé sur votre machine et il suffira de copier coller et d'exécuter le script ci-dessous dans votre terminal pour installer les modules :

pip install selenium
pip install BeautifulSoup4
pip install pandas
pip install python-dotenv
pip install opencv-python
pip install numpy
pip install requests

* changer la valeur du paramètre "objectif" de l'appel de la fonction "parcourt_titres_informations" dans la foncion "main" du fichier "netflix_scrapping.py" pour switcher entre les actions du profil témoin/"fan"/"hostile"
