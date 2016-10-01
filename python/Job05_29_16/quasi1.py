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
    return bUSb == cUSc

def get_L_class(b, S):
    order = S.order
    L_class = set()
    for c in range(order):
        if are_bLc_related(b,S,c):
            L_class.add(c)
    return L_class

#REIMPLEMENT WHEN are_bRc_related(b,S,c) IMPLEMENTED
def get_R_class(a, S):
    return None

def comm_1(a,S):
    comm_1_a = set()
    order = S.order
    for s in range(order):
        s_a = tbl.multiply([s,a])
        a_s = tbl.multiply([a,s])
        if s_a == a_s:
            comm_1_a.add(s)
    return comm_1_a


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
        non_comm = False
        for s in comm_1_a:
            s_c = tbl.multiply([s,c])
            c_s = tbl.multiply([c,s])
            if s_c != c_s:
                non_comm = True
                break
        if not non_comm:
            comm_2_a.add(c)

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
    for (a,b,c,y) in product(range(order), repeat=4):
        #(1)
        q = None
        p = None
        for s in range(order):
            bsy = tbl.multiply([b,s,y])
            ysc = tbl.multiply([y,s,c])
            if bsy == y:
                q = s
            if ysc == y:
                p = s

        if q == None or p == None:
            continue

        #(2)
        yab = tbl.multiply([y,a,b])
        cay = tbl.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        # search for h satisfying (1)*,(3),(4)
        h_found = False
        aya = tbl.multiply([a,y,a])
        for h in range(order):
            bhy = tbl.multiply([b,h,y])
            hya = tbl.multiply([h,y,a])
            hba = tbl.multiply([h,b,a])
            if (bhy == y) and (hya == h) and (hba == aya):
                h_found = True
                break
        if h_found:
            continue

        #pre-test calculations
        ya = tbl.multiply([y,a])
        ay = tbl.multiply([a,y])
        ba = tbl.multiply([b,a])
        ab = tbl.multiply([a,b])
        ca = tbl.multiply([c,a])
        ac = tbl.multiply([a,c])

        #(B1)
        B1 = int(ya in comm_2(ba, tbl))
        #(B2)
        B2 = int(ay in comm_2(ab,tbl))
        #(C1)
        C1 = int(ya in comm_2(ca,tbl))
        #(C2)
        C2 = int(ay in comm_2(ac,tbl))

        if B1 + B2 + C1 + C2 == 4:
            output = ''
            output += 'S#: ' + str(tableNum) + '\n'
            output += str(tbl.cTable) + '\n'
            output += 'a = {0}, b = {1}, c = {2}, p = {3}, q = {4}, y = {5}\n'.format(a,b,c,p,q,y)
            output += 'ba = {0}, ab = {1}, ca = {2}, ac = {3}\n'.format(ba,ab,ca,ac)
            output += 'comm_1(ba) = {' + ', '.join(['{}'.format(s) for s in comm_1(ba, tbl)]) + '}' + ',{:10}'.format('')
            output += 'comm_2(ba) = {' + ', '.join(['{}'.format(s) for s in comm_2(ba, tbl)]) + '},\n'
            output += 'comm_1(ab) = {' + ', '.join(['{}'.format(s) for s in comm_1(ab, tbl)]) + '}' + ',{:10}'.format('')
            output += 'comm_2(ab) = {' + ', '.join(['{}'.format(s) for s in comm_2(ab, tbl)]) + '},\n'
            output += 'comm_1(ca) = {' + ', '.join(['{}'.format(s) for s in comm_1(ca, tbl)]) + '}' + ',{:10}'.format('')
            output += 'comm_2(ca) = {' + ', '.join(['{}'.format(s) for s in comm_2(ca, tbl)]) + '},\n'
            output += 'comm_1(ac) = {' + ', '.join(['{}'.format(s) for s in comm_1(ac, tbl)]) + '}' + ',{:10}'.format('')
            output += 'comm_2(ac) = {' + ', '.join(['{}'.format(s) for s in comm_2(ac, tbl)]) + '},\n\n'
            print output





            


    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
print 'done'
#fh.close();
            
    
"""END OF SCRIPT"""
