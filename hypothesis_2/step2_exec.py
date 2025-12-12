import pandas as pd
import numpy as np
import sys
import os

# Add src to path to import data_loader
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

# Initialize Loader
loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))

print("Loading Data...")
events = loader.load_events()
event_user = loader.load_event_user()
print("Data Loaded.")

# 1. Merge Leaders with Event Dates
print("Merging leader attendance with event dates...")
leaders = event_user[event_user['is_leader'] == 1].copy()
leaders_with_dates = leaders.merge(events[['id', 'start_time']], left_on='event_id', right_on='id', how='left')

# Ensure datetime
leaders_with_dates['start_time'] = pd.to_datetime(leaders_with_dates['start_time'])

# Sort
leaders_with_dates = leaders_with_dates.sort_values(['user_id', 'start_time'])

# 2. Calculate Metrics Loop
leader_stats = []

print("Calculating metrics for each leader...")

for user_id, group in leaders_with_dates.groupby('user_id'):
    dates = group['start_time'].sort_values()
    
    # Basic Stats
    total_events = len(group)
    first_led = dates.iloc[0]
    last_led = dates.iloc[-1]
    
    # Tenure (Days)
    tenure_days = (last_led - first_led).days
    if tenure_days == 0: 
        tenure_days = 1 
    
    # Frequency (Events per Month)
    events_per_month = total_events / (tenure_days / 30.44)
    
    # Consistency (Std Dev of gaps)
    if total_events > 1:
        gaps = dates.diff().dt.total_seconds() / (24 * 3600)
        gaps = gaps.dropna()
        consistency_std = gaps.std()
        avg_gap = gaps.mean()
    else:
        consistency_std = np.nan 
        avg_gap = np.nan
        
    leader_stats.append({
        'leader_user_id': user_id,
        'total_events': total_events,
        'first_led_date': first_led,
        'last_led_date': last_led,
        'tenure_days': tenure_days,
        'events_per_month': events_per_month,
        'consistency_std': consistency_std,
        'avg_gap_days': avg_gap
    })

df_leaders = pd.DataFrame(leader_stats)
df_leaders.set_index('leader_user_id', inplace=True)

print(f"Computed stats for {len(df_leaders)} leaders.")

# 3. Inspect
print("\nTop 5 Consistent Leaders (Lowest Std Dev, min 10 events):")
print(df_leaders[df_leaders['total_events'] >= 10].sort_values('consistency_std').head(5)[['total_events', 'consistency_std', 'events_per_month']])

print("\nTop 5 Most Frequent Leaders:")
print(df_leaders.sort_values('events_per_month', ascending=False).head(5)[['total_events', 'consistency_std', 'events_per_month']])

# 4. Save
df_leaders.to_csv('leaders_quality_metrics.csv')
print("\nSaved leader metrics to leaders_quality_metrics.csv")
