import pypyodbc
import pandas as pd
import numpy as np
from scipy import stats
from Pahoot.settings import con as conn


# SQL query to fetch event data for each period
sql_query = """
WITH PeriodData AS (
    SELECT 
        'Period 5' AS Period, Day, COUNT(*) AS EventCount
    FROM Gaioles
    WHERE Day BETWEEN '2024-03-18' AND '2024-06-11'
    GROUP BY Day
    UNION ALL
    SELECT 
        'Period 6' AS Period, Day, COUNT(*) AS EventCount
    FROM Gaioles
    WHERE Day BETWEEN '2024-06-12' AND '2024-09-08'
    GROUP BY Day
    UNION ALL
    SELECT 
        'Period 7' AS Period, Day, COUNT(*) AS EventCount
    FROM Gaioles
    WHERE Day BETWEEN '2024-09-09' AND '2024-12-31'
    GROUP BY Day
    UNION ALL
    SELECT 
        'Period 8' AS Period, Day, COUNT(*) AS EventCount
    FROM Gaioles
    WHERE Day BETWEEN '2024-10-15' AND '2024-11-25'
    GROUP BY Day
    UNION ALL
    SELECT 
        'Period 9' AS Period, Day, COUNT(*) AS EventCount
    FROM Gaioles
    WHERE Day BETWEEN '2024-05-06' AND '2024-06-05'
    GROUP BY Day
)
SELECT * FROM PeriodData
"""

# Execute the query and fetch the data into a DataFrame
df = pd.read_sql(sql_query, conn)

# Close the connection
conn.close()

# Create a dictionary to store event counts by period
periods = df['period'].unique()
period_data = {period: df[df['period'] == period]['eventcount'].values for period in periods}

# Initialize an empty DataFrame for the p-values table
p_values_matrix = pd.DataFrame(index=periods, columns=periods)

# Calculate p-values for each pairwise comparison
for i in range(len(periods)):
    for j in range(i, len(periods)):  # Start from i to avoid redundant calculations
        period1, period2 = periods[i], periods[j]
        data1, data2 = period_data[period1], period_data[period2]
        
        # Perform t-test
        t_stat, p_value = stats.mannwhitneyu(data1, data2)
        
        # Fill the upper triangle and the diagonal with p-values
        p_values_matrix.loc[period1, period2] = p_value
        p_values_matrix.loc[period2, period1] = p_value  # Make symmetric

# Apply styling to highlight significant p-values
def highlight_p_value(val):
    color = 'red' if val < 0.05 else 'green'
    return f'background-color: {color}'

# Styling the dataframe
styled_df = p_values_matrix.style.applymap(highlight_p_value)

# Display the styled dataframe
# Save the styled table to an HTML file
styled_df.to_html('p_value_comparison.html')