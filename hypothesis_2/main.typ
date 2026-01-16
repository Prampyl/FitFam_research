= Part 2: The Social Anchor – Leadership Quality

== 1. Introduction

=== 1.1. Context: The Volunteer-Led Community
FitFam operates on a unique model: it is a free, volunteer-led fitness community. Unlike commercial gyms where consistency is contractually enforced via paid employment, FitFam relies on "Intrinsic Stakeholders"—members who step up to lead. This decentralized structure creates a highly variable environment where the quality of the "service" (the event) fluctuates significantly between leaders. In this context, the leader serves not just as an instructor, but as the primary "Social Anchor," providing the structural reliability that the organization itself cannot centrally mandate.

=== 1.2. The Research Problem
While user churn is a natural phenomenon in fitness, we posit that it is highly sensitive to the "Leader Effect." New users who encounter a chaotic, inconsistent, or inexperienced leader may perceive the entire community as disorganized and disengage. Conversely, those effectively "anchored" by a high-quality leader may form a habit.

The core research problem is the **Objective Definition of Quality**. In a decentralized ecosystem, we lack standardized performance reviews. Subjective definitions of quality (e.g., "Charisma," "Energy," "Technical Skill") are difficult to quantify at scale. Furthermore, defining quality simply as "those who retain users" risks a tautology. We must identifying *ex-ante* behavioral metrics that predict *ex-post* retention.

=== 1.3. Research Motivation
If we can identify the specific, measurable traits of a leader that predict user survival, we can operationalize "Quality" without relying on subjective observation. This shifts the organizational focus from a "Talent Hunt" (finding charismatic stars) to "Behavioral Design" (training for specific traits). Specifically, we aim to test whether "Boring" metrics like *Consistency* and *Tenure* are more predictive of retention than "Vanity" metrics like *Frequency* or *Class Size*.

=== 1.4. Hypothesis
**Hypothesis 2 (H2):** User retention rates are significantly higher for cohorts that consistently attend sessions led by a "Dominant Leader" who exhibits **High Consistency** (low schedule variance) and **High Tenure** (experience).

== 2. State of the Art

The link between leadership and exercise adherence is one of the most robust findings in sport psychology. However, most research focuses on *subjective* leader traits (personality, style) rather than *objective* structural metrics. Our research bridges this gap by translating qualitative findings into quantitative signals.

=== 2.1. Structural Consistency vs. Instructor Traits
Research by *Hawley-Hague et al.* (The Gerontologist) on older adults' community classes identified "structural assurance" as a primary predictor of adherence. Their work suggests that the reliability of the "frame" (the schedule) reduces the cognitive load of participation. When a schedule is erratic, the user must constantly verify availability, introducing friction. In contrast, **"Structural Consistency"** facilitates habit formation by creating a stable cue. We operationalize this concept using **Schedule Variance** (Standard Deviation of start times): a lower variance implies a stronger habit cue.

=== 2.2. Social Cohesion and Leader Behavior
*Izumi et al.* (American Journal of Preventive Medicine) and *search.Ntoumanis* draw heavily on **Self-Determination Theory (SDT)**, identifying "Relatedness" as a key driver of retention. Leaders who actively foster group cohesion—rather than just delivering content—create "sticky" communities. 
However, measuring "Relatedness" usually requires qualitative surveys. We posit that **Tenure** acts as an effective *post-hoc* proxy for this trait. In a volunteer system, leaders with low social skills are naturally filtered out (they burn out or lose their audience). Thus, long-standing leaders (High Tenure) have effectively passed a "Natural Selection" test for building social capital.

=== 2.3. The Research Gap
Existing literature clearly establishes *that* better leaders retain more users, but it relies heavily on *subjective* data (interviews, surveys, expert observation). There is a paucity of research on how to identify these "High Quality" leaders using only *objective operational logs*. No study to date has explicitly tested whether simple log-based metrics like **Zero-Cancellation Reliability (Consistency)** and **Survivor Longevity (Tenure)** are sufficient to predict retention without ever observing the leader's actual behavior. This study aims to validate these "Digital Twins" of quality.

== 3. Methodology (Initial Design)

To operationalize "Leader Quality," we designed a retrospective cohort study using FitFam's event logs. The initial design focused on three pillars: Attribution, Intrinsic Metrics, and Survival Analysis.

=== 3.1. Data Scope & Cleaning
To ensure the analysis captures "Normal Operations" rather than external shocks, we applied strict filters to the raw event logs:
- **Timeframe (Post-Lockdown):** Data is restricted to the period from **January 2023 to Present**. This excludes the chaotic variance caused by the COVID-19 lockdowns (2020-2022), ensuring that schedule disruptions are attributable to the leader, not government policy.
- **Exclusion of External Cancellations:** Sessions cancelled due to *Force Majeure* (heavy rain (< AQI 200) or severe pollution) were removed from the dataset. We measure a leader's reliability based on factors within their control, not the weather.
- **Guest Leader Filtering:** We excluded "Casual Leaders" with fewer than 5 total events/lifetime. The analysis focuses on "Regulars" who have had a genuine opportunity to establish a rhythm.
- **Metric Definitions:** *Consistency* is defined strictly as the **temporal regularity** of sessions held (e.g., always Tuesday 7pm). It does not require the *content* to be identical (e.g., a leader swapping "HIIT" for "Tabata" is still considered consistent if the slot is held).

