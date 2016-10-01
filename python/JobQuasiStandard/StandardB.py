#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;
import random;


"""START OF FUNCTIONS"""

def getL_EquivalentPairs(tbl):
    result = set();
    for b in tbl.symbols:
        for c in tbl.symbols:
            Sb = tbl.leftMultiplyBySet(b);
            Sc = tbl.leftMultiplyBySet(c);
            Sb.add(b);
            Sc.add(c);
            if Sb == Sc:
                result.add((b, c));
    return result;

def getR_EquivalentPairs(tbl):
    result = set();
    for b in tbl.symbols:
        for c in tbl.symbols:
            bS = tbl.rightMultiplyBySet(b);
            cS = tbl.rightMultiplyBySet(c);
            bS.add(b);
            cS.add(c);
            if bS == cS:
                result.add((b, c));
    return result;

def generateL_Decomposition(tbl):
    decompList = [];
    result = set();
    bLcPairs = getL_EquivalentPairs(tbl);
    for (b, c) in bLcPairs:
        bS = tbl.rightMultiplyBySet(b);
        bS_asList = list(bS);#.sort();
        result.add(tuple(bS_asList));

def generateR_Decomposition(tbl):
    decompList = [];
    result = set();
    bRcPairs = getR_EquivalentPairs(tbl);
    for (b, c) in bRcPairs:
        Sb = tbl.rightMultiplyBySet(b);
        Sb_asList = list(Sb);#.sort();
        result.add(tuple(Sb_asList));

"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# If a range was passed, read tables for this range
if len(sys.argv) >= 5:
    if random.random() > 0.001:
        sys.exit();
    tableNum  = int(sys.argv[3]);
    lastTable = int(sys.argv[4]);
    tbls = CayleyTable.readRangeOfTables(filename,order,
                                         tableNum, lastTable);
else:  #Load all tables
    tableNum = 0;
    tbls = CayleyTable.readAllTables(filename, order);

tableNum = 0;
groupSet = tbls[0].symbols;

for tbl in tbls:

    # Increment the table counter
    tableNum += 1;

    # Generate Decompositions in the case they are needed
    L_Decomp = generateL_Decomposition(tbl);
    R_Decomp = generateR_Decomposition(tbl);

    # Run test for all quadruples in S
    for (a, b, c, h, y, p, q) in product(groupSet, repeat=7):

        if b != c:
            continue;
        
        # Verify clauses 1 - 2
        bhy = tbl.simplifyTerm(b + h + y);
        yhc = tbl.simplifyTerm(y + h + c);
        yab = tbl.simplifyTerm(y + a + b);
        cay = tbl.simplifyTerm(c + a + y);
        hya = tbl.simplifyTerm(h + y + a);
        ayh = tbl.simplifyTerm(a + y + h);
        bp  = tbl.simplifyTerm(b + p);
        ya  = tbl.simplifyTerm(y + a);
        cq  = tbl.simplifyTerm(c + q);
        pb  = tbl.simplifyTerm(p + b);
        ay  = tbl.simplifyTerm(a + y);
        qc  = tbl.simplifyTerm(q + c);

        clause1 = bhy == y and y == yhc;
        clause2 = yab == b and cay == c;
        clause3 = hya == h and h == ayh and bp == ya and ya == cq and pb == ay and ay == qc;
        clause4 = b != c

        if not (clause1 and clause2 and clause3 and clause4):
            continue;
            
        # Set up results printer
        results = ResultPrinter(tableNum, tbl)
        results.addToResults("a", a);
        results.addToResults("b", b);
        results.addToResults("c", c);
        results.addToResults("h", h);
        results.addToResults("y", y);
        results.addToResults("p", p);
        results.addToResults("q", q);
        results.addToResults("L-decomp of " + str(tableNum), L_Decomp)
        results.addToResults("R-decomp of " + str(tableNum), R_Decomp)
        results.printAll();


"""END OF SCRIPT"""
