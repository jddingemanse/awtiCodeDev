# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:13:54 2023

@author: Behafta
"""

import pandas as pd
import numpy as np

#COMPUATION OF ETO USING HARGREAVES AND SAMANI(1985) METHOD 

Data =pd.read_csv('data/Eto13.csv')
Data.loc[:,'Date'] = pd.to_datetime(Data.Date)

# Calculation for one
fi = 0.11
J = Data.Date.dt.dayofyear[0]
d = 0.409*np.sin((2*np.pi*J/365)-1.39)
ws = np.arccos(-np.tan(fi)*np.tan(d))
dr = 1 + 0.033*np.cos((2*np.pi/365)*J)
Gsc = 0.082
Ra =(1440/np.pi)* Gsc*dr*(ws*np.sin(fi)*np.sin(d) + np.cos(fi)*np.cos(d)*np.sin(ws))
ETo =(0.0023)* Ra*(Data.Tmean[0] + 1.78)*np.sqrt(Data.Tmax[0] - Data.Tmin[0])

# turning it into a function
def calculateETo(J,Tmean,Tmax,Tmin):
    fi = 0.11
    d = 0.409*np.sin((2*np.pi*J/365)-1.39)
    ws = np.arccos((-np.tan(fi)*np.tan(d)))
    dr = 1 + 0.033*np.cos((2*np.pi/365)*J)
    Gsc = 0.082
    Ra =(1440/np.pi)* Gsc*dr*(ws*np.sin(fi)*np.sin(d) + np.cos(fi)*np.cos(d)*np.sin(ws))
    ETo =(0.0023)* Ra*(Tmean + 1.78)*np.sqrt(Tmax - Tmin)
    return ETo

for i in Data.index:
    J = Data.Date.dt.dayofyear[i]
    Tmin = Data.Tmin[i]
    Tmax = Data.Tmax[i]
    Tmean = Data.Tmean[i]
    ETo = calculateETo(J,Tmean,Tmax,Tmin)
    Data.loc[i,'ETo'] = ETo


Data.to_csv('output/ETO2.csv')
Data.to_excel('output/ETO_HARGREAVES.xlsx')

 
