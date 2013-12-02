%these values are assigned on script invocation
%correctPath = ''; %path to the correct implementation
%submittedPath = ''; %path to the user implementation
%tests = ''; %test function names used in assertaining code correctness

addpath(correctPath);
ts = feval(tests);
tsClean = {}
for i = 1:length(ts)
    if isstruct(ts{i})
        tsClean{i} = ts{i}
    else
        tsClean{i}.name = "test_" int2str(i);
        tsClean{i}.description = "Test " int2str(i);
        tsClean{i}.f = ts{i};
    end
end
ts = tsClean;

correctReturns = {};
for i = 1:length(ts)
    t = ts{i}.f;
    correctReturns{i} = t();
end
rmpath(correctPath);

addpath(submittedPath);
submittedReturns = {};
errors = {};
for i = 1:length(ts)
    t = ts{i}.f;
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
        outputString = [outputString "Test " int2str(i) " netačan.||" errors{i} " \n"];
    elseif correctReturn == submittedReturns{i}
        outputString = [outputString "Test " int2str(i) " tačan.||" ts{i}.description "\n"];
        successfulAmount = successfulAmount + 1;
    else
        outputString = [outputString "Test " int2str(i) " netačan.||" ts{i}.description "\n"];
    end
end
if i == successfulAmount
    outputString = [outputString "\n" "Zadatak tačan."];
else
    outputString = [outputString "\n" "Zadatak netačan."];
end 

disp(outputString)

disp("|||ENDPRINT|||")
