# Tournois d'échecs

Ce projet a été réalisé dans le cadre de la formation OpenClassrooms *Développeur d'application - Python*.

→ Conception selon le design pattern **Model-View-Controller (MVC)**

Le programme sert à l'organisation de tournois d'échecs.

Un tournoi se déroule de la manière suivante :

1. L'utilisateur créé un tournoi et lui affecte des joueurs ainsi qu'un nombre de rounds.
2. Pour chaque round :
    - le programme génère automatiquement les matchs selon le [*système suisse*](https://fr.wikipedia.org/wiki/Syst%C3%A8me_suisse),
    - l'utilisateurs rentre les résultats des matchs.

L'utilisateur peut :
- créer plusieurs tournois en parallèle,
- modifier le classement d'un joueur à tout moment,
- afficher les informations d'un tournois (participants, résultats des matchs) à tout moment.

## Lancer l'application :
- créer un environnement virtuel : python -m venv [nom]
- activer l'environnement virtuel : [nom]\Scripts\activate
- installer les packages : pip install -r requirements.txt
- exécuter le script : python main.py

## Lancer l'application (Anaconda) :
- créer un environnement virtuel : conda create --name [nom]
- activer l'environnement virtuel : conda activate [nom]
- installer pip : conda install pip
- installer les packages : pip install -r requirements.txt
- exécuter le script : python main.py