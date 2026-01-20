
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
)

#set text(
  font: "New Computer Modern",
  size: 11pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.65em,
)

#show heading: it => [
  #v(0.5em)
  #block(it)
  #v(0.3em)
]

#align(center)[
  #text(17pt, weight: "bold")[Part 1: The First 14 Days -- Habit Formation]
  
  #v(1em)
  _Research Report on Hypothesis 1 (H1)_
]

#v(2em)

= 1. Introduction

== 1.1. Context: The Critical Window
In the fitness industry, the most dangerous period for user churn is the "onboarding phase." Research suggests that nearly 50% of new gym members quit within the first 6 months, with the steepest drop-off occurring in the first few weeks. FitFam, as a volunteer-led community with no financial lock-in (contracts), faces an even steeper challenge. Without the "sunk cost" of a subscription to keep them returning, users rely entirely on intrinsic motivation and rapid habit formation.

== 1.2. The Research Problem
The central question for FitFam's growth is: *Can we predict a user's long-term survival based entirely on their behavior in the first two weeks?*
If we can identify the behavioral "fingerprint" of a future core member within their first 14 days, we can:
1.  **Intervene Early:** Nudge "at-risk" users who display weak habit signals.
2.  **Optimize Onboarding:** Design the first 2 weeks to mimic the behavior of successful users.

== 1.3. Hypothesis
*Hypothesis 1 (H1):* Users who display higher **Frequency** (number of sessions) and higher **Regularity** (consistency of intervals) during their first 14 days are significantly more likely to be retained at 3 months.

= 2. State of the Art

The mechanism of "Habit Formation" is well-documented in behavioral psychology. Lally et al. (2010) famously posited that it takes an average of 66 days to form a habit, but early repetition is crucial.
*   **Frequency Principle:** The more a behavior is repeated in a specific context, the stronger the automaticity (Wood & Rünger, 2016).
*   **Consistency Principle:** Behaviors performed at stable times or contexts (e.g., "Every Monday") are more likely to stick than erratic behaviors.

In the context of FitFam, we posit that the "First 14 Days" serve as the incubation period. Users who treat FitFam as a sporadic novelty will churn; users who treat it as a routine will stay.

= 3. Methodology (Initial Design)

To test H1, we designed a retrospective analysis of all FitFam users with at least 90 days of possible tenure.

== 3.1. Cohort Definition
*   **Population:** Users who joined FitFam between 2018 and 2024.
*   **Exclusion:** Users with less than 90 days since signup (to allow for retention status verification).
*   **Target Variable (Y):** **Retention at 3 Months**. Binary classification:
    *   $1$ (Retained): Attended at least one event after day 90.
    *   $0$ (Churned): No attendance after day 90.

== 3.2. Initial Independent Variables
We extracted two metrics from the user's first 14 days of activity:
1.  **Frequency (Quantity):** Total count of check-ins in the first 14 days.
2.  **Mechanical Regularity (Consistency):** The standard deviation of time intervals (in days) between sessions.
    *   _Logic:_ A user who comes every 2 days ($sigma approx 0$) is more "regular" than one who comes after 1 day, then 5 days, then 2 days.

= 4. Methodological Shift & Refinement

During the exploratory phase, our initial definition of "Regularity" collapsed. Evaluating the results required a fundamental pivot in how we define "Consistency" in a voluntary sports community.

== 4.1. The Failure of "Mechanical Regularity"
While **Frequency** proved to be a robust predictor, **Mechanical Regularity** failed completely ($p approx 1.0$ in initial tests).
*   *The Insight:* Human beings are not metronomes. A user who trains every Tuesday and Thursday (regular) has intervals of 2 days, 5 days, 2 days, 5 days. A simple standard deviation calculation penalizes this "weekly rhythm" as irregular compared to someone who just trains every 3 days randomly.
*   *Conclusion:* We were measuring valid mathematical variation, not behavioral consistency.

== 4.2. The Pivot to "Behavioral Regularity"
We redefined regularity into two meaningful dimensions of user behavior: **Specialization** and **Balance**.

1.  **Category Regularity (Specialization):**
    *   Does the user "shop around" or find a niche? We calculate the ratio of unique categories to total sessions.
    *   *Metric:* $ R_("cat") = N_("unique") / N_("total") $
    *   *Interpretation:* Lower value = High Specialization (fewer categories for same volume). Higher value = High Diversification.
    *   *Note:* This simpler metric was used in the exploratory analysis to capture the "width" of a user's practice.

