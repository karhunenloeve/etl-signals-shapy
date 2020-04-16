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







def zip_to_csv(path:str):
    """
    **Convert a single .sql.zip file into a .csv file**
    this function converts a single .sql.zip file into a single .csv file
    by first extracting its content and then converting the resulting .sql file
    into a .csv file. This will create both a .sql and a .csv file
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file, that is to be converted
    """
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
    **Convert a single .sql.zip file into a .numpy file**
    this function converts a single .sql.zip file into a single .numpy file
    by first extracting its content and then converting the resulting .sql file
    into a .numpy file. This will create both a .sql and a .numpy file
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file, that is to be converted
    """
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
    **Convert a single .sql file into a .csv file**
    this function takes the path to a .sql file and saves the data of Insert statements 
    in a single .csv file as well as saving all additional information in the file 
    in a single .p pickle list
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file that is to be converted
    :param delimiter: the character inserted after a line of data, default: '\n'
    """
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
                    line = line[:-3]  # cuts of the ");\n" end of the sql statement
                    line = line.replace("'","")
                    data.append(line)
                else:   
                    picklelist.append(line)

            write = csv.writer(newfile,delimiter=delimiter)
            write.writerow(data)
            pickle.dump(picklelist, open((filename[:-3] + 'p'),'wb'))

def sql_to_npy(path:str,delimiter:str=',',missing_values:str=''):
    """
    **Convert a single .sql file into a .npy file**
    This function creates a new .npy file at the same location and with the same name
    as the .sql file it is called upon.
    Additional information is also saved in a single .p pickle list
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file that is to be converted
    :param delimiter: the character used for separating data values from each other, default: ','
    :param missing_values: the string used instead of missing data, default: ''
    """
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
                line = line[:-3]  # cuts of the ");\n" end of the sql statement
                line +="\n"
                line = line.replace("'","")
                data.append(line)
            else:
                picklelist.append(line)
        nparray = np.genfromtxt(data,dtype=None,delimiter=delimiter,missing_values=missing_values, encoding = 'ASCII')
        print(nparray)
        np.save(newfilename + "npy", nparray)
        pickle.dump(picklelist, open(newfilename + "p","wb"))


def csv_to_sql(path:str,delimiter:str='\n'):
    """
    **Convert a single .csv file into a .sql file**
    This function creates a new .sql file with insert the data specified in the .csv file
    this function also requies a .p file with the same name as the.csv in the same directory 
    in order to work
    THIS FUNCTION WORKS AS INTENTED
    :param path: this is the path of the .csv file to be converted
    :param delimiter: the character added after a line of data, default: '\n'
    """
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


def csv_to_npy(path:str,delimiter:str=',',missing_values:str=''):
    """
    **Convert a single .csv file into a .npy file**
    This function creates a new .npy file with the data of the .csv file
    this .npy file has the same location and name as the .csv file
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file that is to be converted
    :param delimiter: the char in between to data sets, default: ','
    :param value: the String with wich missing value is interpreted, default: ''
    """
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='csv'):
        print("this is not a csv file")
        return
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    newfilename = filename[:-3] + 'npy'
    data = np.genfromtxt(path, dtype=None,delimiter=delimiter,missing_values=missing_values,encoding = 'ASCII')
    np.save(newfilename,data)


def npy_to_sql(path:str):
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
        for line in np_array:
            newfile.write("INSERT INTO %s VALUES(" %table)
            data = ''
            for value in line:
                data +="'"+value+"'"
            data.replace("''","','")
            newfile.write(data)
            newfile.write(");\n")

def npy_to_csv(path:str):
    """
    **Convert a single .npy file into a .csv file**
    this function creates a new .csv file from the given .npy file
    and saves it at the same location with the same name as the .npy file
    :param path: the path of the .npy file
    """
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")
        return
    if(path[-3:]!='npy'):
        print("this is not an npy file")
        return
    os.chdir(os.path.dirname(path))
    np_array = np.load(path, 'r+')
    filename = ntpath.basename(path)
    pd.DataFrame(np_array).to_csv(filename[:-3] + 'csv', index=False,header=False,index_label = False,quoting = csv.QUOTE_NONE, encoding = 'ASCII')

def gen_GAF(path:str):
    """
    This function is responsible for getting the input from the user,
    to either generate a Gramian Angular Summation or Gramian Angular Difference Field
    :param path: the location of the .npy file
    """
    if(not(os.path.isfile(path))):
        print("this path does not lead to a file")

        return
    if(path[-3:]!='npy'):
        print("this is not an npy file")
        return
    os.chdir(os.path.dirname(path))
    data = np.load(path, encoding = 'ASCII')
    column = int(input("choose the column of the data you provided, which you want to use as your time series:\n"))
    data = data[:,column]
    size = input("enter the size of the image you want: (default 1)\n")
    scaling = int(input("enter if the data should be scaled(1) or not(2):\n"))
    if(scaling == 1):
        sample_range = input("enter the range for your data to be scaled to:\n")
    else:
        sample_range=None
    method = int(input("Enter if you either want a Summation field(1) or a Difference field(2):\n"))
    if(method == 1):
        method = 'summation'
    else:
        method='difference'
    gen_GAF_exec(data, size, sample_range, method)




def gen_GAF_exec(data:list, size:int or float = 1, sample_range:None or tuple = (-1,1), method:str = 'summation'): #TODO this is the function currently worked on
    """
    **generates a Gramian Angular Field from a .npy file**
    this function scales a time series given in form of a single column
    of a .npy file and uses this scaled time series to construct a Gramian Angular Field
    :param path: the location of the .npy file
    """

    #transform the data into a Gramian Angular Field
    gaf = GAF(image_size=size,sample_range=sample_range,method=method)
    data_gaf = gaf.fit_transform(data)
    plt.imshow(data_gaf,cmap='rainbow',origin='lower')
    plt.show()

def false_input(path:str):
    print("this is an invalid option")
    main()

def exit(path:str):
    print("thank you for using shapy, the converter of your choice")


def switchoption(n:int,path:str):
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
            10:exit,
        }
        function = switcher.get(n,false_input)
        function(path)

def main():
        path = input("enter path:\n")
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
        switchoption(n,path)



if __name__ == "__main__":
    main()
