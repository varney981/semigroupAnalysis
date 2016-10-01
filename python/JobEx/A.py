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
    for (a, b, y) in product(groupSet, repeat=3):
        
        # Verify clauses 1 - 2
        yab = tbl.simplifyTerm(y + a + b);
        bay = tbl.simplifyTerm(b + a + y);
        bS  = tbl.rightMultiplyBySet(b)
        bSy = tbl.leftMultiplyByPartialSet(y, bS)
        yS  = tbl.rightMultiplyBySet(y)
        ySb = tbl.leftMultiplyByPartialSet(b, yS)
        ay  = tbl.simplifyTerm(a + y);
        ya  = tbl.simplifyTerm(y + a);
        aya = tbl.simplifyTerm(a + y + a);

        clause1 = y in bSy.union(ySb);
        clause2 = yab == b and bay == b and ay != ya and aya != a;

        if not (clause1 and clause2):
            continue;

        eFound = False;
        for e in groupSet:
            ee = tbl.simplifyTerm(e + e)
            ye = tbl.simplifyTerm(y + e)
            ey = tbl.simplifyTerm(e + y)
            yae = tbl.simplifyTerm(y + a + e)
            eay = tbl.simplifyTerm(e + a + y)

            if e == ee and  ye == y and y == ey and yae == e and e == eay:
                eFound = True;
                break;
        
        if not eFound:
            # Set up results printer
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("y", y);
            results.addToResults("ay", ay);
            results.addToResults("ya", ya);
            results.addToResults("aya", aya);
            results.addToTable("y = yab", y == yab);
            results.addToTable("yab = b", yab == b);
            results.printAll();


"""END OF SCRIPT"""
