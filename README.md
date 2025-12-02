# FitFam Community Analysis

This project analyzes the FitFam fitness community data to understand participation dynamics, leadership quality, and growth trends.

## Directory Structure

*   **`src/`**: Python source code and utility scripts.
    *   `data_loader.py`: Core class for loading and merging JSON data.
    *   `inspect_results.py`: Utility to view notebook outputs in the terminal.
    *   `get_summary_stats.py`: Calculates statistics for reports.
    *   `get_category_stats.py`: Analyzes event category data.
*   **`notebooks/`**: Jupyter notebooks for interactive analysis.
    *   `analysis.ipynb`: The main analysis notebook.
    *   `analysis_output.ipynb`: Executed notebook with results and plots.
*   **`reports/`**: Documentation and analytical reports.
    *   `FitFam_Analysis_Report.md`:  Analytical report.
    *   `project_work_summary.md`: Summary of the codebase and workflow.
    *   `subject_description.md`: Original project description.
*   **`fitfam-json/`**: Raw data files (JSON).

## How to Run

1.  **Setup Environment**: Ensure you have a Python environment with `pandas`, `matplotlib`, `seaborn`, and `jupyter` installed.
2.  **Run Analysis**:
    *   Open `notebooks/analysis.ipynb` in Jupyter Lab/Notebook.
3.  **Inspect Results**:
    *   Run `python src/inspect_results.py` to see the output of the analysis in your terminal.
4.  **Get Statistics**:
    *   Run `python src/get_summary_stats.py` or `python src/get_category_stats.py`.

## Data Source
The data consists of JSON exports from the FitFam backend, located in the `fitfam-json/` directory.
