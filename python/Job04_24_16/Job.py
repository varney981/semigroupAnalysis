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

def get_R_class(a, S):
    order = S.order
    aUaS = set()
    aUaS.add(a)
    for r in range(order):
        aUaS.add(S.multiply([a,r]))
    return aUaS

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

for tbl in tbls:
    # Increment the table counter
    tableNum += 1;
    tbl.transposeTable()
    
    for (a,e,f,y) in product(range(order), repeat=4):
        # test (i), (ii) conditions
        ey = tbl.multiply([e,y])
        yf = tbl.multiply([y,f])
        yae = tbl.multiply([y,a,e])
        fay = tbl.multiply([f,a,y])
        if not(ey == y and y == yf and yae == e and fay == f):
            continue

        # search for h satisfying (1),(3),(4)
        h1 = set()
        h2 = set()
        h3 = set()
        aya = tbl.multiply([a,y,a])
        for h in range(order):
            ehy = tbl.multiply([e,h,y])
            hya = tbl.multiply([h,y,a])
            hea = tbl.multiply([h,e,a])
            if ehy == y:
                h1.add(h)
            if hya == h:
                h2.add(h)
            if hea == aya:
                h3.add(h)

        if len(h1) < 1 or len(h2) < 1 or len(h3) < 1:
        #if len(h3) > 0 and (len(h1) == 0 or len(h2) == 0):
            message = ''
            print('S#: ' + str(tableNum))
            print(tbl.cTable)
            message += 'a = ' + str(a) + ', '
            message += 'e = ' + str(e) + ', '
            message += 'f = ' + str(f) + ', '
            message += 'y = ' + str(y) + '\n'
            message += 'have y as an (e,f)-inverse of a and no h exists satisfying all of (1), (3), (4). The h in S satisfying (1), (3), (4) respectively are\n'
            if len(h1) > 0:
                message += '  (1) h = '
                for h_n in h1:
                    message += str(h_n) + ', '
                message += '\n'
            if len(h2) > 0:
                message += '  (2) h = '
                for h_n in h2:
                    message += str(h_n) + ', '
                message += '\n'
            if len(h3) > 0:
                message += '  (4) h = '
                for h_n in h3:
                    message += str(h_n) + ', '
                message += '\n'

            print(message)





            


    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
