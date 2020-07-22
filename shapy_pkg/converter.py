# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:54:15 2020

@author: Leo Turowski
@executive author: Noah Becker
"""

import csv
import os
import ntpath
from zipfile import ZipFile
import pandas as pd
import numpy as np
import pickle
import typing
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField as GAF
from numpy.lib import recfunctions as rfn
from pyts.datasets import load_gunpoint
from mpl_toolkits.axes_grid1 import ImageGrid

def zip_to_csv(path:str):
    """
    **Convert a packaged sql file into a csv file**

	This function unpacks the given zip file at its location and invokes the given sql_to_csv
	function on the sql file, with the same name as the zip file
	
	param path: as the absolute path to the zip file with the sql in it, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='zip'):
        print("this is not a zip file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_csv(path[:-4])


def zip_to_npy(path:str):
    """
	**Convert a packaged sql file into a npy file**

	This function unpacks the given zip file at its location and invokes the given sql_to_npy
	function on the sql file, with the same name as the zip file
	
	param path: as the absolute path to the zip file with the sql in it, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='zip'):
        print("this is not a zip file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_npy(path[:-4])


def sql_to_csv(path:str,delimiter:str='\n'):
    """
	**Convert a set of INSERT statement into csv format**

	Extracting the Data from a set of INSERT statements saved in a sql file, this function
	converts the data into a csv file where every not INSERT line is saved in a separate pickle
	file and the data of the INSERT statements is stored line after line, with the given delimiter
	at the end of each line.

	param path: as the absolute path to the sql file, type str  
	param delimiter: as the delimiter at the end of each line, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='sql'):
        print("this is not an sql file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with open(filename, 'r') as oldfile:
        with open(filename[:-3] + 'csv', 'w',newline='') as newfile:
            content = oldfile.readlines()
            data = []
            picklelist = []
            for line in content:
                if(line.startswith('I')):
                    line = line.split('(')
                    line = line[1]  # cuts of the Insert part of the sql statement
                    line = line.split(')')  # cuts of the ");\n" end of the sql statement
                    line = line[0]
                    line = line.replace("'","")
                    data.append(line)
                else:   
                    picklelist.append(line)

            write = csv.writer(newfile,delimiter=delimiter)
            write.writerow(data)
            pickle.dump(picklelist, open((filename[:-3] + 'p'),'wb'))

def sql_to_npy(path:str,delimiter:str= ','):
    """
	**Convert a set of INSERT statement into a numpy array**

	Similar to the csv this function also stores unused data in a pickle file and creates
	a brand new file with the extracted data, this time in an npy format, however this time
	the delimiter has to be the delimiter used in the sql file, as well as an additional 
	missing_values string used to represent missing data
	
	param path: as the absolute path to the sql file, type str  
	param delimiter: as the string used in the sql file to separate the data, type str  
	param missing_values: the string used for missing data, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!="sql"):
        print("this is not an sql file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with open(filename, "r") as oldfile:
        newfilename = filename[:-3]
        content = oldfile.readlines()
        data = []
        picklelist = []
        for line in content:
            if(line.startswith("I")):
                line = line.split("(")
                line = line[1]  # cuts of the Insert part of the sql statement
                line = line.split(')')  # cuts of the ");\n" end of the sql statement
                line = line[0]
                line = line.replace("'","")
                data.append(line)
            else:
                picklelist.append(line)
        nparray = np.loadtxt(data, dtype=str,delimiter=delimiter,encoding = 'ASCII',ndmin=2)
        np.save(newfilename + "npy", nparray)
        pickle.dump(picklelist, open(newfilename + "p","wb"))


def csv_to_sql(path:str,delimiter:str='\n'):
    """
	**Convert a csv file into a set of INSERT statements**
	
	This function converts each set of data divided by the given delimiter
	of a csv file into a INSERT statement it also adds data 
	stored in a pickle file, with the same name as the csv file,
	as a commentary at the beginning, as to not impede the functionality
	
	param path: as the absolute path to the csv file, type str 
	param delimiter: as the string used to detect the different data sets, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='csv'):
        print("this is not a csv file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with open(path, newline='') as oldfile:
        newfilename = filename[:-3]
        picklelist = pickle.load(open(newfilename + "p","rb"))
        table = picklelist[0]
        table = table[table.rfind(" ") + 1:-1]
        reader = csv.reader(oldfile,delimiter=delimiter)
        with open(newfilename+ "sql", "w") as newfile:
            newfile.writelines(picklelist)
            for line in reader:
                line=''.join(line)
                line = line.replace(",","','")
                newfile.write("INSERT INTO %s VALUES('" %table)
                newfile.write("%s');\n" % line)


def csv_to_npy(path:str,delimiter:str=','):
    """
	**Convert a csv file into a numpy array representation**

	This function converts a csv file into a 2-dimensional numpy representation,
	while every set of data divided by the given delimiter is interpreted as a new row

	param path: as the absolute path to the csv file, type str  
	param delimiter: the string used to determine the rows of the numpy array, type str  
	param missing_values: as the string used to represent missing data, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='csv'):
        print("this is not a csv file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    newfilename = filename[:-3] + 'npy'
    data = np.loadtxt(path, dtype=str,delimiter=delimiter,encoding = 'ASCII',ndmin=2)
    np.save(newfilename,data)


def npy_to_sql(path:str):
    """
    **Convert a npy file into a set of INSERT statements**

	this function is the reverse function to sql_to_npy and when used in conjuction
	you end up with the same file in the end as you had in the beginning

	param path: as the absolute path to the npy file, type str  
    path=checkpath(path)
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='npy'):
        print("this is not an npy file")
        return
    os.chdir(os.path.dirname(path))
    np_array = np.load(path, 'r')
    filename = ntpath.basename(path)
    with open(filename[:-3] + 'sql', 'w') as newfile:
        picklelist = pickle.load(open(filename[:-3] + "p","rb"))
        newfile.writelines(picklelist)
        table = picklelist[0]
        table = table[table.rfind(" ") + 1:-1]
        for row in np_array:
            data = ','.join(row)
            data += "'"
            data = data.replace(",","','")
            data = data.replace("'NULL'","NULL")
            newfile.write("INSERT INTO {0} VALUES('{1});\n".format(table,data))           

