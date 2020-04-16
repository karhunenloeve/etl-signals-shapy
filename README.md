# Shapy
**Authors:** Leo Turowski, Noah Becker & Luciano Melodia.

A minimal package for quick data management.
There exist 14 functions:
zip_to_csv,
zip_to_npy,
sql_to_csv,
sql_to_npy,
csv_to_sql,
csv_to_npy,
npy_to_sql,
npy_to_csv,
gen_GAF,
gen_GAF_exec,
dalse_input,
exit,
switchoption,
main

zip_to_csv(path):
	Unpacks a zip file with a single sql file in it

	invokes the sql_to_csv function on the unpacked sql file
	
	Parameters:	path: str
					path to the zip file
	Returns: None
	Notes:
		The function does not check if there actually is a packaged sql file
		it only checks if a zip is present.
		the zip file has to have the sqme name as the sql file with an added
		.zip at the end

zip_to_npy(path):
	Unpacks a zip file with a single sql file in it

	invokes the sql_to_npy function on the unpacked sql file
	
	Parameters: path: str
					path to the zip file
	Returns: None
	Notes:
		The function does not check if there actually is a packaged sql file
		it only checks if a zip is present.
		the zip file has to have the sqme name as the sql file with an added
		.zip at the end

sql_to_csv(path,delimiter='\n'):
	converts a sql file into a csv file provided the data is present in INSERT statements
	any data not in an INSERT statement will be saved however in a pickle file
	for later reconstruction of the original file
	this function creates a new csv file and .p pickle file 
	with the same name as the sql file at the same directory as the sql file
	Parameters: path: str
					path to the sql file
				delimiter: str, optional
					The string used to separate different INSERT statements in the csv file
	Returns: None
	Notes:
		If the path is wrong this function will print an error message

sql_to_npy(path,delimiter=',',missing_values=''):
	converts a sql file into a numpy array provided the data is present in INSERT statements
	any data not in an INSERT statement will be saved however in a pickle file
	for later reconstruction of the original file
	this function creates a new .npy file and .p pickle file
	with the same name and directory as the sql file
	Parameters: path: str
					path to the sql file
				delimiter: str, optional
					the string used to separate values
				missing_values: str, optional
					the set of strings coresponding to missing data
	Returns: None
	Notes:
		If the path is wrong this function will print an error message
		the pickle file has to be present, allthough its content is not checked

csv_to_sql(path, delimiter='\n')
	converts a csv file into a sql file with the help of a pickle file
	this will create a series of INSERT statements with the data of the csv file
	preceded by the contents of the pickle file
	Parameters: path: str
					the path to the csv file
				delimiter: str, optional
					the string used to separate different INSERT statements in the csv file
	Returns: None
	Notes:
		If the path is wrong this function will print an error message

csv_to_npy(path, delimiter = ','; missing_values = ''):
	converts a csv file into a numpy array and saves the array in a npy file
	with the same name and directory as the given csv file
	Parameters: path: str
					the path to the csv file
				delimiter: str, optional
					the string used to separate values
				missing_values: str, optional
					the set of strings coresponding to missing data
	Returns: None
	Notes:
		If the path is wrong this function will print an error message

npy_to_sql(path):
	converts a npy file into a sql file
	Parameters: path: str
					the path to the npy file
	Returns: None
	Notes:
		If the path is wrong this function will print an error message

npy_to_csv(path):
	converts a npy file into a csv file
	Parameters: path: str
					the path to the npy file
	Returns: None
	Notes:
		Iff the path is wrong this function will print an error message
gen_GAF(path)
	this function gets the input from the user through the console to generate
	either a Gramian Angular Summation Field or a Gramian Angular Difference Field
	using the gen_GAF_exec function
	Parameters: path: str
					the path to the npy file for the generation of the GAF
	Notes:
		If the path is wrong this function will print an error message
		This function uses the console to get the parameters for the gen_GAF_exec funtion

gen_GAF_exec(data, size = 1, sample_range = (-1,1), method = 'summation')
	this function actually generates a Gramian Angular Field and plots a picture of it
	Parameters: data: list
					this is the content of a npy file
				size: int or float, optional
					Shape of the output images.
					If float, it represents a percentage of the size of each time series
					and must be between 0 and 1.
					Output images are square, 
					thus providing the size of one dimension is enough.
				sample_range: None or tuple, optional
					Desired range of transformed data.
					If None, no scaling is performed and all the values of the input data
					must be between -1 and 1. 
					If tuple, each sample is scaled between min and max;
					min must be greater than or equal to -1 
					and max must be lower than or equal to 1.
				method: 'summation' or 'difference', optional
					Type of Gramian Angular Field.
					‘s’ can be used for ‘summation’ and ‘d’ for ‘difference’.
	Returns: None

false_ input(path):
	this function prints an error message and returns to main
	Parameters: path: str
					this parameter is unused
	Returns: None
	Notes:
	this function is mostly invoked if the main of this program is invoked via console
exit(path):
	this function prints a message and ends the program
	Parameters: path: str
					this parameter is unused
	Returns: None
	Notes
	this function is mostly invoked of the main of this program is invoked via console

switchoption(n, path):
	this function invokes one of the funtions of this program corresponding to the n
	with the path as input
	Parameters: n: int
					this specifies which funtion should be invoked
				path: str
					this parameter is given to the invoked function
	Returns: None

main():
	this function uses the console to get input from the user, as to which function
	should be invoked and where to find the coresponding file
	Parameters: None
	Returns: None

