Tableau de bord GeoNature avec Dash
===================================

Cette application permet de générer un tableau de bord de données en se connectant à une base de données GeoNature.
Il a été utilisé pour réstituer les données lors d'un évenement naturaliste : Explor'Nature.

Il affiche les données d'un jeu de données et d'une commune avec les éléments suivants :

- tableau des espèces
- tableau des nouvelles espèces pour la commune
- tableau des nouvelles espèce pour la structure
- graphique de répartition des nouvelles espèces
- carte de chaleurs de données

Tous les éléments sont filtrables par groupe2 INPN, ordre et famille.


Installation et lancement
=========================

    # Installer les dépendances
    pip install -r requirements.in
    # désampler le fichier de config et le remplir
    cp config.py.sample config.py
    # Lancer l'application  (par défaut disponible sur : http://127.0.0.1:8050/ )
    python dash_app.py