#!/usr/bin/python

from tools import util
from tools import CayleyTable as ct
from tools import ResultPrinter as rp
from random import sample

###START OF FUNCTIONS

###END OF FUNCTIONS


###START OF SCRIPT

#process arguments
args = util.parseArgs()

#create tables using selected mode
if args.mode == "all":
    tables = util.readAllTables(args.order, args.transpose)
elif args.mode == "range":
    tables = util.readRangeOfTables(args.order, args.first, args.last, args.transpose)
elif args.mode == "single":
    tables = util.readSingleTable(args.order, args.singleNum, args.transpose)
else:
    raise ValueError("Mode selected undefined")

#choose omitted condition
omit = args.special
beqc = False
if "bc" in omit:
    beqc = True

#generate output file and (if necessary) a filename
if args.output == None:
    filename = "results/" + __file__[0:-3] + "_order" + str(args.order) + "_" + args.special
else:
    filename = args.output
if args.transpose:
    filename += '_S_op'
filename += '.txt'
with open(filename, 'w') as fh:
    pass

#begin testing
tableNum = 0
for table in tables:
    tableNum += 1
    for (a,b,c) in util.orderProduct(table, 3):
        if beqc and b != c:
            continue
        y_set = set()
        for y in range(table.order):
            yab = table.multiply([y,a,b])
            cay = table.multiply([c,a,y])
            if '1' in omit and yab == b and cay == c and len(table.hInxSy(h=y,x=b,y=y)) > 0:
                y_set.add(y)
            elif '2' in omit and yab == b and len(table.hInxSy(h=y,x=b,y=y)) > 0 and len(table.hInxSy(h=y,x=y,y=c)) > 0:
                y_set.add(y)
        
        if len(y_set) >= 2 and '1' in omit:
            results = rp.ResultPrinter(tableNum, table)
            results.addToResults('a',a)
            results.addToResults('b',b)
            results.addToResults('c',c)
            y_num = 0
            for y in y_set:
                y_num += 1
                results.addToResults('y'+str(y_num),y)
                results.addToResults('h'+str(y_num),sample(table.hInxSy(h=y,x=b,y=y), 1))
            with open(filename, 'a') as fh:
                results.printAll(fh)
        elif len(y_set) >= 2 and '2' in omit:
            results = rp.ResultPrinter(tableNum, table)
            results.addToResults('a',a)
            results.addToResults('b',b)
            results.addToResults('c',c)
            y_num = 0
            for y in y_set:
                y_num += 1
                results.addToResults('y'+str(y_num),y)
                results.addToResults('h'+str(y_num),sample(table.hInxSy(h=y,x=b,y=y), 1))
                results.addToResults('g'+str(y_num),sample(table.hInxSy(h=y,x=y,y=c), 1))
            with open(filename, 'a') as fh:
                results.printAll(fh)
          

            

            


        
###END OF SCRIPT

