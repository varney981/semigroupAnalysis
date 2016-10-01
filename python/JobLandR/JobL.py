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

def get_invertible_terms(tbl):
    result = set()
    unitTerm = tbl.unitElement()
    for p in range(tbl.order):
        if unitTerm in set(tbl.cTable[p,:]) and unitTerm in set(tbl.cTable[:,p]):
            result.add(p)
    return result

def are_bLc_related(b,S,c):
    order = S.order
    bUSb = set()
    bUSb.add(b)
    cUSc = set()
    cUSc.add(c)
    for l in range(order):
        bUSb.add(S.multiply([l,b]))
        cUSc.add(S.multiply([l,c]))
    return get_L_class(b,S) == get_L_class(c,S)

def get_L_class(a, S):
    order = S.order
    aUSa = set()
    aUSa.add(a)
    for l in range(order):
        aUSa.add(S.multiply([l,a]))
    return aUSa

def comm_2(a, S):
    comm_1_a = set()
    comm_2_a = set()
    order = S.order
    for s in range(order):
        s_a = tbl.multiply([s,a])
        a_s = tbl.multiply([a,s])
        if s_a == a_s:
            comm_1_a.add(s)

    for c in range(order):
        for s in comm_1_a:
            s_c = tbl.multiply([s,c])
            c_s = tbl.multiply([c,s])
            if s_c == c_s:
                comm_2_a.add(s)

    return comm_2_a



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
    #tbl.transposeTable()
    
    for (b,c) in product(range(order), repeat=2):
        #Test b,c for L-equiv; if L-equiv, skip pair
        if get_L_class(b, tbl) == get_L_class(c, tbl):
            continue

        for a in range(order):
            #Step 2
            v = None
            w = None
            for (_v, _w) in product(range(order), repeat=2):
                vcab = tbl.multiply([_v,c,a,b])
                cabw = tbl.multiply([c,a,b,_w])
                if vcab == b:
                    v = _v
                if cabw == c:
                    w = _w
                if v and w:
                    break

            if not v or not w:
                continue

            # Step 3
            vc = tbl.multiply([v,c])
            bw = tbl.multiply([b,w])
            if vc != bw:
                print('Step 3 triggered!')
                continue
            else:
                y = vc

            # Step 4
            ba = tbl.multiply([b,a])
            ab = tbl.multiply([a,b])
            comm_2_ba = comm_2(ba, tbl)
            comm_2_ab = comm_2(ab, tbl)

            # Step 5
            ya = tbl.multiply([y,a])
            ay = tbl.multiply([a,y])
            if ya in comm_2_ba and ay in comm_2_ab:
                print 'Step 5 triggered!'






            


    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
