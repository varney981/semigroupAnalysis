#!/usr/bin/python

import sys;
import CayleyTable;
from itertools import product;


"""START OF FUNCTIONS"""

def getNonR_EquivalentPairs(tbl):
    result = set();
    for b in tbl.symbols:
        for c in tbl.symbols:
            bS = tbl.rightMultiplyBySet(b);
            cS = tbl.rightMultiplyBySet(c);
            bS.add(b);
            cS.add(c);
            if bS != cS:
                result.add((b, c));
    return result;

def printStep3(sNum, s, a, b, c, v, w, vc, bw):
    print 'S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c) = (' + a + ', ' + b + ', ' + c + ')';
    print 'v         = ' + v;
    print 'w         = ' + w;
    print 'vc        = ' + vc;
    print 'bw        = ' + bw;
    print;

def printStep5(sNum, s, a, b, c, y, ya, ay, ba, ab, baSecComm, abSecComm):
    print 'S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c, y) = (' + a + ', ' + b + ', ' + c + ', ' + y + ')';
    print 'ya           = ' + v;
    print 'ay           = ' + w;
    print 'ba           = ' + vc;
    print 'ab           = ' + bw;
    print 'Comm_2(ba)   = ' + baSecComm;
    print 'Comm_2(ab)   = ' + abSecComm;
    print;


"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Load all Cayley tables
tbls = CayleyTable.readAllTables(filename, order);

tableNum = 0;
for tbl in tbls:
    tableNum += 1;

    # Generate all (b, c)-pairs without L-equivalence
    bLcPairs = getNonR_EquivalentPairs(tbl);

    # Identify ordered triples (a, b, c) and corresponding terms v, w, such
    # that b == vcab and c == cabw for some v, w in the group set.
    quintvw = [];
    for (b, c) in bLcPairs:
        for a in tbl.symbols:
            vSet = tbl.findLeftMultipleInSetProduct(b, c+a+b);
            wSet = tbl.findRightMultipleInSetProduct(c, c+a+b);
            if len(vSet) > 0 and len(wSet) > 0:
                quintvw.append((a, b, c, vSet.pop(), wSet.pop()));
    
    # Compute vc and bw for each ordered triple (a, b, c). If vc != bw, 
    # print appropriate information. Otherwise, form an ordered quadruple
    # (a, b, c, y) for y = vc.
    quady = [];
    for (a, b, c, v, w) in quintvw:
        vc = tbl.simplifyTerm(v + c);
        bw = tbl.simplifyTerm(b + w);

        if vc != bw:
            printStep3(tableNum, tbl, a, b, c, v, w, vc, bw);
        else:
            y = vc;
            quady.append((a, b, c, y));

    # Determine second commumtants of ba and ab
    quadyAndSecondComm = [];
    for (a, b, c, y) in quady:
        caSecondComm = tbl.findSecondCommutants(c+a);
        acSecondComm = tbl.findSecondCommutants(a+c);
        quadyAndSecondComm.append(((a, b, c, y), caSecondComm, acSecondComm));
    #print quadyAndSecondComm;

    # Test if ya is a second communtant of ba and if ay is a second
    # commutant of ab. If both are true, print for this step.
    for ((a, b, c, y), caSecondComm, acSecondComm) in quadyAndSecondComm:
        ya = tbl.simplifyTerm(y+a);
        ay = tbl.simplifyTerm(a+y);
        if ya in caSecondComm and ay in acSecondComm:
            printStep5(tableNum, tbl, a, b, c, y, ya, ay, ba, ab, 
                        caSecondComm, acSecondComm);

"""END OF SCRIPT"""
