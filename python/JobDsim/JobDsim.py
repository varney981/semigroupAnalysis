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

fh = open('JobDsim' + str(order) + '.txt', 'w')
for tbl in tbls:
    # Increment the table counter
    tableNum += 1;
    if not tbl.hasUnitElement():
        continue;

    L_eq_pairs = getL_EquivalentPairs(tbl)
    R_eq_pairs = getR_EquivalentPairs(tbl)
    possible_p = get_invertible_terms(tbl)
    
    for e in range(tbl.order):
        if not(e == tbl.multiply([e,e])):
            continue
        for f in range(tbl.order):
            if not(f == tbl.multiply([f,f])):
                continue

            d = -1
            for (left,r_d) in L_eq_pairs:
                if(left == e):
                    for (l_d, right) in R_eq_pairs:
                        if(l_d == r_d and right == f):
                            d = l_d
                            break
            if d != -1:
                p = -1
                for _p in possible_p:
                    pe = tbl.multiply([_p,e])
                    fp = tbl.multiply([f,_p])
                    if(pe == fp):
                        p = _p
                        break

                if(p == -1):
                    L_class_e = set(tbl.cTable[:,e])
                    L_class_d = set(tbl.cTable[:,d])
                    R_class_d = set(tbl.cTable[d,:])
                    R_class_f = set(tbl.cTable[f,:])
                    
                    print 'S#' + str(tableNum)
                    print tbl.cTable
                    print 'e = ' + str(e)
                    print 'f = ' + str(f)
                    print 'd = ' + str(d)
                    print 'L-class of e = ' + str(L_class_e)
                    print 'L-class of d = ' + str(L_class_d)
                    print 'R-class of d = ' + str(R_class_d)
                    print 'R-class of f = ' + str(R_class_f)
                    print


                
                



    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
fh.close();
            
    
"""END OF SCRIPT"""
