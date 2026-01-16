import pandas as pd
import numpy as np
import sys
import os

# Add src to path for data loader
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def analyze_profile():
    print("Loading Data...")
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()

    # 1. Leader Metrics
    leaders_df = df[df['is_leader'] == 1].copy()
    leader_stats = []
    
    for user_id, group in leaders_df.groupby('user_id'):
        if len(group) < 5: continue
        dates = group['start_time'].sort_values()
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        consistency_std = gaps.std() if not pd.isna(gaps.std()) else 0
        
        # Frequency
        duration_months = ((dates.iloc[-1] - dates.iloc[0]).days / 30.0)
        duration_months = max(duration_months, 1)
        freq = len(group) / duration_months
        
        tenure_days = (dates.iloc[-1] - dates.iloc[0]).days
        
        leader_stats.append({
            'leader_user_id': user_id,
            'consistency_std': consistency_std,
            'events_per_month': freq,
            'tenure_days': tenure_days
        })
    
    df_leaders = pd.DataFrame(leader_stats)

    # 2. Cohorts & Retention
    attendance = df[['user_id', 'event_id']].merge(df[['event_id', 'is_leader', 'user_id']], on='event_id', suffixes=('', '_leader'))
    attendance = attendance[(attendance['is_leader'] == 1) & (attendance['user_id'] != attendance['user_id_leader'])]
    dominant = attendance.groupby(['user_id', 'user_id_leader']).size().reset_index(name='count')
    dominant = dominant.sort_values(['user_id', 'count'], ascending=[True, False]).drop_duplicates('user_id')
    
    cohorts = dominant.merge(df_leaders, left_on='user_id_leader', right_on='leader_user_id')
    
    user_dates = df.groupby('user_id')['start_time'].agg(['min', 'max'])
    cohorts = cohorts.merge(user_dates, on='user_id')
    NOW = df['start_time'].max()
    cohorts['days_since_last'] = (NOW - cohorts['max']).dt.days
    cohorts['is_active'] = (cohorts['days_since_last'] <= 90).astype(int)
    
    # 3. Leader Performance
    leader_scores = cohorts.groupby('leader_user_id')['is_active'].mean().reset_index(name='leader_retention_rate')
    unique_leaders = df_leaders.merge(leader_scores, on='leader_user_id')

    # 4. Top 25% Stats
    cutoff = unique_leaders['leader_retention_rate'].quantile(0.75)
    top_leaders = unique_leaders[unique_leaders['leader_retention_rate'] >= cutoff]
    
    print("\n--- RESULTS: Rhythm of Top 25% High-Retention Leaders ---")
    print(f"Number of Top Leaders: {len(top_leaders)}")
    print(f"Mean Frequency: {top_leaders['events_per_month'].mean():.2f} events/month")
    print(f"Median Frequency: {top_leaders['events_per_month'].median():.2f} events/month")
    print(f"Mean Consistency (StdDev): {top_leaders['consistency_std'].mean():.2f} days (Lower is better)")
    print(f"Mean Tenure: {top_leaders['tenure_days'].mean():.0f} days (approx {top_leaders['tenure_days'].mean()/365:.1f} years)")
    print(f"Median Tenure: {top_leaders['tenure_days'].median():.0f} days (approx {top_leaders['tenure_days'].median()/365:.1f} years)")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    analyze_profile()
