ts = tests();
% addpath
correctReturns = {}
for i = 1:length(ts)
    t = ts{i};
    correctReturns{i} = t();
end
% rempath


