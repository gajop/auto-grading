function fs = tests()
    fs = { @test1, @test2, @test3};
end
    
function retVal = test1()
    retVal = my_factorial(10);
end

function retVal = test2()
    retVal = my_factorial(5);
end

function retVal = test3()
    retVal = my_factorial(0);
end
