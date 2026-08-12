# Day 3 - Student Performance Analysis (Remote Internship Task)

This folder contains my Day 3 practical task submission for the remote internship.

## 📁 What's in this project

| File | Description |
|---|---|
| `students.csv` | Dataset — 30 student records (name, age, gender, course, attendance, assignment/midterm/final scores). Includes a few intentionally missing/invalid values for the data-cleaning step. |
| `generate_dataset.py` | Script used to generate `students.csv` (not required for analysis, kept for reference/reproducibility). |
| `student_performance_analysis.ipynb` | Main Jupyter notebook — full analysis, cleaning, and charts. |
| `chart1_score_distribution.png` | Chart — distribution of final scores. |
| `chart2_avg_score_by_course.png` | Chart — average final score per course. |
| `chart3_attendance_vs_final_score.png` | Chart — attendance vs final score scatter plot. |
| `CONCLUSION.md` | Short written summary of findings (also included inside the notebook). |

## 📊 What the Notebook Does

1. Loads the dataset with Pandas
2. Displays basic info (`.shape`, `.info()`, `.describe()`, missing value counts)
3. Cleans the data:
   - Treats attendance values above 100% as invalid → converts to missing
   - Fills all missing numeric values with the column median
4. Calculates average Assignment/Midterm/Final scores
5. Finds the student with the highest and lowest final score
6. Filters students with attendance below 75%
7. Filters students at risk of failing (final score below 40)
8. Calculates average final score grouped by course
9. Checks the correlation between attendance and final score
10. Builds 3 charts using Matplotlib
11. Ends with a short conclusion

## ▶️ How to Run

Install the required packages:
```bash
pip install pandas numpy matplotlib jupyter
```

Then open the notebook:
```bash
jupyter notebook student_performance_analysis.ipynb
```
Run all cells from top to bottom (`Kernel > Restart & Run All`).

## 🛠️ Requirements
- Python 3.x
- pandas, numpy, matplotlib, jupyter

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 3 task — practicing data cleaning, analysis, and visualization with Pandas and Matplotlib.*
