# -*- coding: utf-8 -*-
"""
@author: Mesele & Beyene

"""
# TEST FOR OUTLIERS
# Outlier is an observation that significantly deviates from the bulk of the data due to
# error in data collection (either recording or instrument failure error). In hydrometerological data
# presence of outliers causes difficulties when fitting a distribution of the data. There are both
# Low and High outliers. Grubbs and Beck (1972) test (G-B) may be used to detect outliers. The approach
# is commonly used to design hydraulic structures (dams, weirs, bridges ...) due to its moderate  
# threshold. In this test the quantities xH and xL are Higher and Lower limits for outliers. 
# xH = exp(x + KnS)    Where: 'x' and 'S' are mean & standard deviation of the natural logarithms of 
# xL = exp(x - KnS)            the sample repectively and Kn is G-B statistic for various sample sizes.
# Sample values greater than xH are considered to be high outliers, while those less than 
# xL are considered to be low outliers.
# If the outliers are detected for a particular data, then the value(s) will be rejected and checked
# until it becomes within the xH & xL values.
##################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
Data = pd.read_excel('C:/Users/USER/all training/Oulier/Oulier/RF_near_chamo.xlsx')
# Grouping the data based on annual maximum rainfall, this procedure 
# is commonly used for the design of the hydraulic structures to be safe for the peak events. 
Annual_max = Data.drop(columns=['Month','Date']).groupby(by='Year', as_index=False).max()
# Let only 'Gumaide' station is selected for analysis
# by creating new dataFrame for the station
Gumaide_RF = pd.DataFrame({'Year': Annual_max.Year, 'Gumaide': Annual_max.Gumaide_RF})
Gumaide_RF['RF_descending'] = np.sort(Gumaide_RF.Gumaide)[::-1]
Gumaide_RF['Y'] = np.log10(Gumaide_RF.RF_descending)
Gumaide_RF['(Y - Ymean)\u00B2'] = (Gumaide_RF.Y-Gumaide_RF.Y.mean())**2
Gumaide_RF['Cubic'] = (Gumaide_RF.Y-Gumaide_RF.Y.mean())**3
# Estimation of the statistical parameters.
N = len(Gumaide_RF)
Mean = Gumaide_RF.Y.mean()
Std = Gumaide_RF.Y.std()
Cs = (N*np.sum(Gumaide_RF.Cubic))/((N-1)*(N-2)*Std**3)                                      # If Cs > 0.4, check YH first
Kn = -3.62201 + 6.28446*N**(1/4) - 2.49835*N**(1/2) + 0.491436*N**(3/4) - 0.037911*N
YH = Mean + Kn*Std
RF_max = 10**YH

Gumaide_RF['RF_max'] = RF_max

# Plot of daily maximum rainfall data for 33 years and upper boundary

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(Gumaide_RF.Year, Gumaide_RF.Gumaide, label = 'Gumaide', marker = 'o')
ax.plot(Gumaide_RF.Year, Gumaide_RF.RF_max, label = 'Highier_value', marker = '*')
ax.set_title('Gumaide 33 years daily max rainfall data')
ax.set_xlabel('Year')
ax.set_ylabel('Daily maximum rainfall')
ax.legend()

N = len(Gumaide_RF)
Mean = Gumaide_RF.Y.mean()
Std = Gumaide_RF.Y.std()
Cs = (N*np.sum(Gumaide_RF.Cubic))/((N-1)*(N-2)*Std**3)                                      # If Cs > 0.4, check YH first
Kn = -3.62201 + 6.28446*N**(1/4) - 2.49835*N**(1/2) + 0.491436*N**(3/4) - 0.037911*N
YH = Mean + Kn*Std
RF_max = 10**YH
RF = []
# Looping the data

#for RF in Gumaide_RF.Gumaide:
if RF_max > max(Gumaide_RF.Gumaide):
    print('NO HIGHIER OUTLIER')
else:
    print('OUTLIER')
New_data = pd.DataFrame(Gumaide_RF.Gumaide[(Gumaide_RF.Gumaide < RF_max)])

##### Loop for iteratively calculating RF max, removing >RF max, calculating RF max, ...
RFdata = Gumaide_RF.get(['Gumaide','Y','Cubic']).rename(columns={'Gumaide':'RF'})

RFdata_noOutliers = RFdata.copy()

while True:
    # Calculate RF_max
    N = len(RFdata_noOutliers)
    Mean = RFdata_noOutliers.Y.mean()
    Std = np.std(RFdata_noOutliers.Y)
    Cs = (N*np.sum(RFdata_noOutliers.Cubic))/((N-1)*(N-2)*Std**3)                                      # If Cs > 0.4, check YH first
    Kn = -3.62201 + 6.28446*N**(1/4) - 2.49835*N**(1/2) + 0.491436*N**(3/4) - 0.037911*N
    YH = Mean + Kn*Std
    RF_max = 10**YH

    # Check whether there is an outlier
    if max(RFdata_noOutliers.RF) < RF_max:
        print('NO HIGHIER OUTLIER; stopping loop')
        break
    else:
        print('OUTLIER DETECTED; it will be removed, loop will continue')
### Example on how to use the function    
    RFdata_noOutliers = RFdata[RFdata.RF < RF_max]







