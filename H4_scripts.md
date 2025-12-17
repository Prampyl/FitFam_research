

`H4_scripts.md`

-----

````
# 🐍 Analyse H4 : Résilience Environnementale & Fidélité

Ce script a pour but de vérifier si les conditions difficiles (pollution en hiver, chaleur en été) agissent comme un filtre de fidélité pour les utilisateurs.

## 1. Chargement et Préparation des Données
**Ce que fait ce bloc :**
Il importe les outils nécessaires (`pandas`) et charge vos fichiers bruts. Ensuite, il nettoie les données pour ne garder que les utilisateurs qui sont *vraiment* venus aux événements (`checked_in == 1`) et associe chaque participation à une date précise.

```python
import pandas as pd
import numpy as np

# 1. Chargement des fichiers JSON
# Ces fichiers doivent être présents dans le même dossier que le script
events = pd.read_json('events.json')
event_user = pd.read_json('event_user.json')
cancellation_reasons = pd.read_json('cancellation_reasons.json')
cancellation_reason_event = pd.read_json('cancellation_reason_event.json')

# 2. Conversion des dates au format temporel
# Indispensable pour pouvoir extraire les mois et calculer des durées
events['start_time'] = pd.to_datetime(events['start_time'])
cancellation_reason_event['created_at'] = pd.to_datetime(cancellation_reason_event['created_at'])

# 3. Fusion des tables
# On ne garde que les participations effectives (checked_in == 1)
attended = event_user[event_user['checked_in'] == 1].copy()
# On ajoute les infos de l'événement (date, id) à chaque participation
df = attended.merge(events[['id', 'start_time']], left_on='event_id', right_on='id', how='left')

# Suppression des lignes sans date (bug de données potentiel)
df = df.dropna(subset=['start_time'])
````

## 2\. Définition des Saisons Extrêmes

**Ce que fait ce bloc :**
Il crée des repères temporels. On extrait le mois de chaque événement pour identifier s'il a eu lieu pendant une période "difficile" (Hiver ou Été caniculaire).

  * **Hiver/Pollution :** Décembre, Janvier, Février
  * **Été/Chaleur :** Juillet, Août

<!-- end list -->

```python
# Extraction du mois et de l'année
df['month'] = df['start_time'].dt.month
df['year'] = df['start_time'].dt.year

# Définition des "Mois Extrêmes"
# 1=Jan, 2=Fev, 7=Juil, 8=Août, 12=Déc
extreme_months = [1, 2, 7, 8, 12]

# On crée une colonne 'is_extreme' qui vaut 1 si le mois est extrême, 0 sinon
df['is_extreme'] = df['month'].isin(extreme_months).astype(int)
```

## 3\. Analyse de la Rétention (Durée de vie)

**Ce que fait ce bloc :**
C'est le cœur de l'analyse H4. Pour chaque utilisateur, on calcule :

1.  Sa durée de vie (`tenure` : date de fin - date de début).
2.  S'il a déjà bravé un mois extrême (`is_resilient`).
    Ensuite, on compare la durée de vie moyenne des "guerriers" (résilients) vs ceux qui évitent les conditions difficiles.

<!-- end list -->

```python
# Agrégation des stats par utilisateur
user_stats = df.groupby('user_id').agg(
    first_event=('start_time', 'min'),       # Date première venue
    last_event=('start_time', 'max'),        # Date dernière venue
    total_attendance=('event_id', 'count'),  # Nombre total de venues
    extreme_attendance=('is_extreme', 'sum') # Nombre de venues en mois extrêmes
).reset_index()

# Calcul de la "Tenure" en jours
user_stats['tenure_days'] = (user_stats['last_event'] - user_stats['first_event']).dt.days

# Définition du profil "Résilient" : A participé au moins une fois en conditions extrêmes
user_stats['is_resilient'] = user_stats['extreme_attendance'] > 0

# Comparaison finale
print("--- Comparaison de la Rétention (Résilients vs Non-Résilients) ---")
print(user_stats.groupby('is_resilient')['tenure_days'].agg(['mean', 'median', 'count']))
```

## 4\. Analyse du "Churn" Saisonnier

**Ce que fait ce bloc :**
Il sépare les utilisateurs en deux groupes : les "Occasionnels" (Casual) et les "Fidèles" (Core). On regarde ensuite mois par mois quel pourcentage de leur activité annuelle ils réalisent. Cela permet de voir si les occasionnels "disparaissent" l'hiver.

```python
# 1. Segmentation Casual vs Core
# On utilise la médiane (souvent 2 événements) comme seuil
median_attendance = user_stats['total_attendance'].median()
user_stats['user_type'] = np.where(user_stats['total_attendance'] > median_attendance, 'Core', 'Casual')

# On remet cette info dans le tableau principal
df = df.merge(user_stats[['user_id', 'user_type']], on='user_id', how='left')

# 2. Calcul de la saisonnalité
# On compte les venues par mois pour chaque groupe
group_totals = df.groupby('user_type').size().reset_index(name='total_checkins')
monthly_seasonality = df.groupby(['user_type', 'month']).size().reset_index(name='checkins')

# Normalisation (pour avoir des pourcentages)
monthly_seasonality = monthly_seasonality.merge(group_totals, on='user_type')
monthly_seasonality['percentage'] = monthly_seasonality['checkins'] / monthly_seasonality['total_checkins']

print("\n--- Pourcentage d'activité par mois (Saisonnalité) ---")
# Affichage sous forme de tableau croisé pour lecture facile
print(monthly_seasonality.pivot(index='month', columns='user_type', values='percentage'))
```

## 5\. Validation : Est-ce vraiment la pollution ?

**Ce que fait ce bloc :**
Pour être sûr que l'hiver correspond bien à la pollution (et non juste au froid), on regarde les *motifs d'annulation*. Si les annulations "AQI" (Qualité de l'air) explosent en hiver, l'hypothèse est validée.

```python
# On extrait le mois de création de l'annulation
cancellation_reason_event['month'] = cancellation_reason_event['created_at'].dt.month

# On compte les annulations par type et par mois
# ID 1 = Pollution (AQI > 150)
aqi_cancellations = cancellation_reason_event[cancellation_reason_event['cancellation_reason_id'] == 1].groupby('month').size()

# ID 2 = Mauvaise Météo (Pluie/Typhon)
weather_cancellations = cancellation_reason_event[cancellation_reason_event['cancellation_reason_id'] == 2].groupby('month').size()

print("\n--- Annulations cause 'Pollution' par mois ---")
print(aqi_cancellations)

print("\n--- Annulations cause 'Météo' par mois ---")
print(weather_cancellations)
```

```
```