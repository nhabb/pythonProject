import sys
import csv
import re
import os
from tabulate import tabulate

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
        print("-1) Exit")
        print("############################\n")

        try:
            choice = int(input("Input your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        match choice:
            case -1:
                sys.exit("Bye Bye")
            case 1:
                os.system('cls' if os.name == 'nt' else 'clear')
                list_courses()
            case 2:
                os.system('cls' if os.name == 'nt' else 'clear')
                course_name = input("Course Title: ")
                course_id = input("Course ID: ")
                semester = input("Semester: ")
                add_course(course_name, course_id, semester)
            case 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                course_id = input("Course ID: ")
                try:
                    year = check_year(input("Year: "))
                except ValueError:
                    print("Invalid input for year.")
                else:
                    update_course(course_id, year)
            case 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                try:
                    course_id = input("Course ID: ")
                    year = check_year(input("Year: "))
                    average = compute_course_average(course_id, year)
                except FileNotFoundError:
                    print("Invalid file name.")
                except ValueError as e:
                    print(f"Error: {e}")
                else:
                    print(f"Average = {average:.2f}")
            case 5:
                os.system('cls' if os.name == 'nt' else 'clear')
                student_id = input("Student ID: ")
                list_student_grades(student_id)
            case _:
                print("Invalid choice. Please try again.")

def check_year(year):
    if not re.match(r"^\d{4}$", year):
        raise ValueError("Year must be a 4-digit number.")
    return year

def add_course(name, course_id, semester):
    with open("courses.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, course_id, semester])

def list_courses():
    try:
        with open("courses.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            courses = list(reader)
        print("\n" + tabulate(courses[1:], headers=courses[0], tablefmt="github"))
    except FileNotFoundError:
        print("No courses found.")

def update_course(course_id, year):
    with open(f"{course_id}.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        print("Enter student ID and grade. Type 'done' to exit.")
        while True:
            student_id = input("Student ID: ")
            if student_id.lower() == "done":
                break
            try:
                grade = int(input("Grade: "))
                if not (0 <= grade <= 100):
                    raise ValueError
            except ValueError:
                print("Invalid grade. Please enter a number between 0 and 100.")
            else:
                writer.writerow([year, student_id, grade])

def compute_course_average(course_id, year):
    total, count = 0, 0
    with open(f"{course_id}.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == year:
                total += int(row[2])
                count += 1
    if count == 0:
        raise ValueError("No grades found for this course and year.")
    return total / count

def list_student_grades(student_id):
    grades = []
    try:
        with open("courses.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            course_ids = [row[1] for row in reader][1:]
        for course_id in course_ids:
            with open(f"{course_id}.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == student_id:
                        grades.append([course_id, row[0], row[2]])
        if grades:
            print("\n" + tabulate(grades, headers=["Course", "Year", "Grade"], tablefmt="github"))
        else:
            print("No grades found for this student.")
    except FileNotFoundError:
        print("Some files are missing.")

