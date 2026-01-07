import pandas as pd
import numpy as np
import sys
import os
from lifelines import CoxPHFitter

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def main():
    print("--- Starting Refined Analysis (Popularity + Cohort View) ---")
    
    # 1. Load Data
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()
    
    # 2. Calculate Event Counts (for Popularity)
    event_counts = df.groupby('event_id').size()
    df['event_size'] = df['event_id'].map(event_counts)

    # 3. Calculate Leader Metrics
    leaders_df = df[df['is_leader'] == 1].copy()
    leader_stats = []
    
    for user_id, group in leaders_df.groupby('user_id'):
        if len(group) < 5: continue
        
        dates = group['start_time'].sort_values()
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        consistency_std = gaps.std()
        
        # Popularity: Mean size
        popularity = group['event_size'].mean()
        
        # Frequency: Events / Month
        # Avoid division by zero
        tenure_days = (dates.iloc[-1] - dates.iloc[0]).days
        months = max(tenure_days / 30, 0.5) 
        frequency = len(group) / months

        leader_stats.append({
            'leader_user_id': user_id,
            'consistency_std': consistency_std if not pd.isna(consistency_std) else 0,
            'popularity_avg_size': popularity,
            'frequency_monthly': frequency,
            'tenure_days': tenure_days
        })
    
    df_leaders = pd.DataFrame(leader_stats).set_index('leader_user_id')
    print(f"Analyzed {len(df_leaders)} leaders.")
    
    # 4. Identify Dominant Leader
    event_leader_map = leaders_df[['event_id', 'user_id']].drop_duplicates('event_id')
    event_leader_map.columns = ['event_id', 'leader_id']
    
    attendance = df[['user_id', 'event_id', 'start_time', 'category_name']].merge(event_leader_map, on='event_id', how='left')
    attendance = attendance.dropna(subset=['leader_id'])
    attendance = attendance[attendance['user_id'] != attendance['leader_id']] 
    
    
    # 5. Cohort Data with Category
    # We need to know the 'Activity Type' (Category) for the user-leader relationship
    # Group by User, Leader, AND Category to find the dominant trio
    attendance['category_name'] = attendance['category_name'].fillna('Unknown').astype(str)
    # Simplify category: take the first one if comma-separated
    attendance['primary_category'] = attendance['category_name'].apply(lambda x: x.split(',')[0].strip())
    
    ul_counts = attendance.groupby(['user_id', 'leader_id', 'primary_category']).size().reset_index(name='count')
    ul_counts.sort_values(['user_id', 'count'], ascending=[True, False], inplace=True)
    
    # Take top 1
    dominant = ul_counts.drop_duplicates('user_id', keep='first')[['user_id', 'leader_id', 'primary_category']]
    dominant.columns = ['user_id', 'dominant_leader_id', 'dominant_category']
    
    # 5. Cohort Data
    user_last = df.sort_values('start_time').drop_duplicates('user_id', keep='last')[['user_id', 'start_time']]
    NOW = df['start_time'].max()
    user_last['is_retained'] = ((NOW - user_last['start_time']).dt.days <= 90).astype(int)
    # NB: For Cox, Event=Churn. For Retention Table, Value=Retained.
    user_last['churn_event'] = ((NOW - user_last['start_time']).dt.days > 90).astype(int)
    
    cohorts = dominant.merge(user_last, on='user_id')
    cohorts = cohorts.merge(df_leaders, left_on='dominant_leader_id', right_index=True)
    
    user_first = df.sort_values('start_time').drop_duplicates('user_id', keep='first')[['user_id', 'start_time', 'gender']]
    cohorts = cohorts.merge(user_first[['user_id', 'start_time', 'gender']], on='user_id', suffixes=('_last', '_first'))
    cohorts['duration'] = (cohorts['start_time_last'] - cohorts['start_time_first']).dt.days
    cohorts.loc[cohorts['duration'] == 0, 'duration'] = 1

    # Filter for Top 5 Categories to ensure statistical power
    top_categories = cohorts['dominant_category'].value_counts().nlargest(5).index.tolist()
    print(f"\nFiltering for Top 5 Categories: {top_categories}")
    cohorts = cohorts[cohorts['dominant_category'].isin(top_categories)].copy()

    # 6. Descriptive Analysis
    print("\n--- Descriptive Cohort Analysis ---")
    cohorts['consistency_tier'] = pd.qcut(cohorts['consistency_std'], 4, labels=["Tier 1 (Best)", "Tier 2", "Tier 3", "Tier 4 (Worst)"])
    cohorts['popularity_tier'] = pd.qcut(cohorts['popularity_avg_size'], 4, labels=["Tier 4 (Smallest)", "Tier 3", "Tier 2", "Tier 1 (Largest)"])
    
    print("\nRetention Rate by Activity Type (Category):")
    print(cohorts.groupby("dominant_category")["is_retained"].mean().round(4).sort_values(ascending=False))
    
    print("\nRetention Rate by Consistency Tier:")
    print(cohorts.groupby("consistency_tier")["is_retained"].mean().round(4))
    
    # 7. Stratified Cox Regression
    print("\n--- Stratified Cox Proportional Hazards Model ---")
    print("Stratifying by 'dominant_category' to control for activity type baseline differences.")
    
    cox_df = cohorts[['duration', 'churn_event', 'consistency_std', 'frequency_monthly', 'tenure_days', 'gender', 'dominant_category']].copy()
    cox_df['gender'] = cox_df['gender'].fillna('Unknown')
    cox_df = pd.get_dummies(cox_df, columns=['gender'], drop_first=True)
    
    # Rename columns for CoxPH
    cox_df.columns = [c.replace(' ', '_') for c in cox_df.columns]
    
    cph = CoxPHFitter(penalizer=0.1)
    
    try:
        cph.fit(cox_df, duration_col='duration', event_col='churn_event', strata=['dominant_category'])
        print("\nCox Summary (Stratified):")
        print(cph.summary[['coef', 'exp(coef)', 'p']])
    except Exception as e:
        print(f"Cox Model Failed: {e}")

if __name__ == "__main__":
    main()
