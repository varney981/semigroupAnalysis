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
    for b in range(tbl.order):
        for c in range(tbl.order):
            Sb = set(tbl.cTable[:,b]);
            Sc = set(tbl.cTable[:,c]);
            Sb.add(b);
            Sc.add(c);
            if Sb == Sc:
                result.add((b, c));
    return result;

def getR_EquivalentPairs(tbl):
    result = set();
    for b in range(tbl.order):
        for c in range(tbl.order):
            bS = set(tbl.cTable[b,:]);
            cS = set(tbl.cTable[c,:]);
            bS.add(b);
            cS.add(c);
            if bS == cS:
                result.add((b, c));
    return result;


def get_invertible_terms(tbl):
    result = set()
    unitTerm = tbl.unitElement()
    for p in range(tbl.order):
        if unitTerm in set(tbl.cTable[p,:]) and unitTerm in set(tbl.cTable[:,p]):
            result.add(p)
    return result


def write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay):
    result = "";
    result = result + str(tableNum) + ': \n';
    result = result + str(tbl.cTable) + '\n';
    result = result + ('a = {0}, b = {1}, c = {2} , y = {3}, p = {4}, q = {5}' +
                        ', ya = {6}, ay = {7}').format(a,b, c, y, p, q, ya, ay);
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

#fh = open('JobDsim' + str(order) + '.txt', 'w')
for tbl in tbls:
    # Increment the table counter
    tableNum += 1;
    
    for (y,b,h) in product(range(order), repeat=3):
        bhy = tbl.multiply([b,h,y])
        if not(bhy == y):
            continue
        for a in range(order):
            yab = tbl.multiply([y,a,b])
            if not(yab == b):
                continue
            for c in range(order):
                cay = tbl.multiply([c,a,y])
                yhc = tbl.multiply([y,h,c])
                if not(yhc == y and cay == c):
                    continue
                ya = tbl.multiply([y,a])
                ay = tbl.multiply([a,y])
                for p in range(order):
                    bp = tbl.multiply([b,p])
                    pb = tbl.multiply([p,b])
                    if not(bp == ya and pb == ay):
                        continue
                    for q in range(order):
                        cq = tbl.multiply([c,q])
                        qc = tbl.multiply([q,c])
                        if not(cq == ya and ay == qc):
                            continue
                        if (b != c):
                            print "Case found!"
                        else:
                            print "Almost!"



    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
