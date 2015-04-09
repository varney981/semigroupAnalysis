#!/usr/bin/python

import sys;
import CayleyTable;

# Get file name and order from input
filename = sys.argv[1];
order = ord(sys.argv[2]) - ord('0');

# Load all Caylay tables
tbls = CayleyTable.readAllTables(filename, order);

# Run tests on each Cayley table for each permutation of the group set
groupSet = tbls[0].symbols;
#TODO: SET UP OUTPUT FILE
tableNum = 0;
Acount = 0;
Bcount = 0;
total  = 0;
for tbl in tbls:
    tableNum += 1;
    for b in groupSet:
        for c in groupSet:
            # Determine if either the hypothesis for 8A or 8B is true
            hypA = True;
            hypB = True;
            for a in groupSet:
                Scab = set();
                cabS = set();
                bacS = set();
                for elem in groupSet:
                    Scab.add(tbl.simplifyTerm(elem + c + a + b));
                    cabS.add(tbl.simplifyTerm(c + a + b + elem));
                    bacS.add(tbl.simplifyTerm(b + a + c + elem));

                b_Scab = b in Scab;
                c_cabS = c in cabS;
                b_bacS = b in bacS;
                if b_Scab and not c_cabS:
                    hypA = False;
                if b_Scab and not b_bacS:
                    hypB = False;
                if not hypA and not hypB:
                    continue;

            # Do not test conclusion for b and c if neither hypothesis is true
            if not hypA and not hypB:
                continue;

            # Determine relation results
            Sb = set();
            Sc = set();
            bS = set();
            cS = set();
            for elem in groupSet:
                Sb.add(tbl.simplifyTerm(elem + b));
                Sc.add(tbl.simplifyTerm(elem + c));
                bS.add(tbl.simplifyTerm(b + elem));
                cS.add(tbl.simplifyTerm(c + elem));
            bLc = Sb.union([b]) == Sc.union([c]);
            bRc = bS.union([b]) == cS.union([c]);
            bHc = bLc and bRc;

            # Test conclusion for 8A
            if hypA and not bHc:
                Acount += 1;
                print '(b,c) = (' + b + ',' + c + ')';
                print tableNum;
                tbl.printTable();
                print '';
                for a in groupSet:
                    print 'For a = ' + a;
                    cab = tbl.simplifyTerm(c + a + b);
                    Scab = set();
                    cabS = set();
                    for elem in groupSet:
                        Scab.add(tbl.simplifyTerm(elem + cab));
                        cabS.add(tbl.simplifyTerm(cab + elem));
                    Scab_str = '';
                    for elem in Scab:
                        Scab_str = Scab_str + elem;
                    cabS_str = '';
                    for elem in cabS:
                        cabS_str = cabS_str + elem;
                    print cab;
                    print Scab_str;
                    print cabS_str;
                print '';
                print '';

            # Test conclusion for 8B
            if hypB and not bHc:
                Bcount += 1;
                print '(b,c) = (' + b + ',' + c + ')';
                print tableNum;
                tbl.printTable();
                print '';
                for a in groupSet:
                    print 'For a = ' + a;
                    cab = tbl.simplifyTerm(c + a + b);
                    bac = tbl.simplifyTerm(b + a + c);
                    Scab = set();
                    bacS = set();
                    for elem in groupSet:
                        Scab.add(tbl.simplifyTerm(elem + cab));
                        bacS.add(tbl.simplifyTerm(bac + elem));
                    Scab_str = '';
                    for elem in Scab:
                        Scab_str = Scab_str + elem;
                    bacS_str = '';
                    for elem in bacS:
                        Scab_str = Scab_str + elem;
                    print cab;
                    print Scab_str;
                    print bacS_str;
                print '';
                print '';
                


print 'A contradicted: ' + str(Acount) + ' times';
print 'B contradicted: ' + str(Bcount) + ' times';

