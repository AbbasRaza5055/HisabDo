# Conclusion — Day 3 Student Performance Analysis

**Dataset:** 30 students across 4 courses (Computer Science, Software Engineering,
Data Science, Artificial Intelligence).

## Key Findings

- **Data quality:** The raw dataset had a handful of missing values (in Age,
  Attendance, Assignment Score, and Final Score) and one invalid attendance
  entry recorded as 150%, which is impossible for a percentage. Invalid values
  were treated as missing, and all missing numeric values were filled using
  the column median.

- **Average performance:** Across all 30 students, the average final score
  was approximately **52.6**, with assignment scores averaging higher
  (~72.8) than midterm (~67.2) and final scores — suggesting performance
  tends to drop somewhat by the final exam.

- **Top and bottom performers:** The highest final score was **97**
  (Hassan Javed), and the lowest was **20** (Omar Farooq) — a wide spread,
  showing this class has both strong and struggling students.

- **Attendance concerns:** **21 out of 30 students** had attendance below 75%,
  which is a notably large portion of the class and would likely be a
  practical concern in a real classroom setting.

- **At-risk students:** Using a final score below 40 as the threshold,
  **10 students** were identified as at risk of failing.

- **Average score by course:** Computer Science had the highest average
  final score, while Data Science had the lowest in this dataset. The gap
  between the best and worst performing course was moderate, not extreme.

- **Attendance vs. final score:** The correlation between attendance and
  final score came out to **-0.16**, which is weak and essentially shows
  no meaningful relationship in this particular dataset. This was somewhat
  unexpected — intuitively, higher attendance should relate to better
  performance — but with only 30 randomly generated records, no clear
  pattern emerged. This is a useful, honest finding: it's a reminder that
  correlation should be tested with real data rather than assumed, and that
  small sample sizes can easily hide or distort real-world relationships.

## What I Practiced

Loading and inspecting data with Pandas, cleaning missing/invalid values,
filtering rows with conditions, grouping and aggregating data, calculating
correlation, and building basic charts with Matplotlib to visually support
the analysis.
