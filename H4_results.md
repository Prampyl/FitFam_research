
# Analyse H4 : Résilience Environnementale & Fidélité

**Date :** 17 Décembre 2025
**Auteur :** Data Science Team
**Sujet :** Impact des conditions environnementales extrêmes sur la rétention utilisateur.

---

## 1. Hypothèse Initiale (H4)

> **"Extreme environmental conditions (high temperature, pollution) serve as a loyalty filter: users who attend during these times show higher long-term retention, while casual users exhibit strong seasonal churn."**

## 2. Synthèse des Résultats

L'analyse des données **valide l'hypothèse**, avec une distinction majeure entre l'hiver (pollution) et l'été (chaleur).

| Condition | Période | Impact sur Occasionnels | Impact sur Rétention | Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Pollution (AQI)** | Hiver (Déc-Fév) |  Churn Massif (-70%) |  Très Fort | **Vrai Filtre de Loyauté** |
| **Chaleur / Pluie** | Été (Juil-Août) |  Pic d'activité |  Moyen/Fort | **Levier d'Acquisition** |

---

## 3. Analyse Détaillée

### A. L'Hiver : Le "Kill Switch" des utilisateurs occasionnels
L'hiver, marqué par des pics de pollution, agit comme un filtre drastique. C'est la période la plus critique pour le churn.

* **Preuve environnementale :** Les annulations liées à la qualité de l'air (AQI > 150) explosent en Décembre (374) et Janvier (340), contre < 40/mois en été.
* **Comportement des "Casuals" :** L'activité des utilisateurs occasionnels s'effondre. Février ne représente que **3.5%** de leur volume annuel.
* **Rétention des survivants :** Ceux qui participent en hiver sont l'élite de la communauté.
    * *Tenure Médiane (Hivernants) :* **342 jours**
    * *Tenure Médiane (Évitement Hiver) :* **0 jour** (Souvent des "one-off")

### B. L'Été : Une résilience inattendue
Contrairement à l'hypothèse, la chaleur ou la pluie estivale ne font pas fuir les utilisateurs occasionnels.

* **Activité soutenue :** Malgré les annulations météo (pics en Juillet/Septembre), les utilisateurs occasionnels sont **sur-représentés** en été.
* **Motivation > Confort :** Juillet et Août représentent **~22%** de l'activité totale des occasionnels. La motivation saisonnière (ex: "Summer Body") semble compenser l'inconfort climatique.

---

## 4. Données Clés

### Comparaison de la Rétention (Tenure)
*La tenure est définie comme le nombre de jours entre la première et la dernière participation.*

| Segment Utilisateur | Tenure Médiane (Jours) | Interprétation |
| :--- | :--- | :--- |
| **Participants Hiver** (Resilient) | **342.0** | Utilisateurs "Core" |
| **Participants Été** | 245.0 | Utilisateurs engagés mais saisonniers |
| **Utilisateurs Non-Hiver** | 0.0 | Risque de churn immédiat |

### Saisonnalité des Utilisateurs Occasionnels vs Core
*Pourcentage des check-ins annuels réalisés par mois.*

| Mois | Occasionnels (Casual) | Engagés (Core) | Observation |
| :--- | :--- | :--- | :--- |
| **Février** | **3.5%** (Min) | 4.6% |  Creux hivernal |
| **Mai** | 7.1% | 8.4% | |
| **Juillet** | **10.1%** | 9.8% |  Pic estival |
| **Septembre** | **12.3%** (Max) | 10.2% |  Rentrée |

---

## 5. Recommandations Stratégiques

1.  **Campagne de Rétention "Winter Warrior" (Déc-Fév) :**
    * L'hiver est le moment critique. Il faut gamifier la présence durant les pics de pollution (en intérieur) pour éviter le décrochage massif.
    * *Action :* Récompenses exclusives pour la présence en Décembre/Janvier.

2.  **Acquisition Estivale (Juil-Août) :**
    * Ne pas craindre la météo en été. C'est une période d'acquisition naturelle.
    * *Action :* Convertir ces "Summer Casuals" en membres réguliers avant l'arrivée de l'automne.

---

*Méthodologie :*
* *Extreme Months : Jan, Feb, Jul, Aug, Dec.*
* *Casual User : Utilisateur avec une participation inférieure ou égale à la médiane (2).*
* *Resilient User : Utilisateur ayant participé au moins une fois durant un mois extrême.*
```