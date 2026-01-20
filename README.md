# FitFam Research: Hypothesis 2 (The Leader Effect)

**Current Focus:** "Do 'Better' Leaders Retain More Users?"

This branch is dedicated to **Hypothesis 2**, which investigates the impact of Leader Quality on User Retention. It aims to develop an **objective, log-based definition of 'Quality'** that can predict user survival without subjective observation.

---

## 🚀 Executive Summary

Our research challenges the "Rockstar Myth" (that popular leaders are best). Using a **Stratified Cox Proportional Hazards Model**, we found:

- ✅ **Consistency (Schedule Reliability):** The strongest predictor of retention. Users with consistent leaders (low schedule variance) form habits faster.
- ✅ **Tenure (Experience):** A proxy for "Social Capital." Leaders who survive >2 years have tacit community-building skills.
- ❌ **Popularity (Class Size):** A vanity metric. Once controlled for **Activity Type**, class size has **zero correlation** with retention.

**Conclusion:** The "Best" leader is not the one with the biggest crowd, but the one who reduces friction (Reliability).

---

## 📂 Repository Structure

The work is concentrated in the **`hypothesis_2/`** directory:

| Path                             | Description                                                                                                        |
| :------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **`hypothesis_2/main.typ`**      | 📄 **The Final Research Report** (Typst). The primary artifact containing the narrative, methodology, and results. |
| **`hypothesis_2/ML/`**           | 🤖 **Analysis Models**. Contains the statistical scripts.                                                          |
| `ML/h2_step5_validation.py`      | The **Stratified Cox Regression** script. Runs the survival analysis controlling for Activity Type.                |
| `ML/H2_Final_Presentation.ipynb` | Jupyter Notebook generating the charts for the Manager Presentation.                                               |
| **`hypothesis_2/tests/`**        | 🧪 **Validation & Logs**. Output of various stress tests.                                                          |
| `tests/h2_refined_validation.py` | Refined validation logic confirming the Consistency vs Frequency pivot.                                            |

---

## 🛠️ Methodology

### 1. Data Cleaning

- **Timeframe:** Jan 2023 – Present (Excluding COVID-19 lockdowns).
- **Filters:** Removed "Guest Leaders" (<5 events) and Cancellations due to weather/pollution.

### 2. Attribution Logic

We use a **"Dominant Leader"** model. A user's retention outcome is attributed to the leader they visited _most frequently_.

### 3. The Pivot (Diagnostic Phase)

We initially tested **Frequency** and **Popularity**.

- **Frequency** failed due to multicollinearity (Redundant with Consistency).
- **Popularity** failed due to the "Star Cluster Paradox" (confounded by Activity Type).
- **Solution:** We pivoted to **Consistency + Tenure**, validated via **Stratified Cox Regression**.

---

## 📊 Key Diagnostics

- **The Null Result:** Initial Survival Curves (Top vs Bottom Tier) were indistinguishable.
- **The Paradox:** "Superstar" leaders had _lower_ retention than mid-tier leaders.
- **The Confounder:** Activity Type (HIIT = High Churn/High Vol, Running = Low Churn/Low Vol).

---

## 🏃 Getting Started

1.  **View the Report:**
    Open `hypothesis_2/main.typ` in a Typst editor or compile it to PDF.

2.  **Run the Analysis:**

    ```bash
    # Run the Validation Analysis
    python hypothesis_2/ML/h2_step5_validation.py
    ```

3.  **Generate Charts:**
    Run the notebook `hypothesis_2/ML/H2_Final_Presentation.ipynb`.
