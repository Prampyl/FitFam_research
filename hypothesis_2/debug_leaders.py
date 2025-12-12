import pandas as pd
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

# Merge Leaders with Event Dates
leaders = event_user[event_user['is_leader'] == 1].copy()
leaders_with_dates = leaders.merge(events[['id', 'start_time', 'name', 'location_id']], left_on='event_id', right_on='id', how='left')
leaders_with_dates['start_time'] = pd.to_datetime(leaders_with_dates['start_time'])

# Load saved metrics to get the suspicious IDs
try:
    metrics = pd.read_csv('leaders_quality_metrics.csv')
    print("Loaded metrics file.")
except FileNotFoundError:
    print("Metrics file not found, please run step 2 first.")
    sys.exit(1)

# Filter for high frequency BUT with significant history
high_freq = metrics[metrics['total_events'] > 10].sort_values('events_per_month', ascending=False).head(10)
print("\n--- Top 10 High Frequency Leaders (Min 10 Events) ---")
print(high_freq[['leader_user_id', 'total_events', 'tenure_days', 'events_per_month']])

# Pick the top 3 to inspect
suspicious_ids = high_freq['leader_user_id'].head(3).tolist()

print(f"\n--- Inspecting Events for Leaders: {suspicious_ids} ---")

for uid in suspicious_ids:
    print(f"\nUser {uid}:")
    user_events = leaders_with_dates[leaders_with_dates['user_id'] == uid].sort_values('start_time')
    
    # Safe print
    for _, row in user_events[['start_time', 'name']].head(5).iterrows():
        name = str(row['name']).encode('ascii', 'replace').decode('ascii')
        print(f"{row['start_time']} - {name}")
    
    if len(user_events) > 5:
        print("...")
        for _, row in user_events[['start_time', 'name']].tail(5).iterrows():
            name = str(row['name']).encode('ascii', 'replace').decode('ascii')
            print(f"{row['start_time']} - {name}")
