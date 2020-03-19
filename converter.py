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







def zip_to_csv(path):
    """
    **Convert a single .sql.zip file into a .csv file**
    this function converts a single .sql.zip file into a single .csv file
    by first extracting its content and then converting the resulting .sql file
    into a .csv file. This will create both a .sql and a .csv file
    :param path: the path of the file, that is to be converted
    :return: this function returns 1 on a success
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_csv(path[:path.rfind('.')])
    return 1


def zip_to_npy(path):
    """
    **Convert a single .sql.zip file into a .numpy file**
    this function converts a single .sql.zip file into a single .numpy file
    by first extracting its content and then converting the resulting .sql file
    into a .numpy file. This will create both a .sql and a .numpy file
    :param path: the path of the file, that is to be converted
    :return: this function returns 1 on a success
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    with ZipFile(filename, 'r') as zip:
        zip.extractall()
    sql_to_npy(path[:path.rfind('.')])
    return 1


def sql_to_csv(path):
    """
    **Convert a single .sql file into a .csv file**
    :param path: the path of the file that is to be converted
    :return: this function returns 1 on a success
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(filename, 'r')
    newfilename = filename[:filename.rfind('.')] + '.csv'
    newfile = open(newfilename, 'w')
    content = oldfile.readlines()
    data = []
    for line in content:
        if(line.startswith('I')):
            line = line.split('(')
            line = line[1]  # cuts of the Insert part of the sql statement
            line[:len(line) - 2]  # cuts of the ");" end of the sql statement
            line[len(line)] = '\n'
            line = line.replace("'", "")
            data.append(line)
        else:
            line[2:]
            if(line.startswith('v')):
                data.append(line)

        write = csv.writer(newfile, delimeter=',', quoting=csv.QUOTE_ALL)
        write.writerow(data)
        oldfile.close()
        newfile.close()
        return 1


def sql_to_npy(path):
    """
    **Convert a single .sql file into a .npy file**
    This function creates a new .npy file at the same location and with the same name
    as the .sql file it is called upon.
    This function only works if the name of the first insert entry begins with a '# v'
    e.g.: '# val_id'
    :param path: the path of the file that is to be converted
    :return: this function returns 1 on a success
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(filename, 'r')
    newfilename = filename[:filename.rfind('.')] + '.npy'
    content = oldfile.readlines()
    data = []
    for line in content:
        if(line.startswith('I')):
            line = line.split('(')
            line = line[1]  # cuts of the Insert part of the sql statement
            line[:len(line) - 2]  # cuts of the ");" end of the sql statement
            line[len(line)] = '\n'
            line = line.replace("'", "")
            data.append(line)
        else:
            line[2:]
            if(line.startswith('v')):
                data.append(line)
    nparray = np.genfromtxt(data, delimeter=',',
                            missing_values=np.NaN, names=True)
    np.save(newfilename, nparray)
    oldfile.close()
    return 1


def csv_to_sql(path, table):
    """
    **Convert a single .csv file into a .sql file**
    This function creates a new .sql file with insert the data specified in the .csv file
    into the given table it also adds three(3) comment lines in the beginning of the .sql file
    :param path: this is the path of the .csv file to be converted
    :param table: this is the name of the table in which is to be inserted
    :return: this function returns 1 on a success
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    oldfile = open(path, 'r')
    newfilename = filename[:filename.rfind('.')] + '.sql'
    newfile = open(oldfile, 'w')
    newfile.write("# Messwerttabelle %s\n", table)
    newfile.write("#\n")
    content = oldfile.readlines()
    newfile.write("# %s\n", content[0])
    content[1:]
    for line in content:
        line.replace(",", "','")
        newfile.write("INSERT INTO %s VALUES('%s');\n", table, line)
    newfile.close()
    oldfile.close()
    return 1


def csv_to_npy(path):
    """
    **Convert a single .csv file into a .npy file**
    This function creates a new .npy file with the data of the .csv file
    this .npy file has the same location and name as the .csv file
    :param path: the path of the file that is to be converted
    :return: creates a new .npy file
    """
    os.chdir(path + '/../')
    filename = ntpath.basename(path)
    newfilename = filename[:filename.rfind('.')] + '.npy'
    data = np.genfromtxt(path, delimeter=',',
                         missing_values=np.NaN, names=True)
    newfilename.save(data)


def npy_to_sql(path, table):  # TODO idee erst zu csv dann zu sql
    os.chdir(path + '/../')
    oldfile = np.load(path, 'r')
    filename = ntpath.basename(path)
    newfilename = filename[:filename.rfind('.')] + '.sql'
    newfile = open(newfilename, 'w')
    newfile.write("# Messwerttabelle %s\n", table)
    newfile.write("#\n")
    newfile.close()

#hello
def npy_to_csv(path):
    """
    **Convert a single .npy file into a .csv file**
    this function creates a new .csv file from the given .npy file
    and saves it at the same location with the same name as the .npy file
    :param path: the path of the .npy file
    :return: this Method returns 1 on success
    """
    os.chdir(path + '/../')
    np_array = np.load(path, 'r')
    filename = ntpath.basename(path)
    #frame = pd.DataFrame(data=oldfile[1:,1:],index=data[1:,0],cloumns=data[0,1:])
    # frame.to_csv(path[:path.rfind('.')]+'.csv',index=False,header=True)
    pd.Dataframe(np_array).to_csv(
        filename[:filename.rfind('.')] + '.csv', index=False, header=True)
    return 1  # this is for testing purposes

    def switchoption(n,path):
        switcher = {
        1: zip_to_csv(path),
        2: zip_to_npy(path),
        3: sql_to_csv(path),
        4: sql_to_npy(path),
        5: csv_to_sql(path),
        6: csv_to_npy(path),
        }
        return switcher.get(n," is an invalid option")

def main():
        path = input("enter path:\n")
        print"zip_to_csv(1)\n"
        print"zip_to_npy(2) \n"
        print"sql_to_csv(3) \n"
        print"sql_to_npy(4) \n"
        print"csv_to_sql(5) \n"
        print"csv_to_npy(6) \n"
        choose = input("what do you want to do:")

if __name__ == "__main___":
    main()
else:
    main()# why doesn't it go into main???
