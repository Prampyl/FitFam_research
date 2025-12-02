import pandas as pd
import sys
from data_loader import FitFamDataLoader

sys.stdout.reconfigure(encoding='utf-8')

loader = FitFamDataLoader()
df = loader.get_unified_data()

print("--- Top Cities ---")
print(df['city_name'].value_counts().head(10))

print("\n--- Gender Distribution ---")
gender_map = {1: 'Male', 2: 'Female', 0: 'Unknown'}
df['gender_label'] = df['gender'].map(gender_map)
print(df['gender_label'].value_counts(normalize=True))

print("\n--- Retention (Simple) ---")
# Calculate retention: % of users who attended more than 1 event
user_counts = df['user_id'].value_counts()
retained_users = user_counts[user_counts > 1].count()
total_users = user_counts.count()
print(f"Total Users: {total_users}")
print(f"Retained Users (>1 event): {retained_users}")
print(f"Retention Rate: {retained_users/total_users:.2%}")

print("\n--- Power Users ---")
print(f"Users with > 10 events: {user_counts[user_counts > 10].count()}")
print(f"Users with > 50 events (Potential Leaders): {user_counts[user_counts > 50].count()}")
