classdef CayleyTable<handle
    properties
        order;
        Ctable;
        Cset;
    end
        
    methods
        function obj = CayleyTable(addOrder)
            obj.order = addOrder;
            obj.Cset  = cell(1, addOrder);
            for i = 1:addOrder
                obj.Cset{i} = char('A' - 1 + i);
            end
        end
        
        function obj = assignTable(obj, addTable)
            obj.Ctable = addTable;
        end
        
        function result = simplifyTerm(obj, term)
            % Return the same term if 1 character
            if length(term) == 1
                result = term;
                return
            end
            
            result = term(1);

            % Until simplied to one term, cross check the Caylay table
            for i = 2:length(term)
                nextOp = term(i);
                %result(1) = table2array(obj.Ctable(operands(1), operands(2)));
                result = obj.Ctable{result, nextOp};
            end
        end
    end
    
    methods (Static)
        function outputTables = tablesFromFile(filename, gOrder)
            % Format data from file
            formatString = zeros(1, 3 * gOrder^2);
            for i = 1:3:3 * gOrder^2
                formatString(i:i+2) = '%c ';
            end
            formatString = char(formatString);
            formatString(end) = [];
            fileID = fopen(filename);
            tableData = textscan(fileID, formatString, ...
                'Delimiter', ',', 'CollectOutput', 1);
            tableData = cell2mat(tableData(1,:));
%            tableData(:,gOrder^2 + 1) = [];   %Not sure why this is not needed
            tableData = tableData';
            fclose(fileID);
            
            % Create Cayley tables
            [~, numTables] = size(tableData);
            outputTables = [];
            for i = 1:numTables
                outputTables = [outputTables; CayleyTable(gOrder)];
                newTable = array2table(tableData(1:gOrder,i), ...
                    'VariableNames',outputTables(i).Cset(1) , ... 
                    'RowNames', outputTables(i).Cset);
                for element = 2:gOrder
                    newTable = [newTable, ...
                        array2table(tableData(1 + gOrder * (element - 1): element * gOrder,i), ...
                        'VariableNames', outputTables(i).Cset(element), ...
                        'RowNames', outputTables(i).Cset)];
                end
                  
%                     outputTables(i).assignTable( ...
%                         [array2table(tableData(1:3,i), 'VariableNames', {'A'}, 'RowNames', {'A', 'B', 'C'}), ...
%                         array2table(tableData(4:6,i), 'VariableNames', {'B'}, 'RowNames', {'A', 'B', 'C'}), ...
%                         array2table(tableData(7:9,i), 'VariableNames', {'C'}, 'RowNames', {'A', 'B', 'C'})]);
            fixTableArray = table2array(newTable);
            newTable = array2table(fixTableArray', ...
                'VariableNames', outputTables(i).Cset, ...
                'RowNames', outputTables(i).Cset);
            [is_assoc, assoc_str] = CayleyTable.isAssociative(newTable);
            if ~is_assoc
                error(['Table S# ' num2str(i) ' is non-associative! ' ...
                    'Check ' assoc_str]);
            end
            outputTables(i).assignTable(newTable);
            end
        end
        
        function [result, nonassoc_str] = isAssociative(newTable)
            nonassoc_str = [];
            result = 1;
            for left = newTable.Properties.RowNames'
                for mid = newTable.Properties.RowNames'
                    for right = newTable.Properties.RowNames'
                        % Evaluate left terms first
                        left_mid   = newTable{left, mid};
                        left_first = newTable{left_mid, right};
                        
                        % Evaluate right terms first
                        mid_right   = newTable{mid, right};
                        right_first = newTable{left, mid_right};
                        
                        if left_first ~= right_first
                            result    = 0;
                            nonassoc_str  = [left{1}, mid{1}, right{1}];
                        end
                    end
                end
            end
        end
    end
end