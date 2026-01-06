import pandas as pd
import numpy as np
import sys
import os
from lifelines import CoxPHFitter

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def main():
    print("--- Starting H2 Step 7: Dominant Leader Validation ---")
    
    # 1. Load Data
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()
    
    # 2. Recycle Leader Metrics Logic
    leaders_df = df[df['is_leader'] == 1].copy()
    leader_stats = []
    for user_id, group in leaders_df.groupby('user_id'):
        if len(group) < 5: continue 
        dates = group['start_time'].sort_values()
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        consistency_std = gaps.std()
        frequency = len(group) / ((dates.iloc[-1] - dates.iloc[0]).days / 30 + 0.1) # events per month

        leader_stats.append({
            'leader_user_id': user_id,
            'leader_consistency': consistency_std if not pd.isna(consistency_std) else 0,
            'leader_frequency': frequency,
            'leader_tenure': (dates.iloc[-1] - dates.iloc[0]).days
        })
    df_leaders = pd.DataFrame(leader_stats).set_index('leader_user_id')
    
    # 3. Identify Dominant Leader for each user
    print("Identifying Dominant Leaders...")
    # Map event -> leader
    event_leader_map = leaders_df[['event_id', 'user_id']].drop_duplicates('event_id')
    event_leader_map.columns = ['event_id', 'leader_id']
    
    attendance = df[['user_id', 'event_id', 'start_time', 'gender']].merge(event_leader_map, on='event_id', how='left')
    attendance = attendance.dropna(subset=['leader_id'])
    attendance = attendance[attendance['user_id'] != attendance['leader_id']] # exclude self
    
    # Count per user-leader pair
    ul_counts = attendance.groupby(['user_id', 'leader_id']).size().reset_index(name='count')
    ul_counts.sort_values(['user_id', 'count'], ascending=[True, False], inplace=True)
    
    dominant = ul_counts.drop_duplicates('user_id', keep='first')[['user_id', 'leader_id']]
    dominant.columns = ['user_id', 'dominant_leader_id']
    
    # 4. Build Dataset for Cox
    # Get user churn status
    user_last = df.sort_values('start_time').drop_duplicates('user_id', keep='last')[['user_id', 'start_time']]
    NOW = df['start_time'].max()
    user_last['days_since_last'] = (NOW - user_last['start_time']).dt.days
    user_last['churn_event'] = (user_last['days_since_last'] > 90).astype(int)
    
    user_first = df.sort_values('start_time').drop_duplicates('user_id', keep='first')[['user_id', 'start_time', 'gender']]
    user_first.rename(columns={'start_time': 'first_date'}, inplace=True)
    
    cohorts = user_first.merge(user_last[['user_id', 'churn_event', 'start_time']], on='user_id')
    cohorts.rename(columns={'start_time': 'last_date'}, inplace=True)
    cohorts['duration'] = (cohorts['last_date'] - cohorts['first_date']).dt.days
    cohorts.loc[cohorts['duration'] == 0, 'duration'] = 1
    
    # Merge with Dominant Leader
    cohorts = cohorts.merge(dominant, on='user_id')
    
    # Merge with Leader Metrics
    cohorts = cohorts.merge(df_leaders, left_on='dominant_leader_id', right_index=True)
    
    # 5. Run Cox PH
    print("Running Cox PH with Dominant Leader Metrics...")
    
    cox_df = cohorts[['duration', 'churn_event', 'leader_consistency', 'leader_frequency', 'leader_tenure', 'gender']].copy()
    cox_df['gender'] = cox_df['gender'].fillna('Unknown')
    cox_df = pd.get_dummies(cox_df, columns=['gender'], drop_first=True)
    cox_df.columns = [c.replace(' ', '_') for c in cox_df.columns]
    
    cph = CoxPHFitter(penalizer=0.1)
    try:
        cph.fit(cox_df, duration_col='duration', event_col='churn_event')
        
        print("\n--- Cox Results (Dominant Leader) ---")
        coef = cph.params_['leader_consistency']
        pval = cph.summary.loc['leader_consistency', 'p']
        print(f"Dominant Leader Consistency Coef: {coef:.4f}")
        print(f"Dominant Leader Consistency p-val: {pval:.4f}")
        
        coef_freq = cph.params_['leader_frequency']
        pval_freq = cph.summary.loc['leader_frequency', 'p']
        print(f"Dominant Leader Frequency Coef:   {coef_freq:.4f}")
        print(f"Dominant Leader Frequency p-val:   {pval_freq:.4f}")

        # Save results
        with open('cox_dominant_results.txt', 'w', encoding='utf-8') as f:
            f.write(cph.summary.to_string())

    except Exception as e:
        print(f"Cox Failed: {e}")

if __name__ == "__main__":
    main()
