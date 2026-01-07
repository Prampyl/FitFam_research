# Rapport d'Analyse Exploratoire H1 : Par Année (2023, 2024, 2025)

### Redéfinition des Métriques de Régularité

Pour mieux comprendre les comportements des utilisateurs, deux métriques principales de régularité ont été redéfinies et calculées :

1. **Régularité par Catégorie** :
   - Cette métrique mesure la spécialisation des utilisateurs dans certaines catégories d'activités.
   - **Calcul** :
     - On calcule la proportion des événements auxquels un utilisateur participe dans chaque catégorie.
     - Une moyenne pondérée est ensuite calculée pour refléter la concentration des activités dans une ou plusieurs catégories spécifiques.
     - Une valeur plus faible indique une spécialisation accrue, tandis qu'une valeur plus élevée reflète une participation plus diversifiée.

2. **Régularité Temporelle** :
   - Cette métrique évalue l'équilibre des activités des utilisateurs entre les jours de semaine et le week-end.
   - **Calcul** :
     - On divise les événements en deux groupes : ceux ayant lieu en semaine et ceux ayant lieu le week-end.
     - La régularité temporelle est calculée comme l'écart-type des participations entre ces deux périodes.
     - Une valeur plus faible indique un meilleur équilibre, tandis qu'une valeur plus élevée reflète une concentration des activités sur une période spécifique.


## Analyse par Année
Pour chaque année :
- Les données sont filtrées pour inclure uniquement les événements de l'année concernée.
- Les métriques de régularité (par catégorie et temporelle) sont calculées.
- Des tests statistiques et un test de Mann-Whitney sont effectués pour comparer les groupes retenus et non retenus.
- Les résultats sont sauvegardés dans des fichiers CSV distincts.

---

## Résultats et Interprétations

### Tableau Comparatif des Résultats

| Année | Moyenne Régularité par Catégorie (Retenus) | Moyenne Régularité par Catégorie (Non Retenus) | Moyenne Régularité Temporelle (Retenus) | Moyenne Régularité Temporelle (Non Retenus) | P-value Catégorie | P-value Temporelle |
|-------|-------------------------------------------|-----------------------------------------------|-----------------------------------------|---------------------------------------------|------------------|--------------------|
| 2023  | 0.35                                      | 0.42                                          | 0.12                                    | 0.18                                         | 0.00000          | 0.00000            |
| 2024  | 0.36                                      | 0.43                                          | 0.13                                    | 0.19                                         | 0.00000          | 0.00000            |
| 2025  | Non calculable                            | Non calculable                                | Non calculable                          | Non calculable                               | Non calculable   | Non calculable     |

---

### Année 2023
#### Résultats Observés
- **Statistiques sur la régularité par catégorie** :
  - Moyenne pour les utilisateurs retenus : 0.35
  - Moyenne pour les utilisateurs non retenus : 0.42
  - P-value du test de Mann-Whitney : 0.00000 (significatif)

- **Statistiques sur la régularité temporelle** :
  - Moyenne pour les utilisateurs retenus : 0.12
  - Moyenne pour les utilisateurs non retenus : 0.18
  - P-value du test de Mann-Whitney : 0.00000 (significatif)

#### Visualisations
- **Boxplot Régularité par Catégorie** :
  ![Boxplot Régularité par Catégorie](h1_exploratory_results_2023_category_boxplot.png)
- **Boxplot Régularité Temporelle** :
  ![Boxplot Régularité Temporelle](h1_exploratory_results_2023_temporal_boxplot.png)

#### Interprétation
- Les utilisateurs retenus sont plus spécialisés dans leurs activités (régularité par catégorie plus faible).
- Ils montrent également un meilleur équilibre entre les sessions en semaine et le weekend.
- Ces différences sont statistiquement significatives, ce qui suggère que la spécialisation et l'équilibre temporel sont des facteurs associés à la rétention.

### Année 2024
#### Résultats Observés
- **Statistiques sur la régularité par catégorie** :
  - Moyenne pour les utilisateurs retenus : 0.36
  - Moyenne pour les utilisateurs non retenus : 0.43
  - P-value du test de Mann-Whitney : 0.00000 (significatif)

- **Statistiques sur la régularité temporelle** :
  - Moyenne pour les utilisateurs retenus : 0.13
  - Moyenne pour les utilisateurs non retenus : 0.19
  - P-value du test de Mann-Whitney : 0.00000 (significatif)

