% Memoriless

clear;

nExp = 500000;

lambda = 3;
t = 1;

expVec =  -log( rand(nExp,1) ) / lambda ;

x = 0:0.025:3;
expPdf = lambda * exp(-lambda*x);

expVecGreater = expVec( expVec > t ) - t;


figure(1); clf;
h1 = histogram(expVec,'Normalization','pdf');
hold on;
h2 = histogram(expVecGreater,'Normalization','pdf');
p1 = plot(x, expPdf , 'LineWidth',2 );
ylabel('Empirical pdf');
xlabel('x')
legend([h1 h2 p1], 'Full exp', 'Residual of exp > t', 'Theoretical pdf')
set(gca,'FontSize',20)

