
import json
import datetime
import math
import random

# Load Data
print("Loading data (Pure Python)...")
try:
    with open('events.json', 'r') as f:
        events_data = json.load(f)
    with open('event_user.json', 'r') as f:
        event_user_data = json.load(f)
    with open('locations.json', 'r') as f:
        locations_data = json.load(f)
except FileNotFoundError:
    print("Error: JSON files not found.")
    exit()

print("Data loaded.")

# Helper: Parse datetime
def parse_date(date_str):
    if not date_str: return None
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

# 1. Filter Locations for Shanghai (City ID 1)
shanghai_loc_ids = set()
for loc in locations_data:
    if loc.get('city_id') == 1:
        shanghai_loc_ids.add(loc['id'])

print(f"Found {len(shanghai_loc_ids)} Shanghai locations.")

# 2. Process Events
# Map event_id -> {start_time, year, month, is_extreme}
event_map = {}
extreme_months = {1, 2, 7, 8, 12}

for event in events_data:
    if event.get('location_id') in shanghai_loc_ids:
        dt = parse_date(event.get('start_time'))
        if dt:
            is_extreme = 1 if dt.month in extreme_months else 0
            event_map[event['id']] = {
                'start_time': dt,
                'year': dt.year,
                'month': dt.month,
                'is_extreme': is_extreme
            }

print(f"Processed {len(event_map)} Shanghai events.")

# 3. Process Attendance
# User Stats: {user_id: {2023: {...}, 2024: {...}, 'all': {...}}}
user_stats = {}

def init_stat():
    return {
        'count': 0,
        'extreme_count': 0,
        'first_ts': None,
        'last_ts': None
    }

for eu in event_user_data:
    if eu.get('checked_in') == 1:
        eid = eu.get('event_id')
        uid = eu.get('user_id')
        if eid in event_map:
            evt = event_map[eid]
            year = evt['year']
            
            if uid not in user_stats:
                user_stats[uid] = {}
            
            # Aggregate for specific year
            if year not in user_stats[uid]:
                user_stats[uid][year] = init_stat()
            
            s = user_stats[uid][year]
            s['count'] += 1
            if evt['is_extreme']:
                s['extreme_count'] += 1
            ts = evt['start_time'].timestamp()
            if s['first_ts'] is None or ts < s['first_ts']: s['first_ts'] = ts
            if s['last_ts'] is None or ts > s['last_ts']: s['last_ts'] = ts

            # Aggregate for 'all' (only 2023-2025)
            if year in [2023, 2024, 2025]:
                if 'all' not in user_stats[uid]:
                     user_stats[uid]['all'] = init_stat()
                s_all = user_stats[uid]['all']
                s_all['count'] += 1
                if evt['is_extreme']:
                    s_all['extreme_count'] += 1
                if s_all['first_ts'] is None or ts < s_all['first_ts']: s_all['first_ts'] = ts
                if s_all['last_ts'] is None or ts > s_all['last_ts']: s_all['last_ts'] = ts

# Analysis per Year
years = [2023, 2024, 2025]

def get_tenure(stat):
    if stat['first_ts'] is None: return 0
    return (stat['last_ts'] - stat['first_ts']) / 86400 # days

