import sys
import csv
import re
import os
from tabulate import tabulate  # to remove before presentation : there is a type check error here because there are some type faults in the code

# Additional imports for future suggestions (machine learning and encryption)
from sklearn.linear_model import LinearRegression
import hashlib
import random
import numpy as np

def main():
    while True:
        print("\n\n############################")
        print("MENU")
        print("-----------------------------")
        print("1) List of all courses")
        print("2) Add a course to the list")
        print("3) Update a course in the list")
        print("4) Compute a course average")
        print("5) All grades for a student ID")
        print("6) Predict Student Performance")
        print("7) Recommend Courses")
        print("-1) Exit")
        print("############################\n")

        try:
            n = checkIN(input("Input your choice: "))
        except ValueError:
            print("Incorrect value\n")
        else:
            match n:
                case -1:
                    sys.exit("Bye Bye")
                case 1:
                    os.system('cls')
                    listCourses()

                case 2:
                    os.system('cls')
                    cID = input("Course ID: ")
                    if not checkCourse(cID):
                        cName = input("Course Title: ")
                        semester = input("Semester: ")
                        addCourse(cName, cID, semester)
                    else:
                        print("Course already exists!")

                case 3:
                    os.system('cls')
                    cName = input("Course Name: ")
                    try:
                        cYear = checkYear(input("Year: "))
                    except ValueError:
                        print("Invalid input for year")
                    else:
                        updateCourse(cName, cYear)

                case 4:
                    os.system('cls')
                    try:
                        cName = input("Course Name: ")
                        cYear = checkYear(input("Year: "))
                        average = courseAverage(cName, cYear)
                    except FileNotFoundError:
                        print("Invalid file name")
                    except ValueError:
                        print("Invalid input for year")
                    else:
                        print("Average =", average)

                case 5:
                    os.system('cls')
                    stdID = input("Student ID: ")
                    if not stdGrades(stdID):
                        createFile()

                case 6:
                    os.system('cls')
                    stdID = input("Student ID: ")
                    predictPerformance(stdID)

                case 7:
                    os.system('cls')
                    recommendCourses()

                case _:
                    sys.exit("Incorrect value")

def checkIN(n):
    nb = int(n)
    return nb

def checkYear(n):
    if not re.search(r"^\d{4}$", n):
        raise ValueError
    else:
        return n

def checkGrade(grade):
    grade = int(grade)
    if not 0 <= grade <= 100:
        raise ValueError
    else:
        return grade

def listCourses():
    courses = []
    with open("courses.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            courses.append(row)
    print("\n", tabulate(courses[1:], courses[0], tablefmt="github"), "\n", sep="")

def addCourse(cName, cID, semester):
    if checkCourse(cID) == True:
        print("Course already exists")
        return
    with open("courses.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([cName, cID, semester])

def updateCourse(cName, cYear):
    with open(cName + ".csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        print("Enter student ID and grade. Type Done to exit")
        while True:
            try:
                stID = input("Student ID: ").strip()
                if stID.lower() == "done":
                    break
                grade = checkGrade(input("Grade: "))
            except ValueError:
                print("Incorrect value for grade")
                pass
            else:
                writer.writerow([cYear, stID, grade])

def courseAverage(cName, cYear):
    sum = 0
    nb = 0
    with open(cName + ".csv") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == cYear:
                sum += int(row[2])
                nb += 1
        if nb != 0:
            return sum / nb
        else:
            raise ValueError

def stdGrades(stdID):
    files = []
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                files.append(row[1])
    except FileNotFoundError:
        print("Error: 'courses.csv' file not found.")
    except Exception as e:
        print(f"Error: Unable to read 'courses.csv'. {e}")

    stdRecord = []
    for name in files[1:]:
        try:
            with open(name + ".csv") as file:
                reader = csv.reader(file)
                for row in reader:
                    if matches := re.search(r"^(\d{4}),%s,(\d{1,3})$" % stdID, ','.join(row), re.IGNORECASE):
                        stdRecord.append([name, matches.group(1), matches.group(2)])
        except FileNotFoundError:
            print(f"Warning: '{name}.csv' file not found. Skipping.")
            return False
        except Exception as e:
            print(f"Error: Unable to read '{name}.csv'. {e}")
            return False

    if len(stdRecord):
        print(tabulate(stdRecord, headers=["Course", "Year", "Grade"], tablefmt="github"))
        return True
    else:
        print("Student ID not found")
        return False

def createFile():
    cname = input("Enter course name: ")
    cID = input("Enter course ID: ")
    semester = input("Enter semester: ")
    year = input("Enter year: ")
    addCourse(cname, cID, semester)
    updateCourse(cID, year)

def checkCourse(cID):
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 1 and row[1] == cID:
                    return True
        return False
    except FileNotFoundError:
        print("Error: 'courses.csv' file not found.")
        return False

# Student Performance Prediction using Linear Regression (Machine Learning)
def predictPerformance(stdID):
    student_data = []
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                course_id = row[1]
                with open(f"{course_id}.csv") as course_file:
                    course_reader = csv.reader(course_file)
                    for course_row in course_reader:
                        if course_row[1] == stdID:
                            student_data.append([int(course_row[2])])  # grade
    except FileNotFoundError:
        print("Error: File not found")
        return

    # Train a linear regression model (mock example, real data needed)
    X = np.array(range(len(student_data))).reshape(-1, 1)  # Simulated X (e.g., semester)
    y = np.array([data[0] for data in student_data])  # Grades as target
    model = LinearRegression().fit(X, y)
    predicted_grade = model.predict([[len(student_data)]])

    print(f"Predicted Grade for the next course: {predicted_grade[0]}")

# Course Recommendation using past performances
def recommendCourses():
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            courses = [row[1] for row in reader if row]
        print(f"Recommended Courses: {random.sample(courses, 3)}")  # Random course recommendation for demo
    except FileNotFoundError:
        print("Error: 'courses.csv' file not found.")
