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
    # Increment the table counter
    tableNum += 1;

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

    # More debug crap
    if len(quady) > 0:
        printSteps = True;
    else:
        printSteps = False;

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
    

    """Do it again, but print everything this time"""
    if not printSteps:
        continue;

    # Generate all (b, c)-pairs
    all_b_c = set();
    for (b,c) in product(tbl.symbols, repeat=2):
        all_b_c.add((b,c));

    # Generate all (b, c)-pairs without L-equivalence
    bLcPairs = getNonL_EquivalentPairs(tbl);

    # Print step 1
    print '-------- Step 1 ---------'
    print 'S# ' + str(tableNum) + ':';
    tbl.printTable();
    print;

    step1Results = [];
    for (b, c) in all_b_c:
        # Generate a printing object for each pair in step 1
        newResult = ResultPrinter(tableNum, tbl);
        Sb = tbl.leftMultiplyBySet(b);
        Sc = tbl.leftMultiplyBySet(c);
        Sb.add(b);
        Sc.add(c);
        newResult.addToTable('bLc', (b, c) not in bLcPairs);
        newResult.addToResults('b', b);
        newResult.addToResults('c', c);
        newResult.addToResults('b U Sb', Sb);
        newResult.addToResults('c U Sc', Sc);
        newResult.printAll_NoGroup();

    # Print step 2
    print '-------- Step 2 --------';
    for (a,b,c) in product(tbl.symbols, repeat=3):
        newResult = ResultPrinter(tableNum, tbl);
        cab = tbl.simplifyTerm(c + a + b);
        Scab = tbl.leftMultiplyBySet(cab);
        newResult.addToTable('b in Scab', b in Scab);
        newResult.addToTable('c in Scab', c in Scab);
        newResult.addToTable('P', c in Scab and b in Scab);
        newResult.addToResults('a', a);
        newResult.addToResults('b', b);
        newResult.addToResults('c', c);
        newResult.addToResults('cab', cab);
        newResult.addToResults('Scab', Scab);
        newResult.printAll_NoGroup();



    


    # Identify ordered triples (a, b, c) and corresponding terms v, w, such
    # that b == vcab and c == cabw for some v, w in the group set.
    quintvw = [];
    for (b, c) in bLcPairs:
        for a in tbl.symbols:
            vSet = tbl.findLeftMultipleInSetProduct(b, c+a+b);
            wSet = tbl.findRightMultipleInSetProduct(c, c+a+b);
            if len(vSet) > 0 and len(wSet) > 0:
                quintvw.append((a, b, c, vSet.pop(), wSet.pop()));


    # Print step 3
    print '-------- Step 3 --------';
    if len(quintvw) == 0:
        print 'No results';
        print;
    for (a, b, c, v, w) in quintvw:
        newResult = ResultPrinter(tableNum, tbl);
        vc = tbl.simplifyTerm(v + c);
        bw = tbl.simplifyTerm(b + w);
        vcab = tbl.simplifyTerm(v + c + a + b);
        cabw = tbl.simplifyTerm(c + a + b + w);
        newResult.addToTable('vc = bw', vc == bw);
        newResult.addToResults('a', a);
        newResult.addToResults('b', b);
        newResult.addToResults('c', c);
        newResult.addToResults('v', v);
        newResult.addToResults('w', w);
        newResult.addToResults('vcab', vcab);
        newResult.addToResults('cabw', cabw);
        newResult.addToResults('vc', vc);
        newResult.addToResults('bw', bw);
        newResult.printAll_NoGroup();

    
    
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

    # More debug crap
    if len(quady) > 0:
        printSteps = True;
    else:
        printSteps = False;

    # Determine second commumtants of ba and ab
    quadyAndSecondComm = [];
    for (a, b, c, y) in quady:
        baSecondComm = tbl.findSecondCommutants(b+a);
        abSecondComm = tbl.findSecondCommutants(a+b);
        quadyAndSecondComm.append(((a, b, c, y), baSecondComm, abSecondComm));
    
    # Print steps 4 and 5
    print '-------- Step 4 and 5 --------';
    if len(quadyAndSecondComm) == 0:
        print 'No results';
        print;
    for ((a, b, c, y), comm2ba, comm2ab) in quadyAndSecondComm:
        newResult = ResultPrinter(tableNum, tbl);
        ba = tbl.simplifyTerm(b + a);
        ab = tbl.simplifyTerm(a + b);
        ya = tbl.simplifyTerm(y + a);
        ay = tbl.simplifyTerm(a + y);
        newResult.addToTable('ya in comm2(ba)', ya in comm2ba);
        newResult.addToTable('ay in comm2(ab)', ay in comm2ab);
        newResult.addToTable('L', ya in comm2ba and ay in comm2ab);
        newResult.addToResults('a', a);
        newResult.addToResults('b', b);
        newResult.addToResults('c', c);
        newResult.addToResults('y', c);
        newResult.addToResults('ba', ba);
        newResult.addToResults('ab', ab);
        newResult.addToResults('ya', ya);
        newResult.addToResults('ay', ay);
        newResult.addToResults('comm2(ba)', comm2ba);
        newResult.addToResults('comm2(ab)', comm2ab);
        newResult.printAll_NoGroup();

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











    # Print truth table for this set if not yet examined
    """out.addToResults('ya', 'A');

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
    """

"""END OF SCRIPT"""
