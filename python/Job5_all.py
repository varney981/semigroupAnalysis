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
count = 0;
total = 0;
for tbl in tbls:
    tableNum += 1;
    print tableNum;
    for a1 in groupSet:
        for a2 in groupSet:
            for b1 in groupSet:
                for b2 in groupSet:
                    for z in groupSet:
                        for x in groupSet:
                            for d in groupSet:
                                total += 1;

                                # Determine each subset needed for testing
                                b1S = set();
                                Sb2 = set();
                                for elem in groupSet:
                                    b1S.add(tbl.simplifyTerm(b1 + elem));
                                    Sb2.add(tbl.simplifyTerm(elem + b1));

                                # Check clause (1)
                                z_b1S = z in b1S;
                                b1a1z = tbl.simplifyTerm(b1 + a1 + z);
                                clause1 = False;
                                if z_b1S and b1a1z == b1:
                                    clause1 = True;
                                else:
                                    continue;

                                # Check clause (2)
                                x_Sb2 = x in Sb2;
                                xa2b2 = tbl.simplifyTerm(x + a2 + b2);
                                clause2 = False;
                                if x_Sb2 and xa2b2 == b2:
                                    clause2 = True;
                                else:
                                    continue

                                # Check clause (3)
                                da1 = tbl.simplifyTerm(d + a1);
                                a2d = tbl.simplifyTerm(a2 + d);
                                db1 = tbl.simplifyTerm(d + b1);
                                b2d = tbl.simplifyTerm(b2 + d);
                                clause3 = False;
                                if da1 == a2d and db1 == b2d:
                                    clause3 = True;
                                else:
                                    continue;
                                
                                # Check clause (4)
                                xd = tbl.simplifyTerm(x + d);
                                dz = tbl.simplifyTerm(d + z);
                                clause4 = False;
                                if xd == dz:
                                    clause4 == True;

                                if clause1 and clause2 and clause3 and not clause4:
                                    count += 1;


