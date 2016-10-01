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
    for (a, e, f, y) in product(groupSet, repeat=4):
        #Randomly select to do this or not
        if random.random() < 0.99:
            continue;

        # Set up result reporter for this tuple
        results = ResultPrinter(tableNum, tbl);
        results.addToResults('(a, e, f, y)', (a,e,f,y));

        # Abort quadruple if clause (0) is not true
        e2 = tbl.simplifyTerm(e+e);
        f2 = tbl.simplifyTerm(f+f);
        results.addToResults('e2', e2);
        results.addToResults('f2', f2);
        results.addToTable('e == e2', e == e2);
        results.addToTable('f == f2', f == f2);
        if not (e == e2 and f == f2):
            results.printAll();
            continue;

        # Abort quadruple if clause (1) is not true
        ey = tbl.simplifyTerm(e+y);
        yf = tbl.simplifyTerm(y+f);
        results.addToResults('ey', ey);
        results.addToResults('yf', yf);
        results.addToTable('ey == y', ey == y);
        results.addToTable('y == yf', y == yf);
        if not (ey == y and y == yf):
            results.printAll();
            continue;

        # Abort quadruple if clause (2) is not true
        yae = tbl.simplifyTerm(y+a+e);
        fay = tbl.simplifyTerm(f+a+y);
        results.addToResults('yae', yae);
        results.addToResults('fay', fay);
        results.addToTable('yae == e', yae == e);
        results.addToTable('fay == f', fay == f);
        if not (yae == e and fay == f):
            results.printAll();
            continue;

        # Search for a pair (g,h) in S such that:
        # ehy = y = ygf
        # hya = h
        # ayg = g
        # Abort quadruple if such a pair is found
        #print tableNum;
        #print '(' + a + ', ' + e + ', ' + f + ', ' + y + ')';
        pairFound = 0;
        for (g, h) in product(groupSet, repeat=2):
            ehy = tbl.simplifyTerm(e+h+y);
            hya = tbl.simplifyTerm(h+y+a);
            ayg = tbl.simplifyTerm(a+y+g);
            ygf = tbl.simplifyTerm(y+g+f);
            if ehy == y and y == ygf and hya == h and ayg == g:
                pairFound += 1;
        
        if pairFound > 0:
            continue;

        # If the quadruple has satisfied necessary conditions, print results
        ya = tbl.simplifyTerm(y+a);
        ay = tbl.simplifyTerm(a+y);
        results.addToResults("ya", ya);
        results.addToResults("ay", ay);
        results.printAll;
"""END OF SCRIPT"""
