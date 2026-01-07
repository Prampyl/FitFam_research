import pandas as pd
import numpy as np
import sys
import os


# Add src to path
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def main():
    print("--- Starting Leader Metric Correlation Analysis ---")
    
    # 1. Load Data
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    
    # Filter Post-2023
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()
    
    # 2. Calculate Leader Metrics
    print("Calculating metrics for all leaders...")
    leaders_df = df[df['is_leader'] == 1].copy()
    
    leader_stats = []
    for user_id, group in leaders_df.groupby('user_id'):
        if len(group) < 5: continue # Ignore experimental leaders
        
        dates = group['start_time'].sort_values()
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        consistency_std = gaps.std()
        
        # Tenure: Days active
        tenure_days = (dates.iloc[-1] - dates.iloc[0]).days
        
        # Frequency: Events / Month (approx)
        # Avoid division by zero for very short tenure
        months = max(tenure_days / 30, 0.5) 
        frequency = len(group) / months

        leader_stats.append({
            'leader_user_id': user_id,
            'Consistency (StdDev)': consistency_std if not pd.isna(consistency_std) else 0,
            'Frequency (Events/Month)': frequency,
            'Tenure (Days)': tenure_days
        })
    
    stats_df = pd.DataFrame(leader_stats).set_index('leader_user_id')
    print(f"Analyzed {len(stats_df)} leaders.")
    
    # 3. Calculate Correlation
    corr_matrix = stats_df.corr()
    
    print("\n--- Correlation Matrix (Pearson) ---")
    print(corr_matrix.round(4))
    
    # Interpretation Helper
    print("\n--- Interpretation ---")
    c_f = corr_matrix.loc['Consistency (StdDev)', 'Frequency (Events/Month)']
    c_t = corr_matrix.loc['Consistency (StdDev)', 'Tenure (Days)']
    f_t = corr_matrix.loc['Frequency (Events/Month)', 'Tenure (Days)']
    
    print(f"Consistency vs Frequency: {c_f:.4f}")
    if abs(c_f) > 0.5: print("-> STRONG Relationship. (Highly frequent leaders are more/less consistent?)")
    
    print(f"Consistency vs Tenure:    {c_t:.4f}")
    
    print(f"Frequency vs Tenure:      {f_t:.4f}")
    
    # Save to file
    with open('h2_metric_correlations.txt', 'w') as f:
        f.write(corr_matrix.to_string())

if __name__ == "__main__":
    main()
