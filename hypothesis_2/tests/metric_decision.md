# Metric Decision: Should we restart?

## The Problem

You asked if our 3 metrics (Consistency, Tenure, Frequency) are "good".
Our correlation analysis (r = -0.57 between Consistency and Frequency) suggests **they are not optimal.**
We are measuring "Time" (Tenure), "Reliability" (Consistency), and "Volume" (Frequency).
**We are missing "Charisma" (Quality).**

## Critique of Current Metrics

1.  **Consistency (KEEP):** The strongest predictor so far. Essential for habit formation. Valid.
2.  **Tenure (KEEP):** Completely independent from Consistency (r=0.01). Measures experience/authority. Valid.
3.  **Frequency (DROP):** Highly correlated with Consistency. Frequent leaders are naturally regular. It adds "noise" rather than "signal".

## The Evaluation Criteria

A "High Quality" Leader should be:

1.  Reliable (Consistency)
2.  Experienced (Tenure)
3.  **Liked by the Community (MISSING)**

## Proposal: The "Popularity" Metric

We should **restart the metric extraction** by replacing **Frequency** with **Popularity**.

**Definition: Popularity (Average Class Size)**

- The average number of **unique students** per session led by this leader.
- _Rationale:_ If a leader is consistent but boring, their class size might shrink. If they are charismatic, it grows. This captures the "Soft Skills" we cannot measure directly.

## Next Steps (If approved)

1.  Modify `h2_step5_validation.py` (or create step 8) to calculate `avg_class_size` for every leader.
2.  Check correlation of `avg_class_size` vs `Consistency`. (Are consistent leaders also popular?).
3.  Re-run Cox Regression with: `Consistency + Tenure + Popularity`.
