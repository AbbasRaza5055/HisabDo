"""
This small script generates our student dataset and saves it as a CSV file.
We run this once to create students.csv, which the notebook will then load.

We add a few missing values and one invalid entry on purpose,
because the Day 3 task asks us to practice handling messy/missing data.
"""

import pandas as pd
import numpy as np

np.random.seed(42)  # keeps the "random" numbers the same every time we run this

names = [
    "Ali Raza", "Ayesha Khan", "Bilal Ahmed", "Fatima Malik", "Hamza Sheikh",
    "Sana Iqbal", "Usman Tariq", "Zainab Hussain", "Ahmed Butt", "Mahnoor Shah",
    "Hassan Javed", "Iqra Yousaf", "Kamran Aslam", "Laiba Naveed", "Moiz Anwar",
    "Nimra Siddiqui", "Omar Farooq", "Palwasha Khattak", "Qasim Mehmood", "Rabia Saleem",
    "Saad Qureshi", "Tayyaba Rasheed", "Umair Chaudhry", "Warda Ilyas", "Yasir Nawaz",
    "Zoya Baig", "Danish Akhtar", "Eman Fatima", "Faizan Riaz", "Ghazala Parveen"
]

courses = ["Computer Science", "Software Engineering", "Data Science", "Artificial Intelligence"]
genders = ["Male", "Female"]

rows = []
for i, name in enumerate(names):
    # decide gender based on the name list roughly (just for realistic demo data)
    gender = genders[i % 2]

    age = np.random.randint(18, 24)
    course = np.random.choice(courses)
    attendance = np.random.randint(50, 100)          # percentage
    assignment_score = np.random.randint(40, 100)
    midterm_score = np.random.randint(30, 100)
    final_score = np.random.randint(20, 100)

    rows.append([name, age, gender, course, attendance,
                 assignment_score, midterm_score, final_score])

df = pd.DataFrame(rows, columns=[
    "Student_Name", "Age", "Gender", "Course", "Attendance",
    "Assignment_Score", "Midterm_Score", "Final_Score"
])

# ---------------------------------------------------------
# Now we make the data a little messy on purpose,
# so later we can practice cleaning it (task requirement #9)
# ---------------------------------------------------------

# 1. A few missing Attendance values
df.loc[3, "Attendance"] = np.nan
df.loc[15, "Attendance"] = np.nan

# 2. A few missing Assignment_Score values
df.loc[7, "Assignment_Score"] = np.nan

# 3. One missing Final_Score value
df.loc[22, "Final_Score"] = np.nan

# 4. One invalid Attendance value (a typo that resulted in a value above 100%)
df.loc[10, "Attendance"] = 150

# 5. One missing Age value
df.loc[18, "Age"] = np.nan

df.to_csv("students.csv", index=False)
print("students.csv created successfully with", len(df), "rows.")
print("\nMissing values per column:")
print(df.isnull().sum())