def print_stats(resilient_tenures, non_resilient_tenures, labels):
    def safe_mean(l): return sum(l)/len(l) if l else 0
    def safe_median(l): return sorted(l)[len(l)//2] if l else 0
    
    print(f"{labels[0]}: Mean={safe_mean(resilient_tenures):.1f}, Median={safe_median(resilient_tenures):.1f}, Count={len(resilient_tenures)}")
    print(f"{labels[1]}: Mean={safe_mean(non_resilient_tenures):.1f}, Median={safe_median(non_resilient_tenures):.1f}, Count={len(non_resilient_tenures)}")

for year in years:
    print(f"\n--- Analysis for {year} ---")
    res_tenures = []
    non_tenures = []
    
    count_users = 0
    for uid, years_data in user_stats.items():
        if year in years_data:
            stat = years_data[year]
            tenure = get_tenure(stat)
            is_resilient = stat['extreme_count'] > 0
            
            if is_resilient:
                res_tenures.append(tenure)
            else:
                non_tenures.append(tenure)
            count_users += 1
            
    if count_users == 0:
        print("No users found.")
    else:
        print_stats(res_tenures, non_tenures, ["Resilient (Old Def)", "Non-Resilient"])


# Clustering (Simple K-Means in Pure Python)
print("\n--- Clustering (2023-2025 Combined) ---")
data_points = []
user_ids = []

for uid, years_data in user_stats.items():
    if 'all' in years_data:
        stat = years_data['all']
        tenure = get_tenure(stat)
        total = stat['count']
        extreme_ratio = stat['extreme_count'] / total if total > 0 else 0
        
        # Features: total_attendance, tenure, extreme_ratio
        data_points.append([total, tenure, extreme_ratio])
        user_ids.append(uid)

if not data_points:
    print("No data for clustering.")
    exit()

# Standardization
n_samples = len(data_points)
n_features = 3
means = [0] * n_features
stds = [0] * n_features

for p in data_points:
    for i in range(n_features):
        means[i] += p[i]
for i in range(n_features):
    means[i] /= n_samples

for p in data_points:
    for i in range(n_features):
        stds[i] += (p[i] - means[i])**2
for i in range(n_features):
    stds[i] = math.sqrt(stds[i] / n_samples)
    if stds[i] == 0: stds[i] = 1

normalized_data = []
for p in data_points:
    norm_p = []
    for i in range(n_features):
        norm_p.append((p[i] - means[i]) / stds[i])
    normalized_data.append(norm_p)

# K-Means Implementation
k = 4
centroids = random.sample(normalized_data, k)
max_iters = 20
clusters = [[] for _ in range(k)]

for _ in range(max_iters):
    clusters = [[] for _ in range(k)]
    for idx, p in enumerate(normalized_data):
        # Find nearest centroid
        best_dist = float('inf')
        best_c = 0
        for c_idx, c in enumerate(centroids):
            dist = sum((p[i] - c[i])**2 for i in range(n_features))
            if dist < best_dist:
                best_dist = dist
                best_c = c_idx
        clusters[best_c].append(idx)
    
    # Update centroids
    new_centroids = []
    for c_idx in range(k):
        indices = clusters[c_idx]
        if not indices:
            new_centroids.append(centroids[c_idx]) # Keep old if empty
            continue
        
        new_c = [0] * n_features
        for idx in indices:
            p = normalized_data[idx]
            for i in range(n_features):
                new_c[i] += p[i]
        for i in range(n_features):
            new_c[i] /= len(indices)
        new_centroids.append(new_c)
    
    centroids = new_centroids

# Analysis of Clusters
print("\nCluster Profiles (Unscaled):")
print(f"{'ID':<5} {'Count':<10} {'Avg Attend':<15} {'Avg Tenure':<15} {'Avg ExtrRatio':<15}")

cluster_summaries = []

for c_idx in range(k):
    indices = clusters[c_idx]
    count = len(indices)
    if count == 0: continue
    
    avg_obs = [0] * n_features
    for idx in indices:
        orig = data_points[idx]
        for i in range(n_features):
            avg_obs[i] += orig[i]
    
    for i in range(n_features):
        avg_obs[i] /= count
    
    print(f"{c_idx:<5} {count:<10} {avg_obs[0]:<15.1f} {avg_obs[1]:<15.1f} {avg_obs[2]:<15.2f}")
    cluster_summaries.append({
        'id': c_idx,
        'count': count,
        'attend': avg_obs[0],
        'tenure': avg_obs[1],
        'extreme_ratio': avg_obs[2]
    })

# Identify "Resilient" cluster
# High Tenure + High Extreme Ratio
best_c = max(cluster_summaries, key=lambda x: x['tenure'] * (1 + x['extreme_ratio']))
print(f"\nPotential 'Resilient' Cluster: ID {best_c['id']} (High Tenure/Extreme)")

# Identify "Casual" cluster
# Low Attendance + Low Tenure
worst_c = min(cluster_summaries, key=lambda x: x['attend'])
print(f"Potential 'Casual' Cluster: ID {worst_c['id']} (Low Attendance)")

