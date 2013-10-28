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
for i = 1:length(ts)
    t = ts{i};
    submittedReturns{i} = t();
end
rmpath(submittedPath);
disp("|||STARTPRINT|||")

outputString = "";
successfulAmount = 0;
for i = 1:length(ts)
    correctReturn = correctReturns{i}
    submittedReturn = submittedReturns{i}
    if correctReturn == submittedReturn
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
