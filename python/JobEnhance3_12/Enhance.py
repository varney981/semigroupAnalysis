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
    tbl.transposeTable()
    
    for (b,c) in product(range(order), repeat=2):
        # Test property (0)
        if not are_bLc_related(b, tbl, c):
            continue

        for (a,g,h,y) in product(range(order), repeat=4):
            # Test property (1), (2), (3)
            bhy = tbl.multiply([b,h,y])
            ygc = tbl.multiply([y,g,c])
            yab = tbl.multiply([y,a,b])
            cay = tbl.multiply([c,a,y])
            hya = tbl.multiply([h,y,a])
            ayg = tbl.multiply([a,y,g])
            if not (bhy == y and y == ygc and yab == b and cay == c and hya == h and ayg == g):
                continue

            v = tbl.multiply([y,g])

            # Set up failure messages
            fail1 = "make "
            fail2 = ""

            # Test property P
            prop_P = 0
            cav = tbl.multiply([c,a,v])
            vca = tbl.multiply([v,c,a])
            if cav == vca:
                prop_P = 1
            else:
                fail1 = fail1 + "P, "
                fail2 = fail2 + "(ca)v = " + str(cav) + ", v(ca) = " + str(vca) + "\n"

            # Test property Q
            prop_Q = 0
            vcav = tbl.multiply([v,c,a,v])
            if vcav == v:
                prop_Q = 1
            else:
                fail1 = fail1 + "Q, "
                fail2 = fail2 + "v(ca)v= " + str(vcav) + ", v = " + str(v) + "\n"

            # Test property R
            prop_R = 0
            cavca = tbl.multiply([c,a,v,c,a])
            ca = tbl.multiply([c,a])
            if cavca == ca:
                prop_R = 1
            else:
                fail1 = fail1 + "R, "
                fail2 = fail2 + "(ca)v(ca) = " + str(cavca) + ", ca = " + str(ca) + "\n"

            # Test property S
            prop_S = 0
            ca_n = ca
            for i in range(order - 1):
                ca_n = tbl.multiply([ca_n, ca])
            ca_n_plus1 = tbl.multiply([ca_n, ca])
            ca_n_plus1_v = tbl.multiply([ca_n_plus1, v])
            v_ca_n_plus1 = tbl.multiply([v, ca_n_plus1])
            if ca_n_plus1_v == ca_n and ca_n == v_ca_n_plus1:
                prop_S = 1
            else:
                fail1 = fail1 + "S, "
                fail2 = fail2 + "(ca)^(n+1)*v = " + str(ca_n_plus1_v) + ", v*(ca)^(n+1) = " + str(v_ca_n_plus1) + ", ca^n = " + str(ca_n) + "\n"

            # Test property T
            prop_T = 0
            v_n = v
            for i in range(order - 1):
                v_n = tbl.multiply([v, v_n])
            v_n_plus1 = tbl.multiply([v_n, v])
            v_n_plus1_ca = tbl.multiply([v_n_plus1, ca])
            ca_v_n_plus1 = tbl.multiply([ca, v_n_plus1])
            if v_n_plus1_ca == v_n and v_n == ca_v_n_plus1:
                prop_T = 1
            else:
                fail1 = fail1 + "T, "
                fail2 = fail2 + "v^(n+1)*ca = " + str(v_n_plus1_ca) + ", ca*v^(n+1) = " + str(ca_v_n_plus1) + ", v^n = " + str(v_n) + "\n"



            prop_results = prop_P + prop_Q + prop_R + prop_S + prop_T 
            if (prop_results <= 4):
                prop_PTF = 'T' if prop_P == 1 else 'F'
                prop_QTF = 'T' if prop_Q == 1 else 'F'
                prop_RTF = 'T' if prop_R == 1 else 'F'
                prop_STF = 'T' if prop_S == 1 else 'F'
                prop_TTF = 'T' if prop_T == 1 else 'F'
                print("S#: " + str(tableNum))
                print(tbl.cTable)
                print "a = " + str(a)
                print "b = " + str(b)
                print "c = " + str(c)
                print "g = " + str(g)
                print "h = " + str(h)
                print "y = " + str(y)
                print "v = " + str(v)
                print "ya = " + str(tbl.multiply([y,a]))
                print "ay = " + str(tbl.multiply([a,y]))

                ca = tbl.multiply([c,a])
                ac = tbl.multiply([a,c])
                print "ca = " + str(ca)
                print "ac = " + str(ac)

                print("L-class of b = " + str(get_L_class(b, tbl)))
                print("L-class of c = " + str( get_L_class(c, tbl)))
                print("comm^2(ca) = " + str(comm_2(ca, tbl)))
                print("comm^2(ac) = " + str(comm_2(ac, tbl)))
                
                #print '  | P     Q     R     S     T     '
                #print '----------------------------------'
                #print '  | {0:<5} {1:<5} {2:<5} {3:<5} {4:<5} '.format(prop_PTF , prop_QTF , prop_RTF , prop_STF , prop_TTF)
                print
                print fail1 + " fail, with"
                print fail2
                print
                print

    #result_str = write_results(tableNum, tbl, a, b, c, y, p, q, ya, ay);
    #fh.write(result_str + '\n\n');
#fh.close();
            
    
"""END OF SCRIPT"""
