# Day 5 - Model Comparison (Remote Internship Task)

This folder contains my Day 5 practical task submission for the remote internship.
It continues the Student Performance Prediction project from Day 4, now comparing
**two** classification models instead of one.

## 📁 What's in this project

| File | Description |
|---|---|
| `students.csv` | Same dataset from Day 3/4 — 30 student records. |
| `model_comparison.ipynb` | Main notebook — cleans data, trains both models, evaluates and compares them. |
| `chart1_confusion_matrices.png` | Confusion matrices for both models, side-by-side. |
| `chart2_metric_comparison.png` | Bar chart comparing Accuracy/Precision/Recall/F1 for both models. |
| `chart3_decision_tree_structure.png` | Bonus chart — a diagram of how the Decision Tree actually splits the data. |

## 🧠 Comparison Table (from this run)

| Model | Accuracy | Precision | Recall | F1 Score |
|---|---|---|---|---|
| Logistic Regression | 1.000 | 1.000 | 1.000 | 1.000 |
| Decision Tree | 0.833 | 1.000 | 0.800 | 0.889 |

## 🧠 Short Analysis

**Which model performed better?**
Logistic Regression scored higher on Accuracy, Recall, and F1 Score. Both
models tied on Precision (1.0) — meaning whenever either model predicted
"Pass," it was always correct. The Decision Tree's only mistake was
predicting "Fail" for one student who had actually Passed, so it was being
cautious rather than reckless.

**Why did Logistic Regression do better here?**
It combines all features using smooth weights, which fits well since our
target (Overall Score) is itself a weighted combination of the same scores.
The Decision Tree only used 2 splits (based on Midterm and Final Score) and
completely ignored Attendance and Assignment Score — with only 24 training
students, it likely didn't have enough data to learn a more detailed pattern.

**Was the dataset balanced?**
No — 26 students Passed and only 4 Failed (about 87%/13%). This is why we
can't rely on Accuracy alone; a model could reach high accuracy just by
mostly predicting "Pass."

**What could improve the results?**
A larger and more balanced dataset, cross-validation instead of a single
train/test split, more features, and tuning the Decision Tree (or trying
an ensemble method like Random Forest).

**Important caveat:** this comparison is based on a test set of only 6
students, so a single flipped prediction can change which model "wins."
The full reasoning for this is explained in detail inside the notebook.

## ▶️ How to Run

Install the required packages:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Then open the notebook:
```bash
jupyter notebook model_comparison.ipynb
```
Run all cells from top to bottom (`Kernel > Restart & Run All`).

## 🛠️ Requirements
- Python 3.x
- pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 5 task — comparing Logistic Regression and Decision Tree classifiers using
Accuracy, Precision, Recall, and F1 Score (not accuracy alone).*
