%correctPath = '';
%submittedPath = '';

addpath(correctPath);
ts = tests();
correctReturns = {};
for i = 1:length(ts)
    t = ts{i};
    correctReturns{i} = t();
end
rmpath(correctPath);

addpath(submittedPath);
submittedReturns = {};
errors = {};
for i = 1:length(ts)
    t = ts{i};
    try
        submittedReturns{i} = t();
        errors{i} = 0;
    catch
        submittedReturns{i} = 0; % exact value doesn't matter, should never be checked
        msg = lasterror.message;
        errors{i} = msg;
    end
end
rmpath(submittedPath);
disp("|||STARTPRINT|||")

outputString = "";
successfulAmount = 0;
for i = 1:length(ts)
    correctReturn = correctReturns{i};
    if errors{i} ~= 0
        outputString = [outputString "Test " int2str(i) " netačan. " errors{i} " \n"];
    elseif correctReturn == submittedReturns{i}
        outputString = [outputString "Test " int2str(i) " tačan.\n"];
        successfulAmount = successfulAmount + 1;
    else
        outputString = [outputString "Test " int2str(i) " netačan.\n"];
    end
end
if i == successfulAmount
    outputString = [outputString "\n" "Zadatak tačan."];
else
    outputString = [outputString "\n" "Zadatak netačan."];
end 

disp(outputString)

disp("|||ENDPRINT|||")
