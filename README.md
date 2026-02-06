"# Projet SAE - Jupyter Notebook" 
 # Projet SAE - Analyse des Salaires en Data Science et developpemnt d'un outils streamlit

Ce projet a été réalisé dans le cadre de la SAE . Il consiste en la création d'une application interactive permettant d'explorer et de visualiser les tendances salariales mondiales dans le secteur de la Data Science.

##  Objectifs du Projet
L'objectif principal est d'extraire des informations pertinentes à partir d'un jeu de données brut pour comprendre les facteurs qui influencent la rémunération des professionnels de la donnée (Data Scientists, Data Engineers, ML Engineers, etc.).
- Identifier les zones géographiques les plus rémunératrices.
- Analyser l'impact de l'expérience et de la taille de l'entreprise.
- Étudier l'évolution des salaires au fil des années.

##  Résumé de l'Application Streamlit
L'application propose un tableau de bord (Dashboard) interactif avec :
- **Filtres dynamiques :** Sélection par plage de salaire, niveau d'expérience et taille d'entreprise.
- **Indicateurs Clés (KPI) :** Affichage en temps réel du salaire moyen, médian et du volume de postes.
- **Exportation :** Possibilité de télécharger les données filtrées au format CSV.
- **Design optimisé :** Interface en mode sombre (anthracite) pour un meilleur confort visuel.

##  Bibliothèques Utilisées
Pour mener à bien ce projet, les bibliothèques Python suivantes ont été mobilisées :
- **Streamlit** : Pour la création de l'interface web interactive.
- **Pandas** : Pour la manipulation et le nettoyage des données.
- **NumPy** : Pour les calculs statistiques.
- **Plotly Express** : Pour les graphiques interactifs (Treemap, Violin, Boxplot).
- **Matplotlib & Seaborn** : Pour les analyses statistiques avancées (Matrice de corrélation).

##  Analyses Réalisées
L'application explore plusieurs dimensions :
1. **Masse Salariale :** Répartition financière par intitulé de poste via un Treemap.
2. **Impact Géographique :** Comparaison détaillée entre les USA et le reste du monde.
3. **Évolution Temporelle :** Courbes d'évolution des salaires pour les 10 métiers les plus représentés.
4. **Télétravail :** Analyse de la corrélation entre le ratio de travail à distance et le salaire.
5. **Distribution Locale :** Zoom spécifique sur le marché français.

##  Source des Données
Les données proviennent du dataset public **"Data Science Job Salaries"** disponible sur Kaggle.
- **Lien des données :** https://www.kaggle.com/datasets/ .

---
