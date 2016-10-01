import numpy

class CayleyTable(object):
    """Table object used to perform group operations"""
    def __init__(self, order):
        """Initialize an empty CayleyTable"""
        self.cTable  = numpy.zeros((order, order), dtype=numpy.int);
        self.order   = order;
        self.unitElementFound = False;
        self.prevUnit = None;

    def multiply(self, term):
        """Using the term, return evaluated term for the group"""
        if len(term) == 1:
            #If the term is already evaluated or else can be done in one step
            return term;
        elif len(term) == 2:
            return self.cTable[term[0], term[1]];

        #Recursively process term using table
        newTerm = self.multiply(term[0:len(term) - 1]);
        return self.cTable[newTerm][term[len(term) - 1]];

    def transposeTable(self):
        self.cTable = numpy.transpose(self.cTable)
        self.unitElementFound = False;
        self.prevUnit = None;

    def hasUnitElement(self):
        """Check for a unit element"""
        leftUnities = [];
        for left in range(0, self.order):
            isLeftUnity = True;
            for right in range(0, self.order):
                if not self.multiply([left,right]) == right:
                    isLeftUnity = False;
                    break;
            if isLeftUnity:
                leftUnities.append(left);

        for right in leftUnities:
            isRightUnity = True;
            for left in range(0, self.order):
                if not self.multiply([left,right]) == left: 
                    isRightUnity = False;
                    break;
            if isRightUnity:
                return True;

        return False;

    def unitElement(self):
        """Return unit element"""
        if self.unitElementFound:
            return self.prevUnit;

        leftUnities = [];
        for left in range(0, self.order):
            isLeftUnity = True;
            for right in range(0, self.order):
                if not self.multiply([left,right]) == right:
                    isLeftUnity = False;
                    break;
            if isLeftUnity:
                leftUnities.append(left);

        for right in leftUnities:
            isRightUnity = True;
            for left in range(0, self.order):
                if not self.multiply([left,right]) == left: 
                    isRightUnity = False;
                    break;
            if isRightUnity:
                self.unitElementFound = True;
                self.prevUnit = right;
                return right;
                        
    def Sy(self, y):
        """For passed term y and the group set for this table, compute the set Sy"""
        result = set();
        rightTerm = self.multiply(y);
        return set(self.cTable[:][rightTerm]);

    def xS(self, x):
        """For passed term x and the group set for this table, compute the set xS"""
        result = set();
        leftTerm = self.multiply([x]);
        return set(self.cTable[leftTerm][:]);

    def Py(self, right, setTerms):
        """For passed term right and the passed set, compute the set S(right)"""
        result = set();
        rightTerm = self.multiply([right]);
        for leftTerm in setTerms:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;
        
    def xP(self, left, setTerms):
        """For passed term left and the passed set, compute the set (left)S"""
        result = set();
        leftTerm = self.multiply([left]);
        for rightTerm in setTerms:
            result.add(self.multiply([leftTerm , rightTerm]));
        return result;

    def xSy(self,x,y):
        """For passed terms x,y and the group set for this table, compute the set xSy"""
        return self.rightMultiplyByPartialSet(self.xS(x))

    def xInSy(self, x, y):
        """Find left multiples of x = zy.
        
        For passed terms x, y and for the group set for this table, compute the
        set Sy and return each term z in S such that x = zy. If no such z is found,
        return the empty set.
        """     
        result = set();
        rightTerm = self.multiply([y]);
        for leftTerm in range(self.order):
            productTerm = self.multiply([leftTerm , rightTerm]);
            if productTerm == x:
                result.add(leftTerm)
        return result;
        
    def xInyS(self, x, y):
        """Find the right multiples of x = yz.
        
        For passed terms x, y and for the group set for this table, compute the 
        set yS and return each term z in S such that x = yz. If no such z is
        found, return the empty set.
        """
        result = set();
        leftTerm = self.multiply([y]);
        for rightTerm in range(self.order):
            productTerm = self.multiply([leftTerm , rightTerm]);
            if productTerm == x:
                result.add(rightTerm)
        return result;

    def comm_1(self, x):
        """Find all elements a in the group set such that xa == ax.
        
        The method returns a set containing all elements in the group set that
        commute with the term passed. If none are found, the empty set is returned.
        """
        result = set();
        for a in range(self.order):
            ax = self.multiply([a,x]);
            xa = self.multiply([x,a]);
            if ax == xa:
                result.add(a);
        return result;

    def comm_2(self, a):
        comm_1_a = set()
        comm_2_a = set()
        order = self.order
        for s in range(order):
            s_a = tbl.multiply([s,a])
            a_s = tbl.multiply([a,s])
            if s_a == a_s:
                comm_1_a.add(s)

        for c in range(order):
            non_comm = False
            for s in comm_1_a:
                s_c = tbl.multiply([s,c])
                c_s = tbl.multiply([c,s])
                if s_c != c_s:
                    non_comm = True
                    break
            if not non_comm:
                comm_2_a.add(c)

        return comm_2_a

    def findSecondCommutants(self, x):
        """Determine second commutant elements of x.
        
        First, find the set A such that each element in A commutes with x.
        Then find the set B such that each element in B commutes with
        each element in A. Return set B.
        """
        result = set();
        firstCommSet = self.findFirstCommutants(x);
        for b in self.order:
            isCommutant = 1;
            for a in firstCommSet:
                ba = self.multiply([b,a]);
                ab = self.multiply([a,b]);
                if ba != ab:
                    isCommutant = 0;
                    break;
            if isCommutant:
                result.add(b);
        return result;

    def power(self, operand, n):
        if n == 0:
            return self.unitElement();
        elif n == 1:
            return operand;

        # compute power
        result = operand;
        for i in range(n-1):
            result = self.multiply([result, operand])
        return result;


    def are_xLy_related(self,x,y):
        order = S.order
        xUSx = set(self.xS(x)).add(x)
        yUSy = set(self.xS(y)).add(y)
        return xUSx == yUSy

    def are_xRy_related(self,x,y):
        order = S.order
        xUxS = set(self.Sy(x)).add(x)
        yUyS = set(self.Sy(y)).add(y)
        return xUxS == yUyS

    def get_invertible_terms(self):
        result = set()
        unitTerm = self.unitElement()
        for p in range(self.order):
            if unitTerm in set(self.cTable[p,:]) and unitTerm in set(self.cTable[:,p]):
                result.add(p)
        return result

    def get_L_class(self, x):
        order = self.order
        L_class = set()
        for y in range(order):
            if are_xLy_related(x,y):
                L_class.add(y)
        return L_class

    def get_R_class(self, y):
        order = self.order
        R_class = set()
        for x in range(order):
            if are_xRy_related(x,y):
                R_class.add(x)
        return R_class
