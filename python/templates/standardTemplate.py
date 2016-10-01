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
    tables = readAllTables(args.order)
elif args.mode == "range":
    tables = readRangeOfTables(args.order, args.first, args.last)
elif args.mode == "single":
    tables = readSingleTable(args.order, args.singleNum)
else:
    raise ValueError("Mode selected undefined")

#go to work

###END OF SCRIPT

