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
    for (a, b, c, y) in product(tbl.symbols, repeat=4):
        
        # Identify initial clauses
        bS = tbl.rightMultiplyBySet(b);
        bSy = tbl.leftMultiplyByPartialSet(y, bS);
        yS = tbl.rightMultiplyBySet(y);
        ySc = tbl.leftMultiplyByPartialSet(c, bS);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);


        reqClause1 = y in bSy.intersection(ySc);
        reqClause2 = yab == b and cay == c;

        if not (reqClause1 and reqClause2):
            continue;

        # Calculate ba values for use in next step
        ba = tbl.simplifyTerm(b + a);
        ba_2 = tbl.simplifyTerm(ba + ba);
        ba_n = ba;

        for multipleNum in range(0, order - 1):
            ba_n = tbl.simplifyTerm(ba + ba_n);
        ba_n1 = tbl.simplifyTerm(ba_n + ba);


        # Identify required z value that meets requirements
        z = 'Z';
        for z_test in tbl.symbols:
            zba = tbl.simplifyTerm(z_test + ba);
            baz = tbl.simplifyTerm(ba + z_test);
            zba_2 = tbl.simplifyTerm(z_test + ba_2);
            ba_n1_z  = tbl.simplifyTerm(ba_n1 + z_test);

            clause1 = zba == baz;
            clause2 = zba_2 == ba;
            clause3 = ba_n1_z == ba_n;

            if clause1 and clause2 and clause3:
                z = z_test;


        # Identify all h in S meeting specified conditions
        h_list = [];
        for h in tbl.symbols:
            bhy = tbl.simplifyTerm(b + h + y);
            hya = tbl.simplifyTerm(h + y + a);

            if not (y == bhy and hya == h):
                continue;

            yh = tbl.simplifyTerm(y + h);
            if not yh == z:
                h_list.append(h);
        
        if len(h_list) > 0:
            out = ResultPrinter(tableNum, tbl);
            out.addToResults('a', a);
            out.addToResults('b', b);
            out.addToResults('c', c);
            out.addToResults('y', y);
            out.addToResults('z', z);

            # Add h variables to the results and y multiple
            for i in range(1, len(h_list) + 1):
                h_i = h_list[i - 1];
                yh_i = tbl.simplifyTerm(y + h_i);
                out.addToResults('y(h' + str(i) + ')', yh_i);
            
            out.printAll();


"""END OF SCRIPT"""
