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
    tbl.cTable[0][0] = 0
    tbl.cTable[0][1] = 1
    tbl.cTable[0][2] = 2
    tbl.cTable[1][0] = 1
    tbl.cTable[1][1] = 1
    tbl.cTable[1][2] = 2
    tbl.cTable[2][0] = 2
    tbl.cTable[2][1] = 1
    tbl.cTable[2][2] = 2
    # Increment the table counter
    tableNum += 1;
    
    for (a,b,c,y) in product(range(order), repeat=4):
        #bS = set(tbl.cTable[b,:]);
        #bSy = set(tbl.cTable[list(bS),y])
        #Sc = set(tbl.cTable[:,c]);
        #ySc = set(tbl.cTable[y,list(Sc)])
        #if not (y in bSy.intersection(ySc)):
        #    continue

        yab = tbl.multiply([y,a,b])
        cay = tbl.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        p_set = set()
        pq_found = False
        failed = False
        for _p in range(order):
            _q = _p
            bqy = tbl.multiply([b,_q,y])
            ypc = tbl.multiply([y,_p,c])
            pya = tbl.multiply([_p,y,a])
            ayp = tbl.multiply([a,y,_p])
            if (bqy == y and ypc == y and pya == _p and _p == ayp):
                pq_found = True
                p_set.add(_p)
                pba = tbl.multiply([_p,b,a])
                aya = tbl.multiply([a,y,a])
                if (pba == aya):
                    failed = True
            if failed:
                break

        if (failed or not pq_found):
            #print(failed)
            #print(pq_found)
            continue
        else:
            print("S#: " + str(tableNum))
            print(tbl.cTable)
            print "a = " + str(a)
            print "b = " + str(b)
            print "c = " + str(c)
            print "y = " + str(y)
            count = 1
            for p_i in p_set:
                p_iba = tbl.multiply([p_i,b,a])
                print "p" + str(count) + " = " + str(p_i) + " , p" + str(count) + "ba = " + str(p_iba)
            print



    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
