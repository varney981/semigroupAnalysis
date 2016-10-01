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

    """ PART: 1 """

    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, y) in product(groupSet, repeat=4):
        # Verify (1) y in bSy INTERSECT ySc
        bS  = tbl.rightMultiplyBySet(b);
        bSy = tbl.leftMultiplyByPartialSet(y, bS);
        yS  = tbl.rightMultiplyBySet(y);
        ySc = tbl.leftMultiplyByPartialSet(c, yS);
        
        if not (y in bSy.intersection(ySc)):
            continue;

        # Verify (2) yab = b and cay = c
        yab = tbl.simplifyTerm(y+a+b);
        cay = tbl.simplifyTerm(c+a+y);
        if not (yab == b and cay == c):
            continue;
        
        # Search for (g, h) in S such that 
        # bhy = y = ygc and hya = h and ayg = g
        ghPairFound = False;
        for (g, h) in product(groupSet, repeat=2):
            bhy = tbl.simplifyTerm(b+h+y);
            ygc = tbl.simplifyTerm(y+g+c);
            hya = tbl.simplifyTerm(h+y+a);
            ayg = tbl.simplifyTerm(a+y+g);
            if bhy == y and y == ygc and hya == h and ayg == g:
                ghPairFound = True;
                break;
        if ghPairFound:
            continue;

        print "It's happening!"
"""END OF SCRIPT"""
