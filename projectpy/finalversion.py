import sys
import csv
import re
import os
#CORRECTION changed table to the correct tabulate function
from tabulate import tabulate  ## to remove before presentation : there is a type check error here because there is some type faults in the code 

def main() :
    while True:
        print("\n\n############################")
        print( "MENU" )
        print( "-----------------------------" )
        print( "1) List of all courses" )
        print( "2) Add a course to the list" )
        print( "3) Update a course in the list" )
        print( "4) Compute a course average" )
        print( "5) All grades for a student ID" )
        print( "-1) Exit" )
        print("############################\n")

        try:
            n = checkIN( input( "Input your choice: " ) )
        except ValueError :
            print( "Incorrect value\n" )
        else :
            match n :
                case -1 :
                    sys.exit( "Bye Bye" )
                case 1 :
                    os.system('cls')
                    listCourses()

                case 2 :
                    os.system('cls')
                    cID = input( "Course ID: " )
                    #correction added checkCourse function to avoid creating an existing file
                    if not checkCourse(cID):
                        cName = input( "Course Title: " )
                        semester = input( "Semester: " )
                        addCourse(cName , cID, semester )
                    else:
                        print("Course already exists!")

                case 3 :
                    os.system('cls')
                    cName = input( "Course Name: " )
                    try :
                        cYear = checkYear(input( "Year: " ))
                    except ValueError:
                        print( "Invalid input for year" )
                    else :
                        updateCourse( cName , cYear )

                case 4 :
                    os.system('cls')
                    try :
                        cName = input( "Course Name: " )
                        cYear = checkYear(input( "Year: " ))
                        average = courseAverage( cName , cYear )
                    except FileNotFoundError:
                        print( "Invalid file name" )
                    except ValueError :
                        print( "Invalid input for year" )
                    else :
                        print( "Average =", average )

                
                case 5 :
                    #Correction Added an if condition to handle error of using this case before case 3
                    os.system('cls')
                    stdID = input( "Student ID: " )
                    if not stdGrades( stdID ) :
                        createFile()

                case _ :
                    sys.exit( "Incorrect value" )

def checkIN( n ) :
    nb = int( n )
    return nb

def checkYear( n ) :
    
    #SEARCH function re.search takes a string and checks if the string is of exactly 4 characters if not it raises a Valueerror
    #r it handles the '\' ( raw string literal) like a character not like "\ n".
    # ^ indicates start of string.
    #  \d{4} it means the string must contain 4 digits.
    # "," A literal comma, matching exactly one comma in the input string.
    # "$" asserts the end of the string.
    
    if not re.search( r"^\d{4}$" , n ) :
        raise ValueError
    else :
        return n

def checkGrade( grade ) :
    grade = int( grade )
    if not 0 <= grade <= 100 :
        raise ValueError
    else :
        return grade

def listCourses() :
    courses = []
    #CORRECTION changed f to file to make the name correct
    with open("courses.csv" ) as file :
        reader = csv.reader( file )
        for row in reader:
            courses.append( row )
    #TABPRINT tabulate is a function from tabulate module ,converting data into human-readable table with Github format having the list course[0] as a header, and the lists courses[1:] as data of the tables
    print( "\n" , tabulate( courses[1:] , courses[0] , tablefmt = "github" ) , "\n" , sep = "" ) ##suggestion to adjust courses list name to listofcourses for more readable content

def addCourse( cName , cID , semester ) :
    with open( "courses.csv" , "a" , newline='' , encoding = 'utf-8'  ) as file :
        writer = csv.writer( file )
        writer.writerow( [cName , cID , semester] )

def updateCourse( cName , cYear ) :
    with open( cName+".csv" , "a" , newline='' , encoding = 'utf-8' ) as file :
        writer = csv.writer( file )
        print( "Enter student ID and grade. Type Done to exit" )
        while True :
            try :
                #CORRECTION validating that the string inputted must not have spaces 
                stID = input( "Student ID: " ).strip()
                if stID.lower() == "done" :
                    break
                grade = checkGrade( input( "Grade: " ) )
            except ValueError :
                print( "Incorrect value for grade" )
                pass
            else :
                writer.writerow( [cYear , stID , grade ] )

def courseAverage(cName , cYear) :
    with open( cName+".csv" ) as file :
        reader = csv.reader( file )
        for row in reader:
            if row[0] == cYear :
                sum += row[2]
                nb += 1
        if sum != 0 :
            return sum / nb
        else :
            raise( ValueError )
        
def stdGrades(stdID):
    #Correction added declaration for list files 
    files = []
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                files.append(row[1])
    #Correction added return to properly use function in main match case
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
                    # SEARCH function re.search takes a string and checks if the string is of exactly 4 characters if not it raises a ValueError
                    # r it handles the '\\' ( raw string literal) like a character not like "\\ n".
                    # ^ indicates start of string.
                    # \\d{4} it means the string must contain 4 digits.
                    # "," A literal comma, matching exactly one comma in the input string.
                    # "$" asserts the end of the string.
                    # "%s" is a placeholder for the value of stdID. The % operator performs string formatting, substituting the value of stdID into the regular expression.
                    # This part will match the exact value of stdID in the input string. (replace value of stdID in the file)
                    # \\d{1,3} it means the string must contain 1 to 3 digits.
                    # re.IGNORECASE flag that makes the search insensitive
                    if matches := re.search( r"^(\d{4}),%s,(\d{1,3})$" %stdID , ','.join(row) , re.IGNORECASE ) :
                        #Search group method used to locate grp 1 and 2 from the re.search
                        stdRecord.append( [name , matches.group(1) , matches.group(2)] )
        except FileNotFoundError:
            #correction added error handling for file not found errors 
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


#correction added a function to handle the error occuring in case 5
def createFile():
    cname = input("Enter course name: ")
    cID = input("Enter course ID: ")
    semester = input("Enter semester: ")
    year = input("Enter year: ")
    addCourse(cname,cID,semester)
    updateCourse(cID,year)

def checkCourse(cID):
    try:
        with open("courses.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if the course ID matches exactly in any row of the CSV
                if len(row) > 1 and row[1] == cID:
                    return True  # Course exists
        return False  # Course does not exist
    except FileNotFoundError:
        print("Error: 'courses.csv' file not found.")
        return False

if __name__ == "__main__" :
    main()