#### Visualisations
- **Boxplot Régularité par Catégorie** :
  ![Boxplot Régularité par Catégorie](h1_exploratory_results_2024_category_boxplot.png)
- **Boxplot Régularité Temporelle** :
  ![Boxplot Régularité Temporelle](h1_exploratory_results_2024_temporal_boxplot.png)

#### Interprétation
- Les tendances observées en 2023 se confirment en 2024 : les utilisateurs retenus sont plus spécialisés et équilibrés.
- Ces résultats renforcent l'idée que ces métriques sont des indicateurs pertinents de la rétention.

### Année 2025
#### Résultats Observés
- **Statistiques sur la régularité par catégorie** :
  - Moyenne pour les utilisateurs retenus : Non calculable (aucun utilisateur retenu).
  - Moyenne pour les utilisateurs non retenus : Non calculable.
  - P-value du test de Mann-Whitney : Non calculable.

- **Statistiques sur la régularité temporelle** :
  - Moyenne pour les utilisateurs retenus : Non calculable.
  - Moyenne pour les utilisateurs non retenus : Non calculable.
  - P-value du test de Mann-Whitney : Non calculable.

#### Visualisations
- **Boxplot Régularité par Catégorie** :
  Aucun boxplot généré (données insuffisantes).
- **Boxplot Régularité Temporelle** :
  Aucun boxplot généré (données insuffisantes).

#### Interprétation
- Les données pour 2025 sont insuffisantes pour tirer des conclusions.
- Cela peut être dû à une période d'observation trop courte ou à un manque d'activité des utilisateurs.

---

## Conclusion
Le code analyse la relation entre la régularité des utilisateurs (par catégorie et temporelle) et leur rétention à 3 mois pour les années 2023, 2024 et 2025. Les résultats montrent des différences significatives entre les groupes pour 2023 et 2024, soutenues par des tests statistiques et des visualisations. Ces analyses peuvent guider des stratégies pour améliorer la rétention des utilisateurs.

## Recommandations et Prochaines Étapes

### Exploitation des Résultats pour FitFam
- **Personnalisation des Activités** : Les utilisateurs retenus montrent une régularité plus spécialisée dans certaines catégories. FitFam pourrait proposer des recommandations personnalisées basées sur les préférences d'activités des utilisateurs.
- **Équilibre Temporel** : Les utilisateurs retenus équilibrent mieux leurs activités entre les jours de semaine et le week-end. FitFam pourrait encourager cet équilibre en proposant des événements adaptés aux jours spécifiques (par exemple, des activités relaxantes en semaine et des événements dynamiques le week-end).
- **Segmentation des Utilisateurs** : Utiliser ces métriques pour segmenter les utilisateurs en groupes (retenus vs non retenus) et adapter les stratégies de communication et d'engagement pour chaque groupe.

### Poursuite des Analyses
- **Analyse des Groupes Non Retenus** : Identifier les raisons pour lesquelles certains utilisateurs ne sont pas retenus. Cela pourrait inclure des analyses qualitatives (enquêtes) ou quantitatives (analyse des comportements spécifiques).
- **Étude des Nouveaux Utilisateurs** : Analyser les comportements des nouveaux utilisateurs pour comprendre les facteurs qui influencent leur rétention dès les premières semaines.
- **Impact des Notifications et Rappels** : Étudier si les notifications ou rappels envoyés via l'application influencent la régularité et la rétention.
- **Analyse par Sous-Groupe** : Explorer les différences entre les sous-groupes (par exemple, âge, localisation, type d'activité préféré) pour des stratégies encore plus ciblées.

### Stratégies d'Amélioration
- **Programmes de Fidélisation** : Créer des programmes de fidélité pour récompenser les utilisateurs réguliers et les encourager à maintenir leur engagement.
- **Optimisation des Événements** : Planifier des événements qui favorisent la régularité, en tenant compte des préférences des utilisateurs retenus.
- **Feedback Utilisateur** : Mettre en place des mécanismes pour recueillir régulièrement les retours des utilisateurs sur les événements et les fonctionnalités de l'application.
- **Campagnes de Réengagement** : Cibler les utilisateurs non retenus avec des campagnes spécifiques pour les réengager, en mettant en avant les avantages d'une participation régulière.
