# Day 6 - Hyperparameter Tuning with GridSearchCV (Remote Internship Task)

This folder contains my Day 6 practical task submission for the remote internship.
It continues the Student Performance Prediction project, adding feature scaling
and hyperparameter tuning with GridSearchCV.

## 📁 What's in this project

| File | Description |
|---|---|
| `students.csv` | Same dataset from Day 3/4/5 — 30 student records. |
| `hyperparameter_tuning.ipynb` | Main notebook — cleaning, scaling, GridSearchCV tuning, and 3-way model comparison. |
| `chart1_all_metrics_comparison.png` | Bar chart comparing Accuracy/Precision/Recall/F1/ROC-AUC across all 3 models. |
| `chart2_roc_curves.png` | ROC curves for Logistic Regression, Default Decision Tree, and Tuned Decision Tree. |
| `chart3_tuned_tree_structure.png` | Diagram of the tuned Decision Tree's structure. |

## 🧠 Comparison Table (from this run)

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Decision Tree (Default) | 0.833 | 1.000 | 0.800 | 0.889 | 0.900 |
| Decision Tree (Tuned) | 0.833 | 1.000 | 0.800 | 0.889 | 0.900 |

**Best parameters found by GridSearchCV:**
`{'criterion': 'gini', 'max_depth': 2, 'min_samples_leaf': 1, 'min_samples_split': 2}`

## 🧠 Short Analysis

**Did tuning improve the Decision Tree?** No — the tuned tree's metrics came
out identical to the default (untuned) tree from Day 5. GridSearchCV searched
20+ combinations of `max_depth`, `min_samples_split`, `min_samples_leaf`, and
`criterion`, and converged on essentially what the default tree was already
doing.

**Why?** This is an honest finding about dataset size, not a failed
experiment. Our training set only has 24 students, with just 3 "Fail"
examples. There isn't enough data for different hyperparameter settings to
meaningfully separate from each other — a more complex tree would likely
have **overfit** rather than generalized better. GridSearchCV correctly
identified that a simple, shallow tree was the right call here.

**Logistic Regression still leads** across Accuracy, Recall, F1, and
ROC-AUC — tuning the Decision Tree didn't close that gap on this test set.

**What this teaches:** hyperparameter tuning is a search process, not a
guarantee of improvement — especially with a small dataset. It's a useful
confirmation, not a wasted step: it tells us we aren't missing a hidden,
better-performing tree that we just didn't try.

Full reasoning, code, and all outputs are in the notebook.

## ▶️ How to Run

Install the required packages:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Then open the notebook:
```bash
jupyter notebook hyperparameter_tuning.ipynb
```
Run all cells from top to bottom (`Kernel > Restart & Run All`).

## 🛠️ Requirements
- Python 3.x
- pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 6 task — feature scaling, GridSearchCV hyperparameter tuning, and comparing
tuned vs untuned models using multiple evaluation metrics including ROC-AUC.*
