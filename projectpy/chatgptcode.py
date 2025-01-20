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
                clear_console()
                list_courses()
            case 2:
                clear_console()
                course_name = input("Course Title: ")
                course_id = input("Course ID: ")
                semester = input("Semester: ")
                add_course(course_name, course_id, semester)
            case 3:
                clear_console()
                course_id = input("Course ID: ")
                try:
                    year = check_year(input("Year: "))
                except ValueError as e:
                    print(f"Error: {e}")
                else:
                    update_course(course_id, year)
            case 4:
                clear_console()
                try:
                    course_id = input("Course ID: ")
                    year = check_year(input("Year: "))
                    average = compute_course_average(course_id, year)
                except FileNotFoundError:
                    print("Course file not found.")
                except ValueError as e:
                    print(f"Error: {e}")
                else:
                    print(f"Average = {average:.2f}")
            case 5:
                clear_console()
                student_id = input("Student ID: ")
                get_student_grades(student_id)
            case _:
                print("Invalid choice. Please try again.")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_year(year):
    if not re.match(r"^\d{4}$", year):
        raise ValueError("Year must be a 4-digit number.")
    return year

def add_course(name, course_id, semester):
    if not all([name, course_id, semester]):
        print("All fields are required to add a course.")
        return
    with open("courses.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, course_id, semester])
    print(f"Course '{name}' added successfully.")

def list_courses():
    try:
        with open("courses.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            courses = list(reader)
        if courses:
            print("\n" + tabulate(courses[1:], headers=courses[0], tablefmt="github"))
        else:
            print("No courses available.")
    except FileNotFoundError:
        print("No courses found.")

def update_course(course_id, year):
    file_name = f"{course_id}.csv"
    try:
        with open(file_name, "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            print("Enter student ID and grade. Type 'done' to exit.")
            while True:
                student_id = input("Student ID: ").strip()
                if student_id.lower() == "done":
                    break
                try:
                    grade = int(input("Grade: "))
                    if not (0 <= grade <= 100):
                        raise ValueError("Grade must be between 0 and 100.")
                except ValueError as e:
                    print(f"Error: {e}")
                else:
                    writer.writerow([year, student_id, grade])
        print("Course updated successfully.")
    except FileNotFoundError:
        print(f"Course file '{file_name}' not found.")

def compute_course_average(course_id, year):
    total, count = 0, 0
    file_name = f"{course_id}.csv"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == year:
                    total += int(row[2])
                    count += 1
        if count == 0:
            raise ValueError("No grades found for this course and year.")
        return total / count
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist.")

def get_student_grades(student_id):
    grades = []
    try:
        with open("courses.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            course_ids = [row[1] for row in reader][1:]
        for course_id in course_ids:
            try:
                with open(f"{course_id}.csv", "r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[1] == student_id:
                            grades.append([course_id, row[0], row[2]])
            except FileNotFoundError:
                print(f"Course file '{course_id}.csv' is missing.")
        if grades:
            print("\n" + tabulate(grades, headers=["Course", "Year", "Grade"], tablefmt="github"))
        else:
            print(f"No grades found for student ID '{student_id}'.")
    except FileNotFoundError:
        print("Courses file not found.")

if __name__ == "__main__":
    main()
