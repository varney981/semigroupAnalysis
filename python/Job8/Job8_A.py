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
total  = 0;
for tbl in tbls:
    tableNum += 1;
    for b in groupSet:
        for c in groupSet:
            # Determine if either the hypothesis for 8A or 8B is true
            hypA = True;
            for a in groupSet:
                Scab = set();
                cabS = set();
                for elem in groupSet:
                    Scab.add(tbl.simplifyTerm(elem + c + a + b));
                    cabS.add(tbl.simplifyTerm(c + a + b + elem));

                b_Scab = b in Scab;
                c_cabS = c in cabS;
                if b_Scab and not c_cabS:
                    hypA = False;
                    break;

            # Do not test conclusion for b and c if neither hypothesis is true
            if not hypA:
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
                print 'S#: ' + str(tableNum);
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
                    print 'cab =  ' + cab;
                    print 'Scab = ' + Scab_str;
                    print 'cabS = ' + cabS_str;
                print '';
                print '';


print 'A contradicted: ' + str(Acount) + ' times';

