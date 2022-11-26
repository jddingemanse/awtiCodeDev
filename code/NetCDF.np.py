# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 01:31:10 2022

@author: user
"""


import numpy as np

##1 NC to CSV
import xarray as xr
ds = xr.open_dataset('data/pr_RCA4.nc')
df = ds.to_dataframe()
df.to_csv('output/pr_RCA4.csv')

ds.history    
ds.dims
ds.data_vars
ds.keys()

ds['rlon']
ds.rlon
ds.rlat.dims
ds.pr.dims
ds.rlon.attrs

ds.pr.shape
ds.pr.size

ds.close()


import xarray as xr
import pandas as pd
ds=xr.open_dataset('data/pr_RCA4.nc')

latmin,latmax,lonmin,lonmax=5,6,37,38
dsku = ds.pr[:,(ds.rlat>latmin)&(ds.rlat<latmax),(ds.rlon>lonmin)&(ds.rlon<lonmax)]

startTime=pd.to_datetime('2011-01-01')
endTime = pd.to_datetime('2012-01-01')
dsku_1yr = dsku[(dsku.time>=startTime)&(dsku.time<endTime)]
dfku = dsku_1yr.to_dataframe()
dfku.to_csv('output/dfku.csv')

timeAvg = np.mean(dsku_1yr,axis=(1,2))
locAvg = np.mean(dsku_1yr,axis=0)

import matplotlib.pyplot as plt
%matplotlib
fig,ax=plt.subplots()
locAvg.plot(ax=ax,cmap='coolwarm')

fig,ax=plt.subplots()
timeAvg.plot(ax=ax)




