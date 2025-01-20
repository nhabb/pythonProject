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

        try :
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
                    cName = input( "Course Title: " )
                    cID = input( "Course ID: " )
                    semester = input( "Semester: " )
                    addCourse(cName , cID, semester  )

                case 3 :
                    os.system('cls')
                    cName = input( "Course ID: " )

                case 4 :
                    os.system('cls')
                    try :
                        cName = input( "Course ID: " )
                        cYear = checkYear(input( "Year: " ))
                        average = courseAverage( cName , cYear )
                    except FileNotFoundError:
                        print( "Invalid file name" )
                    except ValueError :
                        print( "Invalid input for year" )
                    else :
                        print( "Average =", average )

                
                case 5 :
                    os.system('cls')
                    stdID = input( "Student ID: " )
                    stdGrades( stdID )

                case _ :
                    sys.exit( "Incorrect value" )

def checkIN( n ) :
    nb = int( n )
    return nb

def checkYear( n ) :
    '''
    #SEARCH function re.search takes a string and checks if the string is of exactly 4 characters if not it raises a Valueerror
    #r it handles the '\' ( raw string literal) like a character not like "\ n".
    # ^ indicates start of string.
    #  \d{4} it means the string must contain 4 digits.
    # "," A literal comma, matching exactly one comma in the input string.
    # "$" asserts the end of the string.
    '''
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
                stID = input( "Student ID: " )
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


def stdGrades( stdID ) :
#CORRECTION replaced undeclared variable files in the lines below to file without s which was initially declared 
    with open( "courses.csv" ) as file :
        reader = csv.reader( file )
        for row in reader :
            file.append( row[1] )
    '''
    #SEARCH function re.search takes a string and checks if the string is of exactly 4 characters if not it raises a Valueerror
    #r it handles the '\' ( raw string literal) like a character not like "\ n".
    # ^ indicates start of string.
    #  \d{4} it means the string must contain 4 digits.
    # "," A literal comma, matching exactly one comma in the input string.
    # "$" asserts the end of the string.
    # "%s" is a placeholder for the value of stdID. The % operator performs string formatting, substituting the value of stdID into the regular expression.
        This part will match the exact value of stdID in the input string. (replace value of stdID in the file)
    #  \d{1,3} it means the string must contain 1 to 3 digits.
    # re.IGNORECASE flag that makes the search insensitive 
    '''
    stdRecord = []
    for name in file[1:] :
        with open( name+".csv" ) as file :
            reader = csv.reader( file )
            for row in reader :
                if matches := re.search( r"^(\d{4}),%s,(\d{1,3})$" %stdID , ','.join(row) , re.IGNORECASE ) :
                    stdRecord.append( [name , matches.group(1) , matches.group(2)] )

    if len(stdRecord) :
        print( tabulate( stdRecord , headers = [ "Course" , "Year" , "Grade" ] , tablefmt = "github" ) )
    else :
        print( "Student ID not found" )
    


if __name__ == "__main__" :
    main()

## we need to add file reading handling  
## force user to use case 3 before using case 5 