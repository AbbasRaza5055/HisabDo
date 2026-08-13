"""
This script retrains our best model (Logistic Regression, from Day 4-6)
on the full pipeline, and saves it to disk using joblib so the API can
load it without retraining every time.

We save TWO things:
1. The trained model itself
2. The fitted StandardScaler (Day 6 introduced scaling - we need the
   exact same scaler that was fit on training data, not a new one,
   otherwise incoming API requests would be scaled inconsistently)
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# ---------------------------------------------------------
# Step 1: Load and clean the data (same as Day 3-6)
# ---------------------------------------------------------
df = pd.read_csv("students.csv")

df.loc[df["Attendance"] > 100, "Attendance"] = np.nan
numeric_columns = ["Age", "Attendance", "Assignment_Score", "Midterm_Score", "Final_Score"]
for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# ---------------------------------------------------------
# Step 2: Create the target column (same as Day 4-6)
# ---------------------------------------------------------
df["Overall_Score"] = (
    df["Assignment_Score"] * 0.20 +
    df["Midterm_Score"] * 0.30 +
    df["Final_Score"] * 0.50
)
df["Result"] = np.where(df["Overall_Score"] >= 40, 1, 0)  # 1 = Pass, 0 = Fail

# ---------------------------------------------------------
# Step 3: Select features (same order every time - this matters!)
# ---------------------------------------------------------
FEATURE_ORDER = ["Attendance", "Assignment_Score", "Midterm_Score", "Final_Score"]

X = df[FEATURE_ORDER]
y = df["Result"]

# ---------------------------------------------------------
# Step 4: Train-test split (same random_state as Day 4-6, for consistency)
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------------
# Step 5: Scale features (same as Day 6)
# ---------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------
# Step 6: Train the final model
# ---------------------------------------------------------
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Quick sanity check - confirm this matches our Day 4-6 results
from sklearn.metrics import accuracy_score
test_pred = model.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, test_pred)
print(f"Sanity check - test accuracy: {test_accuracy:.3f} (should match Day 4-6 results)")

# ---------------------------------------------------------
# Step 7: Save the model AND the scaler
# ---------------------------------------------------------
joblib.dump(model, "model/logistic_regression_model.joblib")
joblib.dump(scaler, "model/scaler.joblib")
joblib.dump(FEATURE_ORDER, "model/feature_order.joblib")

print("\nModel, scaler, and feature order saved successfully to /model")
print(f"Feature order: {FEATURE_ORDER}")
