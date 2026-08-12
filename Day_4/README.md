# Day 4 - Student Performance Prediction (Remote Internship Task)

This folder contains my Day 4 practical task submission for the remote internship.

## 📁 What's in this project

| File | Description |
|---|---|
| `students.csv` | Same dataset from Day 3 — 30 student records. |
| `student_performance_prediction.ipynb` | Main notebook — full ML pipeline from data cleaning to model evaluation. |
| `chart1_confusion_matrix.png` | Confusion matrix showing correct vs incorrect predictions. |
| `chart2_pass_fail_counts.png` | Bar chart showing how many students Pass vs Fail. |
| `chart3_feature_importance.png` | Bonus chart — which features the model relied on most. |

## 📝 In Simple Words

**What problem I solved:**
I built a small machine learning model that looks at a student's attendance
and scores, and predicts whether they will **Pass** or **Fail**.

**What features I used:**
- Attendance
- Assignment Score
- Midterm Score
- Final Score

**How I created the Pass/Fail label:**
Instead of just picking one existing score column and calling it the answer
(which would let the model "cheat" by copying a rule that was already
visible in the data), I calculated a weighted **Overall Score** first:
- Assignment Score → 20%
- Midterm Score → 30%
- Final Score → 50%

Then: **Overall Score ≥ 40 → Pass (1)**, otherwise **Fail (0)**.

**What model I selected:**
Logistic Regression — a simple, commonly used model for problems where the
answer is one of two categories (here: Pass or Fail).

**Accuracy achieved:**
The model reached 100% accuracy on the test set. However, I explain clearly
inside the notebook why this number should be taken with caution — our test
set only has 6 students in it (since the whole dataset is just 30 students),
and most students in the dataset pass, so there's very little room for the
model to make a mistake. A high score here shows the model learned the
pattern correctly on this small example, not that it would perform this well
on a large, real-world dataset.

**What I learned:**
- How to turn a scoring problem into a Pass/Fail prediction problem by
  creating a target column myself.
- Why building the target directly from a feature (without changing it) can
  cause "data leakage," and how to avoid that.
- Why looking at accuracy alone can be misleading, especially with a small
  or imbalanced dataset — which is why I also used a confusion matrix and
  classification report.
- How to train, test, and evaluate a basic Scikit-learn classification
  model from start to finish.

## ▶️ How to Run

Install the required packages:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Then open the notebook:
```bash
jupyter notebook student_performance_prediction.ipynb
```
Run all cells from top to bottom (`Kernel > Restart & Run All`).

## 🛠️ Requirements
- Python 3.x
- pandas, numpy, matplotlib, seaborn, scikit-learn, jupyter

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 4 task — practicing basic classification with Scikit-learn (Logistic Regression).*
