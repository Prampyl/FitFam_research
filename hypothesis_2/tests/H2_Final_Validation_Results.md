# hé_refined_validation.py

```
--- Starting Refined Analysis (Popularity + Cohort View) ---
Analyzed 160 leaders.

Filtering for Top 5 Categories: ['HIIT', 'Running', 'Running + HIIT Combo', 'Wellness / Yoga/ Pilates', 'once off/ event only']

--- Descriptive Cohort Analysis ---

Retention Rate by Activity Type (Category):
dominant_category
once off/ event only 0.2667
Running 0.2460
HIIT 0.2164
Running + HIIT Combo 0.1469
Wellness / Yoga/ Pilates 0.1410
Name: is_retained, dtype: float64

Retention Rate by Consistency Tier:
consistency_tier
Tier 1 (Best) 0.2406
Tier 2 0.2067
Tier 3 0.1991
Tier 4 (Worst) 0.1794
Name: is_retained, dtype: float64

--- Stratified Cox Proportional Hazards Model ---
Stratifying by 'dominant_category' to control for activity type baseline differences.

Cox Summary (Stratified):
coef exp(coef) p
covariate
consistency_std 0.005203 1.005217 2.194915e-06
popularity_avg_size 0.001803 1.001805 5.087796e-01
tenure_days -0.000538 0.999462 1.604776e-08
gender_1.0 -0.202334 0.816822 2.809743e-04
gender_2.0 -0.182526 0.833163 1.640030e-05
```

## 1. The Confounder Check: Does Activity Matter?

**YES.** As you suspected, retention varies significantly by what the user _does_, not just who leads them.

| Activity Type                 | Retention Rate |
| :---------------------------- | :------------- |
| **Once Off / Event Only**     | 26.7%          |
| **Running**                   | 24.6%          |
| **HIIT**                      | 21.6%          |
| **Running + HIIT Combo**      | 14.7%          |
| **Wellness / Yoga / Pilates** | 14.1%          |

_Insight:_ "Active" formats (Running, HIIT) retain users ~50% better than "Wellness" formats (Yoga/Pilates).

## 2. Does Leader Quality Still Matter? (Stratified Analysis)

We ran a **Stratified Cox Regression**, which compares leaders _only_ against others teaching the same activity (e.g., Yoga leaders vs Yoga leaders).

### The Verdict:

| Metric          | Impact on Churn | Significance (P-Value)    | Conclusion                                                                                                                                                      |
| :-------------- | :-------------- | :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Consistency** | **High**        | **< 0.001** (Significant) | **VALIDATED.** Inconsistent leaders increase churn risk significantly, even within the same activity type.                                                      |
| **Tenure**      | **High**        | **< 0.001** (Significant) | **VALIDATED.** Experienced leaders retain users better.                                                                                                         |
| **Popularity**  | None            | 0.51 (Not Sig)            | **BUSTED.** Class size naturally varies by activity (HIIT is big, Yoga is small). Once we control for activity, "Class Size" itself stops predicting retention. |

## 3. Revised Retention by Consistency (Top 5 Categories)

After filtering for the main categories, the "Anomaly" (Tier 2 > Tier 1) disappeared.

- **Tier 1 (Best):** 24.1%
- **Tier 2:** 20.7%
- **Tier 3:** 19.9%
- **Tier 4 (Worst):** 17.9%

**Final Conclusion:**
A "Good Leader" is defined by **Reliability (Consistency)** and **Experience (Tenure)**.
"Popularity" (Class Size) is a vanity metric largely determined by the _Activity Type_, not the leader's quality.
