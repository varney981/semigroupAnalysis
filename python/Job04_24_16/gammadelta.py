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
    #tbl.transposeTable()
    for (a,b,c,g,h,y) in product(range(order), repeat=6):
        # search for h satisfying (1),(2),(4)
                
        #(1)
        bhy = tbl.multiply([b,h,y])
        ygc = tbl.multiply([y,g,c])
        if not (bhy == y and y == ygc):
            continue

        #(2)
        yab = tbl.multiply([y,a,b])
        cay = tbl.multiply([c,a,y])
        if not (yab == b and cay == c):
            continue

        #(3)
        hya = tbl.multiply([h,y,a])
        ayg = tbl.multiply([a,y,g])
        if not (hya == h and g == ayg):
            continue

        #(4)
        aya = tbl.multiply([a,y,a])
        hba = tbl.multiply([h,b,a])
        acg = tbl.multiply([a,c,g])
        if not (hba == aya and aya == acg):
            continue

        #test z
        z = tbl.multiply([y,h])
        ba = tbl.multiply([b,a])

        #gamma
        zba = tbl.multiply([z,ba])
        baz = tbl.multiply([ba,z])
        gamma = zba == baz

        #delta
        zba_2 = tbl.multiply([z,ba,ba])
        delta = zba_2 == ba

        if not (gamma and delta):
            output = ''
            output += 'S#: ' + str(tableNum) + '\n'
            output += str(tbl.cTable) + '\n'
            output += 'a = {0}, b = {1}, c = {2}, g = {3}, h = {4}, y = {5}\n'.format(a,b,c,g,h,y)
            zbaz = tbl.multiply([z,b,a,z])
            bazba = tbl.multiply([b,a,z,b,a])
            output += 'z = {0}, ba = {1}, z(ba) = {2}, (ba)z = {3}, z(ba)z = {4}, (ba)z(ba) = {5}'.format(z,ba,zba,baz,zbaz,bazba)
            output += 'z(ba)^2 = {0}'.format(zba_2)
            output += '---------------------'
            output += '| (gamma) | (delta) |'
            output += '|    {0}    |    {1}    |'.format(str(gamma)[0],str(delta)[0])
            output += '---------------------'
            print output





            


    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
print 'done'
#fh.close();
            
    
"""END OF SCRIPT"""
