import sys;


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


class ResultPrinter(object):
    """Convenient printing object for results"""
    def __init__(self, tableNum, tbl):
        """Initialize a result printing object"""
        self.truthTableDoubles = [];
        self.numStatements     = 0;
        self.resultDoubles     = [];
        self.numResults        = 0;
        self.tableNum          = tableNum;
        self.refTable          = tbl;

    def addToTable(self, label, value):
        """Boolean values for a truth table"""
        self.truthTableDoubles.append((label, value));
        self.numStatements += 1;

    def addToResults(self, label, value):
        """Label and tuple of values for said tuple"""
        if type(value) is set or type(value) is list:
            value = setAsString(value);
        self.resultDoubles.append((label, value));
        self.numResults += 1;

    def printAll(self):
        """Print truth table and results side by side"""
        print 'S# ' + str(self.tableNum) + ':';
        self.refTable.printTable();
        print;
        print '+' + 18 * '-' + '+' + 18 * '-' + '+'
        print '|' + '{0:18}'.format('Statement') + '|' + '{0:18}'.format('T/F') + '|' + '  Results';
        for line in range(0, max(self.numStatements, self.numResults)):
            if line < self.numStatements:
                statement     = self.truthTableDoubles[line][0];
                statementPart = '{0:18}'.format(statement);
                booleanRes    = str(self.truthTableDoubles[line][1]);
                booleanPart   = '{0:18}'.format(booleanRes);
            else:
                statementPart = '{0:18}'.format(' ');
                booleanPart   = '{0:18}'.format(' ');
            tablePart = '|' + statementPart + '|' + booleanPart + '|';

            if line < self.numResults:
                term = self.resultDoubles[line][0];
                termEval = str(self.resultDoubles[line][1]);
                resultPart = term + ' = ' + termEval;
            else:
                resultPart = ' ';

            print tablePart + '  ' + resultPart;
        print '+' + 18 * '-' + '+' + 18 * '-' + '+' + '-' * 36
        print;

    def printAll_NoGroup(self, fh=None):
        """Print truth table and results side by side"""
        if fh == None:
            print '+' + 18 * '-' + '+' + 18 * '-' + '+'
            print '|' + '{0:18}'.format('Statement') + '|' + '{0:18}'.format('T/F') + '|' + '  Results';
            for line in range(0, max(self.numStatements, self.numResults)):
                if line < self.numStatements:
                    statement     = self.truthTableDoubles[line][0];
                    statementPart = '{0:18}'.format(statement);
                    booleanRes    = str(self.truthTableDoubles[line][1]);
                    booleanPart   = '{0:18}'.format(booleanRes);
                else:
                    statementPart = '{0:18}'.format(' ');
                    booleanPart   = '{0:18}'.format(' ');
                tablePart = '|' + statementPart + '|' + booleanPart + '|';

                if line < self.numResults:
                    term = self.resultDoubles[line][0];
                    termEval = str(self.resultDoubles[line][1]);
                    resultPart = term + ' = ' + termEval;
                else:
                    resultPart = ' ';

                print tablePart + '  ' + resultPart;
            print '+' + 18 * '-' + '+' + 18 * '-' + '+' + '-' * 36
            print;
        else:
            fh.write('+' + 18 * '-' + '+' + 18 * '-' + '+\n');
            fh.write('|' + '{0:18}'.format('Statement') + '|' + '{0:18}'.format('T/F') + '|' + '  Results\n');
            for line in range(0, max(self.numStatements, self.numResults)):
                if line < self.numStatements:
                    statement     = self.truthTableDoubles[line][0];
                    statementPart = '{0:18}'.format(statement);
                    booleanRes    = str(self.truthTableDoubles[line][1]);
                    booleanPart   = '{0:18}'.format(booleanRes);
                else:
                    statementPart = '{0:18}'.format(' ');
                    booleanPart   = '{0:18}'.format(' ');
                tablePart = '|' + statementPart + '|' + booleanPart + '|';

                if line < self.numResults:
                    term = self.resultDoubles[line][0];
                    termEval = str(self.resultDoubles[line][1]);
                    resultPart = term + ' = ' + termEval;
                else:
                    resultPart = ' ';

                fh.write(tablePart + '  ' + resultPart + '\n');
            fh.write('+' + 18 * '-' + '+' + 18 * '-' + '+' + '-' * 36 + '\n\n');

    def printTable(self):
        """Print truth table and results side by side"""
        print 'S# ' + str(self.tableNum) + ':';
        self.refTable.printTable();
        print;
        print '+' + 18 * '-' + '+' + 18 * '-' + '+'
        print '|' + '{0:18}'.format('Statement') + '|' + '{0:18}'.format('T/F') + '|';
        for line in range(0, self.numStatements):
            statement     = self.truthTableDoubles[line][0];
            statementPart = '{0:18}'.format(statement);
            booleanRes    = str(self.truthTableDoubles[line][1]);
            booleanPart   = '{0:18}'.format(booleanRes);
            print '|' + statementPart + '|' + booleanPart + '|';
        print '+' + 18 * '-' + '+' + 18 * '-' + '+' + '-' * 36;
        print;

    def printResults(self):
        """Print desired results"""
        print 'S# ' + str(self.tableNum) + ':';
        self.refTable.printTable();
        print;
        for line in range(0, self.numResults):
            term = self.resultDoubles[line][0];
            termEval = str(self.resultDoubles[line][1]);
            resultPart = term + ' = ' + termEval;
            print resultPart;
        print '-' * 72;
        print;
