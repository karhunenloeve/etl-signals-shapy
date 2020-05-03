# Shapy
**Authors:** Leo Turowski, Noah Becker & Luciano Melodia.

A minimal package for quick data management.

# Contents

1. [Converting Sql statements](#Converting Sql statements)
	- [zip_to_csv](#zip_to_csv)
	- [zip_to_npy](#zip_to_npy)
	- [sql_to_csv](#sql_to_csv)
	- [sql_to_npy](sql_to_npy)
2.[Converting csv files](#Converting csv files)
	[csv_to_sql](#csv_to_sql)
	[csv_to_npy](#csv_to_npy)
3.[Converting npy files](#Converting noy files)
	[npy_to_sql](#npy_to_sql)
	[npy_to_csv](#npy_to_csv)
4.[Interpretation of data](#Interpretation)
	[gen_GAF](#gen_GAF)
	[gen_GAF_exec](#gen_GAF_exec)
5.[Quality of life functions](#Quality)
	[false_input](#false_input)
	[exit](#exit)
	[switchoption](#switchoption)
	[main](#main)
	[checkpath](#checkpath)
  
## Converting Sql statements

### zip_to_csv
	zip_to_csv(path:str)

	**Convert a packaged sql file into a csv file**

	This function unpacks the given zip file at its location and invokes the given sql_to_csv
	function on the sql file, with the same name as the zip file
	
	param path: as the absolute path to the zip file with the sql in it, type str  

### zip_to_npy
	zip_to_npy(path:str)

	**Convert a packaged sql file into a npy file**

	This function unpacks the given zip file at its location and invokes the given sql_to_npy
	function on the sql file, with the same name as the zip file
	
	param path: as the absolute path to the zip file with the sql in it, type str  

### sql_to_csv
	sql_to_csv(path:str, delimiter:str = '\n')

	**Convert a set of INSERT statement into csv format**

	Extracting the Data from a set of INSERT statements saved in a sql file, this function
	converts the data into a csv file where every not INSERT line is saved in a separate pickle
	file and the data of the INSERT statements is stored line after line, with the given delimiter
	at the end of each line.

	param path: as the absolute path to the sql file, type str  
	param delimiter: as the delimiter at the end of each line, type str  

### sql_to_npy
	sql_to_npy(path:str, delimiter:str = ',', missing_values:str = '')

	**Convert a set of INSERT statement into a numpy array**

	Similar to the csv this function also stores unused data in a pickle file and creates
	a brand new file with the extracted data, this time in an npy format, however this time
	the delimiter has to be the delimiter used in the sql file, as well as an additional 
	missing_values string used to represent missing data
	
	param path: as the absolute path to the sql file, type str  
	param delimiter: as the string used in the sql file to separate the data, type str  
	param missing_values: the string used for missing data, type str  

## Converting csv files

### csv_to_sql
	csv_to_sql(path:str, delimiter:str = '\n')

	**Convert a csv file into a set of INSERT statements**
	
	This function converts each set of data divided by the given delimiter
	of a csv file into a INSERT statement it also adds data 
	stored in a pickle file, with the same name as the csv file,
	as a commentary at the beginning, as to not impede the functionality
	
	param path: as the absolute path to the csv file, type str  
	param delimiter: as the string used to detect the different data sets, type str  


### csv_to_npy
	csv_to_npy(path:str, delimiter:str = '\n'; missing_values:str = '')

	**Convert a csv file into a numpy array representation**

	This function converts a csv file into a 2-dimensional numpy representation,
	while every set of data divided by the given delimiter is interpreted as a new row

	param path: as the absolute path to the csv file, type str  
	param delimiter: the string used to determine the rows of the numpy array, type str  
	param missing_values: as the string used to represent missing data, type str  

## Converting npy files

### npy_to_sql
	npy_to_sql(path:str)

	**Convert a npy file into a set of INSERT statements**

	this function is the reverse function to sql_to_npy and when used in conjuction
	you end up with the same file in the end as you had in the beginning

	param path: as the absolute path to the npy file, type str  

### npy_to_csv
	npy_to_csv(path:str)

	**Converts a npy file into a csv representation of the data**

	Similar to npy_to_sql this function is the reverse function to csv_to_npy
	
	param path: as the absolute path to the npy file, type str  

## Interpretation of data
	
### gen_GAF
	gen_GAF(path:str)

	**Generate a Gramian Angular Field with User input**

	this function gets the input from the user through the console to generate
	either a Gramian Angular Summation Field or a Gramian Angular Difference Field
	from the data of a numpy array using the gen_GAF_exec function
	
	param path: as the absolute path to the npy file, type str  

### gen_GAF_exec
	gen_GAF_exec(data:list, size:int or float = 1, sample_range:None or tuple = (-1,1), method:'summation'or'difference' = 'summation')
	
	**Generate a Gramian angular Field**

	this is the actual function when it comes to generating a Gramian Angular Field
	out of the data of a numpy array. This function takes different variables to determine
	how the Field should be scaled, what its size should be 
	and if it is either a summation or difference Field
	
	param data: as the content of a npy file , type list  
	param size: this is the size of the square output image, type int or float  
	param sample_range: as the range the data should be scaled to, type None or tuple  
	param method: as the type of field it should be, type 'summation' or 'difference'  

## Quality of life functions

### false_ input
	false_imput(path:str)

	**Print error and return to main**

	this function prints an error message to the console and returns to main
	
	param path: this parameter is only there so the function has a proper form, type str  
				
### exit
	exit(path:str)

	**Print Message and end program**

	This function prints a message to the console and ends the program
	param path: this parameter is only there so the function has a proper form, type str  

### switchoption
	switchoption(n:int , path:str)

	**Invoke a function**

	this function invokes one of the funtions of this program corresponding to the n
	and gives it the path as input
	param n: this number specifies which dunction should be invoked, type int  
	param path: this is the path to the file used for the function to be invoked, type str  


### main
	main()

	**Get User input and invoke functions**

	this function uses the console to get input from the user, as to which function
	should be invoked and where to find the coresponding file

### checkpath
	checkpath(path:str)->str

	**check the path for relativity**

	this function removes any quotation from a path and checks if it is relative or absolute
	it returns a *cleansed* path being the absolute representation of the given path

	param path: the string to be used as a path, type str    
	return path: the absolute path, type str  
