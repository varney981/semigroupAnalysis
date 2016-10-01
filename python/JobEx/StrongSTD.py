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
    for (a, b, y) in product(groupSet, repeat=6):
        
        # Verify clauses 1 - 2
        yab = tbl.simplifyTerm(y + a + b);
        bay = tbl.simplifyTerm(b + a + y);
        bS  = tbl.rightMultiplyBySet(b)
        bSy = tbl.leftMultiplyByPartialSet(y, bS)
        yS  = tbl.rightMultiplyBySet(y)
        ySb = tbl.leftMultiplyByPartialSet(b, yS)
        ay  = tbl.simplifyTerm(a + y);
        ya  = tbl.simpligyTerm(y + a);
        aya = tbl.simplifyTerm(a + y + a);

        clause1 = y in bSy.union(ySb);
        clause2 = yab == b and bay == b and ay != ya and aya != a;

        if not (clause1 and clause2 and clause3):
            continue;

        pqPairFound = False;
        ya = tbl.simplifyTerm(y + a)
        ay = tbl.simplifyTerm(a + y)
        for (p, q) in product(groupSet, repeat=2):
            bp = tbl.simplifyTerm(b + p)
            cq = tbl.simplifyTerm(c + q)
            pb = tbl.simplifyTerm(p + b)
            qc = tbl.simplifyTerm(q + c)

            if bp == ya and ya == cq and pb == ay and ay == qc:
                pqPairFound = True;
                break;
        
        if not pqPairFound:
            # Set up results printer
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("c", c);
            results.addToResults("g", g);
            results.addToResults("h", h);
            results.addToResults("y", y);
            results.addToResults("ya", ya);
            results.addToResults("ay", ay);
            results.printAll();


"""END OF SCRIPT"""
