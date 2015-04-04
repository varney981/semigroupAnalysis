function Order3Test()
% Load all Caylay tables and get properties
tbls = CayleyTable.tablesFromFile('order3.csv');
numberOfSets = length(tbls);
count = 0;
total = 0;

% Run tests on each Caylay table for each permutation of the group set
groupSet = {'A', 'B', 'C'};
outputFile = fopen('Odd.txt', 'w');
for tableNum = 1:numberOfSets
    workTable = tbls(tableNum);
    for aNum = 1:3
        a = groupSet{aNum};
        for bNum = 1:3
            b = groupSet{bNum};
            for cNum = 1:3
                c = groupSet{cNum};
                
                cab = workTable.simplifyTerm([c, a, b]);
                bac = workTable.simplifyTerm([b, a, c]);
                
                % Determine each subset needed for testing
                Scab1 = workTable.simplifyTerm(['A', cab]);
                Scab2 = workTable.simplifyTerm(['B', cab]);
                Scab3 = workTable.simplifyTerm(['C', cab]);
                Scab  = [Scab1; Scab2; Scab3];
                
                Sbac1 = workTable.simplifyTerm(['A', bac]);
                Sbac2 = workTable.simplifyTerm(['B', bac]);
                Sbac3 = workTable.simplifyTerm(['C', bac]);
                Sbac  = [Sbac1; Sbac2; Sbac3];
                
                cabS1 = workTable.simplifyTerm([cab, 'A']);
                cabS2 = workTable.simplifyTerm([cab, 'B']);
                cabS3 = workTable.simplifyTerm([cab, 'C']);
                cabS  = [cabS1; cabS2; cabS3];
                
                bacS1 = workTable.simplifyTerm([bac, 'A']);
                bacS2 = workTable.simplifyTerm([bac, 'B']);
                bacS3 = workTable.simplifyTerm([bac, 'C']);
                bacS  = [bacS1; bacS2; bacS3];
                
                % Determine all truth values needed listed in STEP 2
                b_Scab = any(b == Scab);  %(1)
                c_Sbac = any(c == Sbac);  %(2)
                b_bacS = any(b == bacS);  %(3)
                c_cabS = any(c == cabS);  %(4)
                
                % Identify "interesting" results as detailed in STEP 3
                if (((b_Scab || c_Sbac) && ~(b_bacS && c_cabS)) || ...
                        ((b_bacS || c_cabS) && ~(b_Scab && c_Sbac))) ...
                        && (b_Scab + c_Sbac + b_bacS + c_cabS ~= 2 || ...
                        (b_Scab + b_bacS < 2 && c_Sbac + c_cabS < 2))
                    count = count + 1;
                    fprintf(outputFile, ...
                        ['S# %d:\r\n' ...
                        'S: %c %c %c\r\n' ...
                        '   %c %c %c\r\n' ...
                        '   %c %c %c\r\n\r\n' ...
                        '(a,b,c) = (%c,%c,%c)\r\n' ...
                        'cab  = %s\r\n' ...
                        'bac  = %s\r\n' ...
                        'Sbac = %s\r\n' ...
                        'Scab = %s\r\n' ...
                        'bacS = %s\r\n' ...
                        'cabS = %s\r\n\r\n' ...
                        'Left  T/F   Right  T/F\r\n' ...
                        ' (1)   %c     (3)    %c\r\n'  ...
                        ' (2)   %c     (4)    %c\r\n\r\n\r\n'  ...
                        ], ... 
                        tableNum, ...
                        table2array(workTable.Ctable('A','A')),table2array(workTable.Ctable('A','B')) ,table2array(workTable.Ctable('A','C')), ... 
                        table2array(workTable.Ctable('B','A')),table2array(workTable.Ctable('B','B')) ,table2array(workTable.Ctable('B','C')), ...
                        table2array(workTable.Ctable('C','A')),table2array(workTable.Ctable('C','B')) ,table2array(workTable.Ctable('C','C')), ...
                        a, b, c, ...
                        unique(cab)', ...
                        unique(bac)', ...
                        unique(Sbac)', ...
                        unique(Scab)', ...
                        unique(bacS)', ...
                        unique(cabS)', ...
                        'F' + 14 * b_Scab, 'F' + 14 * b_bacS, ...
                        'F' + 14 * c_Sbac, 'F' + 14 * c_cabS);
                end
                total = total + 1;
            end
        end
    end
end
count
total
fclose(outputFile);
end