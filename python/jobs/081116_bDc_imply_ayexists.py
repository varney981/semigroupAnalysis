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
special_str = ''


#generate output file and (if necessary) a filename
filename = raw_input("Please enter specific file name, or leave blank for generated name >> ")
if filename == '':
    filename = "results/" + __file__[0:-3] + "_order" + str(order) + "_" + special_str
    filename += transpose_postfix
    filename += '.txt'
with open(filename, 'w') as fh:
    pass

#begin testing
tableNum = 0
for table in tables:
    tableNum += 1
    for (b,c,d) in util.orderProduct(table,3):
        if table.are_xLy_related(d,c) and table.are_xRy_related(b,d):
            a_found = False
            for a in range(order):
                cab = table.multiply([c,a,b])
                Scab = table.Sy(cab)
                if not b in Scab:
                    continue
                cabS = table.xS(cab)
                if not c in cabS:
                    continue
                a_found = True
                break
            if not a_found:
                results = rp.ResultPrinter(tableNum, table)
                results.addToResults('b',b)
                results.addToResults('c',c)
                for a in range(order):
                    cab = table.multiply([c,a,b])
                    results.addToResults("Sc"+str(a)+"b",table.Sy(cab))
                for a in range(order):
                    cab = table.multiply([c,a,b])
                    results.addToResults("c"+str(a)+"bS",table.xS(cab))
                with open(filename,'w') as fh:
                    results.printAll(fh)



###END OF SCRIPT