def npy_to_csv(path:str):
    """
	**Converts a npy file into a csv representation of the data**

	Similar to npy_to_sql this function is the reverse function to csv_to_npy
	
	param path: as the absolute path to the npy file, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='npy'):
        print("this is not an npy file")
        return
    os.chdir(os.path.dirname(path))
    np_array = np.load(path, 'r')
    filename = ntpath.basename(path)
    with open(filename[:-3] + 'csv', 'w') as newfile:
        for row in np_array:
            data = ','.join(row)
            newfile.write("{0}\n".format(data))

def gen_GAF(path:str):
    """
	**Generate a Gramian Angular Field with User input**

	this function gets the input from the user through the console to generate
	either a Gramian Angular Summation Field or a Gramian Angular Difference Field
	from the data of a numpy array using the gen_GAF_exec function
	
	param path: as the absolute path to the npy file, type str  
    """
    path=checkpath(path)
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='npy'):
        print("this is not an npy file")
        return
    os.chdir(os.path.dirname(path))
    np_array = np.load(path, encoding = 'ASCII')
    method = int(input("Enter if you either want a Summation field(1) or a Difference field(2):\n"))
    if(method == 1):
        method = 'summation'
    else:
        method='difference'
    null_value=input("Enter the number you want to represent missing/NULL values (Default: 0):\n")
    gen_GAF_exec(np_array,(-1,1), method,null_value)

def gen_GAF_exec(data:list, sample_range:None or tuple = (-1,1), method:str = 'summation',null_value:str='0'):
    """
	**Generate a Gramian angular Field**

	this is the actual function when it comes to generating a Gramian Angular Field
	out of the data of a numpy array. This function takes different variables to determine
	how the Field should be scaled, what its size should be 
	and if it is either a summation or difference Field
	
	param data: as the content of a npy file , type list  
	param size: this is the size of the square output image, type int or float  
	param sample_range: as the range the data should be scaled to, type None or tuple  
	param method: as the type of field it should be, type 'summation' or 'difference' 
    param **null_value**: as the number to use instead of NULL, type str
    """
    gaf = GAF(sample_range=sample_range,method=method)
    data = np.where(data=='NULL', null_value , data)
    data = data[:,3:].astype(dtype=float)
    data_gaf = gaf.fit_transform(data)
    plt.imshow(data_gaf[0],cmap='rainbow',origin='lower')
    plt.show()

def false_input(path:str):
    """
	**Print error and return to main**

	this function prints an error message to the console and returns to main
	
	param path: this parameter is only there so the function has a proper form, type str 
    """
    print("this is an invalid option")
    main()

def exit(path:str):
    """
	**Print Message and end program**

	This function prints a message to the console and ends the program
	param path: this parameter is only there so the function has a proper form, type str 
    """
    print("thank you for using shapy, the converter of your choice")


def switchoption(n:int,path:str):
    """
	**Invoke a function**

	this function invokes one of the funtions of this program corresponding to the n
	and gives it the path as input
	param n: this number specifies which dunction should be invoked, type int  
	param path: this is the path to the file used for the function to be invoked, type str
    """
    switcher = {
            1: zip_to_csv,
            2: zip_to_npy,
            3: sql_to_csv,
            4: sql_to_npy,
            5: csv_to_sql,
            6: csv_to_npy,
            7: npy_to_sql,
            8: npy_to_csv,
            9: gen_GAF,
            0:exit,
        }
    function = switcher.get(n,false_input)
    function(path)

def checkpath(path:str):
    """
    **check the path for relativity**

    this function removes any quotation from a path and checks if it is relative or absolute
    it returns a *cleansed* path being the absolute representation of the given path

    param path: the string to be used as a path, type str    
    return path: the absolute path, type str  
    """
    path=path.replace('"','')
    path=path.replace("'","")
    if(os.path.isabs(path)):
        return path
    return os.getcwd+path

def main():
    """
	**Get User input and invoke functions**

	this function uses the console to get input from the user, as to which function
	should be invoked and where to find the coresponding file
    """
    path = input("enter path:\n")
    path_array = os.listdir(path)
    print("to exit (0)\n")
    print("zip_to_csv(1)\n")
    print("zip_to_npy(2)\n")
    print("sql_to_csv(3)\n")
    print("sql_to_npy(4)\n")
    print("csv_to_sql(5)\n")
    print("csv_to_npy(6)\n")
    print("npy_to_sql(7)\n")
    print("npy_to_csv(8)\n")
    print("gen_GAF(9)\n")
    n = int(input("what do you want to do:"))

    for element in path_array:
        switchoption(n,path + "/" + element)

if __name__ == "__main__":
    main()
