# Jaques Evan - 
## Module 164 11.06.2023

Mon projet consiste en une interface (HTML, FLASK, Python, etc.) et une BD MySql.

Il s'agit d'une gestion de cours de yoga, afin de répertorier les enfants et les parents avec toutes leurs informations, les cours et les factures.

Soit un système CRUD (Create Read Update Delete) adapté aux besoins sur les 8 tables de ma BD : “t_parents”; “t_adresse”; "t_mail"; "t_telephone"; "t_factures"; "t_enfants"; "t_sante"; "t_cours".

## Avertissement
Ayant eu des problèmes au niveau des boutons DELETE sur mes tables "t_parents" et "t_enfants" il est impossble de les supprimer mais cela fonctionne sur la table "t_factures". J'ai aussi avec ma table "t_parents" l'impossibilité de lier des enfants, j'ai une erreur de proxy que j'ai eu trop tard pour vous demander. Mon projet a aussi eu quelques changements au cours de route, ne sachant pas comment faire exactement pour la gestion des cours, je me suis arreter a ce qui était fesable pour moi. 
# Quels sont les prérequis pour faire fonctionner mon projet ?

Un serveur MySql doit être installé

* LARAGON (heidi.sql) ou XAMPP ou UWAMP
* MAC : MAMP ou https://www.codeur.com/tuto/creation-de-site-internet/version-mysql/

Python doit être installé.

* ATTENTION : Cocher la case pour que le “PATH” intègre le programme Python
* Une fois la “case à cocher” du PATH cochée, il faut choisir d’installer
* Un peu avant la fin du processus d’installation, cliquer sur “disabled length limit” et cliquer sur “CLOSE”
* Le test de Python se fait après avec le programme “PyCharm”

Installer “GIT”
* https://gitforwindows.org/
* Le test de “GIT” se fait dans le programme “PyCharm”

## Configuration de PyCharm
* Il faut installer “PyCharm” (community) et utiliser la même version IDE pour faire fonctionner le projet.
* Lors de l’installation, il faut cocher toutes les options ASSOCIATIONS, ADD PATH, etc
* Ouvrir “PyCharm” pour la première fois pour le configurer. Choisir le bouton “New Project”
* Changer le répertoire pour ce nouveau projet, il faut créer un nouveau répertoire “vide” sur votre disque en local.
* Il est important d’avoir sélectionné le répertoire que vous venez de créer car “PyCharm” va automatiquement créer un environnement virtuel (venv) dans ce répertoire
* Menu : File->Settings->Editor->General->Auto Import (rubrique Python) cocher “Show auto-import tooltip”

## PyCharm vient d’ouvrir une fenêtre avec le contenu du “main.py” pour configurer les actions “UNDO” et “REDO”

* Sélectionner tout le texte avec “CTRL-A” puis “CTRL-X” (Couper), puis “CTL-Z” (UNDO) et faites un REDO “CTRL-Y” et “PyCharm” va vous demander de choisir l’action du “CTRL-Y” raccourci pour faire un “REDO”. 

# Guide pour faire fonctionner mon projet
## Démarrer le serveur MySql (Laragon(heidi.sql), uwamp ou xamp ou mamp, etc.))

* Dans “PyCharm”, importer MA BD à partir du fichier DUMP
* Ouvrir le fichier APP_YOGA_164/database/1_ImportationDumpSql.py
* Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)

## En cas d’erreurs /!\ 

* Ouvrir le fichier .env à la racine du projet, contrôler les indications de connexion pour la bd.

## Test simple de la connexion à la BD

* Ouvrir le fichier APP_YOGA_164/database/2_test_connection_bd.py
* Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)

## Démarrer le microframework FLASK

* Dans le répertoire racine du projet, ouvrir le fichier run_mon_app.py
* Cliquer avec le bouton droit sur l’onglet de ce fichier et choisir “run” (CTRL-MAJ-F10)
* Dans la console du “run” il doit y avoir un lien à cliquer de cette forme :
  * Running on http://127.0.0.1:5005
* Cliquer dessus afin d'ouvrir dans votre navigateur mon projet

# Vous voici sur le visuel de mon projet final !