import json
import os

def create_notebook():
    cells = []

    # --- CELL 1: Imports & Setup ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# FitFam Data Extraction & Visualization for Manager Presentation\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "from lifelines import KaplanMeierFitter\n",
            "import sys\n",
            "import os\n",
            "\n",
            "# Styles\n",
            "sns.set_theme(style=\"whitegrid\", context=\"talk\")\n",
            "plt.rcParams['figure.figsize'] = (12, 6)\n",
            "\n",
            "# Data Loading\n",
            "sys.path.append(os.path.abspath(os.path.join('..', 'src')))\n",
            "from data_loader import FitFamDataLoader\n",
            "\n",
            "print(\"Loading Raw Data...\")\n",
            "loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))\n",
            "df = loader.get_unified_data()\n",
            "df['start_time'] = pd.to_datetime(df['start_time'])\n",
            "df = df[df['start_time'] >= '2023-01-01'].copy() # Focus on recent data\n",
            "print(f\"Data Loaded: {len(df)} events\")"
        ]
    })

    # --- CELL 2: Feature Engineering (Leader Metrics) ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Calculate Leader Metrics (Consistency, Tenure, Popularity)\n",
            "\n",
            "# Event Size\n",
            "event_counts = df.groupby('event_id').size()\n",
            "df['event_size'] = df['event_id'].map(event_counts)\n",
            "\n",
            "# Leader Stats\n",
            "leaders_df = df[df['is_leader'] == 1].copy()\n",
            "leader_stats = []\n",
            "\n",
            "print(\"Calculating Leader Metrics...\")\n",
            "for user_id, group in leaders_df.groupby('user_id'):\n",
            "    if len(group) < 5: continue # Filter strictly casual leaders\n",
            "    \n",
            "    dates = group['start_time'].sort_values()\n",
            "    gaps = dates.diff().dt.total_seconds() / (24 * 3600)\n",
            "    consistency_std = gaps.std() if not pd.isna(gaps.std()) else 0\n",
            "    popularity = group['event_size'].mean()\n",
            "    tenure_days = (dates.iloc[-1] - dates.iloc[0]).days\n",
            "    \n",
            "    leader_stats.append({\n",
            "        'leader_user_id': user_id,\n",
            "        'consistency_std': consistency_std,\n",
            "        'popularity_avg_size': popularity,\n",
            "        'tenure_days': tenure_days\n",
            "    })\n",
            "\n",
            "df_leaders = pd.DataFrame(leader_stats)\n",
            "print(f\"Leaders Analyzed: {len(df_leaders)}\")"
        ]
    })

    # --- CELL 3: Cohort Construction (Dominant Leader) ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 2. Connect Users to their \"Dominant Leader\"\n",
            "\n",
            "# Identify who led whom\n",
            "attendance = df[['user_id', 'event_id']].merge(df[['event_id', 'is_leader', 'user_id']], on='event_id', suffixes=('', '_leader'))\n",
            "attendance = attendance[(attendance['is_leader'] == 1) & (attendance['user_id'] != attendance['user_id_leader'])]\n",
            "\n",
            "# Find most frequent leader for each user\n",
            "dominant = attendance.groupby(['user_id', 'user_id_leader']).size().reset_index(name='count')\n",
            "dominant = dominant.sort_values(['user_id', 'count'], ascending=[True, False]).drop_duplicates('user_id')\n",
            "\n",
            "# Merge Leader Metrics to User\n",
            "cohorts = dominant.merge(df_leaders, left_on='user_id_leader', right_on='leader_user_id')\n",
            "\n",
            "# Calculate User Outcomes (Retention)\n",
            "user_dates = df.groupby('user_id')['start_time'].agg(['min', 'max'])\n",
            "cohorts = cohorts.merge(user_dates, on='user_id')\n",
            "\n",
            "# Churn Flag: Inactive for > 90 days relative to NOW\n",
            "NOW = df['start_time'].max()\n",
            "cohorts['days_since_last'] = (NOW - cohorts['max']).dt.days\n",
            "cohorts['is_active'] = (cohorts['days_since_last'] <= 90).astype(int)\n",
            "cohorts['duration'] = (cohorts['max'] - cohorts['min']).dt.days\n",
            "cohorts.loc[cohorts['duration'] == 0, 'duration'] = 1\n",
            "cohorts['churned'] = 1 - cohorts['is_active']\n",
            "\n",
            "print(f\"User Cohorts Constructed: {len(cohorts)} users linked to leaders.\")"
        ]
    })

    # --- CELL 3b: Calculate Leader Stats (Frequency) ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Add Frequency (Events Per Month) to Leaders\n",
            "# We calculate this based on their active lifespan\n",
            "leader_freq = []\n",
            "for user_id, group in df[df['is_leader']==1].groupby('user_id'):\n",
            "    if len(group) < 5: continue\n",
            "    dates = group['start_time'].sort_values()\n",
            "    duration_months = ((dates.iloc[-1] - dates.iloc[0]).days / 30.0)\n",
            "    duration_months = max(duration_months, 1) # Avoid div by zero\n",
            "    freq = len(group) / duration_months\n",
            "    leader_freq.append({'leader_user_id': user_id, 'events_per_month': freq})\n",
            "\n",
            "df_freq = pd.DataFrame(leader_freq)\n",
            "cohorts = cohorts.merge(df_freq, on='leader_user_id', how='left')\n",
            "\n",
            "# Calculate Leader Retention Score (Avg retention of their cohort)\n",
            "leader_scores = cohorts.groupby('leader_user_id')['is_active'].mean().reset_index(name='leader_retention_rate')\n",
            "cohorts = cohorts.merge(leader_scores, on='leader_user_id', how='left')"
        ]
    })

     # --- CELL 4: Profiling the Best ---
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## The Rhythm of High Retention Leaders\n",
            "We analyze the **Top 25% of Leaders** (ranked by the retention rate of their students).\n",
            "What is their \"Signature Rhythm\"?"
        ]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Segment Leaders into Quartiles by Retention Rate\n",
            "unique_leaders = cohorts[['leader_user_id', 'leader_retention_rate', 'consistency_std', 'events_per_month']].drop_duplicates()\n",
            "unique_leaders['Performance_Tier'] = pd.qcut(unique_leaders['leader_retention_rate'], 4, labels=['Bottom 25%', 'Mid-Low', 'Mid-High', 'Top 25%'])\n",
            "\n",
            "# Stats of the Top 25%\n",
            "top_leaders = unique_leaders[unique_leaders['Performance_Tier'] == 'Top 25%']\n",
            "print(\"--- PROFILE OF A TOP LEADER ---\")\n",
            "print(f\"Avg Consistency (StdDev): {top_leaders['consistency_std'].mean():.2f} days (Variance)\")\n",
            "print(f\"Avg Frequency: {top_leaders['events_per_month'].mean():.2f} events/month\")\n",
            "print(f\"Median Frequency: {top_leaders['events_per_month'].median():.2f} events/month\")\n",
            "\n",
            "# Visualization: Frequency vs Consistency (Colored by Performance)\n",
            "plt.figure(figsize=(10, 6))\n",
            "sns.scatterplot(data=unique_leaders, x='consistency_std', y='events_per_month', hue='Performance_Tier', palette='viridis', alpha=0.7)\n",
            "plt.title('The \"Sweet Spot\": Low Variance + Moderate Frequency', fontsize=16)\n",
            "plt.xlabel('Consistency (Days Variance) -> Lower is Better')\n",
            "plt.ylabel('Frequency (Events/Month)')\n",
            "plt.xlim(0, 30) # Zoom in\n",
            "plt.ylim(0, 10) # Zoom in\n",
            "plt.show()"
        ]
    })

     # --- CELL 6: Definitions ---
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## What is \"Reliability\"?\n",
            "We define **Reliability** as the combination of two objective metrics:\n",
            "1.  **Consistency (Schedule Reliability):** Does this event happen at the same time every week? (Low variance is good).\n",
            "2.  **Tenure (Institutional Reliability):** Has this leader been here for a long time? (Experience is good).\n",
            "\n",
            "We will analyze each separately."
        ]
    })

    # --- CELL 5: Metric 1 - Consistency Analysis ---
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## Metric 1: Consistency (Schedule Variance)\n*\"Can I count on this event happening next week?\"*"]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create Consistency Bins (Lower StdDev = Better)\n",
            "cohorts['const_tier'] = pd.qcut(cohorts['consistency_std'], 4, labels=[\"Tier 1 (Reliable)\", \"Tier 2\", \"Tier 3\", \"Tier 4 (Chaotic)\"])\n",
            "const_retention = cohorts.groupby('const_tier')['is_active'].mean().reset_index()\n",
            "\n",
            "# Plot Bar Chart\n",
            "plt.figure(figsize=(10, 5))\n",
            "sns.barplot(data=const_retention, x='const_tier', y='is_active', palette='magma_r')\n",
            "plt.title('Retention by Leader Consistency (Low Variance)', fontsize=16)\n",
            "plt.ylabel('User Retention Rate')\n",
            "plt.ylim(0, 0.4)\n",
            "plt.show()"
        ]
    })

    # --- CELL 6: Metric 1 - Consistency Survival Curve ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Survival Curve for Consistency\n",
            "plt.figure(figsize=(12, 6))\n",
            "kmf = KaplanMeierFitter()\n",
            "for tier in [\"Tier 1 (Reliable)\", \"Tier 4 (Chaotic)\"]:\n",
            "    mask = cohorts['const_tier'] == tier\n",
            "    kmf.fit(cohorts[mask]['duration'], cohorts[mask]['churned'], label=tier)\n",
            "    kmf.plot_survival_function(ci_show=False, linewidth=3)\n",
            "plt.title('User Survival: Reliable vs Chaotic Schedule', fontsize=16)\n",
            "plt.xlabel('Days in Community')\n",
            "plt.xlim(0, 365)\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.show()"
        ]
    })

    # --- CELL 7: Metric 2 - Tenure Analysis ---
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## Metric 2: Tenure (Experience)\n*\"Does this leader have the social capital to anchor the group?\"*"]
    })
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create Tenure Bins\n",
            "# We define buckets: <6 Months, 6-12 Months, 1-2 Years, >2 Years\n",
            "bins = [-1, 180, 365, 730, 9999]\n",
            "labels = ['< 6 Months', '6-12 Months', '1-2 Years', '> 2 Years']\n",
            "cohorts['tenure_tier'] = pd.cut(cohorts['tenure_days'], bins=bins, labels=labels)\n",
            "tenure_retention = cohorts.groupby('tenure_tier')['is_active'].mean().reset_index()\n",
            "\n",
            "# Plot Bar Chart\n",
            "plt.figure(figsize=(10, 5))\n",
            "sns.barplot(data=tenure_retention, x='tenure_tier', y='is_active', palette='viridis')\n",
            "plt.title('Retention by Leader Tenure (Experience)', fontsize=16)\n",
            "plt.ylabel('User Retention Rate')\n",
            "plt.ylim(0, 0.4)\n",
            "plt.show()"
        ]
    })
    
     # --- CELL 8: Metric 2 - Tenure Survival Curve ---
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Survival Curve for Tenure\n",
            "plt.figure(figsize=(12, 6))\n",
            "kmf_tenure = KaplanMeierFitter()\n",
            "for tier in ['< 6 Months', '> 2 Years']:\n",
            "    mask = cohorts['tenure_tier'] == tier\n",
            "    kmf_tenure.fit(cohorts[mask]['duration'], cohorts[mask]['churned'], label=tier)\n",
            "    kmf_tenure.plot_survival_function(ci_show=False, linewidth=3)\n",
            "plt.title('User Survival: New Leader (<6mo) vs Veteran (>2yr)', fontsize=16)\n",
            "plt.xlabel('Days in Community')\n",
            "plt.xlim(0, 365)\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.show()"
        ]
    })

    # --- Write Notebook ---
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.8"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    output_path = os.path.join(r'd:\shanghai\SR01\FitFam_research\hypothesis_2', 'Manager_Presentation_Charts.ipynb')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    
    print(f"Notebook created: {output_path}")

if __name__ == "__main__":
    create_notebook()
