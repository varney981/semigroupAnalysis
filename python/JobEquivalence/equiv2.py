#!/usr/bin/python

import sys;
import random;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;


"""START OF FUNCTIONS"""

def getL_EquivalentPairs(tbl):
    result = set();
    return result;

def getR_EquivalentPairs(tbl):
    result = set();
    return result;

def getD_EquivalentPairs(tbl):
    result = set();
    return result;

def getD_EquivalentPairsWithLink(tbl):
    result = set();
    return result;


"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# If a range was passed, read tables for this range
if len(sys.argv) >= 5:
    #if random.random() > 0.01:
    #    sys.exit();
    tableNum  = int(sys.argv[3]);
    lastTable = int(sys.argv[4]);
    tbls = CayleyTable.readRangeOfTables(filename,order,
                                         tableNum, lastTable);
else:  #Load all tables
    tableNum = 0;
    tbls = CayleyTable.readAllTables(filename, order);

for tbl in tbls:
    # Increment the table counter
    tableNum += 1;

    # Obtain D triplets
    D_equivTrips = getD_EquivalentPairsWithLink(tbl);
    
    for (b, g, c) in D_equivTrips:
        rsFound = False;
        rsPairs = set()
        for (r,s) in product(tbl.symbols, repeat=2):
            rs = tbl.simplifyTerm(r+s);
            sr = tbl.simplifyTerm(s+r);
            if (b == rs and c == sr):
                rsFound = True;
                break;

        if not rsFound:
           results = ResultPrinter(tableNum, tbl);
           results.addToResults('b', b);
           results.addToResults('c', c);
           results.addToResults('g', g);
           results.printResults();
    
"""END OF SCRIPT"""
