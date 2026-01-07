import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_results():
    # --- Data from H2_Final_Validation_Results.md ---
    
    # 1. Retention by Activity Type
    activity_data = {
        'Activity': ['Once Off / Event', 'Running', 'HIIT', 'Running + HIIT', 'Wellness / Yoga'],
        'Retention Rate': [0.2667, 0.2460, 0.2164, 0.1469, 0.1410]
    }
    df_activity = pd.DataFrame(activity_data)
    
    # 2. Retention by Consistency Tier
    consistency_data = {
        'Tier': ['Tier 1 (Best)', 'Tier 2', 'Tier 3', 'Tier 4 (Worst)'],
        'Retention Rate': [0.2406, 0.2067, 0.1991, 0.1794]
    }
    df_consistency = pd.DataFrame(consistency_data)

    # --- Plotting ---
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Activity Type
    sns.barplot(
        data=df_activity, 
        y='Activity', 
        x='Retention Rate', 
        palette='viridis', 
        ax=axes[0]
    )
    axes[0].set_title('Retention Rate by Activity Type\n(The Confounder)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Retention Rate (90 Days)')
    axes[0].set_xlim(0, 0.3)
    for i, v in enumerate(df_activity['Retention Rate']):
        axes[0].text(v + 0.005, i, f"{v:.1%}", va='center')

    # Plot 2: Consistency Tier (The Validated Signal)
    # Using a diverging color palette to emphasize Best vs Worst
    sns.barplot(
        data=df_consistency, 
        x='Tier', 
        y='Retention Rate', 
        palette='magma_r', 
        ax=axes[1]
    )
    axes[1].set_title('Retention Rate by Leader Consistency\n(Controlling for Activity w/ Stratified Cox)', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Retention Rate')
    axes[1].set_ylim(0, 0.3)
    for i, v in enumerate(df_consistency['Retention Rate']):
        axes[1].text(i, v + 0.005, f"{v:.1%}", ha='center')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_results()
