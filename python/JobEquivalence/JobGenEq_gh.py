#!/usr/bin/python

import sys;
import random;
import numpy;
sys.path.insert(0, "CayleyTable/");
import CayleyTable_Matrices as CayleyTable;
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

def y_in_bSy_intersect_ySc(y, b, c, groupTable):
    bS  = (groupTable.cTable[b, :]).tolist();
    bSy = set(groupTable.cTable[bS, y].tolist());
    yS  = (groupTable.cTable[y, :]).tolist();
    ySc = set(groupTable.cTable[bS, c].tolist());
    
    return y in bSy.intersection(ySc);

def find_p_and_q(b, y, a, c, groupTable):
    for (p,q) in product(range(0, groupTable.order), repeat=2):
        bp = groupTable.multiply([b,p]);
        ya = groupTable.multiply([y,a]);
        cq = groupTable.multiply([c,q]);
        pb = groupTable.multiply([p,b]);
        ay = groupTable.multiply([a,y]);
        qc = groupTable.multiply([q,c]);

        if bp == ya and ya == cq and pb == ay and ay == qc:
            return(p, q);

    return (None, None);

def find_r_and_s(b, c, groupTable):
    for (r, s) in product(range(0, groupTable.order), repeat=2):
        rs = groupTable.multiply([r,s]);
        sr = groupTable.multiply([s,r]);
        if b == rs and c == sr:
            return (r, s);

    return (None, None);

def write_results(tableNum, tbl, a, b, c, h, y, ya, ay, hy, yh):

    result = "";
    result = result + str(tableNum) + ': \n';
    result = result + str(tbl.cTable) + '\n';
    result = result + ('a = {0}, b = {1}, c = {2} , h = {3}, y = {4}' +
                        ', ya = {5}, ay = {6}, hy = {7}, yh = {8}').format(a, b,
                        c, h, y, ya, ay, hy, yh);
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

fh = open('JobGenEq_gh_Results_Order' + str(order) + '.txt', 'w')
for tbl in tbls:
    # Increment the table counter
    tableNum += 1;
    if not tbl.hasUnitElement():
        continue;
    for (b, c, h, y) in product(range(0, order), repeat=4):
        bhy = tbl.multiply([b, h, y]);
        yhc = tbl.multiply([y, h, c]);
        
        if not (bhy == y and y == yhc):
            continue;
        for a in range(0, order):
            yab = tbl.multiply([y,a,b]);
            cay = tbl.multiply([c,a,y]);
            if not (yab == b and cay == c):
                continue;

            hya = tbl.multiply([h,y,a]);
            ayh = tbl.multiply([a,y,h]);
            if not (hya == h and h == ayh):
                continue;

            # Search for disqualifying r, s
            (r, s) = find_r_and_s(b, c, tbl);

            if not ((r, s) == (None, None)):
                continue;

            ya = tbl.multiply([y,a]);
            ay = tbl.multiply([a,y]);
            hy = tbl.multiply([h,y]);
            yh = tbl.multiply([y,h]);
            result_str = write_results(tableNum, tbl, a, b, c, h, y, ya, ay, hy, yh);
            fh.write(result_str + '\n\n');
            fh.close();
            sys.exit(-1);
      
            
    
"""END OF SCRIPT"""
