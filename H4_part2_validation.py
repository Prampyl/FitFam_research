
import json
import datetime
import math

print("Loading data for Part 2...")
try:
    with open('events.json', 'r') as f: events = json.load(f)
    with open('event_user.json', 'r') as f: event_user = json.load(f)
    with open('locations.json', 'r') as f: locations = json.load(f)
    with open('cancellation_reason_event.json', 'r') as f: cancellations = json.load(f)
except Exception as e:
    print(e)
    exit()

def parse_date(date_str):
    if not date_str: return None
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except: return None

# Filter for Shanghai (Loc ID logic)
shanghai_locs = {l['id'] for l in locations if l.get('city_id') == 1}

# Events Map
extreme_months = {1, 2, 7, 8, 12}
event_map = {}
for e in events:
    if e.get('location_id') in shanghai_locs:
        dt = parse_date(e.get('start_time'))
        if dt:
            is_extreme = 1 if dt.month in extreme_months else 0
            event_map[e['id']] = {'year': dt.year, 'month': dt.month, 'is_extreme': is_extreme, 'ts': dt.timestamp()}

# User Stats for Reconstruction of Clusters (Simplified logic based on Part 1 output)
# Part 1 logic: 
# Features: Total Attendance, Tenure, Extreme Ratio.
# K-Means is non-deterministic so I can't perfectly reproduce the IDs without saving the model.
# I will implement a "rule-based" classification that mimics the clusters I found.
# Clusters found:
# C0: "Regular Resilient" (Avg Tenure ~530, Ratio ~0.4, Attend ~30)
# C1: "Super Core" (Avg Tenure ~740, Ratio ~0.4, Attend ~192)
# C2: "Fair Weather Casual" (Avg Tenure ~45, Ratio ~0.05, Attend ~3.5)
# C3: "Winter/Extreme Casual" (Avg Tenure ~42, Ratio ~0.87, Attend ~3.4)

def classify_user(stats):
    total = stats['count']
    if total == 0: return None
    tenure = (stats['last_ts'] - stats['first_ts']) / 86400
    ratio = stats['extreme_count'] / total
    
    # Simple Heuristics to mimic clusters
    if tenure > 200:
        if total > 100: return "Super Core" # C1
        else: return "Regular Resilient" # C0
    else:
        if ratio > 0.5: return "Extreme Casual (New Year?)" # C3
        else: return "Fair Weather Casual" # C2

user_data = {}
for eu in event_user:
    if eu.get('checked_in') == 1:
        eid = eu.get('event_id')
        uid = eu.get('user_id')
        if eid in event_map:
            if uid not in user_data:
                user_data[uid] = {'count':0, 'extreme_count':0, 'first_ts':None, 'last_ts':None, 'months':[]}
            
            s = user_data[uid]
            evt = event_map[eid]
            s['count'] += 1
            if evt['is_extreme']: s['extreme_count'] += 1
            if s['first_ts'] is None or evt['ts'] < s['first_ts']: s['first_ts'] = evt['ts']
            if s['last_ts'] is None or evt['ts'] > s['last_ts']: s['last_ts'] = evt['ts']
            s['months'].append(evt['month'])

# Analysis of Seasonality per Group
seasonality = {
    "Super Core": {},
    "Regular Resilient": {},
    "Fair Weather Casual": {},
    "Extreme Casual (New Year?)": {}
}

for uid, stats in user_data.items():
    group = classify_user(stats)
    if not group: continue
    
    for m in stats['months']:
        seasonality[group][m] = seasonality[group].get(m, 0) + 1

print("\n--- Seasonality (Check-in count per Month per Group) ---")
print(f"{'Month':<5} {'SuperCore':<10} {'Regular':<10} {'FairWeather':<12} {'ExtremeCasual'}")
for m in range(1, 13):
    print(f"{m:<5} {seasonality['Super Core'].get(m,0):<10} {seasonality['Regular Resilient'].get(m,0):<10} {seasonality['Fair Weather Casual'].get(m,0):<12} {seasonality['Extreme Casual (New Year?)'].get(m,0)}")

# Cancellation Analysis (2023-2025)
print("\n--- Cancellations (2023-2025) ---")
cancellations_by_month = {}
cancellation_types = {1: "Pollution", 2: "Weather", 3: "Other"} # Assuming 3 is generic

for c in cancellations:
    dt = parse_date(c.get('created_at'))
    if dt and dt.year in [2023, 2024, 2025]:
        m = dt.month
        reason = c.get('cancellation_reason_id')
        if reason in [1, 2]: # Only care about Env reasons
            key = (m, reason)
            cancellations_by_month[key] = cancellations_by_month.get(key, 0) + 1

print(f"{'Month':<5} {'Pollution (ID 1)':<15} {'Weather (ID 2)'}")
for m in range(1, 13):
    pol = cancellations_by_month.get((m, 1), 0)
    wea = cancellations_by_month.get((m, 2), 0)
    print(f"{m:<5} {pol:<15} {wea}")
