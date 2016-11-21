#!/usr/bin/python

from tools import util
from tools import CayleyTable as ct
from tools import ResultPrinter as rp

###START OF FUNCTIONS

###END OF FUNCTIONS


###START OF SCRIPT

#get order of tables
order = int(raw_input("What order semigroups do you want to test? >>"))

#ask to transpose tables
isTransposed = False
transpose_postfix = ''
transpose = raw_input("Do you want to transpose the tables? ([Y]/[n]) >> ")
if transpose == 'Y' or transpose == 'y':
    transpose_postfix = '_S_op'
    isTransposed = True
    
#create tables using selected mode
mode = raw_input("Which tables to test?([]All/[R]ange/[S]ingle) >> ")
if mode == 'S' or mode == 's':
    tables = util.readSingleTable(args.order, args.singleNum, isTransposed)
elif mode == 'R' or mode == 'r':
    first_table = raw_input("First table number? >> ")
    last_table = raw_input("Last table number? >> ")
    tables = util.readRangeOfTables(args.order, first_table, last_table, isTransposed)
else:
    tables = util.readAllTables(order, isTransposed)

#set special arguments here


#generate output file and (if necessary) a filename
filename = raw_input("Please enter specific file name, or leave blank for generated name >> "
if filename == '':
    filename = "results/" + __file__[0:-3] + "_order" + str(args.order) + "_" + special_str
    filename += transpose_postfix
    filename += '.txt'
with open(filename, 'w') as fh:
    pass

#begin testing


###END OF SCRIPT

