# FitFam Research Project: Work Summary (17/09/2025)

## Project Overview
This project aims to analyze the FitFam fitness community data to understand participation dynamics, leadership quality, and growth trends. We have successfully established a data processing pipeline, performed exploratory data analysis, and generated key insights regarding community demographics and engagement.

## Methodology & Workflow
1.  **Data Extraction**: We accessed raw data from JSON exports containing information on Users, Events, Locations, and Attendance.
2.  **Data Cleaning & Connection**:
    *   Merged disparate datasets to link **Users** to **Events** they attended.
    *   Connected **Events** to **Locations** and **Cities** to understand geographic distribution.
    *   Handled missing values and normalized data formats (e.g., timestamps, city names).
3.  **Analysis**:
    *   Calculated descriptive statistics for participation and leadership.
    *   Visualized trends in growth and retention.
    *   Identified key leaders and "Power Users" (potential leaders).

## Codebase Description

### 1. Data Processing
*   **`data_loader.py`**: The core utility script for data ingestion.
    *   **`FitFamDataLoader` Class**: Handles loading of JSON files (`users.json`, `events.json`, `event_user.json`, etc.).
    *   **`get_unified_data()`**: A crucial function that performs complex merges. It joins attendance records with event details, location metadata, and user demographics into a single, comprehensive DataFrame for analysis. It handles column renaming and conflict resolution (e.g., distinguishing between event organizer and attendee).

### 2. Analysis & Reporting
*   **`analysis_output.ipynb`** (formerly `analysis.ipynb`): The main computational notebook.
    *   Contains the executable code for the entire analysis workflow.
    *   Generates visualizations for:
        *   Monthly attendance trends.
        *   Top cities by activity.
        *   Gender distribution.
        *   Leadership activity (events led per user).
        *   User retention cohorts.
*   **`get_summary_stats.py`**: A specialized script to extract precise, high-level metrics for reporting.
    *   Calculates exact numbers for top cities, gender proportions, and retention rates.
    *   Used to validate findings and provide concrete numbers for the final report.
*   **`inspect_results.py`**: A utility script designed to parse and display the textual output of the analysis notebook.
    *   Useful for reviewing results without launching a Jupyter environment.
    *   Includes error handling to surface any issues during notebook execution.


