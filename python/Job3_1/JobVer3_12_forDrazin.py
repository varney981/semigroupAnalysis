#!/usr/bin/python


"""START OF FUNCTIONS"""

def getL_EquivalentPairs(tbl):
    A = set();
    for b in range(tbl.order):
        for c in range(tbl.order):
            Sb = the set formed by multiplying b on the left by all d in S;
            Sc = the set formed by multiplying c on the left by all d in S;
            Include b in Sb
            Include c in Sc
            if Sb and Sc have the same contents:
                add the pair (b,c) to the set, A, to be returned;
    return A to the user;



"""END OF FUNCTIONS"""


"""START OF SCRIPT"""
###
### LOAD THE TABLES FROM FILES
###

for tbl in tbls:
    # Increment the table counter
    tableNum += 1;
    
    # This function is detailed in word at the top
    bcPairs = getL_EquivalentPairs(tbl)

    # Iterate over each L-Eq pair that was found above
    for (b,c) in bcPairs:

        # range(n) gives the set {0,1,...,n - 1}
        # product(range(n), repeat=k) gives the cartesian product for k sets of range(n)
        for (a,y) in product(range(order), repeat=2):
            # Each Cayley table is represented as a matrix
            # The left multiple is the row index, and the right multiple is the col index
            # The matrix is indexed as "A[left index, right index]" for matrix A

            # Columns or rows can be extracted by using ":" as an index
            # Here, : is our S, meaning we use each element in S as a right multiple
            bS = set(tbl.cTable[b,:]);

            # Using bS as the set of left multiples, bSy is calculated
            bSy = set(tbl.cTable[list(bS),y])

            # Similarly, Sc is calculated
            Sc = set(tbl.cTable[:,c]);
            ySc = set(tbl.cTable[y,list(Sc)])

            # The keyword "continue" means we will go to the next (a,y) pair
            if not (y in bSy.intersection(ySc)):
                continue

            # Multiplication of multiple elements is done using a process
            # programmed in a different file
            yab = tbl.multiply([y,a,b])
            cay = tbl.multiply([c,a,y])

            # == is the equalitly operator
            if not (yab == b and cay == b):
                continue

            for d in range(order):
                # Determine all the products needed to do the last tests
                bad = tbl.multiply([b,a,d])
                dba = tbl.multiply([d,b,a])
                yad = tbl.multiply([y,a,d])
                dya = tbl.multiply([d,y,a])

                dab = tbl.multiply([d,a,b])
                abd = tbl.multiply([a,b,d])
                day = tbl.multiply([d,a,y])
                ayd = tbl.multiply([a,y,d])

                cad = tbl.multiply([b,a,d])
                dca = tbl.multiply([d,b,a])

                dac = tbl.multiply([d,a,b])
                acd = tbl.multiply([a,b,d])


                # Usually I will do a simple statement if no results are found,
                # then make the results more detailed once I know a counterexample
                # exists.
                if (bad == dba) and not (yad == dya):
                    print 'T Invalid!'
                if (dab == abd) and not (day == ayd):
                    print 'U Invalid!'
                if (cad == dca) and not (yad == dya):
                    print 'V Invalid!'
                if (dac == acd) and not (day == ayd):
                    print 'W Invalid!'


    
"""END OF SCRIPT"""
