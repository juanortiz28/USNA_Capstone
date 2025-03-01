clc; clear

%% Trial 1: 23FEB25

% load data
data = load("Data_23FEB.mat");

% extract
latts = data.fulloutputtable.Latitude;
longs = data.fulloutputtable.Longitude;
time_stamps = data.fulloutputtable.Timestamp;
accuracies = data.fulloutputtable.Accuracy;

% means
mean_latitude = mean(latts, 'omitnan');
mean_longitude = mean(longs, 'omitnan');
mean_accuracy = mean(accuracies, 'omitnan');

time_span = max(time_stamps) - min(time_stamps);
total_duration = duration(time_span, 'Format', 'hh:mm:ss');

% Display results
fprintf('Mean Latitude: %.6f\n', mean_latitude);
fprintf('Mean Longitude: %.6f\n', mean_longitude);
fprintf('Mean Accuracy: %.2f meters\n', mean_accuracy);
fprintf('Total Data Collection Duration: %s\n', char(total_duration));

figure(1);
geoplot(latts, longs, '-o', 'LineWidth', 2, 'MarkerSize', 4);
hold on
comet(latts, longs)
geobasemap('streets'); % Choose a map style (e.g., 'satellite', 'topographic', 'streets')
title('GPS Path');
% xlabel('Longitude');
% ylabel('Latitude');
grid on;
hold off

% Plot histogram
figure(2);
histogram(accuracies, 'BinWidth', 1); % Adjust bin width if needed
xlabel('Accuracy (meters)');
ylabel('Frequency');
title('Accuracy Distribution');
grid on;


% Plot accuracy over time
figure;
plot(time_stamps, accuracies, '-o', 'LineWidth', 1);
xlabel('Timestamp');
ylabel('Accuracy (meters)');
title('Accuracy Over Time');
grid on;
datetick('x', 'yyyy-mm-dd HH:MM', 'keeplimits'); % Format x-axis labels
xtickangle(45); % Rotate x-axis labels for readability


%% Trial 2: 

