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

#run test
tableNum = 0
for table in tables:
    tableNum += 1
    for (a,b,c,y) in util.orderProduct(table, 4):
        #test (2)
        yab = table.multiply([y,a,b])
        cay = table.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        #test (1)
        gh_found = False
        for (g,h) in util.orderProduct(table, 2):
            bhy = table.multiply([b,h,y])
            ygc = table.multiply([y,g,c])
            if bhy == ygc and ygc == y:
                gh_found = True
                true_g = g
                true_h = h
                break
        if not gh_found:
            continue
        g = true_g
        h = true_h

        #find all w that satisfy (*)
        w_set = set()
        for w in range(table.order):
            cabw = table.multiply([c,a,b,w])
            if cabw == c:
                w_set.add(w)
        
        #test way = y for all found w
        for w in w_set:
            way = table.multiply([w,a,y])
            if way != y:
                cab = table.multiply([c,a,b])
                results = rp.ResultPrinter(tableNum, table)
                results.addToResults('a',a)
                results.addToResults('b',b)
                results.addToResults('c',c)
                results.addToResults('y',y)
                results.addToResults('g',g)
                results.addToResults('h',h)
                results.addToResults('cab',cab)
                results.addToResults('w',w)
                results.addToResults('way',way)
                with open(filename, 'a') as fh:
                    fh.write('way = y is false for \n')
                    results.printAll(fh)
###END OF SCRIPT

