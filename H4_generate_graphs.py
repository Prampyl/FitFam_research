
import json
import datetime
import math

print("Generating Graphs (Pure Python SVG)...")

# --- SVG Helper Class ---
class SvgPlotter:
    def __init__(self, width=800, height=400):
        self.width = width
        self.height = height
        self.padding = 50
        self.elements = []
    
    def add_rect(self, x, y, w, h, fill, opacity=1.0):
        self.elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="{opacity}" />')

    def add_text(self, x, y, text, size=12, color="black", anchor="middle"):
        self.elements.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}" text-anchor="{anchor}">{text}</text>')

    def add_line(self, x1, y1, x2, y2, stroke="black", width=2):
        self.elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" />')
    
    def add_polyline(self, points, stroke="blue", width=2, fill="none"):
        pts = " ".join([f"{p[0]},{p[1]}" for p in points])
        self.elements.append(f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" />')
    
    def add_circle(self, x, y, r, fill, stroke="none"):
        self.elements.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" />')

    def save(self, filename):
        svg = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" style="background-color:white">'
        svg += "".join(self.elements)
        svg += '</svg>'
        with open(filename, 'w') as f:
            f.write(svg)

# --- Data Loading (Reusing logic) ---
def parse_date(date_str):
    if not date_str: return None
    try: return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except: return None

try:
    with open('events.json', 'r') as f: events = json.load(f)
    with open('event_user.json', 'r') as f: event_user = json.load(f)
    with open('locations.json', 'r') as f: locations = json.load(f)
    with open('cancellation_reason_event.json', 'r') as f: cancellations = json.load(f)
except:
    print("Error loading data")
    exit()

shanghai_locs = {l['id'] for l in locations if l.get('city_id') == 1}
extreme_months = {1, 2, 7, 8, 12}
event_map = {}
for e in events:
    if e.get('location_id') in shanghai_locs:
        dt = parse_date(e.get('start_time'))
        if dt:
            is_extreme = 1 if dt.month in extreme_months else 0
            event_map[e['id']] = {'year': dt.year, 'month': dt.month, 'is_extreme': is_extreme, 'ts': dt.timestamp()}

# --- Prepare Data ---

# 1. Retention Data (2023, 2024, 2025)
# Re-calculate simple resilient tenure vs non-resilient for bar chart
user_stats_by_year = {2023:{'res':[], 'non':[]}, 2024:{'res':[], 'non':[]}, 2025:{'res':[], 'non':[]}}
user_tracker = {} # uid -> {year: {count, ext_count, first, last}}

for eu in event_user:
    if eu.get('checked_in') == 1 and eu.get('event_id') in event_map:
        uid = eu.get('user_id')
        evt = event_map[eu['event_id']]
        y = evt['year']
        if y in [2023, 2024, 2025]:
            if uid not in user_tracker: user_tracker[uid] = {}
            if y not in user_tracker[uid]: user_tracker[uid][y] = {'c':0, 'ex':0, 'f':evt['ts'], 'l':evt['ts']}
            s = user_tracker[uid][y]
            s['c'] += 1
            if evt['is_extreme']: s['ex'] += 1
            if evt['ts'] < s['f']: s['f'] = evt['ts']
            if evt['ts'] > s['l']: s['l'] = evt['ts']

for uid, years in user_tracker.items():
    for y, s in years.items():
        tenure = (s['l'] - s['f']) / 86400
        if s['ex'] > 0: user_stats_by_year[y]['res'].append(tenure)
        else: user_stats_by_year[y]['non'].append(tenure)

retention_data = []
for y in [2023, 2024, 2025]:
    r = user_stats_by_year[y]['res']
    n = user_stats_by_year[y]['non']
    r_mean = sum(r)/len(r) if r else 0
    n_mean = sum(n)/len(n) if n else 0
    retention_data.append((y, r_mean, n_mean))

# 2. Seasonality Data
# Re-classify for seasonality graph
seasonality = {
    "Super Core": [0]*13,
    "Resilient": [0]*13,
    "Fair Weather": [0]*13,
    "Nomad": [0]*13
}

# Simple classification
for uid, years in user_tracker.items():
    # Use global stats (approx)
    all_c = 0
    all_ex = 0
    min_f = float('inf')
    max_l = 0
    
    # Months tracking involves replay, let's just do a simplified mapping
    # Actually, simpler: Iterate events again for seasonality based on User Class
    # First classify user based on 2023-2025 aggregate
    pass

# We need user class first
user_classes = {}
for uid, years in user_tracker.items():
    # Aggregate
    tot_c = sum(y['c'] for y in years.values())
    tot_ex = sum(y['ex'] for y in years.values())
    
    # Approx tenure (max last - min first across years considered)
    # This is a bit disjointed but enough for viz
    ts_starts = [y['f'] for y in years.values()]
    ts_ends = [y['l'] for y in years.values()]
    tenure = (max(ts_ends) - min(ts_starts)) / 86400 if ts_starts else 0
    
    ratio = tot_ex / tot_c if tot_c > 0 else 0
    
    # Classification Logic (Same as Part 2)
    cls = "Fair Weather"
    if tenure > 200:
        if tot_c > 100: cls = "Super Core"
        else: cls = "Resilient"
    else:
        if ratio > 0.5: cls = "Nomad"
        else: cls = "Fair Weather"
    user_classes[uid] = cls

# Now counts per month
month_counts = {k: [0]*13 for k in seasonality.keys()}
for eu in event_user:
    if eu.get('checked_in') == 1 and eu.get('event_id') in event_map:
        uid = eu.get('user_id')
        if uid in user_classes:
            m = event_map[eu['event_id']]['month']
            month_counts[user_classes[uid]][m] += 1

# Normalize seasonality (Percentage of Annual Activity)
seasonality_pct = {}
for grp, counts in month_counts.items():
    total = sum(counts)
    if total > 0:
        seasonality_pct[grp] = [c/total*100 for c in counts] # index 0 is dummy
    else:
        seasonality_pct[grp] = [0]*13

# 3. Cancellation Data
cancel_counts = {'Pollution': [0]*13, 'Weather': [0]*13}
for c in cancellations:
    dt = parse_date(c.get('created_at'))
    if dt and dt.year in [2023, 2024, 2025]:
        reason = c.get('cancellation_reason_id')
        if reason == 1: cancel_counts['Pollution'][dt.month] += 1
        elif reason == 2: cancel_counts['Weather'][dt.month] += 1


# --- Plot 1: Retention Bar Chart ---
plot = SvgPlotter(600, 400)
plot.add_text(300, 30, "Tenure by Group: Resilient vs Non-Resilient (Days)", size=16)
# Axes
margin_L, margin_B = 60, 50
W = 600 - margin_L - 20
H = 400 - margin_B - 50
max_val = max([d[1] for d in retention_data]) * 1.1
scale_y = H / max_val

# Y Axis Grid
plot.add_line(margin_L, 50, margin_L, 50+H) # Y axis
plot.add_line(margin_L, 50+H, margin_L+W, 50+H) # X axis
for i in range(0, int(max_val), 50):
    y = 50 + H - (i * scale_y)
    plot.add_line(margin_L-5, y, margin_L, y)
    plot.add_text(margin_L-15, y+4, str(i), size=10, anchor="end")

# Bars
bar_w = 40
gap = 80
start_x = margin_L + 50

for i, (year, res, non) in enumerate(retention_data):
    x = start_x + (i * (bar_w * 2 + gap))
    
    # Non-Resilient
    h_non = non * scale_y
    y_non = 50 + H - h_non
    plot.add_rect(x, y_non, bar_w, h_non, fill="#FF6B6B") # Red
    plot.add_text(x + bar_w/2, y_non - 5, f"{int(non)}", size=10)
    
    # Resilient
    h_res = res * scale_y
    y_res = 50 + H - h_res
    plot.add_rect(x + bar_w, y_res, bar_w, h_res, fill="#4ECDC4") # Teal
    plot.add_text(x + bar_w + bar_w/2, y_res - 5, f"{int(res)}", size=10)
    
    # Label
    plot.add_text(x + bar_w, 50 + H + 20, str(year), size=12)

# Legend
plot.add_rect(450, 60, 15, 15, "#4ECDC4")
plot.add_text(520, 72, "Resilient", anchor="middle")
plot.add_rect(450, 85, 15, 15, "#FF6B6B")
plot.add_text(520, 97, "Non-Resilient", anchor="middle")

plot.save("graph_retention.svg")


# --- Plot 2: Seasonality Line Chart ---
plot = SvgPlotter(800, 400)
plot.add_text(400, 30, "Seasonality Profile (% of Annual Check-ins)", size=16)

# Axes
margin_L, margin_B = 60, 50
W = 800 - margin_L - 150 # Right space for legend
H = 400 - margin_B - 50
max_val = 20 # 20% max roughly
scale_y = H / max_val
scale_x = W / 11 # 12 months, 11 gaps

plot.add_line(margin_L, 50, margin_L, 50+H)
plot.add_line(margin_L, 50+H, margin_L+W, 50+H)

# Grid
for i in range(0, 21, 5):
    y = 50 + H - (i * scale_y)
    plot.add_line(margin_L, y, margin_L+W, y, stroke="#eee")
    plot.add_text(margin_L-10, y+4, f"{i}%", size=10, anchor="end")

months = ["J","F","M","A","M","J","J","A","S","O","N","D"]
for i, m in enumerate(months):
    x = margin_L + i * scale_x
    plot.add_text(x, 50+H+20, m, size=12)

colors = {"Super Core": "#333333", "Resilient": "#2ECC71", "Fair Weather": "#F1C40F", "Nomad": "#3498DB"}

legend_y = 100
for grp, vals in seasonality_pct.items():
    if not vals: continue
    color = colors.get(grp, "black")
    points = []
    # vals index 1..12
    for m in range(1, 13):
        idx = m - 1
        x = margin_L + idx * scale_x
        val = vals[m]
        y = 50 + H - (val * scale_y)
        points.append((x, y))
        plot.add_circle(x, y, 3, color)
    
    plot.add_polyline(points, stroke=color, width=2)
    
    # Legend
    plot.add_line(margin_L+W+20, legend_y, margin_L+W+50, legend_y, stroke=color, width=3)
    plot.add_text(margin_L+W+60, legend_y+4, grp, anchor="start", size=10)
    legend_y += 30

plot.save("graph_seasonality.svg")


# --- Plot 3: Cancellations Bar Chart ---
plot = SvgPlotter(600, 400)
plot.add_text(300, 30, "Cancellations: Pollution vs Weather (2023-2025 Combined)", size=16)

# Axes
max_c = max(max(cancel_counts['Pollution']), max(cancel_counts['Weather'])) * 1.2
scale_y = H / max_c
start_x = margin_L + 20
bar_w = 15
gap = 20
month_step = (W - 20) / 12

plot.add_line(margin_L, 50, margin_L, 50+H)
plot.add_line(margin_L, 50+H, margin_L+W, 50+H)

# Y-Axis Labels & Grid
step_y = max(1, int(max_c / 5))
for i in range(0, int(max_c + step_y), step_y):
    y = 50 + H - (i * scale_y)
    if y < 50: continue
    plot.add_line(margin_L-5, y, margin_L, y)
    plot.add_text(margin_L-10, y+4, str(i), size=10, anchor="end")
    if i > 0: plot.add_line(margin_L, y, margin_L+W, y, stroke="#eee")

for i in range(12):
    m = i + 1
    x_center = margin_L + (i * month_step) + (month_step/2)
    
    # Pollution (Black)
    val_p = cancel_counts['Pollution'][m]
    h_p = val_p * scale_y
    y_p = 50 + H - h_p
    plot.add_rect(x_center - bar_w, y_p, bar_w, h_p, "#555555")
    
    # Weather (Blue)
    val_w = cancel_counts['Weather'][m]
    h_w = val_w * scale_y
    y_w = 50 + H - h_w
    plot.add_rect(x_center, y_w, bar_w, h_w, "#3498DB")
    
    # Label
    plot.add_text(x_center, 50+H+20, months[i], size=10)

# Legend
plot.add_rect(450, 60, 15, 15, "#555555")
plot.add_text(520, 72, "Pollution", anchor="middle")
plot.add_rect(450, 85, 15, 15, "#3498DB")
plot.add_text(520, 97, "Weather", anchor="middle")

plot.save("graph_cancellations.svg")

print("Done. Generated graph_retention.svg, graph_seasonality.svg, graph_cancellations.svg")
