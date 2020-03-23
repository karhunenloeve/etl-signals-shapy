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






def zip_to_csv(path):
    """
    **Convert a single .sql.zip file into a .csv file**
    this function converts a single .sql.zip file into a single .csv file
    by first extracting its content and then converting the resulting .sql file
    into a .csv file. This will create both a .sql and a .csv file
    :param path: the path of the file, that is to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_csv(path[:-4])


def zip_to_npy(path):
    """
    **Convert a single .sql.zip file into a .numpy file**
    this function converts a single .sql.zip file into a single .numpy file
    by first extracting its content and then converting the resulting .sql file
    into a .numpy file. This will create both a .sql and a .numpy file
    :param path: the path of the file, that is to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_npy(path[:-4])


def sql_to_csv(path):
    """
    **Convert a single .sql file into a .csv file**
    this function takes the path to a .sql file and saves the data of Insert statements 
    in a single .csv file as well as saving all additional information in the file 
    in a single .p pickle list
    :param path: the path of the file that is to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(filename, 'r')
    newfilename = filename[:-3]
    newfile = open(newfilename + 'csv', 'w')
    content = oldfile.readlines()
    data = []
    picklelist = []
    for line in content:
        if(line.startswith('I')):
            line = line.split('(')
            line = line[1]  # cuts of the Insert part of the sql statement
            line = line[:-3]  # cuts of the ");\n" end of the sql statement
            line.append("\n") 
            line = line.replace("'", "")
            data.append(line)
        else:
            picklelist.append(line)

        write = csv.writer(newfile, delimeter=',', quoting=csv.QUOTE_ALL)
        write.writerow(data)
        pickle.dump(picklelist, open((newfilename + 'p'),'wb'))
        oldfile.close()
        newfile.close()


def sql_to_npy(path):
    """
    **Convert a single .sql file into a .npy file**
    This function creates a new .npy file at the same location and with the same name
    as the .sql file it is called upon.
    Additional information is also saved in a single .p pickle list
    :param path: the path of the file that is to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(filename, 'r')
    newfilename = filename[:-3]
    content = oldfile.readlines()
    data = []
    picklelist = []
    for line in content:
        if(line.startswith("I")):
            line = line.split("(")
            line = line[1]  # cuts of the Insert part of the sql statement
            line = line[:-3]  # cuts of the ");\n" end of the sql statement
            line.append("\n")
            line = line.replace("'", "")
            data.append(line)
        else:
            picklelist.append(line)
    nparray = np.genfromtxt(data, delimeter=',',
                            missing_values='')
    np.save(newfilename + 'npy', nparray)
    pickle.dump(picklelist, open(newfilename + "p","wb"))
    oldfile.close()


def csv_to_sql(path):
    """
    **Convert a single .csv file into a .sql file**
    This function creates a new .sql file with insert the data specified in the .csv file
    this function also requies a .p file with the same name as the.csv in the same directory 
    in order to work
    :param path: this is the path of the .csv file to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(path, 'r')
    newfilename = filename[:-3]
    picklelist = pickle.load(open(newfilename + "p","rb"))
    newfile = open(oldfile, 'w')
    newfile.writelines(picklelist)
    content = oldfile.readlines()
    table = picklelist[0]
    table = table[table.rfind(" ") + 1:-1]
    for line in content:
        line.replace(",", "','")
        newfile.write("INSERT INTO %s VALUES('%s');\n", table, line)
    newfile.close()
    oldfile.close()


def csv_to_npy(path):
    """
    **Convert a single .csv file into a .npy file**
    This function creates a new .npy file with the data of the .csv file
    this .npy file has the same location and name as the .csv file
    :param path: the path of the file that is to be converted
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    newfilename = filename[:-3] + 'npy'
    data = np.genfromtxt(path, delimeter=',',
                         missing_values='')
    newfilename.save(data)


def npy_to_sql(path):  # TODO idee erst zu csv dann zu sql
    os.chdir(path + '/../')
    np_array = np.load(path, 'r')
    filename = ntpath.basename(path)
    newfile = open(filename[:-3] + 'sql', 'w')
    picklelist = pickle.load(open(filename[:-3] + "p","rb"))
    newfile.writelines(picklelist)
    table = picklelist[0]
    table = table[table.rfind(" ") + 1:-1]
    for line in np_array:
        newfile.write("INSERT INTO %s VALUES(", table)
        for value in line:
            newfile.write("'%s'", value)
        newfile.write(");\n")
    newfile.close()

def npy_to_csv(path):
    """
    **Convert a single .npy file into a .csv file**
    this function creates a new .csv file from the given .npy file
    and saves it at the same location with the same name as the .npy file
    :param path: the path of the .npy file
    """
    os.chdir(path + '/../')
    np_array = np.load(path, 'r')
    filename = ntpath.basename(path)
    pd.Dataframe(np_array).to_csv(filename[:-3] + 'csv', index=False) 

def switchoption(n,path):
        switcher = {
        1: zip_to_csv(path),
        2: zip_to_npy(path),
        3: sql_to_csv(path),
        4: sql_to_npy(path),
        5: csv_to_sql(path),
        6: csv_to_npy(path),
        }
        function = switcher.get(n,lambda: " is an invalid option")
        function()

def main():
        path = input("enter path:\n")
        print("zip_to_csv(1)\n")
        print("zip_to_npy(2) \n")
        print("sql_to_csv(3) \n")
        print("sql_to_npy(4) \n")
        print("csv_to_sql(5) \n")
        print("csv_to_npy(6) \n")
        n = input("what do you want to do:")
        switchoption(n,path)



if __name__ == "__main__":
    main()
