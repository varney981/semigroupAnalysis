#!/usr/bin/python

import sys;
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

# Load all Cayley tables
tbls = CayleyTable.readAllTables(filename, order);

# Run tests on each Cayley table for each permutation of the group set
groupSet = tbls[0].symbols;
tableNum = 0;
for tbl in tbls:
    tableNum += 1;
    for (a, b, h, y) in product(groupSet, repeat=4):
        # Confirm each necessary inverse
        bhy = tbl.simplifyTerm(b + h + y);
        yhb = tbl.simplifyTerm(y + h + b);
        if bhy != y or yhb != y:
            continue;

        yab = tbl.simplifyTerm(y + a + b);
        bay = tbl.simplifyTerm(b + a + y);
        if yab != b or bay != b:
            continue;

        ayh = tbl.simplifyTerm(a + y + h);
        hya = tbl.simplifyTerm(h + y + a);
        if ayh != h or hya != hya:
            continue;

        # Check conclusion
        ah = tbl.simplifyTerm(a + h);
        ha = tbl.simplifyTerm(h + a);
        by = tbl.simplifyTerm(b + y);
        yb = tbl.simplifyTerm(y + b);
        if by != yb:
            if ah == ha:
                print "LOLOLOL not implying";
            print "S# " + str(tableNum) + ":";
            tbl.printTable();
            print "a = " + a + ", b = " + b + ", h = " + h + ", y = " + y;
            print "ah = " + ah;
            print "ha = " + ha;
            print "by = " + by;
            print "yb = " + yb;
            print;
            print;
        
        """
        # Confirm each condition, quit if any are unsatisfied
        cab = tbl.simplifyTerm(c + a + b);
        if len(tbl.findLeftMultipleInSetProduct(b, cab)) == 0:
            continue;

        if len(tbl.findRightMultipleInSetProduct(c, cab)) > 0:
            continue;

        Sc = tbl.leftMultiplyBySet(c);
        failed = False;
        for x in Sc:
            xab = tbl.simplifyTerm(x + a + b);
            xax = tbl.simplifyTerm(x + a + x);
            if xab == b and not xax == x:
                failed = True;
        if failed:
            continue;

        tbl.printTable();
        print "(a, b, c) = (" + a + ", " + b + ", " + c + ")";
        xv_list = "(x, v) = ";
        for x in Sc:
            for v in groupSet:
                if x == tbl.simplifyTerm(v + c):
                    xv_list = xv_list + "(" + x + ", " + v + ") or ";
                    break;
        xv_list = xv_list[0: len(xv_list) - 3];
        print xv_list;
        print;
        print;
        """
        
"""END OF SCRIPT"""
