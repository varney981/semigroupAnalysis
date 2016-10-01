#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;
import random;


"""START OF FUNCTIONS"""

def setAsString(writeSet):
    setStr   = '{';
    sliceEnd = -1;
    for elem in writeSet:
        setStr = setStr + elem + ', ';
        sliceEnd += 3;
    setStr = setStr[0:sliceEnd];
    setStr = setStr + '}';
    return setStr;

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = '../tables/order4.csv';
order = 4;

tableNum = 0;
tbls = CayleyTable.readAllTables(filename, order);

tableNum   = 0;
groupSet   = tbls[0].symbols;
charSet    = set();
charSet.add('a'); charSet.add('b');charSet.add('c');charSet.add('g');charSet.add('h');charSet.add('y');
eliminated   = set();
possible = set();
fullSet    = set();

for char1 in charSet:
    fullSet.add(char1);


for char1 in charSet:
    for char2 in charSet:
        fullSet.add(char1 + char2);

for char1 in charSet:
    for char2 in charSet:
        for char3 in charSet:
            fullSet.add(char1 + char2 + char3);
    
for char1 in charSet:
    for char2 in charSet:
      for char3 in charSet:
          for char4 in charSet:
              fullSet.add(char1 + char2 + char3 + char4);

possible = fullSet.copy();
for tbl in tbls:

    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, g, h, y) in product(groupSet, repeat=6):
        # Verify clauses 1 - 2
        ba  = tbl.simplifyTerm(b + a);
        ab  = tbl.simplifyTerm(a + b);
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);
        bay = tbl.simplifyTerm(b + a + y);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;
        clause4 = bay == b;

        if not (clause1 and clause2 and clause3 and clause4):
            continue;
            
        # Create a dictionary for use below
        termValues = {'a' : a, 'b' : b, 'c' : c, 'g' : g, 'h' : h, 'y' : y};
        oldNumEliminated = len(eliminated);

        for m in fullSet:

            mEval = [];
            for mTerm in m:
                mEval.append(termValues[mTerm]);

            mEval = ''.join(mEval);
            mEval = tbl.simplifyTerm(mEval);
            mba   = tbl.simplifyTerm(mEval + ba);
            bam   = tbl.simplifyTerm(ba + mEval);

            if mba != bam:
               eliminated.add(m);

        '''
        if len(eliminated) != oldNumEliminated:
            possible = (fullSet.difference(eliminated)).copy();
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("c", c);
            results.addToResults("g", g);
            results.addToResults("h", h);
            results.addToResults("y", y);
            results.addToResults("Remaining monom.", possible);
            results.printAll();
        '''

# Exchange full set with possible set
printList = sorted(list(fullSet.difference(eliminated)));

# print printList;
fullSet = (fullSet.difference(eliminated)).copy();
printList = sorted(list(fullSet));
print 'n = 4 list';
print printList;

eliminated = set()

# Get file name and order from input
filename = '../tables/order5.csv';
order = 5;
tableNum = 0;
tbls = CayleyTable.readAllTables(filename, order);
groupSet   = tbls[0].symbols;

for tbl in tbls:

    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, g, h, y) in product(groupSet, repeat=6):
        # Verify clauses 1 - 2
        ba  = tbl.simplifyTerm(b + a);
        ab  = tbl.simplifyTerm(a + b);
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);
        bay = tbl.simplifyTerm(b + a + y);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;
        clause4 = bay == b;

        if not (clause1 and clause2 and clause3 and clause4):
            continue;
            
        # Create a dictionary for use below
        termValues = {'a' : a, 'b' : b, 'c' : c, 'g' : g, 'h' : h, 'y' : y};
        oldNumEliminated = len(eliminated);

        for m in fullSet:

            mEval = [];
            for mTerm in m:
                mEval.append(termValues[mTerm]);

            mEval = ''.join(mEval);
            mEval = tbl.simplifyTerm(mEval);
            mba   = tbl.simplifyTerm(mEval + ba);
            bam   = tbl.simplifyTerm(ba + mEval);

            if mba != bam:
               eliminated.add(m);

        '''
        if len(eliminated) != oldNumEliminated:
            possible = (fullSet.difference(eliminated)).copy();
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("c", c);
            results.addToResults("g", g);
            results.addToResults("h", h);
            results.addToResults("y", y);
            results.addToResults("Remaining monom.", possible);
            results.printAll();
        '''

# print printList;
fullSet = (fullSet.difference(eliminated)).copy();
printList = sorted(list(fullSet));
print 'n = 5 list';
print printList;

eliminated = set()

# Get file name and order from input
filename = '../tables/order6.csv';
order = 6;
tableNum = 0;
tbls = CayleyTable.readAllTables(filename, order);
groupSet   = tbls[0].symbols;

for tbl in tbls:
    
    #print str(tableNum) + ' out of ' + str(len(tbls));

    # Increment the table counter
    tableNum += 1;

    # Run test for all quadruples in S
    for (a, b, c, g, h, y) in product(groupSet, repeat=6):
        # Verify clauses 1 - 2
        ba  = tbl.simplifyTerm(b + a);
        ab  = tbl.simplifyTerm(a + b);
        bhy = tbl.simplifyTerm(b + h + y);
        ygc = tbl.simplifyTerm(y + g + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayg = tbl.simplifyTerm(a + y + g);
        bay = tbl.simplifyTerm(b + a + y);

        clause1 = bhy == y and y == ygc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and ayg == g;
        clause4 = bay == b;

        if not (clause1 and clause2 and clause3 and clause4):
            continue;
            
        # Create a dictionary for use below
        termValues = {'a' : a, 'b' : b, 'c' : c, 'g' : g, 'h' : h, 'y' : y};
        oldNumEliminated = len(eliminated);

        for m in fullSet:

            mEval = [];
            for mTerm in m:
                mEval.append(termValues[mTerm]);

            mEval = ''.join(mEval);
            mEval = tbl.simplifyTerm(mEval);
            mba   = tbl.simplifyTerm(mEval + ba);
            bam   = tbl.simplifyTerm(ba + mEval);

            if mba != bam:
               eliminated.add(m);

        '''
        if len(eliminated) != oldNumEliminated:
            possible = (fullSet.difference(eliminated)).copy();
            results = ResultPrinter(tableNum, tbl)
            results.addToResults("a", a);
            results.addToResults("b", b);
            results.addToResults("c", c);
            results.addToResults("g", g);
            results.addToResults("h", h);
            results.addToResults("y", y);
            results.addToResults("Remaining monom.", possible);
            results.printAll();
        '''
printList = sorted(list(fullSet.difference(eliminated)));
print 'n = 6:'
print printList;

"""END OF SCRIPT"""
