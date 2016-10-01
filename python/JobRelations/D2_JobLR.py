#!/usr/bin/python

import sys;
sys.path.insert(0, "CayleyTable/");
import CayleyTable;
sys.path.insert(0, "ResultPrinter/");
from ResultPrinter import ResultPrinter;
from itertools import product;


"""START OF FUNCTIONS"""

def getNonL_EquivalentPairs(tbl):
    result = set();
    for b in tbl.symbols:
        for c in tbl.symbols:
            Sb = tbl.leftMultiplyBySet(b);
            Sc = tbl.leftMultiplyBySet(c);
            Sb.add(b);
            Sc.add(c);
            if Sb != Sc:
                result.add((b, c));
    return result;

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

def printStep5L(sNum, s, a, b, c, y, ya, ay, ba, ab, baSecComm, abSecComm):
    print 'S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c, y) = (' + a + ', ' + b + ', ' + c + ', ' + y + ')';
    print 'ya           = ' + ya;
    print 'ay           = ' + ay;
    print 'ba           = ' + ba;
    print 'ab           = ' + ab;
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

def printStep5R(sNum, s, a, b, c, y, ya, ay, ca, ac, caSecComm, acSecComm):
    print 'S# ' + str(sNum) + ':';
    s.printTable();
    print '(a, b, c, y) = (' + a + ', ' + b + ', ' + c + ', ' + y + ')';
    print 'ya           = ' + ya;
    print 'ay           = ' + ay;
    print 'ca           = ' + ca;
    print 'ac           = ' + ac;
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


def printTruthTable(bLc,bRc,ya_comm2_ba, ya_comm2_ca, ay_comm2_ab, ay_comm2_ac):
    print 'Statement        |    T/F';
    print '----------------------------------------------';
    print 'bLc              |   ' + str(bLc);
    print 'bRc              |   ' + str(bRc);
    print 'ya in comm_2(ba) |   ' + str(ya_comm2_ba);
    print 'ya in comm_2(ca) |   ' + str(ya_comm2_ca);
    print 'ay in comm_2(ab) |   ' + str(ay_comm2_ab);
    print 'ay in comm_2(ac) |   ' + str(ay_comm2_ac);
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

# Generate all possible truth table combinations
remainingCombos = set();
for (t1, t2, t3, t4, t5, t6) in product(set([True, False]), repeat=6):
    remainingCombos.add((t1,t2,t3,t4,t5,t6));

tableNum = 0;
for tbl in tbls:
    # Reset test values for the truth table
    bLc         = False;
    bRc         = False;
    ya_comm2_ba = False;
    ya_comm2_ca = False;
    ay_comm2_ab = False;
    ay_comm2_ac = False;

    # Increment the table counter
    tableNum += 1;

    # Set up output
    out = ResultPrinter(tableNum, tbl);
    ya_print = 'None';
    ay_print = 'None';
    y_print  = 'None';
    a_print  = 'None';
    b_print  = 'None';
    c_print  = 'None';
    ya_comm2_ba_print = 'None';
    ya_comm2_ca_print = 'None';
    ay_comm2_ab_print = 'None';
    ay_comm2_ac_print = 'None';


    # Generate all (b, c)-pairs without L-equivalence
    bLcPairs = getNonL_EquivalentPairs(tbl);
    bLc = len(bLcPairs) > 0;

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
        baSecondComm = tbl.findSecondCommutants(b+a);
        abSecondComm = tbl.findSecondCommutants(a+b);
        quadyAndSecondComm.append(((a, b, c, y), baSecondComm, abSecondComm));

    # Test if ya is a second communtant of ba and if ay is a second
    # commutant of ab. If both are true, print for this step.
    ya_comm2_ba = False;
    ay_comm2_ab = False;
    for ((a, b, c, y), baSecondComm, abSecondComm) in quadyAndSecondComm:
        ya = tbl.simplifyTerm(y+a);
        ay = tbl.simplifyTerm(a+y);
        if ya in baSecondComm:
            ya_comm2_ba = True;
        if ay in abSecondComm:
            ay_comm2_ab = True;
        if ya in baSecondComm and ay in abSecondComm:
            ab = tbl.simplifyTerm(a + b);
            ba = tbl.simplifyTerm(b + a);
            printStep5L(tableNum, tbl, a, b, c, y, ya, ay, ba, ab, 
                        baSecondComm, abSecondComm);
    
    # Generate all (b, c)-pairs without R-equivalence
    bRcPairs = getNonR_EquivalentPairs(tbl);
    bRc = len(bRcPairs) > 0;

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
        if ya in caSecondComm:
            ya_comm2_ca = True;
        if ay in acSecondComm:
            ay_comm2_ac = True;
        if ya in caSecondComm and ay in acSecondComm:
            ac = tbl.simplifyTerm(a + b);
            ca = tbl.simplifyTerm(b + a);
            printStep5R(tableNum, tbl, a, b, c, y, ya, ay, ca, ac, 
                        caSecondComm, acSecondComm);

    # Determine results to print
    out.addToResults

    # Print truth table for this set if not yet examined
    out.addToResults('ya', 'A');

    if (bLc, bRc, ya_comm2_ba, ya_comm2_ca, 
          ay_comm2_ab, ay_comm2_ac) in remainingCombos:
        remainingCombos.remove((bLc, bRc, ya_comm2_ba, ya_comm2_ca,
                                    ay_comm2_ab, ay_comm2_ac));
        out.addToTable('bLc', bLc);
        out.addToTable('bRc', bRc);
        out.addToTable('ya in comm2(ba)', ya_comm2_ba)
        out.addToTable('ya in comm2(ca)', ya_comm2_ca)
        out.addToTable('ay in comm2(ab)', ay_comm2_ab)
        out.addToTable('ay in comm2(ac)', ay_comm2_ac)
        out.printAll();

"""END OF SCRIPT"""