2.  **Temporal Regularity (Work/Life Balance):**
    *   Does the user train only on weekends or balance their week? We measure the deviation of weekday proportion from 50%.
    *   *Metric:* $ R_("temp") = | (N_("wd") / N_("total")) - 0.5 | $
    *   *Interpretation:* Low score = Balanced Routine (close to 50/50 split). High score = Imbalanced (e.g., Weekend Warrior or Weekday compulsive).

= 5. Results & Discussion

== 5.1. Primary Findings
Our analysis across multiple years (2023, 2024) confirms that early behavior is highly predictive of long-term retention.

#figure(
  table(
    columns: (auto, auto, auto, auto),
    inset: 10pt,
    align: center,
    [*Year*], [*Metric*], [*Result (p-value)*], [*Direction*],
    "2023-24", "Frequency", "< 0.001", "Positive (More is better)",
    "2023-24", "Category Regularity", "< 0.001", "Significant (Specialization is better)",
    "2023-24", "Temporal Regularity", "< 0.001", "Significant (Balance is better)",
    "All", "Mech. Regularity", "> 0.5", "Insignificant (Noise)",
  ),
  caption: [Summary of Statistical Tests (Mann-Whitney U)]
)

== 5.2. The Power of Frequency
Frequency remains the undisputed king of retention metrics.
*   **Retained Users:** Averaged ~3.01 sessions in the first 14 days.
*   **Churned Users:** Averaged ~1.69 sessions.
*   *Implication:* The "Magic Number" is 3. If a user does not attend at least 3 times in their first two weeks, their probability of churning skyrockets. Mere exposure breeds habit.

== 5.3. The "Niche" Effect (Category Regularity)
Contrary to the belief that users should "explore everything FitFam has to offer," our data suggests that **Specialization** drives retention.
*   **Retained Users** tend to find a "home" category (e.g., only Running) quickly.
*   **Churned Users** often display chaotic exploration without settling.
*   *Psychological Mechanism:* Finding a "tribe" or a specific format that works builds competence and social comfort faster than constantly being a novice in new formats.

== 5.4. The "Lifestyle" Effect (Temporal Regularity)
Retained users show a significantly better balance between Weekday and Weekend activity ($p < 0.001$).
*   Users who only attend on weekends (Weekend Warriors) are more fragile.
*   Users who integrate fitness into their work week (Tuesday/Thursday) AND their weekend form a resilient "lifestyle" habit that survives schedule disruptions.

= 6. Visual Evidence

*(Note: Figures referenced from analysis notebooks)*

#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  [
    #rect(width: 100%, height: 150pt, fill: luma(240))[
      #align(center + horizon)[*Figure 1: Frequency Distribution* \ Retained users show a distinct shift towards higher initial volume.]
    ]
  ],
  [
    #rect(width: 100%, height: 150pt, fill: luma(240))[
      #align(center + horizon)[*Figure 2: Category Regularity* \ Retained users have lower scores, indicating higher specialization in specific activity types.]
    ]
  ]
)

= 7. Conclusion & Recommendations

The "Broad-Spectrum" approach to onboarding—encouraging users to try everything whenever they want—is inefficient. The H1 analysis suggests a targeted "Precision Onboarding" strategy.

== 7.1. Validated Profile of a "Survivor"
The user most likely to reach Month 3 is one who:
1.  **Attends 3+ times** in the first 14 days.
2.  **Picks a Lane:** Focuses on a specific activity type (e.g., "I am a Runner").
3.  **Builds a Rhythm:** Attends during the week, not just the weekend.

== 7.2. Strategic Recommendations
1.  **The "First 3" Challenge:** Gamify the onboarding to incentivize 3 sessions in 2 weeks. This is the critical activation threshold.
2.  **Niche Onboarding:** Instead of "Welcome to FitFam, look at our 50 event types," try "Welcome! Are you a Runner or a Yogi?" Direct them to deep-dive into one vertical first.
3.  **Weekday Nudges:** Specific push notifications for weekend-only users to try a Tuesday morning session to bridge the weekly gap.

== 7.3. Limitations
*   *Correlation vs Causation:* Does specialization cause retention, or do committed people naturally specialize?
*   *Yearly Variance:* 2025 data was insufficient for validation. This model should be re-run annually.

#v(2em)
#line(length: 100%)
#text(0.8em, style: "italic")[Report generated for FitFam Research -- H1 Analysis Team]

= References

Lally, P., van Jaarsveld, C. H. M., Potts, H. W. W., & Wardle, J. (2010). How are habits formed: Modelling habit formation in the real world. _European Journal of Social Psychology_, 40(6), 998–1009.

Wood, W., & Rünger, D. (2016). Psychology of Habit. _Annual Review of Psychology_, 67(1), 289–314.
