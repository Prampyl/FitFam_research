import pandas as pd
import numpy as np
import sys
import os
from lifelines import KaplanMeierFitter, CoxPHFitter
import matplotlib.pyplot as plt

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def main():
    print("--- Starting H2 Step 5: Statistical Validation ---")
    
    # 1. Load Data
    print("Loading Unified Data...")
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    print(f"Loaded {len(df)} rows.")

    # 2. Filter Post-2023
    print("Filtering Post-2023...")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()
    print(f"Records Post-2023: {len(df)}")

    # 3. Calculate Leader Metrics
    print("Calculating Leader Metrics...")
    # Identify leaders (where is_leader == 1)
    # Note: 'is_leader' column comes from event_user.json. 
    # get_unified_data merges event_user, so it should be there.
    if 'is_leader' not in df.columns:
        print("Error: 'is_leader' column not found.")
        return

    leaders_df = df[df['is_leader'] == 1].copy()
    
    leader_stats = []
    for user_id, group in leaders_df.groupby('user_id'):
        if len(group) < 5: continue # Skip guest leaders
        
        dates = group['start_time'].sort_values()
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        consistency_std = gaps.std()
        
        leader_stats.append({
            'leader_user_id': user_id,
            'leader_consistency': consistency_std if not pd.isna(consistency_std) else 0,
            'leader_tenure': (dates.iloc[-1] - dates.iloc[0]).days,
            'leader_total_events': len(group)
        })
    
    df_leaders = pd.DataFrame(leader_stats).set_index('leader_user_id')
    print(f"Analyzed {len(df_leaders)} leaders (min 5 events).")

    # 4. Build User Cohorts (The \"First Exposure\")
    print("Building User Cohorts...")
    # Sort by user and time
    df_sorted = df.sort_values(['user_id', 'start_time'])
    
    # Group by user to get first event info
    # We want: First Event Date, City, Category, Gender, and Who Led it.
    
    # To get the leader of the first event, we need a map: event_id -> leader_id
    # Since an event might have multiple leaders, we take the one with most events or just the first one found.
    event_leader_map = leaders_df.sort_values('user_id').drop_duplicates('event_id')[['event_id', 'user_id', 'city_name', 'category_name']]
    event_leader_map.columns = ['event_id', 'leader_user_id_vals', 'city_name_vals', 'category_name_vals']
    
    # Get first event for each user
    user_firsts = df_sorted.drop_duplicates('user_id', keep='first')[['user_id', 'event_id', 'start_time', 'gender']]
    
    # Get last event for each user (for churn calculation)
    user_lasts = df_sorted.drop_duplicates('user_id', keep='last')[['user_id', 'start_time']]
    user_lasts.columns = ['user_id', 'last_event_date']
    
    # Merge
    cohorts = user_firsts.merge(user_lasts, on='user_id')
    
    # Merge with Leader Map to identify \"First Leader\"
    cohorts = cohorts.merge(event_leader_map[['event_id', 'leader_user_id_vals', 'city_name_vals', 'category_name_vals']], on='event_id', how='left')
    
    # Drop users with no identified leader
    cohorts = cohorts.dropna(subset=['leader_user_id_vals'])
    
    # 5. Define Survival Columns
    # Event: Churn. 
    # Definition: If (Now - Last Event) > 90 days, then Churned (1). Else Censored (0).
    # Duration: Days between First Event and Last Event (if churned) or Now (if active)?
    # Standard: T = (Last_Date - First_Date). If Churned, Event=1.
    
    NOW = df['start_time'].max()
    cohorts['days_since_last'] = (NOW - cohorts['last_event_date']).dt.days
    cohorts['churn_event'] = (cohorts['days_since_last'] > 90).astype(int)
    
    cohorts['duration'] = (cohorts['last_event_date'] - cohorts['start_time']).dt.days
    # Filter out 0 duration (users who only came once and churned immediately? or generally 1-day tenure)
    # Survival Analysis works best with duration > 0.
    cohorts.loc[cohorts['duration'] == 0, 'duration'] = 1 
    
    # 6. Merge with Leader Metrics
    cohorts = cohorts.merge(df_leaders, left_on='leader_user_id_vals', right_index=True)
    
    # 7. Prepare for Cox PH
    print("Running Multivariate Cox Regression...")
    
    # Select columns
    cox_df = cohorts[[
        'duration', 'churn_event', 
        'leader_consistency', 'leader_tenure', 
        'city_name_vals', 'category_name_vals', 'gender'
    ]].copy()
    
    # Clean Categorical
    # Fill NAs
    cox_df['city_name_vals'] = cox_df['city_name_vals'].fillna('Unknown')
    cox_df['category_name_vals'] = cox_df['category_name_vals'].fillna('Unknown')
    cox_df['gender'] = cox_df['gender'].fillna('Unknown')
    
    # Encode Categorical (One-Hot)
    # Dropping 'Unknown' or first to avoid collinearity
    cox_df = pd.get_dummies(cox_df, columns=['city_name_vals', 'category_name_vals', 'gender'], drop_first=True)
    
    # Rename columns to avoid syntax errors in Cox
    cox_df.columns = [c.replace(' ', '_').replace('/', '_').replace('-', '_') for c in cox_df.columns]
    
    # Fit Cox Model with Penalizer to handle collinearity
    # Using a small penalizer (0.1) often solves singularity without biasing too much
    cph = CoxPHFitter(penalizer=0.1)
    try:
        cph.fit(cox_df, duration_col='duration', event_col='churn_event')
        
        # Save summary to file to avoid Windows terminal encoding errors
        with open('cox_results.txt', 'w', encoding='utf-8') as f:
            f.write(cph.summary.to_string())
            
        print("\n--- Cox Proportional Hazards Results ---")
        print("Full summary saved to: cox_results.txt")
        
        # Print specific key metrics (safe for terminal)
        if 'leader_consistency' in cph.params_:
            coef = cph.params_['leader_consistency']
            pval = cph.summary.loc['leader_consistency', 'p']
            print(f"Leader Consistency Coef: {coef:.4f}")
            print(f"leader_consistency p-val: {pval:.4f}")
            
            print("\nInterpretation check: Higher 'consistency' value means LESS consistent (higher std dev).")
            if coef > 0:
                print("Result: POSITIVE coefficient. (Inconsistency INCREASES hazard -> Consistent leaders RETAIN users).")
            else:
                print("Result: NEGATIVE coefficient. (Inconsistency DECREASES hazard -> Users prefer inconsistent leaders?).")
        
    except Exception as e:
        print(f"Cox Logic Failed: {e}")
        # Fallback: Try with fewer variables if it fails again
        print("Retrying with minimal model (Leader Metrics only)...")
        try:
             # dynamically select gender column if exists
             gender_cols = [c for c in cox_df.columns if 'gender' in c]
             cols_to_use = ['duration', 'churn_event', 'leader_consistency', 'leader_tenure'] + gender_cols
             
             cph.fit(cox_df[cols_to_use], duration_col='duration', event_col='churn_event')
             print("Minimal Model Coef:", cph.params_['leader_consistency'])
        except Exception as e2:
             print(f"Minimal Cox Failed: {e2}")

    # 8. Kaplan Meier by Tier (Verification)
    print("\nRunning Kaplan-Meier by Tier...")

    q1 = cohorts['leader_consistency'].quantile(0.25)
    q3 = cohorts['leader_consistency'].quantile(0.75)
    
    top_tier = cohorts[cohorts['leader_consistency'] <= q1]
    bottom_tier = cohorts[cohorts['leader_consistency'] >= q3]
    
    kmf = KaplanMeierFitter()
    
    plt.figure(figsize=(10,6))
    
    kmf.fit(top_tier['duration'], top_tier['churn_event'], label='Top Tier (Consistent)')
    kmf.plot()
    
    kmf.fit(bottom_tier['duration'], bottom_tier['churn_event'], label='Bottom Tier (Inconsistent)')
    kmf.plot()
    
    plt.title("Survival Curve: Leader Consistency Impact")
    plt.savefig('h2_km_curve.png')
    print("Saved KM Curve to h2_km_curve.png")

if __name__ == "__main__":
    main()
