import pandas as pd
import matplotlib.pyplot as plt
from calendar import month_abbr

# Load the dataset
df = pd.read_csv('assets/data_2005_2015.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Filter data for 2005-2014
data_2005_2014 = df[(df['Date'].dt.year >= 2005) & (df['Date'].dt.year <= 2014)]
data_2015 = df[df['Date'].dt.year == 2015]

# Remove leap day (Feb 29)
data_2005_2014 = data_2005_2014[~((data_2005_2014['Date'].dt.month == 2) & (data_2005_2014['Date'].dt.day == 29))]
data_2015 = data_2015[~((data_2015['Date'].dt.month == 2) & (data_2015['Date'].dt.day == 29))]

# Create 'Month_Day' for grouping
data_2005_2014['Month_Day'] = data_2005_2014['Date'].dt.strftime('%m-%d')
data_2015['Month_Day'] = data_2015['Date'].dt.strftime('%m-%d')

# Group by Month_Day
min_2005_2014 = data_2005_2014[data_2005_2014['Element'] == 'TMIN'].groupby('Month_Day')['Data_Value'].min()
max_2005_2014 = data_2005_2014[data_2005_2014['Element'] == 'TMAX'].groupby('Month_Day')['Data_Value'].max()
min_2015 = data_2015[data_2015['Element'] == 'TMIN'].groupby('Month_Day')['Data_Value'].min()
max_2015 = data_2015[data_2015['Element'] == 'TMAX'].groupby('Month_Day')['Data_Value'].max()

# Set up the months for labels
months = [month_abbr[i] for i in range(1, 13)]
month_starts = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

# Create a figure
plt.figure(figsize=(12, 6))

# Plot 2005-2014 min/max
plt.plot(min_2005_2014.values, label='Min Temp (2005-2014)', color='blue')
plt.plot(max_2005_2014.values, label='Max Temp (2005-2014)', color='red')

# Highlight 2015 temperatures that exceed limits
exceeds_max = max_2015[max_2015 > max_2005_2014]
below_min = min_2015[min_2015 < min_2005_2014]

# Shade the area between the minimum and maximum lines
plt.fill_between(range(len(min_2005_2014)), min_2005_2014.values, max_2005_2014.values, color='grey', alpha=0.2)

# Scatter plot for 2015 temperatures that exceed limits
plt.scatter(exceeds_max.index, exceeds_max.values, color='orange', label='2015 Above Max', zorder=3)
plt.scatter(below_min.index, below_min.values, color='purple', label='2015 Below Min', zorder=3)

# Add labels and titles
plt.xticks(month_starts, months)
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.title('Daily Min and Max Temperatures (2005-2014) with 2015 Extremes')
plt.legend(loc='best')
plt.grid(True)

# Save the plot
plt.savefig('output/weather_plot.png')
plt.show()
