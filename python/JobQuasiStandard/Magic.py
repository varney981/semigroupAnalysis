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
        abh = tbl.simplifyTerm(a + b + h);
        hba = tbl.simplifyTerm(h + b + a);
        aya = tbl.simplifyTerm(a + y + a);
        ach = tbl.simplifyTerm(a + c + h);
        hca = tbl.simplifyTerm(h + c + a);

        clause1 = bhy == y and y == yhc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayh == h;
        clause4 = abh == hba and hba == aya and aya == ach and ach == hca;

        if not (clause1 and clause2 and clause3 and clause4):
            continue;

        # Search for a disqualifing q term
        qFound = False;
        ya = tbl.simplifyTerm(y + a);
        ay = tbl.simplifyTerm(a + y);
        for q in groupSet:
            cq = tbl.simplifyTerm(c + q);
            qc = tbl.simplifyTerm(q + c);
            if ya == cq and ay == qc:
                qFound = True;
                break;
            
        if qFound:
            continue;

        # Set up results printer
        results = ResultPrinter(tableNum, tbl)
        results.addToResults("a", a);
        results.addToResults("b", b);
        results.addToResults("c", c);
        results.addToResults("h", h);
        results.addToResults("y", y);
        results.printAll();


"""END OF SCRIPT"""
