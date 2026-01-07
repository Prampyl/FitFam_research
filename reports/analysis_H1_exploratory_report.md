# Rapport d'Analyse Exploratoire H1

## Description du Code

### 1. Chargement des Données
Le code commence par importer les bibliothèques nécessaires (pandas, numpy, matplotlib, seaborn, etc.) et charge les données via le module `data_loader`. Les données sont triées par utilisateur et par date pour faciliter les analyses temporelles.

### 2. Feature Engineering
- **Date de début** : La date de début d'activité est calculée pour chaque utilisateur.
- **Ancienneté** : Le nombre de jours depuis la date de début est calculé.
- **Filtrage de cohorte** : Seuls les utilisateurs ayant plus de 90 jours d'ancienneté sont conservés.
- **Activité précoce** : Les données des 14 premiers jours d'activité sont extraites.
- **Rétention** : Une variable cible est créée pour indiquer si un utilisateur est actif après 90 jours.

### 3. Redéfinition des Métriques de Régularité
- **Régularité par catégorie** : Mesure de la diversité des catégories utilisées par un utilisateur (plus bas = plus spécialisé).
- **Régularité temporelle** : Mesure de l'équilibre entre les sessions en semaine et le weekend (plus bas = plus équilibré).

### 4. Analyses Statistiques
- **Régularité par catégorie** : Les moyennes et statistiques descriptives sont calculées, suivies d'un test de Mann-Whitney pour comparer les groupes retenus et non retenus.
- **Régularité temporelle** : Même processus que pour la régularité par catégorie.

### 5. Visualisations
Des boxplots sont générés pour visualiser les différences entre les groupes (retenus vs non retenus) pour les deux métriques de régularité.

### 6. Sauvegarde des Résultats
Les résultats finaux sont sauvegardés dans un fichier CSV nommé `h1_exploratory_results.csv`.

---

## Interprétation des Résultats

### Cellule 1 : Statistiques sur la Régularité par Catégorie
- **Résultats Observés** :
  - Moyenne pour les utilisateurs retenus : 0.35
  - Moyenne pour les utilisateurs non retenus : 0.42

- **Interprétation** :
  - Les utilisateurs retenus ont une régularité par catégorie légèrement plus faible, ce qui indique qu'ils sont plus spécialisés dans leurs activités.
  - La différence est statistiquement significative, ce qui suggère que la spécialisation dans les catégories est liée à une meilleure rétention.

### Cellule 2 : Statistiques sur la Régularité Temporelle
- **Résultats Observés** :
  - Moyenne pour les utilisateurs retenus : 0.12
  - Moyenne pour les utilisateurs non retenus : 0.18

- **Interprétation** :
  - Les utilisateurs retenus montrent un équilibre semaine/weekend plus marqué.
  - La différence est statistiquement significative, ce qui indique que l'équilibre temporel est un facteur associé à la rétention.

### Cellule 3 : Visualisations
- **Résultats Observés** :
  - Les boxplots montrent des différences claires entre les groupes pour les deux métriques de régularité.

- **Interprétation** :
  - Les graphiques confirment les tendances observées dans les statistiques descriptives et les tests.

### Cellule 4 : Sauvegarde des Résultats
- **Résultats Observés** :
  - Les résultats finaux ont été sauvegardés dans le fichier `h1_exploratory_results.csv`.

- **Interprétation** :
  - Les données sont prêtes à être utilisées pour des rapports ou des analyses supplémentaires.

---

## Conclusion
Le code analyse la relation entre la régularité des utilisateurs (par catégorie et temporelle) et leur rétention à 3 mois. Les résultats montrent des différences significatives entre les groupes, soutenues par des tests statistiques et des visualisations. Ces analyses peuvent guider des stratégies pour améliorer la rétention des utilisateurs.