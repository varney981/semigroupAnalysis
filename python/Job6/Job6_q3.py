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
            for b in groupSet:
                total += 1;

                # Determine each subset needed for testing
                ba1a2b = b + a1 + a2 + b;
                ba2a1b = b + a2 + a1 + b;
                ba2a1b = b + a2 + a1 + b;
                ba1a2b = b + a1 + a2 + b;
                Sba1a2b = set();
                Sba2a1b = set();
                ba2a1bS = set();
                ba1a2bS = set();
                for elem in groupSet:
                    Sba1a2b.add(tbl.simplifyTerm(elem + ba1a2b));
                    Sba2a1b.add(tbl.simplifyTerm(elem + ba2a1b));
                    ba2a1bS.add(tbl.simplifyTerm(ba2a1b + elem));
                    ba1a2bS.add(tbl.simplifyTerm(ba1a2b + elem));

                # Determine truth values for inclusion statements
                b_Sba1a2b = b in Sba1a2b;
                b_Sba2a1b = b in Sba2a1b;
                b_ba1a2bS = b in ba1a2bS;
                b_ba2a1bS = b in ba2a1bS;

                # Check question 3 (true if condition is contradicted)
                if b_Sba1a2b and b_ba1a2bS and not (b_Sba2a1b and b_ba2a1bS):
                    q3 = True;
                else:
                    q3 = False;

                # Check if a counter-example was found for question 3
                if q3:
                    count += 1;

print count;


