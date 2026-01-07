import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from data_loader import FitFamDataLoader

def main():
    print("--- Starting H2 Step 6: Metric Critique & Attribution Analysis ---")
    
    # 1. Load Data
    print("Loading Unified Data...")
    loader = FitFamDataLoader(data_dir=os.path.abspath(os.path.join('..', 'fitfam-json')))
    df = loader.get_unified_data()
    
    # Filter Post-2023 for relevance
    df['start_time'] = pd.to_datetime(df['start_time'])
    df = df[df['start_time'] >= '2023-01-01'].copy()
    print(f"Records Post-2023: {len(df)}")

    # 2. Identify Leaders (to map IDs)
    if 'is_leader' not in df.columns:
        print("Error: 'is_leader' column missing.")
        return
    
    # Create a map of event_id -> leader_id
    # We need to know who led every event users went to
    leaders_df = df[df['is_leader'] == 1][['event_id', 'user_id', 'start_time']].drop_duplicates('event_id')
    leaders_df.columns = ['event_id', 'leader_user_id', 'event_start_time']
    
    # 3. Analyze User History
    print("Analyzing User History for Attribution Stickiness...")
    
    # Filter for users (attendees) -> is_leader=0 (usually, or just everyone's attendance)
    # We'll look at everyone's attendance as a participant
    # But strictly, we care about "students".
    
    # Merge attendance with leader info
    # df has one row per user-event.
    attendance = df[['user_id', 'event_id', 'start_time']].merge(
        leaders_df[['event_id', 'leader_user_id']], on='event_id', how='left'
    )
    
    # Drop where leader is unknown or self (if leader attended own event?)
    attendance = attendance.dropna(subset=['leader_user_id'])
    attendance = attendance[attendance['user_id'] != attendance['leader_user_id']] # remove self-attendance
    
    # 4. Calculate "First Leader"
    attendance.sort_values(['user_id', 'start_time'], inplace=True)
    
    first_leaders = attendance.drop_duplicates('user_id', keep='first')[['user_id', 'leader_user_id']]
    first_leaders.columns = ['user_id', 'first_leader_id']
    
    # 5. Calculate "Stickiness"
    # Stickiness = (Events with First Leader) / (Total Events)
    
    # Group by User and Leader to count interactions
    user_leader_counts = attendance.groupby(['user_id', 'leader_user_id']).size().reset_index(name='count')
    
    # Get total events per user
    user_total_counts = attendance.groupby('user_id').size().reset_index(name='total_events')
    
    # Filter for users with > 1 event (otherwise stickiness is trivially 100%)
    valid_users = user_total_counts[user_total_counts['total_events'] > 1]['user_id']
    
    metrics = first_leaders[first_leaders['user_id'].isin(valid_users)].merge(
        user_leader_counts, 
        left_on=['user_id', 'first_leader_id'], 
        right_on=['user_id', 'leader_user_id'], 
        how='left'
    )
    metrics = metrics.merge(user_total_counts, on='user_id')
    
    metrics['stickiness'] = metrics['count'] / metrics['total_events']
    
    avg_stickiness = metrics['stickiness'].mean()
    median_stickiness = metrics['stickiness'].median()
    
    print(f"\n--- Stickiness Results (Users > 1 event, N={len(metrics)}) ---")
    print(f"Average 'First Leader' Stickiness: {avg_stickiness:.2%}")
    print(f"Median 'First Leader' Stickiness:  {median_stickiness:.2%}")
    print("Interpretation: on average, a user spends X% of their time with their 'First Leader'.")
    print("If this is low (<25%), 'First Leader' is a weak proxy for influence.")

    # 6. Identify "Dominant Leader"
    # The leader with whom the user attended the MOST events
    print("\nIdentifying Dominant Leaders...")
    
    # Sort counts descending
    user_leader_counts.sort_values(['user_id', 'count'], ascending=[True, False], inplace=True)
    dominant_leaders = user_leader_counts.drop_duplicates('user_id', keep='first')[['user_id', 'leader_user_id', 'count']]
    dominant_leaders.columns = ['user_id', 'dominant_leader_id', 'dominant_count']
    
    # Compare First vs Dominant
    comparison = metrics.merge(dominant_leaders, on='user_id')
    comparison['same_leader'] = comparison['first_leader_id'] == comparison['dominant_leader_id']
    
    match_rate = comparison['same_leader'].mean()
    print(f"Match Rate (First == Dominant): {match_rate:.2%}")
    print("Interpretation: How often is the first leader also the one they see most?")
    
    # 7. Distribution of Dominant Stickiness
    comparison['dominant_stickiness'] = comparison['dominant_count'] / comparison['total_events']
    
    print(f"Avg Dominant Stickiness: {comparison['dominant_stickiness'].mean():.2%}")
    
    # Save metrics for Step 7 if needed
    comparison[['user_id', 'first_leader_id', 'dominant_leader_id', 'stickiness', 'dominant_stickiness', 'same_leader']].to_csv('h2_attribution_metrics.csv', index=False)
    print("\nSaved detailed metrics to h2_attribution_metrics.csv")

if __name__ == "__main__":
    main()
