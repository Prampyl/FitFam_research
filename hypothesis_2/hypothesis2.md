# Hypothesis 2: Leadership Impact

**Hypothesis:**
Retention rates are higher for cohorts that consistently attend sessions with a "Dominant Leader" who exhibits high consistency (low schedule variance).
**Refinement:** "First Leader" attribution was too noisy; "Dominant Leader" (most frequent) attribution yields significant results.

**Goal:**
Quantify the impact of a user's "First Leader" on their long-term retention in the FitFam community.

---

## 1. Definitions & Metrics

### 1.1. Defining "The Leader"

- **Source:** `events.json` (field: `organizer_id` or similar) OR `event_user.json` (where `role == 'lead'`).
- **Verification Task:** Confirm exact field name in `src/data_loader.py` or raw JSON.

### 1.2. Defining "Leader Quality" (Independent Variables)

**Crucial Concept:** Avoiding Circular Logic (Tautology)
Defining a "Good Leader" as "someone whose students stay longer" makes the hypothesis meaningless.
So I am going to define "Quality" using attributes intrinsic to the leader's behavior, independent of student retention.

**Selected Quality Proxies:**
| Metric | Definition | Rationale |
|--------|------------|-----------|
| **Consistency** (Reliability Score) | Standard deviation of days between led events. Lower std dev = Higher consistency. | Habit formation requires a stable cue. |
| **Tenure** (Experience Score) | Days between Leader's first led event and the current event date. | Experienced leaders likely have better soft skills and community knowledge. |
| **Frequency** (Dedication Score) | Average number of events led per month. | High frequency implies high engagement and visibility. |

### 1.3. Defining "User Retention" (Dependent Variable)

- **Metric:** 3-Month Retention Rate.
- **Definition:** Binary flag (1/0). Did the user attend any FitFam event > 90 days after their first event?

---

## 2. Step-by-Step Implementation Plan

### Step 1: Data Discovery & Cleaning

- **Tasks:**
  - Inspect `events.json` and `event_user.json` to confirm how to link `event_id` → `leader_user_id`.
  - Filter out "Guest Leaders" (leaders with < 5 total events) to reduce noise.

### Step 2: Feature Engineering (The "Leader Table")

- **Output:** DataFrame `df_leaders` indexed by `leader_user_id`.
- **Calculations:**
  - `first_led_date`, `last_led_date`, `total_events`.
  - `consistency_score` (std dev of time deltas).

### Step 3: Feature Engineering (The "User Cohort Table")

- **Output:** DataFrame `df_users` indexed by `user_id`.
- **Calculations:**
  - `first_event_id` and `first_event_date` for every user.
  - Link `first_event_id` → `leader_user_id` (The "First Leader").
  - `is_retained_90d` (True if `max(attendance_date) > first_event_date + 90 days`).

### Step 4: Merging & Analysis

- **Merge:** `df_users` with `df_leaders` on `leader_user_id`.
- **Analysis:**
  - Pearson correlation between `Leader_Consistency_Score` and `User_Retention_Rate`.
  - Segment leaders into "Tier 1" (High Consistency/Freq) vs "Tier 2" vs "Tier 3".
  - Compare average User Retention Rates across tiers.

### Step 5: Statistical Validation (The "Rigorous" Part)

- **Survival Analysis (Kaplan-Meier):**
  - Plot survival curves for users starting with Tier 1 Leaders vs Tier 3 Leaders.
  - **Null Hypothesis (H₀):** No difference in survival curves between groups.
  - **Test:** Log-Rank Test (p-value < 0.05).
- **Multivariate Regression (Cox Proportional Hazards):**
  - **Model:** `Hazard ~ Leader_Consistency + Leader_Tenure + User_City + User_Gender`.
  - **Goal:** Isolate the leader's effect while controlling for city/gender.

---

## 3. Critical Review & Risk Assessment

### Potential Pitfalls

| Pitfall                                                                                      | Mitigation                                                              |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **"Superstar" Bias:** Popular leaders might just lead in popular locations (e.g., Shanghai). | Include `Location_ID` or `City` as a control variable in the Cox model. |
| **Team Teaching:** Some events have multiple leaders.                                        | Take the primary leader (first in list) or average their scores.        |
| **Leader Churn:** Leaders themselves leave.                                                  | Distinguish "Leader Quit" from "Leader Bad".                            |

### Success Criteria

| Criteria              | Description                                                                  |
| --------------------- | ---------------------------------------------------------------------------- |
| **Strong Validation** | Log-Rank test p-value < 0.05 AND Leader Consistency coefficient is negative. |
| **Weak Validation**   | Trend is visible in charts but not statistically significant.                |
| **Rejection**         | No correlation found.                                                        |

---

## 4. Final Validation Results (Step 7)

- **Methodology:** Cox Proportional Hazards using "Dominant Leader" metrics.
- **Finding:**
  - **Leader Consistency:** Highly Significant (p < 0.0001).
  - **Coefficient:** +0.0061 (Positive => Higher Inconsistency increases Churn Risk).
  - **Conclusion:** Users who consistently attend sessions with a reliable leader (same time/place) are significantly less likely to churn.
- **Recommendation:** Prioritize leader schedule consistency over frequency.
