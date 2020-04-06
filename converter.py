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






def zip_to_csv(path:str):
    """
    **Convert a single .sql.zip file into a .csv file**
    this function converts a single .sql.zip file into a single .csv file
    by first extracting its content and then converting the resulting .sql file
    into a .csv file. This will create both a .sql and a .csv file
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file, that is to be converted
    """
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
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_npy(path[:-4])


def sql_to_csv(path:str,delimiter:str='\n',quotechar='#'):
    """
    **Convert a single .sql file into a .csv file**
    this function takes the path to a .sql file and saves the data of Insert statements 
    in a single .csv file as well as saving all additional information in the file 
    in a single .p pickle list
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file that is to be converted
    """
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

            write = csv.writer(newfile,delimiter=delimiter,quotechar=quotechar)
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
    """
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with open(filename, 'r') as oldfile:
        newfilename = filename[:-3]
        content = oldfile.readlines()
        data = []
        picklelist = []
        for line in content:
            if(line.startswith("I")):
                line = line.split("(")
                line = line[1]  # cuts of the Insert part of the sql statement
                line = line[:-3]  # cuts of the ");\n" end of the sql statement
                line += "\n"
                line = line.replace("'","")
                data.append(line)
            else:
                picklelist.append(line)
        nparray = np.genfromtxt(data,dtype=None,delimiter=delimiter,missing_values=missing_values, encoding = 'cp1252')
        np.save(newfilename + 'npy', nparray)
        pickle.dump(picklelist, open(newfilename + "p","wb"))


def csv_to_sql(path:str,delimiter:str='\n',quotechar:str='#'):
    """
    **Convert a single .csv file into a .sql file**
    This function creates a new .sql file with insert the data specified in the .csv file
    this function also requies a .p file with the same name as the.csv in the same directory 
    in order to work
    THIS FUNCTION WORKS AS INTENTED
    :param path: this is the path of the .csv file to be converted
    """
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    with open(path, newline='') as oldfile:
        newfilename = filename[:-3]
        picklelist = pickle.load(open(newfilename + "p","rb"))
        table = picklelist[0]
        table = table[table.rfind(" ") + 1:-1]
        reader = csv.reader(oldfile,delimiter=delimiter,quotechar=quotechar)
        with open(newfilename+ "sql", "w") as newfile:
            newfile.writelines(picklelist)
            for line in reader:
                line=''.join(line)
                line = line.replace(",","','")
                newfile.write("INSERT INTO %s VALUES('" %table)
                newfile.write("%s');\n" % line)


def csv_to_npy(path:str,delimiter:str=',',missing_value:str=''):
    """
    **Convert a single .csv file into a .npy file**
    This function creates a new .npy file with the data of the .csv file
    this .npy file has the same location and name as the .csv file
    THIS FUNCTION WORKS AS INTENDED
    :param path: the path of the file that is to be converted
    """
    os.chdir(os.path.dirname(path))
    filename = ntpath.basename(path)
    newfilename = filename[:-3] + 'npy'
    data = np.genfromtxt(path, dtype=None,delimiter=delimiter,missing_values=missing_values,encoding = 'cp1252')
    np.save(newfilename,data)


def npy_to_sql(path:str):
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

def npy_to_csv(path:str,delimiter:str='\n',quotechar:str='#'):
    """
    **Convert a single .npy file into a .csv file**
    this function creates a new .csv file from the given .npy file
    and saves it at the same location with the same name as the .npy file
    :param path: the path of the .npy file
    """
    os.chdir(os.path.dirname(path))
    np_array = np.load(path, 'r+')
    filename = ntpath.basename(path)
    pd.DataFrame(np_array).to_csv(filename[:-3] + 'csv', index=False,header=False,index_label = False,quoting = csv.QUOTE_NONE, encoding = 'cp1252')
    """
    data = []
    with open(filename[:-3] + 'csv',mode='r',newline='') as infile:
        reader = csv.reader(infile,delimiter=delimiter,quotechar=quotechar,quoting=csv.QUOTE_NONE)
        for line in reader:
            line[0]=""
            data.append(line)
    with open(filename[:-3] + 'csv',mode='w',newline='') as outfile:
        write = csv.writer(outfile,delimiter=delimiter,quotechar=quotechar,quoting=csv.QUOTE_NONE)
        write.writerow(data)
    """

def gen_GAF(path:str): #TODO this is the function currently worked on
    """
    *generates a Gramian Angular Field from a .npy file*
    """
    os.chdir(os.path.dirname(path))
    data = np.load(path)
    data = data[:,3] #Nur fuer Testzwecke
    min_ = np.amin(data)
    max_ = np.amax(data)
    scaled_data = (2*serie - max_ -min_)/(max_ - min_)  #scaliert auf Intervall von [-1;1]
    scaled_data = np.where(scaled_data >= 1., 1., scaled_data)
    scaled_data = np.where(scaled_data <= -1., -1., scaled_data)
    phi = np.arccos(scaled_data)
    r=np.linspace(0,1, len(scaled_data))
    gaf = tabulate(phi, phi, cos_sum)
    return (gaf, phi, r, scaled_data)

def tabulate(x, y, f):
    """Return a table of f(x, y). Useful for the Gram-like operations."""
    return np.vectorize(f)(*np.meshgrid(x, y, sparse=True))

def cos_sum(a,b):
    """this function is used for tabulate to calculate the cosin sum"""
    return math.cos(a+b)


def false_input(path:str):
    print("this is an invalid option")

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
        }
        function = switcher.get(n,false_input)
        function(path)

def main():
        path = input("enter path:\n")
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
