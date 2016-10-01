#!/usr/bin/python

import sys;
import random;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;


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

def getD_EquivalentPairs(tbl):
    result = set();
    L_equivPairs = getL_EquivalentPairs(tbl);
    R_equivPairs = getR_EquivalentPairs(tbl);

    for LPair in L_equivPairs:
        for RPair in R_equivPairs:
            if LPair[1] == RPair[0]:
                result.add((LPair[0], RPair[1]));

    return result;

def getD_EquivalentPairsWithLink(tbl):
    result = set();
    L_equivPairs = getL_EquivalentPairs(tbl);
    R_equivPairs = getR_EquivalentPairs(tbl);

    for LPair in L_equivPairs:
        for RPair in R_equivPairs:
            if LPair[1] == RPair[0]:
                result.add((LPair[0], LPair[1], RPair[1]));

    return result;


"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

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

    # Obtain D triplets
    D_equivPairs = getD_EquivalentPairs(tbl);
    
    for (b, c1) in D_equivPairs:
        for (c2, d) in D_equivPairs:
            if c1 != c2:
                continue;
        
            c = c1;
            for (r, s, t, u) in product(tbl.symbols, repeat=4):
                rs = tbl.simplifyTerm(r+s);
                sr = tbl.simplifyTerm(s+r);
                tu = tbl.simplifyTerm(t+u);
                ut = tbl.simplifyTerm(u+t);
                if not (b == rs and c == sr and sr == tu and d == ut):
                    continue;

                vwFound = False;
                for (v, w) in product(tbl.symbols, repeat=2):
                    vw = tbl.simplifyTerm(v+w);
                    wv = tbl.simplifyTerm(w+v);
                    if (b == vw and d == wv):
                        vwFound = True;
                        break;


                if not vwFound:
                    results = ResultPrinter(tableNum, tbl);
                    results.addToResults('b', b);
                    results.addToResults('c', c);
                    results.addToResults('d', d);
                    results.addToResults('r', r);
                    results.addToResults('s', s);
                    results.addToResults('t', t);
                    results.addToResults('u', u);
                    results.printResults();
    
"""END OF SCRIPT"""
