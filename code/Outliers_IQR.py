# -*- coding: utf-8 -*-
"""

@author: Mesele & Beyene
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read and load the dataset
example_data = pd.read_csv('C:/Users/USER/all training/Python_2023/example_data.csv') #getting data

#Box-plot: the mean, the median, the quartiles, and the minimum and maximum observations are graphically represented. The length of the box also represents the interquartile range, while the total length of the plot (including the length of the lines on the left and right side of the plot) represents the ‘range’.
#Plot the distribution plot(Box-plot) for the features
fig, ax = plt.subplots(figsize = (8,6))
ax.boxplot(example_data.Discharge)

#Peakflow.sort_values(by = ['Discharge'], inplace=True, ascending=False)
# Finding the IQR (Inter Qurtile Range)
Q1 = example_data.Discharge.quantile(0.25) # First quartile(for 25th percentile): This means that only 25 percent of the data in the data set 
Q2 = example_data.Discharge.quantile(0.5) # Second quartile (Midian)
Q3 = example_data.Discharge.quantile(0.75) # Third quartile (for 75th percentile): This means that only 75 percent of the data in the data set
IQR = Q3 - Q1 # Inter Qurtile Range
# Finding the upper and lower limits
lower_bound = Q1 - 1.5 * IQR # Any value above lower bound (minimum) is an outlier.
upper_bound = Q3 + 1.5 * IQR # Any value above upper bound (maximum) is an outlier.

#Finding outliers
Dischargedata_noOutlier = example_data[(example_data.Discharge <= upper_bound) & (example_data.Discharge >= lower_bound)].dropna() #removing outliers for this column is to remove any value above upper bound and below lower bound
Outliers = example_data[(example_data.Discharge > upper_bound) | (example_data.Discharge < lower_bound)].dropna()

# Setting outliers to nan
data_new = example_data.copy()
data_new.loc[(example_data.Discharge > upper_bound) | (example_data.Discharge < lower_bound),'Discharge'] = np.nan

# Example: turning it into a function
def remove_outliers(data,column):
    """
    Remove outliers from column in the given DataFrame. Original data is kept, a new column is added in which outliers are turned into nan values. Outliers are all values outside IQR*1.5.
    THIS DOCSTRING CAN BE IMPROVED
    """
    data = data.copy()
    to_clean = data[column].copy()
    Q1 = to_clean.quantile(0.25)
    Q3 = to_clean.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    cleaned = to_clean[(to_clean >= lower_bound) & (to_clean <= upper_bound)].dropna()
    data[column+'_cleaned'] = cleaned
    no_outliers = to_clean.count()-cleaned.count()
    print(f'{no_outliers} outliers found. Column {column}_cleaned is added, in which those outliers are missing.')
    return data
### Example on how to use the function
cleaned_data = remove_outliers(Dischargedata_noOutlier,'Discharge')
