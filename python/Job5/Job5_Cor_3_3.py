#!/usr/bin/python

import sys;
import CayleyTable;
from itertools import product as cartProduct;

# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Load all Caylay tables
tbls = CayleyTable.readAllTables(filename, order);

# Run tests on each Cayley table for each permutation of the group set
groupSet = tbls[0].symbols;
#TODO: SET UP OUTPUT FILE
tableNum = 0;
count = 0;
total = 0;
for tbl in tbls:
    tableNum += 1;
    for (a, b, c) in cartProduct(groupSet, repeat=3):
        ab = tbl.simplifyTerm(a + b);
        ba = tbl.simplifyTerm(b + a);
        ac = tbl.simplifyTerm(a + c);
        ca = tbl.simplifyTerm(c + a);
        b_Scab = tbl.findLeftMultipleInSetProduct(b, c+a+b);  #empty if not true
        c_cabS = tbl.findRightMultipleInSetProduct(c, c+a+b); #empty if not true
        if len(b_Scab) > 0 and len(c_cabS) > 0 and ab == ba and ac == ca:
            for (v, w) in cartProduct(b_Scab, c_cabS):
                vca = tbl.simplifyTerm(v + c + a);
                abw = tbl.simplifyTerm(a + b + w);
                if vca != abw:
                    print tableNum;
                    tbl.printTable();
                    print '(a = ' + a + ', b = ' + b + ', c = ' + c + ')';
                    print;
