#!/usr/bin/python

from tools import util
from tools import CayleyTable as ct
from tools import ResultPrinter as rp

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

#run designated job
job = args.special
tableNum = -1
for table in tables:
    tableNum += 1
    for (a,b,c,y) in util.orderProduct(table, 4):
        #(1)
        if not y in table.xSy(b,y).intersection(table.xSy(y,c)):
            continue

        #(2)
        yab = table.multiply([y,a,b])
        cay = table.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        for d in range(table.order):
            if job == 'omit3':
                #(4),(5)
                db = table.multiply([d,b])
                bd = table.multiply([b,d])
                dc = table.multiply([d,c])
                cd = table.multiply([c,d])
                if not (db == bd and dc == cd):
                    continue

                #test the conclusion: yd = dy
                yd = table.multiply([y,d])
                dy = table.multiply([d,y])
                if yd != dy:
                    results = rp.ResultPrinter(tableNum, table)
                    results.addToResults('a', a)
                    results.addToResults('b', b)
                    results.addToResults('c', c)
                    results.addToResults('y', y)
                    results.addToResults('d', d)
                    results.addToResults('db = bd', db)
                    results.addToResults('dc = cd', cd)
                    results.addToResults('yd', yd)
                    results.addToResults('dy', dy)
                    with open(filename, 'a') as fh:
                        results.printAll(fh)
                    

            if job == 'omit4':
                #(3),(5)
                da = table.multiply([d,a])
                ad = table.multiply([a,d])
                dc = table.multiply([d,c])
                cd = table.multiply([c,d])
                if not (da == ad and dc == cd):
                    continue

                #test the conclusion: yd = dy
                yd = table.multiply([y,d])
                dy = table.multiply([d,y])
                if yd != dy:
                    results = rp.ResultPrinter(tableNum, table)
                    results.addToResults('a', a)
                    results.addToResults('b', b)
                    results.addToResults('c', c)
                    results.addToResults('y', y)
                    results.addToResults('d', d)
                    results.addToResults('da = ad', da)
                    results.addToResults('dc = cd', cd)
                    results.addToResults('yd', yd)
                    results.addToResults('dy', dy)
                    with open(filename, 'a') as fh:
                        results.printAll(fh)
                    
###END OF SCRIPT

