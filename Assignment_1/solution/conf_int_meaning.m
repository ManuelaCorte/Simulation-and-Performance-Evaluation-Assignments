% Confidence intervals

clear;

lambda = 3;
trueMean = 1/lambda;

gamma = 0.99;
eta = norminv((1+gamma)/2);

nExp = 10000;
nDrawsPerExp = 2000;

% draws = zeros(nDrawsPerExp,nExp);
% for iExp = 1 : nExp
%     ***
% end
draws = -log( rand(nDrawsPerExp,nExp ) ) / lambda;

% Conf int for the mean
cInt = zeros(2,nExp);
for iExp = 1 : nExp
    currMean = mean( draws(:,iExp) );
    currStd = std( draws(:,iExp) );
    cInt(1,iExp) = currMean - eta*currStd/sqrt(nDrawsPerExp);
    cInt(2,iExp) = currMean + eta*currStd/sqrt(nDrawsPerExp);
end

% Check whether true mean is inside interval
isMeanInInterval = zeros(1,nExp);
for iExp = 1 : nExp
    if trueMean >= cInt(1,iExp) && trueMean <= cInt(2,iExp)
        isMeanInInterval(iExp) = 1;
    end
end

1 - sum(isMeanInInterval)/nExp

firstExpNotIn = find(isMeanInInterval==0,1,'first');

dataSetNotIn = draws(:,firstExpNotIn);

x = 0:0.025:6;
expPdf = lambda * exp(-lambda*x);

figure(3); clf;
h1 = histogram(dataSetNotIn ,'Normalization','pdf');
hold on;
p1 = plot(x, expPdf , 'LineWidth',2 );

