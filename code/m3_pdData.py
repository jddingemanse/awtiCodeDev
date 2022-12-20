# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 13:28:25 2021

@author: jandi
"""
import pandas as pd
import numpy as np

##1 IMPORT DATA
meteoData=pd.read_csv('data/m3_meteoData.csv')
meteoDatatxt=pd.read_csv('data/m3_meteoData.txt',sep='\t')
meteoDataExcel=pd.read_excel('data/m3_meteoData.xlsx',sheet_name='Sheet1')

##2 ACCESSING
#Get one Series
meteoData['Temp_Out']
meteoData.Temp_Out #This only works for Series with a name without spaces
#Get one row
meteoData.loc[500]
#Get one 'cell'
meteoData.Temp_Out[500]
meteoData.loc[500]['Temp_Out']
#Get multiple rows
meteoData.loc[500:515]
#Get multiple columns
meteoData.get(['Datetime','Temp_Out','Windspeed'])
#Get multiple rows and columns
meteoData.get(['Datetime','Temp_Out','Windspeed']).loc[500:515]
#Get data only for rows with some conditions
#For example, only the rows in which meteoData.Temp_Out<15
meteoData.loc[meteoData.Temp_Out<15]
meteoData.loc[meteoData.Temp_Out<15].get(['Datetime','Temp_Out','Windspeed'])

##3 CHANGING
#Renaming all indices
meteoData.set_axis(meteoData.Datetime,0)
#Renaming only some indices or Series
meteoData.rename(columns={'Datetime':'date and time','Temp_Out':'temperature'})
#Deleting some column(s) or row(s)
meteoData.drop(index=[0,1,2])
meteoData.drop(columns=['AirDensity','ET '])

#Adding a column
meteoData['temperatureK'] = meteoData.Temp_Out+273.15

##4 CREATING
df1 = pd.DataFrame({'name1':(1,2,3),'name2':[4,5,6]})
df2 = pd.DataFrame({'datetime':meteoData.Datetime,'temperature':meteoData.Temp_Out})

##5 TIME DATA
# Timestamps and timedeltas
meteoData['Timestamp']=pd.to_datetime(meteoData.Datetime,dayfirst=True)
max(meteoData.Timestamp)
totalTime = max(meteoData.Timestamp) - min(meteoData.Timestamp)
dayDelta = pd.to_timedelta(1,unit='day')
weekDelta = dayDelta * 7

# The method .resample
weekAvg=meteoData.resample(rule='H',on='Timestamp').mean()

##6 EXPORTING
weekAvg.to_csv('output/meteoDataWeek.csv')
weekAvg.to_excel('output/meteoDataWeek.xlsx',sheet_name='WeekAverages')
    
