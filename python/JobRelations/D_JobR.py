#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
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
    print 'Step 3 TEST Results for S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c) = (' + a + ', ' + b + ', ' + c + ')';
    print 'v         = ' + v;
    print 'w         = ' + w;
    print 'vc        = ' + vc;
    print 'bw        = ' + bw;
    print;

def printStep5(sNum, s, a, b, c, y, ya, ay, ba, ab, baSecComm, abSecComm):
    print 'Step 5 Results for S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c, y) = (' + a + ', ' + b + ', ' + c + ', ' + y + ')';
    print 'ya           = ' + ya;
    print 'ay           = ' + ay;
    print 'ca           = ' + ca;
    print 'ac           = ' + ac;
    print 'Comm_2(ba)   = ';
    for elem in baSecComm:
        print elem;
    print
    print 'Comm_2(ab)   = ';
    for elem in abSecComm:
        print elem;
    print '----------------------------------------------';
    print;
    print;

def printStep5DEBUG(sNum, s, a, b, c, y, ya, ay, caSecComm, acSecComm):
    print 'Step 5 TEST Results for S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c, y) = (' + a + ', ' + b + ', ' + c + ', ' + y + ')';
    print 'ya           = ' + ya;
    print 'ay           = ' + ay;
    print 'Comm_2(ca)   = ';
    for elem in caSecComm:
        print elem;
    print
    print 'Comm_2(ac)   = ';
    for elem in acSecComm:
        print elem;
    print '----------------------------------------------';
    print;
    print;

def printNotbRcPairs(sNum, tbl, bRcPairs):
    print 'Non-bRc Pairs for S# ' + str(sNum) + ':';
    tbl.printTable();
    if len(bRcPairs) == 0:
        print 'none';
    for (b, c) in bRcPairs:
        sys.stdout.write('(' + b + ', ' + c + ') ');
    print;
    print '----------------------------------------------';
    print;
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

    # Generate all (b, c)-pairs without R-equivalence
    bRcPairs = getNonR_EquivalentPairs(tbl);
    printNotbRcPairs(tableNum, tbl, bRcPairs);

    # Identify ordered triples (a, b, c) and corresponding terms v, w, such
    # that b == vcab and c == cabw for some v, w in the group set.
    quintvw = [];
    for (b, c) in bRcPairs:
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
        printStep3(tableNum, tbl, a, b, c, v, w, vc, bw);

        if vc != bw:
            pass;
            #printStep3(tableNum, tbl, a, b, c, v, w, vc, bw);
        else:
            y = vc;
            quady.append((a, b, c, y));

    # Determine second commumtants of ba and ab
    quadyAndSecondComm = [];
    for (a, b, c, y) in quady:
        caSecondComm = tbl.findSecondCommutants(c+a);
        acSecondComm = tbl.findSecondCommutants(a+c);
        quadyAndSecondComm.append(((a, b, c, y), caSecondComm, acSecondComm));

    # Test if ya is a second communtant of ba and if ay is a second
    # commutant of ab. If both are true, print for this step.
    for ((a, b, c, y), caSecondComm, acSecondComm) in quadyAndSecondComm:
        """print tableNum;
        print (a, b, c, y);
        print caSecondComm;
        print acSecondComm;
        print;"""
        ya = tbl.simplifyTerm(y+a);
        ay = tbl.simplifyTerm(a+y);
        printStep5DEBUG(tableNum, tbl, a, b, c, y, ya, ay, 
            caSecondComm, acSecondComm);
        if ya in caSecondComm and ay in acSecondComm:
            ac = tbl.simplifyTerm(a + c);
            ca = tbl.simplifyTerm(c + a);
            printStep5(tableNum, tbl, a, b, c, y, ya, ay, ca, ac, 
                        caSecondComm, acSecondComm);

"""END OF SCRIPT"""