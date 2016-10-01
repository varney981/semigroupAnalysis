#!/usr/bin/python

import sys;
import random;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;


"""START OF FUNCTIONS"""

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Generate all possible truth table combinations
remainingCombos = set();
for (t1, t2, t3, t4, t5, t6) in product(set([True, False]), repeat=6):
    remainingCombos.add((t1,t2,t3,t4,t5,t6));

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

    # Try each (a, b, c, y) tuple in S
    for (a, b, c, g, y) in product(tbl.symbols, repeat=5):
        
        # Identify initial clauses
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        ayg = tbl.simplifyTerm(a + y + g);
        aya = tbl.simplifyTerm(a + y + a);
        acg = tbl.simplifyTerm(a + c + g);

        if not (ygc == y and yab == b and cay == c and ayg == g and aya == acg):
            continue;

        # Identify all h in S meeting specified conditions
        h_list = [];
        for h in tbl.symbols:
            bhy = tbl.simplifyTerm(b + h + y);
            hya = tbl.simplifyTerm(h + y + a);
            hba = tbl.simplifyTerm(h + b + a);

            if y == bhy and hya == h and hba == aya:
                h_list.append(h);
        
        if len(h_list) > 1:
            out = ResultPrinter(tableNum, tbl);
            out.addToResults('a', a);
            out.addToResults('b', b);
            out.addToResults('c', c);
            out.addToResults('g', g);
            out.addToResults('y', y);

            # Add h variables to the results and y multiple
            for i in range(1, len(h_list) + 1):
                h_i = h_list[i - 1];
                h_iy = tbl.simplifyTerm(h_i + y);
                out.addToResults('h' + str(i), h_i);
                #out.addToResults('(h' + str(i) + ')y', h_iy);
            
            out.printAll();


"""END OF SCRIPT"""
