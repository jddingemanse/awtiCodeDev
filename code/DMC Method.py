# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 00:31:53 2022

@author: user
"""

import pandas as pd
import numpy as np
DMC=pd.read_csv('data/DMC.csv')

#Rainfall data reported from a station may not be always consistent over 
#the period of observation of rainfall record.
#Double Mass Curve(DMC) Analysis is used to adjust inconsistent data.

# Making the cumulative sum for the single and group data
dataIn = DMC.get(['PA','Pgroup'])
cumulative = dataIn.cumsum().rename(columns={'PA':'sumA','Pgroup':'sumGroup'})
data = dataIn.join(cumulative)

import matplotlib.pyplot as plt
%matplotlib
import numpy as np
#plotting single versus average
fig,ax = plt.subplots()
ax.plot(data.sumA,data.sumGroup,marker='o',ls='--',label='Single versus group')
maxdata = data.iloc[:,-2:].max().max()
ax.plot([0,maxdata],[0,maxdata],c='r',ls=':',label='Reference line')
ax.set_xlabel('Single station')
ax.set_ylabel('Average of group')
fig.legend()
ax.set_title('Cumulative Mass Curve')
 #by using slope method corect the inconsistent data
#CB=changeBefor=CB=X1/Y1
#changeCumA= X1=DMC.loc[11]['CumpA']-0
#changeCumulativeGuroup=Y1=DMC.loc[11]['CumPgroup']-0
#CB=X1/Y1

# X1=DMC.loc[11]['CumpA']-0
# Y1=DMC.loc[11]['CumPgroup']-0

X1,Y1=data.loc[11,['sumA','sumGroup']] - 0

CB=X1/Y1

#CA=changeAfter=CA=X2/Y2
#changeCumA=X2=DMC.loc[19]['CumpA']-DMC.loc[11]['CumpA']
#changeCumulativeGuroup=Y2=DMC.loc[19]['CumPgroup']-DMC.loc[11]['CumPgroup']
#CA=X2/Y2
# DMC.loc[19]['CumpA']
# DMC.loc[19]['CumPgroup']

# X2=DMC.loc[19]['CumpA']-DMC.loc[11]['CumpA']
# Y2=DMC.loc[19]['CumPgroup']-DMC.loc[11]['CumPgroup']

X2,Y2=data.loc[19,['sumA','sumGroup']] - np.array([X1,Y1])

CA=X2/Y2

#k=changeBefor/changeAfter
#K=CB/CA
K=CB/CA

#Then multiplay from the index of 11 up to the end by K factor
 #not the comltive of A 

data.loc[11:,'K'] = K
data.loc[:10,'K'] = 1
data['PAnew'] = data['PA'] * data['K']
data['sumAnew'] = data['PAnew'].cumsum()

#plotting single versus average, corrected for K
fig,ax = plt.subplots()
ax.plot(data.sumAnew,data.sumGroup,marker='o',ls='--',label='Single versus group, K corrected')
maxdata = data.sumGroup.max()
ax.plot([0,maxdata],[0,maxdata],c='r',ls=':',label='Reference line')
ax.set_xlabel('Single station')
ax.set_ylabel('Average of group')
fig.legend()
ax.set_title('Cumulative Mass Curve')





















