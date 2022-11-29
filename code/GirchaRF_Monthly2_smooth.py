# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:42:08 2022

@author: Nebiyu
"""
# One of the reviewers of my submitted paper commented me to change the curved line to smooth. 
#This code is created to plot the smooth line instead of curved line. 
#You may also face such problems. In case this script will hopefully help you!

#Here both the curved line and smooth lines are plotted to see their difference.


import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
%matplotlib
import numpy as np
import pandas as pd

Smooth=pd.read_excel('output/GirchaSmooth.xlsx', sheet_name='Sheet1')
#Curved line 
fig,ax=plt.subplots()
ax.plot(Smooth.Date,Smooth.Hist, c='k',ls='--',label='Hist')
ax.plot(Smooth.Date,Smooth.Rain45,c='k',ls='--',label='RCP4.5')
ax.plot(Smooth.Date,Smooth.Rain85,c='red',label='RCP8.5')
ax.plot(Smooth.Date,Smooth.Obs,c='b',label='Obs')
ax.set_xlabel('Month')
ax.set_ylabel('Total Monthly Rainfall (mm)')
ax.set_title('Gircha Projected Rainfall for CCLM4 model')
fig.legend(loc='upper right')
fig.savefig('output/Projected_Gircha_Monthly1_curved.png', dpi=120)
plt.show()

#smooth line
X_Y_SplineH = make_interp_spline(Smooth.Date,Smooth.Hist)
X_Y_SplineO = make_interp_spline(Smooth.Date,Smooth.Obs)
X_Y_Spline45 = make_interp_spline(Smooth.Date,Smooth.Rain45)
X_Y_Spline85 = make_interp_spline(Smooth.Date,Smooth.Rain85)
x=np.linspace(Smooth.Date.min(),Smooth.Date.max())
yH=X_Y_SplineH(x)
yO=X_Y_SplineO(x)
y45=X_Y_Spline45(x)
y85=X_Y_Spline85(x)
fig,ax=plt.subplots()
ax.plot(x,yO,c='b',label='Obs')
ax.plot(x,yH, c='green', ls='-.',label='Hist')
ax.plot(x,y45, c='k',ls='--',label='RCP4.5')
ax.plot(x,y85, c='red',label='RCP8.5')
ax.set_xlabel('Month')
ax.set_ylabel('Total Monthly average Rainfall (mm)')
ax.set_title('Gircha Projected Rainfall for CCLM4 model')
plt.legend()
fig.savefig('output/Projected_Gircha_Monthly1_smooth.png', dpi=120)
plt.show()

