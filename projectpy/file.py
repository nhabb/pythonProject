from tabulate import tabulate

help(tabulate)

def tabulate(
    tabular_data: Mapping[str, Iterable[Any]] | Iterable[Iterable[Any]],
    headers: str | dict[str, str] | Sequence[str] = (),
    tablefmt: str | TableFormat = "simple",
    floatfmt: str | Iterable[str] = "g",
    intfmt: str | Iterable[str] = "",
    numalign: str | None = "default",
    stralign: str | None = "default",
    missingval: str | Iterable[str] = "",
    showindex: str | bool | Iterable[Any] = "default",
    disable_numparse: bool | Iterable[int] = False,
    colalign: Iterable[str | None] | None = None,
    maxcolwidths: int | Iterable[int | None] | None = None,
    rowalign: str | Iterable[str] | None = None,
    maxheadercolwidths: int | Iterable[int] | None = None,
) -> str: ...


    print( "\n" , tabulate( courses[1:] , courses[0] , tablefmt = "github" ) , "\n" , sep = "" )


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


    def stdGrades( stdID ) :
#CORRECTION replaced undeclared variable files in the lines below to file without s which was initially declared 
    with open( "courses.csv" ) as file :
        reader = csv.reader( file )
        for row in reader :
            file.append( row[1] )
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