=== 3.2. Attribution Strategy: The "Dominant Leader"
A core challenge in community fitness is that users may attend events led by multiple different leaders. Attributing a user's retention to their "First Leader" proved too noisy, as a single initial session is a weak signal.
Instead, we adopted the **"Dominant Leader"** attribution model. We identify the leader with whom a specific user has attended the *most* sessions. This leader is assumed to have the strongest influence on that user's perception of the community.

=== 3.3. Initial Independent Variables (Defined Quality)
We initially hypothesized that "Quality" could be captured by four objective metrics, each representing a specific theoretical dimension of leadership:

1.  **Consistency (Habit Theory):** Defined as the standard deviation of time intervals between led events. *Rationale:* A predictable signal reduces friction for habit formation.
2.  **Tenure (Social Capital Theory):** The lifespan of the leader within the system. *Rationale:* Surviving leaders accumulate institutional knowledge and trust.
3.  **Frequency (Exposure Theory):** The average number of events led per month. *Rationale:* Higher visibility leaders create more "touchpoints" for new users to be onboarded.
4.  **Popularity (Democratic Selection Theory):** The average class size. *Rationale:* We assumed the "Market" is efficient—i.e., high-quality leaders will naturally attract larger crowds. Thus, crowd size was our initial proxy for "Charisma."

=== 3.3. Statistical Validation Plan
The robustness of these metrics was to be tested using **Survival Analysis**:
- **Kaplan-Meier Curves:** To visualize the unadjusted "life expectancy" of users managed by High vs. Low quality leaders.
- **Cox Proportional Hazards Model:** To calculate the Hazard Ratio (risk of churn) for each leader metric, while controlling for potential confounders such as **User Gender** and **City**.
This rigorous approach ensures that we are measuring the *leader's* impact, not just demographics.

== 4. Empirical Diagnostics & Methodological Refinement

During the preliminary analysis, several assumptions of the initial design were challenged by the data. The "Naive Model" (unstratified) produced paradoxical results, necessitating a formal diagnostic phase.

=== 4.1. Signal Failure in Initial Metrics
The first diagnostic warning came from the preliminary Survival Analysis. When we segmented leaders into "Top Tier" and "Bottom Tier" based on our initial metrics (Frequency and Popularity), the resulting Kaplan-Meier survival curves were **statistically indistinguishable** (Log-Rank p > 0.4). The "Best" leaders performed no better than the "Worst." 

#figure(
  rect(width: 100%, height: 60pt, fill: luma(240))[
    #align(center + horizon)[*Insert Figure 1 Here* \ Initial Kaplan-Meier Curves (Failed)]
  ],
  caption: [The Null Result. Survival curves for "Top Tier" vs "Bottom Tier" leaders (using initial metrics) show extensive overlap, visually confirming the lack of predictive power before refinement.]
)

This null result indicated that our definition of "Quality" was fundamentally flawed. Investigation revealed two specific failures:
- **Frequency (Multicollinearity):** We found that "High Frequency" leaders were almost universally "High Consistency" leaders. Mathematically, these two variables provided the same information. To avoid multicollinearity in the regression, we dropped "Frequency" in favor of "Consistency," which is the more fundamental behavioral trait.
- **Popularity (Non-Monotonicity):** We expected a linear relationship (Bigger Class = Better Leader). Instead, we observed a U-shaped and inverted curve. "Superstar Leaders" (50+ students) paradoxically had *lower* retention than mid-tier leaders. This "Star Cluster Paradox" suggested that class size was effectively a vanity metric that masked underlying churn dynamics.

=== 4.2. Identification of the Confounder: Activity Bias
Investigating the "Star Cluster Paradox" revealed a critical structural confounder: **Activity Type**.
FitFam events are not homogeneous.
- **HIIT & Bootcamp:** Naturally attract large crowds (High Popularity) but induce high churn due to physical intensity.
- **Yoga & Run:** Naturally have smaller caps (Low Popularity) but foster "stickier" behavior.
By failing to control for Activity Type, the naive model was punishing Yoga leaders for having small classes (a constraint of the activity) and rewarding HIIT leaders for churn-heavy volumes. Comparing a HIIT leader to a Yoga leader was a "Category Error."

#figure(
  rect(width: 100%, height: 60pt, fill: luma(240))[
    #align(center + horizon)[*Insert Figure 2 Here* \ Retention Rate by Activity Type]
  ],
  caption: [The Critical Confounder. Bar chart demonstrating that "sticky" activities (e.g., Running) have naturally higher retention than "churn-heavy" activities (e.g., HIIT), regardless of leader quality.]
)

