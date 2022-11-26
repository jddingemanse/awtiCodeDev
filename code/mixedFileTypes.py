# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 10:29:13 2022

@author: jandirk
"""

import pandas as pd
import numpy as np
import math

def ncDataSelect(dataset,coord,method='closest',timeperiod=None,data_var=None):
    """
    This function selects data from a NetCDF file based on the provided coordinates. It can be used,for example, to select data of a NetCDF file at the same location as a measurement station.

    Parameters
    ----------
    dataset : Xarray DataSet
        This should be a dataset (typically the result of a NetCDF file) with at least one data_var, and this data_var should have three dimensions: time, latitude and longitude.
    coord : 2-sized collection of lat,lon coordinate.
        Provide the coordinate as (lat,lon) for which you want to select data from the provided DataSet.
    method : str, optional
        One of {'m1','closest','m2','average','m3','idw'}. The default is 'closest'.
        Based on the provided coordinate, 4 surrounding coordinates from the DataSet are selected.
        m1/closest: select the closest coordinate.
        m2/average: take the average of the 4 surrounding coordinates.
        m3/idw: take the inverse distance weighted average of the 4 surrounding coordinates.
    timeperiod : 2-sized collection of datetimes (starttime,endtime), optional
        NOT YET IMPLEMENTED. The default is None.
    data_var : str, optional
        If the provided DataSet has multiple data_vars, you can select a specific one here. The default is None. If None, automatically the first of dataset.data_vars is selected.

    Returns
    -------
    dfOut : Pandas DataFrame
        A single column DataFrame, indexed by time, with as column the selected data.

    """
    coord = np.array(coord)
    latdim = np.array(dataset.dims)[pd.Series(dataset.dims.keys()).str.find('at')>-1][0]
    londim = np.array(dataset.dims)[pd.Series(dataset.dims.keys()).str.find('on')>-1][0]
    timedim = np.array(dataset.dims)[pd.Series(dataset.dims.keys()).str.find('im')>-1][0]
    
    lats = dataset[latdim]
    lons = dataset[londim]
    minLat = np.max(lats[lats<coord[0]])
    maxLat = np.min(lats[lats>coord[0]])
    minLon = np.max(lons[lons<coord[1]])
    maxLon = np.min(lons[lons>coord[1]])
    
    coords = np.array([coord,[minLat,minLon],[minLat,maxLon],[maxLat,minLon],[maxLat,maxLon]])

    data_vars = np.array(dataset.data_vars)
    if data_var == None:
        data_var = data_vars[0]
        print('data variable not selected. This dataset has '+str(data_vars)+'. Using '+data_var+'.')
    elif data_var not in data_vars:
        print(data_var+' not found in dataset. This dataset has '+str(data_vars)+'. Using '+str(data_vars[0])+'.')
        data_var = data_vars[0]
    else:
        print(data_var+' selected to use.')

    # Calculate distances to the four points
    distances = []
    for coord in coords[1:]:
        dist = math.dist(coords[0],coord)
        distances.append(dist)
    distances = np.array(distances)

    if method in ['m1','closest']:
        iClose = list(distances).index(min(distances))
        cClose = coords[iClose+1]
        dataOut = dataset.sel({latdim:cClose[0],londim:cClose[1]})[data_var]
    elif method in ['m2','average']:
        selData = dataset.sel({latdim:[minLat,maxLat],londim:[minLon,maxLon]})
        dataOut = selData.mean(dim=(latdim,londim))[data_var]
    elif method in ['m3','idw']:
        selData = dataset.sel({latdim:[minLat,maxLat],londim:[minLon,maxLon]})
        reshape = selData[data_var].shape[:1]+(selData[data_var].shape[1]*selData[data_var].shape[2],)
        arrayData = np.array(selData[data_var]).reshape(reshape)
        weights = []
        for i in range(len(distances)):
            weight = (1/distances[i])/np.sum(1/distances)
            weights.append(weight)
        weights=np.array(weights).reshape((1,4))
        dataOut = np.sum(arrayData*weights,axis=1)
    else:
        print('Method '+str(method)+' unknown. Please select from one of "m1", "closest", "m2", "average", "m3", "idw".')
        return

    dfOut = pd.DataFrame({data_var:dataOut},index=dataset[timedim])
    return dfOut

def alignStationNc(stationdata,ncdata,resample='m'):
    stationresampled = stationdata.resample(rule=resample).mean()
    aligned = stationresampled.copy()
    ncresampled = ncdata.resample(rule=resample).mean()
    aligned.loc[:,'ncdata'] = ncresampled.iloc[:,0]
    return aligned
   
def upsampleData(data1,data2,timestep1='D',timestep2='m'):
    data1.set_axis(['data1raw'],axis=1,inplace=True)
    data1 = data1.resample(rule=timestep1).mean()
    data2 = data2.resample(rule=timestep2).mean().loc[data1.index.min():data1.index.max()]
    data2 = data2.fillna(-999)
    data1['data2res'] = data2.resample(rule=timestep1).mean()
    data1.loc[:,'data2res']=data1.data2res.fillna(method='bfill').replace(-999,np.nan)
    data1avg = data1.data1raw.resample(rule=timestep2).mean().fillna(-999)
    data1['avgfilled'] = data1avg
    data1.loc[:,'avgfilled'] = data1.avgfilled.fillna(method='bfill').replace(-999,np.nan)
    data1.loc[:,'weights'] = data1.data1raw/data1.avgfilled
    data1['data2upsampled'] = data1.data2res*data1.weights
    
    dataOut = data1.get(['data1raw','data2upsampled'])
    return dataOut
