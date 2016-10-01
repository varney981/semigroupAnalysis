#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
from itertools import product as cartProduct;


"""START OF FUNCTIONS"""
def print_yhya(tableNum, tbl, a, b, h, y, yhya, yh):
    print 'S#: ' + str(tableNum);
    print tbl.printTable();
    print '(a, b, h, y) = (' + a + ', ' + b + ', ' + h + ', ' + y + ')';
    print '(yhya, yh) = (' + yhya + ', ' + yh + ')';

def print_ayhya(tableNum, tbl, a, b, h, y, ayhya):
    print 'S#: ' + str(tableNum);
    print tbl.printTable();
    print '(a, b, h, y) = (' + a + ', ' + b + ', ' + h + ', ' + y + ')';
    print 'ayhya = ' + ayhya;

def print_results(clause1, clause2, alpha, beta):
    print '------------------------------'
    print '   Clause     |     T/F'
    print 'bhy = y = yhb |    ' + str(clause1);
    print 'yab = b = bay |    ' + str(clause2);
    print 'yhya  =/= yh  |    ' + str(alpha);
    print 'ayhya =/= h   |    ' + str(beta);
    print '------------------------------'

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
    for (a, b, h, y) in cartProduct(groupSet, repeat=4):
        bhy = tbl.simplifyTerm(b + h + y);
        yhb = tbl.simplifyTerm(y + h + b);
        yab = tbl.simplifyTerm(y + a + b);
        bay = tbl.simplifyTerm(b + a + y);

        # Check if both clauses of the hypothesis hold
        clause1 = (bhy == y) and (yhb == y);
        clause2 = (yab == b) and (bay == b);
        if not (clause1 and clause2):
            continue;

        # Check the conclusion for contradictions
        yhya  = tbl.simplifyTerm(y + h + y + a);
        yh    = tbl.simplifyTerm(y + h);
        ayhya = tbl.simplifyTerm(a + y + h + y + a);
        if yhya != yh and ayhya != h:
            print_yhya(tableNum, tbl, a, b, h, y, yhya, yh);
            print_results(clause1, clause2, yhya != yh, ayhya != h);
            print;
            print;
        elif ayhya != h and 0:
            print_ayhya(tableNum, tbl, a, b, h, y, ayhya);
            print_results(clause1, clause2, yhya != yh, ayhya != h);
            print;
            print;
"""END OF SCRIPT"""
