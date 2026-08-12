"""
Day 2 Practical Task - Student Data Analysis
Remote Internship

In this task, we store data about 10 students and use Pandas
to analyze that data (filtering, average, highest, lowest, etc.)
"""

import pandas as pd

# ---------------------------------------------------------
# Step 1: Create the student data
# ---------------------------------------------------------
# We are using a Python dictionary here. Each key is a column name,
# and each value is a list of data for that column.
# This is a simple way to organize data before turning it into a DataFrame.

student_data = {
    "Name": [
        "Ali Raza",
        "Ayesha Khan",
        "Bilal Ahmed",
        "Fatima Malik",
        "Hamza Sheikh",
        "Sana Iqbal",
        "Usman Tariq",
        "Zainab Hussain",
        "Ahmed Butt",
        "Mahnoor Shah"
    ],
    "Age": [20, 21, 19, 22, 20, 21, 23, 20, 22, 19],
    "Course": [
        "Computer Science",
        "Software Engineering",
        "Data Science",
        "Computer Science",
        "Artificial Intelligence",
        "Software Engineering",
        "Data Science",
        "Computer Science",
        "Artificial Intelligence",
        "Data Science"
    ],
    "Marks": [85, 67, 92, 58, 74, 88, 45, 79, 63, 95]
}

# ---------------------------------------------------------
# Step 2: Convert the dictionary into a Pandas DataFrame
# ---------------------------------------------------------
# A DataFrame is like a table (rows and columns), similar to an Excel sheet.
# Pandas makes it easy to filter, sort, and calculate things on this table.

df = pd.DataFrame(student_data)


# ---------------------------------------------------------
# Step 3: Function to display all students
# ---------------------------------------------------------
def show_all_students(dataframe):
    """
    Simply prints the whole student table.
    """
    print("\n===== All Students =====")
    print(dataframe)


# ---------------------------------------------------------
# Step 4: Function to display students with marks above 70
# ---------------------------------------------------------
def show_high_scorers(dataframe):
    """
    Filters the DataFrame and shows only students who scored above 70.
    """
    # This line means: "give me only the rows where Marks column is > 70"
    high_scorers = dataframe[dataframe["Marks"] > 70]

    print("\n===== Students with Marks Above 70 =====")
    print(high_scorers)


# ---------------------------------------------------------
# Step 5: Function to calculate average marks
# ---------------------------------------------------------
def get_average_marks(dataframe):
    """
    Returns the average (mean) of the Marks column.
    """
    average = dataframe["Marks"].mean()
    return average


# ---------------------------------------------------------
# Step 6: Function to find the student with the highest marks
# ---------------------------------------------------------
def get_top_student(dataframe):
    """
    Finds the row where Marks is the maximum, and returns that student's name.
    """
    # idxmax() gives us the index (row number) of the highest value
    top_index = dataframe["Marks"].idxmax()
    top_student = dataframe.loc[top_index]
    return top_student


# ---------------------------------------------------------
# Step 7: Function to find the student with the lowest marks
# ---------------------------------------------------------
def get_lowest_student(dataframe):
    """
    Finds the row where Marks is the minimum, and returns that student's name.
    """
    lowest_index = dataframe["Marks"].idxmin()
    lowest_student = dataframe.loc[lowest_index]
    return lowest_student


# ---------------------------------------------------------
# Step 8: Function to display total number of students
# ---------------------------------------------------------
def get_total_students(dataframe):
    """
    Returns how many rows (students) are in the DataFrame.
    """
    total = len(dataframe)
    return total


# ---------------------------------------------------------
# Step 9: Run everything (main program)
# ---------------------------------------------------------
# This is where we actually call all the functions above,
# one by one, and print the results nicely.

show_all_students(df)

show_high_scorers(df)

average_marks = get_average_marks(df)
print(f"\n===== Average Marks =====\n{average_marks:.2f}")

top_student = get_top_student(df)
print("\n===== Student with Highest Marks =====")
print(f"Name  : {top_student['Name']}")
print(f"Marks : {top_student['Marks']}")

lowest_student = get_lowest_student(df)
print("\n===== Student with Lowest Marks =====")
print(f"Name  : {lowest_student['Name']}")
print(f"Marks : {lowest_student['Marks']}")

total_students = get_total_students(df)
print(f"\n===== Total Number of Students =====\n{total_students}")

print("\nDay 2 task completed successfully!")
