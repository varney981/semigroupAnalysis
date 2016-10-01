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

print "-----------PART 1-----------"
for tbl in tbls:

    """ PART: 1 """
    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, g, h, y) in product(groupSet, repeat=6):
        
        # Verify clauses 1 - 3
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;

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


print "-----------PART 2-----------"
tableNum = 0;
for tbl in tbls:

    """ PART: 2 """
    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, g, h, y) in product(groupSet, repeat=6):
        
        # Verify clauses 1 - 3
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;

        if not (clause1 and clause2 and clause3):
            continue;

        pFound = False;
        ya = tbl.simplifyTerm(y + a)
        ay = tbl.simplifyTerm(a + y)
        for p in groupSet:
            bp = tbl.simplifyTerm(b + p)
            pb = tbl.simplifyTerm(p + b)

            if bp == ya and pb == ay:
                pFound = True;
                break;
        
        if not pFound:
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


print "-----------PART 3-----------"
tableNum = 0;
for tbl in tbls:

    """ PART: 3 """
    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, c, g, h, y) in product(groupSet, repeat=5):
        b = c;
        
        # Verify clauses 1 - 3
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;

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


print "-----------PART 4-----------"
tableNum = 0;
for tbl in tbls:

    """ PART: 4 """
    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, c, g, h, y) in product(groupSet, repeat=5):
        b = c;
        
        # Verify clauses 1 - 3
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;

        if not (clause1 and clause2 and clause3):
            continue;

        pFound = False;
        ya = tbl.simplifyTerm(y + a)
        ay = tbl.simplifyTerm(a + y)
        for p in groupSet:
            bp = tbl.simplifyTerm(b + p)
            pb = tbl.simplifyTerm(p + b)

            if bp == ya and pb == ay:
                pFound = True;
                break;
        
        if not pFound:
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
