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

print args.special
print filename


#run designated job
job = args.special  #partA or partB
if not job in ["partA", "partB"]:
    raise ValueError("Not valid job in --special")
tableNum = -1
for table in tables:
    tableNum += 1
    for (a,b,c,y) in util.orderProduct(table,4):
        #(1)
        if not y in table.xSy(b,y).intersection(table.xSy(y,c)):
            continue

        #(2)
        yab = table.multiply([y,a,b])
        cay = table.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        #(*)
        if job == 'partA':
            ya = table.multiply([y,a])
            ay = table.multiply([a,y])
            ba = table.multiply([b,a])
            ca = table.multiply([c,a])
            ab = table.multiply([a,b])
            ac = table.multiply([a,c])
        if job == 'partA' and not ya in table.comm_2(ba).intersection(table.comm_2(ca)):
            continue
        if job == 'partA' and not ay in table.comm_2(ab).intersection(table.comm_2(ac)):
            continue

        #(**)
        if job == 'partB' and not y in table.comm_2(a):
            continue
        
        gh_exist = False
        aya = table.multiply([a,y,a])
        for (g,h) in util.orderProduct(table,2):
            bhy = table.multiply([b,h,y])
            ygc = table.multiply([y,g,c])
            hya = table.multiply([h,y,a])
            ayg = table.multiply([a,y,g])
            hba = table.multiply([h,b,a])
            acg = table.multiply([a,c,g])
            #(1*)
            if not (bhy == y and y == ygc):
                continue
            #(3)
            if not (hya == h and ayg == g):
                continue
            #(4)
            if not (hba == aya and aya == acg):
                continue
            
            gh_exist = True
            break

        if job == "partA" and not gh_exist:
            results = rp.ResultPrinter(tableNum, table)
            results.addToResults('a', a)
            results.addToResults('b', b)
            results.addToResults('c', c)
            results.addToResults('y', y)
            results.addToResults('ya', ya)
            results.addToResults('ba', ba)
            results.addToResults('ca', ca)
            results.addToResults('comm_1(ba)', table.comm_1(ba))
            results.addToResults('comm_2(ba)', table.comm_2(ba))
            results.addToResults('comm_1(ca)', table.comm_1(ca))
            results.addToResults('comm_2(ca)', table.comm_2(ca))
            results.addToResults('ay', ay)
            results.addToResults('ab', ab)
            results.addToResults('ac', ac)
            results.addToResults('comm_1(ab)', table.comm_1(ab))
            results.addToResults('comm_2(ab)', table.comm_2(ab))
            results.addToResults('comm_1(ac)', table.comm_1(ac))
            results.addToResults('comm_2(ac)', table.comm_2(ac))
            with open(filename, 'a') as fh:
                results.printAll(fh)
        if job == "partB" and not gh_exist:
            results = rp.ResultPrinter(tableNum, table)
            results.addToResults('a', a)
            results.addToResults('b', b)
            results.addToResults('c', c)
            results.addToResults('y', y)
            results.addToResults('comm_1(a)', table.comm_1(a))
            results.addToResults('comm_2(a)', table.comm_2(a))
            with open(filename, 'a') as fh:
                results.printAll(fh)
            



                
###END OF SCRIPT