=== 4.3. The Solution: Stratified Cox Regression
To neutralize this confounder, we moved from a standard Cox Proportional Hazards model to a **Stratified Cox Model**.
Instead of pooling all data, the model allows the baseline hazard function $h_0(t)$ to vary by **Activity Category**. Effectively, this means the model compares a leader's performance *only* relative to peers teaching the same activity. This isolates the "Leader Effect" from the "Activity Effect."

*Final Model Specification:*
$ h(t|X) = h_0(t) exp(beta_1 dot text("Consistency") + beta_2 dot text("Tenure") + beta_3 dot text("Controls")) $
*Stratified by:* Activity Category (HIIT, Running, Yoga, etc.)



== 5. Results & Discussion

=== 5.1. Primary Findings
The stratified Cox regression analysis yielded definitive results, validating the "Reliability Model" over the "Popularity Model."

- **Consistency (Habit Enabler):** **Highly Significant (p < 0.001).** 
  Users whose dominant leader had low schedule variance showed a significantly lower risk of churn. This serves as empirical validation of *Hawley-Hague's* "Structural Assurance": reliability is a prerequisite for habit formation. A chaotic schedule breaks the habit loop.

#figure(
  rect(width: 100%, height: 60pt, fill: luma(240))[
    #align(center + horizon)[*Insert Figure 3 Here* \ Retention Rate by Consistency & Tenure Tiers]
  ],
  caption: [The Descriptive Signal. Bar charts showing a clear "step-ladder" effect: retention rises monotonically as Leader Consistency improves (lower variance) and Tenure increases.]
)

#figure(
  rect(width: 100%, height: 60pt, fill: luma(240))[
    #align(center + horizon)[*Insert Figure 4 Here* \ Kaplan-Meier Survival Curves]
  ],
  caption: [The Validation signal. Survival curves stratified by Leader Consistency, showing a clear divergence: users with "Tier 1" consistent leaders have significantly longer community lifespans than those with "Tier 4" inconsistent leaders.]
)
- **Tenure (Trust Proxy):** **Highly Significant (p < 0.001).** 
  Leader experience was a robust predictor of retention. This supports our specific operationalization of *Izumi's* "Social Cohesion"—leaders who survive the volunteer filter for years have acquired the tacit skills to retain a group.
- **Popularity (The "Vanity" Check):** **Not Significant (p = 0.51).** 
  Once Activity Type was controlled for, class size lost all predictive power. This debunked the "Democratic Selection" hypothesis. A "Superstar" with a megaphone is no effective than a quiet leader with a consistent small group.

=== 5.2. Interpretation: The "Social Anchor" Validated
These findings strongly support **Hypothesis 2** and provide a clear definition for "Leader Quality."
In a volunteer ecosystem, Quality is not defined by **Charisma** (Popularity) or **Volume** (Frequency), but by **Reliability** (Consistency). The most effective leaders are not necessarily the ones who shout the loudest, but those who reduce the cognitive load for users by simply being predictable. They provide the stable "Social Anchor" upon which users can build their own habits.
The study effectively replaces the "Rockstar Myth" with the "Reliability Mandate."

=== 5.3. Limitations
- **Survivor Bias:** It is possible that "Better" leaders stay longer (High Tenure) *because* they are successful, rather than tenure causing success. However, from a user's perspective, the signal is the same: find an experienced leader.
- **Dominant Leader Assumption:** We attribute a user's entire outcome to their most-frequent leader. In reality, users may have a portfolio of leaders. Future work could use a time-weighted influence model.

=== 5.4. Conclusion & Transition: From Infrastructure to Agency
Part 2 established that a reliable leader provides the necessary **External Infrastructure** for retention. Consistency and Experience reduce environmental friction, creating a safe "container" for the user.

However, a high-quality leader is necessary but not sufficient. The presence of a stable anchor does not guarantee that a user will hold on. The locus of control now shifts from the *Provider* (Leader) to the *User* (Participant). 
Having validated the environment, we must now investigate the user's own behavioral patterns. Specifically, does the speed and intensity of their *initial* engagement—their "First 4 Weeks"—serve as a critical window for habit formation?

=== References
#list(
  [**Hawley-Hague, H., et al. (2014).** Multiple levels of influence on older adults' attendance and adherence to community exercise classes. *The Gerontologist*, 54(4), 599-610. (Evidence for "Structural Consistency").],
  [**Izumi, B. T., et al. (2015).** Leader behaviors, group cohesion, and participation in a walking group program. *American Journal of Preventive Medicine*, 49(1), 41-49. (Evidence for "Tenure as Social Capital").],
  [**Ntoumanis, N., et al. (2017).** The use of self-determination theory in health behaviour change interventions: a meta-analysis. *Health Psychology Review*, 11(2), 219-243. (Evidence for "Motivational Climate").]
)

= Part 3: The Behavioral Predictor – Early Attendance & Consistency
// Hypothèse: Early attendance frequency predicts long-term retention.
