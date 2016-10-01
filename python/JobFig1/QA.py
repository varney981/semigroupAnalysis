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
    
    for (a,b,y) in product(range(order), repeat=3):
        # Test condition (2)
        c = b
        yab = tbl.multiply([y,a,b])
        cay = tbl.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        # Test condition (1)
        p = None
        q = None
        pq_found = False
        for (_p, _q) in product(range(order), repeat=2):
            bqy = tbl.multiply([b,_q,y])
            ypc = tbl.multiply([y,_p,c])
            if (bqy == y and ypc == y):
                pq_found = True
                p = _p
                q = _q
                break
        if not(pq_found):
            continue

        # Test property B
        prop_B = False
        h = None
        for _h in range(order):
            bhy = tbl.multiply([b,_h,y])
            yhb = tbl.multiply([y,_h,b])
            hya = tbl.multiply([_h,y,a])
            ayh = tbl.multiply([a,y,_h])
            if (bhy == y and y == yhb and hya == h and ayh == h):
                h = _h
                prop_B = True
                break
        
        # Test property C
        prop_C = False
        ya = tbl.multiply([y,a])
        ay = tbl.multiply([a,y])
        r = None
        s = None
        for (_r,_s) in product(range(order), repeat=2):
            br = tbl.multiply([b,_r])
            cs = tbl.multiply([c,_s])
            rb = tbl.multiply([_r,b])
            sc = tbl.multiply([_s,c])
            if (br == ya and ya == cs and rb == ay and ay == sc):
                r = _s
                s = _s
                prop_C = True
                break

        # Test property D
        prop_D = False
        h = None
        aya = tbl.multiply([a,y,a])
        for _h in range(order):
            bhy = tbl.multiply([b,_h,y])
            yhc = tbl.multiply([y,_h,c])
            hya = tbl.multiply([_h,y,a])
            ayh = tbl.multiply([a,y,_h])
            hba = tbl.multiply([_h,b,a])
            ach = tbl.multiply([a,c,_h])
            if (bhy == y and y == yhc and hya == h and ayh == h and hba == aya and aya == ach):
                h = _h
                prop_D = True
                break

        # Property E true by definition

        # Test Property F
        prop_F = False
        h = None
        g = None
        aya = tbl.multiply([a,y,a])
        for (_g,_h) in product(range(order), repeat=2):
            bhy = tbl.multiply([b,_h,y])
            ygc = tbl.multiply([y,_g,c])
            hya = tbl.multiply([_h,y,a])
            ayg = tbl.multiply([a,y,_g])
            hba = tbl.multiply([_h,b,a])
            acg = tbl.multiply([a,c,_g])
            if (bhy == y and y == ygc and hya == h and ayg == g and hba == aya and aya == acg):
                g = _g
                h = _h
                prop_F = True
                break

        # Test Property G
        prop_G = False
        h = None
        for _h in range(order):
            bhy = tbl.multiply([b,_h,y])
            yhc = tbl.multiply([y,_h,c])
            hya = tbl.multiply([_h,y,a])
            ayh = tbl.multiply([a,y,_h])
            if (bhy == y and y == yhc and hya == h and ayh == h):
                h = _h
                prop_G = True
                break

        # Print table for interesting results
        if not (prop_B and prop_C and prop_D and prop_F and prop_G):






    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
