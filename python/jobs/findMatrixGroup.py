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
job = args.special
if not ("6.2" in job or "6.3" in job):
    raise ValueError("Select a job number")

tableNum = 0
allRegular = True
for table in tables:
    tableNum += 1
    for (a,b,c,y) in util.orderProduct(table, 4):
        #test for * condition (b = c)
        if '_star' in job and b != c:
            continue

        #determine job number
        if "6.2" in job and not table.isAnnihilator(y=y,a=a,b=b,c=c):
            continue
        elif "6.3" in job and not table.isHybrid(y=y,a=a,b=b,c=c):
            continue

        #test if cab in cabScab
        cab = table.multiply([c,a,b])
        cabScab = table.xSy(x=cab,y=cab)
        if not cab in cabScab:
            allRegular = False
            results = rp.ResultPrinter(tableNum, table)
            results.addToResults('a',a)
            results.addToResults('b',b)
            results.addToResults('c',c)
            results.addToResults('y',y)
            results.addToResults('cab',cab)
            results.addToResults('cabScab',cabScab)
            with open(filename, 'a') as fh:
                results.printAll(fh)

if "6.2" in job and allRegular:
    with open(filename, 'a') as fh:
        op_fix = "_op" if args.transpose else ''
        fh.write("For all S" + op_fix + " tested, (3), (4), (5) imply that cab is regular.")

if "6.3" in job and allRegular:
    with open(filename, 'a') as fh:
        op_fix = "_op" if args.transpose else ''
        fh.write("For all S" + op_fix + " tested, (3), (6), (5) imply that cab is regular.")
            

###END OF SCRIPT

