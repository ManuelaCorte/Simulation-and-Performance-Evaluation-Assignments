% Poisson arrivals

clear;

lambda = 4;
T = 4;
N = lambda*T;

nDraws = 100000;

unifInterarrivalsVec = [];
while length(unifInterarrivalsVec) < nDraws
    currUnif = rand(N,1) * T;
    currUnifSorted = sort(currUnif,'ascend');
    interArrivals = currUnifSorted - [0; currUnifSorted(1:N-1)];
    unifInterarrivalsVec  = [unifInterarrivalsVec ; interArrivals];
end

expInterarrivalVec = [];
while length(expInterarrivalVec) < nDraws
    currExp = -log( rand(N+1,1) )/ lambda;
%     if sum(currExp(1:N)) > T
%         continue;
%     end
    if sum(currExp(1:N)) < T && sum(currExp) > T
        expInterarrivalVec = [expInterarrivalVec; currExp(1:N)];
    end
end


x = 0:0.025:3;
expPdf = lambda * exp(-lambda*x);

figure(2); clf;
h1 = histogram(unifInterarrivalsVec ,'Normalization','pdf');
hold on;
h2 = histogram(expInterarrivalVec ,'Normalization','pdf');
p1 = plot(x, expPdf , 'LineWidth',2 );
