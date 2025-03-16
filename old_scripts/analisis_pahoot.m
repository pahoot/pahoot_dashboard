gener = readmatrix("Data_gener.csv");
febrer = readmatrix("Data_febrer.csv");
marc = readmatrix("Data_marc.csv");
abril = readmatrix("Data_abril.csv");
maig = readmatrix("Data_maig.csv");
juny = readmatrix("Data_juny.csv");
jul = readmatrix("Data_juliol.csv");
ago = readmatrix("Data_agost.csv");
set = readmatrix("Data_setembre.csv");
oct = readmatrix("Data_octubre.csv");
nov = readmatrix("Data_novembre.csv");
des = readmatrix("Data_desembre.csv");
noms = ['Rubèn Llorens i Poblador', 'Benet Fité i Abril', 'Roger Jordi Martínez i Pardell',... 
    "Alejandro Jiménez i Roldán 'Jimeno'", 'Víctor Lopera i Jiménez', 'Marc Grau i Boncompte',... 
    'Roger Perna i Montané', 'Pol Simón i Massot'];
%%
gener(isnan(gener)) = 0;
febrer(isnan(febrer)) = 0;
marc(isnan(marc)) = 0;
abril(isnan(abril)) = 0;
maig(isnan(maig)) = 0;
juny(isnan(juny)) = 0;
jul(isnan(jul)) = 0;
ago(isnan(ago)) = 0;
set(isnan(set)) = 0;
oct(isnan(oct)) = 0;
nov(isnan(nov)) = 0;
des(isnan(des)) = 0;

gener = gener(1:8, :);
febrer = febrer(1:8, :);
marc = marc(1:8, :);
abril = abril(1:8, :);
maig = maig(1:8, :);
juny = juny(1:8, :);
jul = jul(1:8, :);
ago = ago(1:8, :);
set = set(1:8, :);
oct = oct(1:8, :);
nov = nov(1:8, :);
des = des(1:8,:);

tot = horzcat(gener(1:8, :), febrer(1:8, :), marc(1:8, :), abril(1:8, :), maig(1:8, :), juny(1:8, :), jul(1:8, :), ago(1:8, :), set(1:8, :), oct(1:8, :), nov(1:8, :),des);
%%
total_ind = sum(tot,2);
%streaks
streak_sense = zeros(1,8);
streak_amb = zeros(1,8);
for row=1:size(tot,1)
    count_sense=0;
    count_amb=0;
    for dia=1:size(tot,2)
        if tot(row,dia) == 0
            count_sense=count_sense+1;
            count_amb = 0;
            if count_sense>streak_sense(row)
                streak_sense(row) = count_sense;
            end
        else
            count_sense=0;
            count_amb = count_amb+1;
            if count_amb>streak_amb(row)
                streak_amb(row) = count_amb;
            end
        end
    end
end
horzcat(noms',streak_sense')
horzcat(noms',streak_amb')
horzcat(noms',max(tot,[],2))
%%
% First transform all numbers into 1
B = tot;
B(tot>0) = 1;


% Compute the Matthews correlation coefficient between all pairs of rows
n = size(B,1);
MCC = zeros(n);

for i = 1:n-1
    for j = i+1:n
        % Compute the elements needed for MCC calculation
        A = B(i,:);
        B_ = B(j,:);
        C = (A==1 & B_==1);
        D = (A==0 & B_==0);
        P = (A==1 & B_==0);
        Q = (A==0 & B_==1);
        S = sqrt((sum(C)+sum(D))*(sum(C)+sum(P))*(sum(D)+sum(Q))*(sum(P)+sum(Q)));
        MCC(i,j) = (sum(C)*sum(D) - sum(P)*sum(Q)) / S;
        MCC(j,i) = MCC(i,j); % Because MCC is symmetric
    end
end

%%
h=heatmap(MCC);
h.XData={'RLP','BFA','RJMP','AJR','VLJ','MGB','RPM','PSM'};
h.YData={'RLP','BFA','RJMP','AJR','VLJ','MGB','RPM','PSM'};
colormap('parula')
%%
monthly_totals = [sum(gener, 2), sum(febrer, 2), sum(marc, 2), sum(abril, 2), sum(maig, 2), sum(juny, 2), sum(jul, 2), sum(ago, 2), sum(set, 2), sum(oct, 2), sum(nov, 2),sum(des,2)];
averages = [mean(gener, 2), mean(febrer, 2), mean(marc, 2), mean(abril, 2), mean(maig, 2), mean(juny, 2), mean(jul, 2), mean(ago, 2), mean(set, 2), mean(oct, 2), mean(nov, 2),mean(des,2)];
% Assuming you have the names of individuals (replace with actual names)

% Plot bar chart for each person
figure;
plot(averages', 'o-', 'LineWidth', 2); % Adjust 'LineWidth' as needed
xlabel('Mes');
ylabel('Gaioles');
title('Gaioles mensuals');
noms_curts = {'RLP','BFA','RJMP','AJR','VLJ','MGB','RPM','PSM'};
legend(noms_curts, 'Location', 'Best');
grid on
%%

% Calculate cumulative sums
cumulative_totals = cumsum(monthly_totals');

% Plot cumulative line chart for each person
figure;
plot(cumulative_totals, 'o-', 'LineWidth', 2);
xlabel('Mes');  
ylabel('Gaioles');
xlim([1, 12]);
ylim([0,180]);
title('Gaioles acumulades');
legend(noms_curts, 'Location', 'Best');
grid on;



