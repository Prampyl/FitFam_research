import pandas as pd
import sys
from data_loader import FitFamDataLoader

sys.stdout.reconfigure(encoding='utf-8')

loader = FitFamDataLoader()
df = loader.get_unified_data()

print("--- Top Categories ---")
print(df['category_name'].value_counts().head(10))

print("\n--- Top Categories in Shanghai ---")
shanghai_df = df[df['name_city'].str.contains('Shanghai', na=False)]
print(shanghai_df['category_name'].value_counts().head(5))

print("\n--- Top Categories in Virtual ---")
virtual_df = df[df['name_city'].str.contains('Virtual', na=False) | df['name_city'].str.contains('线上', na=False)]
print(virtual_df['category_name'].value_counts().head(5))
