#!/usr/bin/python

import sys;
import CayleyTable;

# Quick function for printing sets in set notation
def setAsString(writeSet):
    setStr   = '{';
    sliceEnd = -1;
    for elem in writeSet:
        setStr = setStr + elem + ', ';
        sliceEnd += 3;
    setStr = setStr[0:sliceEnd];
    setStr = setStr + '}';
    return setStr;

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


                # Check question 1 (true if condition is contradicted)
                if b_Sba1a2b and not b_Sba2a1b:
                    q1 = True;
                else:
                    q1 = False;

                # Check question 2 (true if condition is contradicted)
                if b_Sba1a2b and not b_ba2a1bS:
                    q2 = True;
                else:
                    q2 = False;

                # Check question 3 (true if condition is contradicted)
                if b_Sba1a2b and b_ba1a2bS and not (b_Sba2a1b and b_ba2a1bS):
                    q3 = True;
                else:
                    q3 = False;

                # Check if a counter-example was found for any question
                if q1 or q2 or q3:
                    print 'S# ' + str(tableNum);
                    tbl.printTable();
                    print;
                    print '(a1 = ' + a1 + ', a2 = ' + a2 + ', b = ' + b + ')';
                    print;
                    print 'Sba1a2b = ' + setAsString(Sba1a2b);
                    print;
                    print 'Sba2a1b = ' + setAsString(Sba2a1b);
                    print;
                    print 'ba1a2bS = ' + setAsString(ba1a2bS);
                    print;
                    print 'ba2a1bS = ' + setAsString(ba2a1bS);
                    print;
                    print;
                    print 'Property     | True/False';
                    print 'b in Sba1a2b |  ' + str(b_Sba1a2b)
                    print 'b in Sba2a1b |  ' + str(b_Sba2a1b)
                    print 'b in ba1a2bS |  ' + str(b_ba1a2bS)
                    print 'b in ba2a1bS |  ' + str(b_ba2a1bS)
                    print;
                    print 'Question     | True/False';
                    print 'Question 1   |  ' + str(q1);
                    print 'Question 2   |  ' + str(q2);
                    print 'Question 3   |  ' + str(q3);
                    print '--------------------------------';
                    print;
                    count += 1;

# Run tests on each transposed Cayley table for each permutation of the group set
tableNum = 0;
count = 0;
total = 0;
for tbl in tbls:
    tableNum += 1;

    # Skip this table if it is non-associative
    if not tbl.transposeTable():
        continue;

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


                # Check question 1 (true if condition is contradicted)
                if b_Sba1a2b and not b_Sba2a1b:
                    q1 = True;
                else:
                    q1 = False;

                # Check question 2 (true if condition is contradicted)
                if b_Sba1a2b and not b_ba2a1bS:
                    q2 = True;
                else:
                    q2 = False;

                # Check question 3 (true if condition is contradicted)
                if b_Sba1a2b and b_ba1a2bS and not (b_Sba2a1b and b_ba2a1bS):
                    q3 = True;
                else:
                    q3 = False;

                # Check if a counter-example was found for any question
                if q1 or q2 or q3:
                    print 'S# ' + str(tableNum) + '*';
                    tbl.printTable();
                    print;
                    print '(a1 = ' + a1 + ', a2 = ' + a2 + ', b = ' + b + ')';
                    print;
                    print 'Sba1a2b = ' + setAsString(Sba1a2b);
                    print;
                    print 'Sba2a1b = ' + setAsString(Sba2a1b);
                    print;
                    print 'ba1a2bS = ' + setAsString(ba1a2bS);
                    print;
                    print 'ba2a1bS = ' + setAsString(ba2a1bS);
                    print;
                    print;
                    print 'Property     | True/False';
                    print 'b in Sba1a2b |  ' + str(b_Sba1a2b)
                    print 'b in Sba2a1b |  ' + str(b_Sba2a1b)
                    print 'b in ba1a2bS |  ' + str(b_ba1a2bS)
                    print 'b in ba2a1bS |  ' + str(b_ba2a1bS)
                    print;
                    print 'Question     | True/False';
                    print 'Question 1   |  ' + str(q1);
                    print 'Question 2   |  ' + str(q2);
                    print 'Question 3   |  ' + str(q3);
                    print '--------------------------------';
                    print;
                    count += 1;
