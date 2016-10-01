#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;
import random;


"""START OF FUNCTIONS"""

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Load all Cayley tables
tbls = CayleyTable.readAllTables(filename, order);

tableNum = 0;
groupSet = tbls[0].symbols;

for tbl in tbls:

    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, y) in product(groupSet, repeat=4):
        
        # Verify clauses 1 - 2
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        bS  = tbl.rightMultiplyBySet(b)
        bSy = tbl.leftMultiplyByPartialSet(y, bS)
        yS  = tbl.rightMultiplyBySet(y)
        ySc = tbl.leftMultiplyByPartialSet(c, yS)

        clause1 = y in bSy.intersection(ySc);
        clause2 = yab == b and cay == c;

        if not (clause1 and clause2):
            continue;

        hFound = False;
        for h in groupSet:
            bhy = tbl.simplifyTerm(b + h + y)
            hya = tbl.simplifyTerm(h + y + a)

            if bhy == y and  hya == h:
                hFound = True;
                break;
        
        if not hFound:
            # Set up results printer
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("c", c);
            results.addToResults("y", y);
            results.printAll();


"""END OF SCRIPT"""
