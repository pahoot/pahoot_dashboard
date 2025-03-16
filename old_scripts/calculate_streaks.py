import pandas as pd
import numpy as np
import os

# Folder containing the data files
folder_path = 'data_2024'

# List of months and corresponding CSV file names
months = ['gener', 'febrer', 'marc', 'abril', 'maig', 'juny', 'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre']

# Initialize an empty list to store DataFrames
dfs = []

# Read each CSV file for the months and append to the list
for month in months:
    file_path = os.path.join(folder_path, f'Data_{month}.csv')
    df = pd.read_csv(file_path, header=None).iloc[:, 1:]
    names = pd.read_csv(file_path, header=None).iloc[:, 0]
    df.columns = range(df.shape[1])  # Reset column indices for this DataFrame
    dfs.append(df)

# Concatenate all DataFrames horizontally (like horzcat in MATLAB)
tot = pd.concat(dfs, axis=1, ignore_index=True)

# Calculate the total events for each person (sum across all days)
tot_ind = tot.sum(axis=1)

# Initialize lists to store streak lengths
n_rows = tot.shape[0]  # Number of rows (people)
streak_sense = np.zeros(n_rows)  # Streaks with events (1s)
streak_amb = np.zeros(n_rows)    # Streaks without events (0s)

# Loop through each person (row) to calculate the streaks
for row in range(n_rows):
    count_sense = 0
    count_amb = 0
    for dia in range(tot.shape[1]):  # Loop through days (columns)
        if tot.iloc[row, dia] == 0:
            # Day with no event
            count_sense += 1
            count_amb = 0
            streak_sense[row] = max(streak_sense[row], count_sense)
        else:
            # Day with an event
            count_sense = 0
            count_amb += 1
            streak_amb[row] = max(streak_amb[row], count_amb)

# Create a final DataFrame with the results
# Set the rownames equal to names
result = pd.DataFrame({
    'Streak_with_events': streak_amb,
    'Streak_without_events': streak_sense,
    'Total_events': np.array(tot_ind)
}, index=names)

# Display the result
print(result)