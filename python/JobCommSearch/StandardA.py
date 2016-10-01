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
    for (a, b, c, g, h, y, p, q) in product(groupSet, repeat=8):
        
        # Verify clauses 1 - 2
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);
        bp  = tbl.simplifyTerm(b + p);
        ya  = tbl.simplifyTerm(y + a);
        cq  = tbl.simplifyTerm(c + q);
        pb  = tbl.simplifyTerm(p + b);
        ay  = tbl.simplifyTerm(a + y);
        qc  = tbl.simplifyTerm(q + c);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g and bp == ya and ya == cq and pb == ay and ay == qc;
        clause4 = g != h

        if not (clause1 and clause2 and clause3 and clause4):
            continue;
            
        # Set up results printer
        results = ResultPrinter(tableNum, tbl)
        results.addToResults("a", a);
        results.addToResults("b", b);
        results.addToResults("c", c);
        results.addToResults("g", g);
        results.addToResults("h", h);
        results.addToResults("y", y);
        results.addToResults("p", p);
        results.addToResults("q", q);
        results.printAll();


"""END OF SCRIPT"""
