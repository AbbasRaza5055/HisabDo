"""
Day 1 Practical Task - Basic Python Project
Remote Internship

This script collects basic user info, stores it, applies conditions,
loops over data, uses a function, and displays a final summary.
"""

# ---------------------------------------------------------
# 1. Take basic information from the user
# ---------------------------------------------------------
name = input("Enter your name: ")
age = int(input("Enter your age: "))
city = input("Enter your city: ")

# Collect a few skills as a list (comma-separated input)
skills_input = input("Enter your skills (comma-separated, e.g. Python, SQL, Excel): ")

# ---------------------------------------------------------
# 2. Store information using variables or lists
# ---------------------------------------------------------
# Split the skills string into a list, and clean up extra spaces
skills = [skill.strip() for skill in skills_input.split(",") if skill.strip() != ""]

# A list to store some quick facts we generate about the user
user_facts = []

# ---------------------------------------------------------
# 5. Use at least one function
# ---------------------------------------------------------
def get_age_category(user_age):
    """
    Takes an age and returns a simple category.
    Demonstrates a function with a parameter and a return value.
    """
    if user_age < 13:
        return "Child"
    elif user_age < 20:
        return "Teenager"
    elif user_age < 60:
        return "Adult"
    else:
        return "Senior"


def build_summary(user_name, user_age, user_city, user_skills):
    """
    Builds a formatted summary string from the user's data.
    Demonstrates a function that takes multiple parameters.
    """
    skills_text = ", ".join(user_skills) if user_skills else "No skills entered"
    return (
        f"Name    : {user_name}\n"
        f"Age     : {user_age}\n"
        f"City    : {user_city}\n"
        f"Skills  : {skills_text}"
    )


# ---------------------------------------------------------
# 3. Use if/else conditions
# ---------------------------------------------------------
category = get_age_category(age)
user_facts.append(f"Age category: {category}")

if len(skills) == 0:
    user_facts.append("No skills were entered.")
elif len(skills) == 1:
    user_facts.append("You entered exactly one skill. Consider learning more!")
else:
    user_facts.append(f"You entered {len(skills)} skills. Great range!")

if age >= 18:
    user_facts.append("You are eligible for most internships/jobs by age.")
else:
    user_facts.append("You are below the typical working age in many regions.")

# ---------------------------------------------------------
# 4. Use a loop
# ---------------------------------------------------------
print("\nProcessing your skills...")
for index, skill in enumerate(skills, start=1):
    print(f"  {index}. {skill} - noted successfully")

# ---------------------------------------------------------
# 6. Display the final output
# ---------------------------------------------------------
print("\n" + "=" * 40)
print("           FINAL SUMMARY")
print("=" * 40)
print(build_summary(name, age, city, skills))

print("\nQuick Facts:")
for fact in user_facts:
    print(f" - {fact}")

print("=" * 40)
print("Task completed successfully. Thank you!")
