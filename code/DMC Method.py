# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 00:31:53 2022

@author: user Behafta
"""

import pandas as pd
import numpy as np
Data=pd.read_csv('data/DMC1.csv')

#Rainfall data reported from a station may not be always consistent over 
#the period of observation of rainfall record.
#Double Mass Curve(DMC) Analysis is used to adjust inconsistent data.

# Making the cumulative sum for the single and group data
dataIn = Data.get(['PA','Pgroup'])
cumulative = dataIn.cumsum().rename(columns={'PA':'sumA','Pgroup':'sumGroup'})
data = dataIn.join(cumulative)

import matplotlib.pyplot as plt
%matplotlib
import numpy as np
#plotting single versus average
fig,ax = plt.subplots()
ax.plot(data.sumA,data.sumGroup,marker='o',ls='--',label='Single versus group')
ax.set_xlabel('Single station')
ax.set_ylabel('Average of group')
fig.legend()
ax.set_title('Cumulative Mass Curve')
 #by using slope method corect the inconsistent data
#CB=changeBefor=CB=X1/Y1
#changesumA= X1=DMC.loc[11]['sumA']-0
#changesumGroup=Y1=DMC.loc[11]['sumGroup']-0
#CB=X1/Y1

# X1=DMC.loc[11]['sumA']-0
# Y1=DMC.loc[11]['sumGroup']-0

X1,Y1=data.loc[11,['sumA','sumGroup']] - 0

CB=Y1/X1

#CA=changeAfter=CA=X2/Y2
#changeCumA=X2=DMC.loc[19]['sumA']-DMC.loc[11]['CumpA']
#changeCumulativeGuroup=Y2=DMC.loc[19]['sumGroup']-DMC.loc[11]['sumGroup']
#CA=X2/Y2
# DMC.loc[19]['sumA']
# DMC.loc[19]['sumGroup']

# X2=DMC.loc[19]['sumA']-DMC.loc[11]['sumA']
# Y2=DMC.loc[19]['sumGroup']-DMC.loc[11]['sumGroup']

X2,Y2=data.loc[19,['sumA','sumGroup']] - np.array([X1,Y1])

CA=Y2/X2

#k=AfterchangeSlop/BeforchangeSlope
#K=CB/CA
K=CA/CB

#Then multiplay from the index of 11 up to the end by K factor
 #not the comltive of A 

data.loc[11:19,'K'] = K
data.loc[:10,'K'] = 1
data['PAnew'] = data['PA'] * data['K']
data['sumAnew'] = data['PAnew'].cumsum()

#plotting single versus average, corrected for K
fig,ax = plt.subplots()
ax.plot(data.sumGroup,data.sumAnew,marker='o',ls='--',label='Single versus group, K corrected')
ax.set_xlabel('Single station')
ax.set_ylabel('Average of group')
fig.legend()
ax.set_title('Cumulative Mass Curve')



















