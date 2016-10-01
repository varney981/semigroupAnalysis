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
    for (a, b, c, h, y) in product(groupSet, repeat=5):
        
        # Verify clauses 1 - 2
        bhy = tbl.simplifyTerm(b + h + y);
        yhc = tbl.simplifyTerm(y + h + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayh = tbl.simplifyTerm(a + y + h);

        clause1 = bhy == y and y == yhc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayh == h;

        if not (clause1 and clause2 and clause3):
            continue;

        # Search for a disqualifing g term
        gFound = False;
        aya = tbl.simplifyTerm(a + y + a);
        for g in groupSet:
            ygc = tbl.simplifyTerm(y + g + c);
            ayg = tbl.simplifyTerm(a + y + g);
            acg = tbl.simplifyTerm(a + c + g);
            if ygc == y and ayg == g and aya == acg:
                gFound = True;
                break;
            
        if gFound:
            continue;

        # Set up results printer
        results = ResultPrinter(tableNum, tbl)
        results.addToResults("a", a);
        results.addToResults("b", b);
        results.addToResults("c", c);
        results.addToResults("h", h);
        results.addToResults("y", y);
        results.addToResults("aya", aya);
        results.printAll();


"""END OF SCRIPT"""
