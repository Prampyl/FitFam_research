# Rapport d'Analyse - Hypothèse H1 : Impact de l'Activité Précoce sur la Rétention à 3 Mois

## Date du Rapport
6 janvier 2026

## Auteur
Analyse automatisée basée sur le notebook `analysis_H1.ipynb`

## Contexte du Projet
Ce rapport analyse les données de l'application FitFam pour tester l'hypothèse H1 concernant l'impact de l'activité précoce des utilisateurs sur leur rétention à long terme.

## 1. Objectif de l'Analyse
L'objectif principal est de déterminer si l'activité des utilisateurs durant leurs 14 premiers jours d'inscription influence leur rétention à 3 mois. Plus précisément, nous testons deux aspects :
- **Fréquence** : Le nombre total de sessions dans les 14 premiers jours
- **Régularité** : La régularité des visites (mesurée par l'écart-type des jours entre sessions)

L'hypothèse sous-jacente est que les utilisateurs plus actifs et réguliers au début sont plus susceptibles de rester engagés sur le long terme.

## 2. Méthodologie

### 2.1 Chargement des Données
- Utilisation du module `FitFamDataLoader` pour charger les données unifiées
- Données triées par utilisateur et date
- Période d'analyse : du 2018-08-07 au 2025-03-22
- Nombre total d'utilisateurs : 21 304
- Nombre total de sessions : 405 861

### 2.2 Préparation des Données (Feature Engineering)
- **Calcul de l'ancienneté** : Pour chaque utilisateur, détermination de la date de première session
- **Filtrage de cohorte** : Seuls les utilisateurs inscrits depuis plus de 90 jours sont analysés (pour permettre l'évaluation de la rétention à 3 mois)
- **Variables explicatives (X)** :
  - Fréquence : Nombre de sessions dans les 14 premiers jours
  - Régularité : Écart-type des jours entre sessions (nécessite au moins 3 sessions)
- **Variable cible (Y)** : Rétention à 3 mois (1 si l'utilisateur a eu au moins une session après 90 jours, 0 sinon)

### 2.3 Analyse Statistique
- Visualisations : Boxplots comparant les groupes retenus vs non retenus
- Tests statistiques : Test de Mann-Whitney U (non-paramétrique) pour comparer les distributions
- Niveau de significativité : α = 0.05

## 3. Résultats

### 3.1 Statistiques Descriptives
D'après les données analysées (sur 21 016 utilisateurs analysables) :

- **Fréquence moyenne (14 premiers jours)** :
  - Utilisateurs retenus : 3.01 sessions
  - Utilisateurs non retenus : 1.69 sessions

- **Régularité moyenne (écart-type des jours)** :
  - Utilisateurs retenus : 1.96 jours
  - Utilisateurs non retenus : 1.90 jours

### 3.2 Visualisations
Les boxplots montrent :
- Pour la fréquence : Les utilisateurs retenus ont une médiane plus élevée (environ 3 sessions vs 1.5 pour les non-retenus), confirmant l'impact positif de l'activité précoce
- Pour la régularité : Les distributions sont très similaires entre les groupes, avec une légère tendance à une plus grande variabilité chez les retenus (médiane légèrement plus élevée)

### 3.3 Tests Statistiques
- **Fréquence** :
  - Test de Mann-Whitney U : p-valeur = 0.00000
  - Résultat : Significatif - Les utilisateurs retenus viennent effectivement plus souvent dans les 14 premiers jours

- **Régularité** :
  - Test de Mann-Whitney U : p-valeur = 0.99979
  - Résultat : Non significatif - Contrairement à l'hypothèse, les utilisateurs retenus ne sont pas nécessairement plus réguliers

## 4. Discussion
Les résultats montrent un impact clair de la fréquence d'activité précoce sur la rétention à 3 mois. Les utilisateurs qui s'engagent plus intensivement dès le début ont une meilleure chance de rester actifs sur le long terme.

Cependant, concernant la régularité, les résultats suggèrent que l'écart-type des jours entre sessions n'est pas un bon prédicteur de rétention. En fait, les utilisateurs qui restent pourraient explorer différents types de cours à différents moments, créant une apparente irrégularité qui masque en réalité un engagement plus profond avec l'offre complète de FitFam.

Cette observation remet en question l'idée que la "régularité mécanique" (comme venir 3 fois par semaine toujours le même jour) soit le meilleur indicateur de fidélité. Au contraire, une exploration diversifiée de l'offre pourrait être le signe d'un engagement plus durable.

## 5. Limites de l'Analyse
- Analyse rétrospective sur données historiques
- Définition de la rétention basée uniquement sur la présence d'au moins une session après 90 jours
- Régularité calculée seulement pour les utilisateurs ayant au moins 3 sessions dans les 14 premiers jours
- Pas de contrôle d'autres facteurs confondants (âge, localisation, type d'activités préférées, etc.)

## 6. Recommandations
1. **Actions marketing** : Encourager l'activité intensive dans les premières semaines via des programmes d'onboarding
2. **Révision des métriques** : Considérer des indicateurs d'engagement plus nuancés que la simple régularité temporelle
3. **Analyses complémentaires** : Étudier l'impact des types d'activités et de la diversité d'exploration sur la rétention
4. **Suivi longitudinal** : Mettre en place un système de tracking en temps réel pour valider ces insights

## 7. Conclusion
L'hypothèse H1 est partiellement validée : la fréquence d'activité précoce est un prédicteur significatif de la rétention à 3 mois. Cependant, la régularité telle que mesurée n'apparaît pas comme un facteur déterminant, suggérant que les stratégies de fidélisation devraient privilégier l'engagement global plutôt que la routine stricte.

Cette analyse fournit des insights précieux pour optimiser les efforts de rétention de FitFam et mérite d'être complétée par des études plus approfondies.