# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:03:58 2023

@author: user
"""

import pandas as pd
import numpy as np

#A number of methods are available for estimating missing rainfall data. 
#this is  inverse distance method
 
#Ak   BT  We  Sh  Be smon@S1221
#32   20  19  24  30  these are the distance beteewn each stations. 

RF_Data2=pd.read_csv('data/RF_Data2.csv')
RF = pd.read_csv('data/RF_Data2.csv',na_values='na')

def fillingIDW(inputCols,distances):
    distances = np.array(distances)
    distSq = (distances**2).reshape((1,len(distances)))
    filled = (inputCols/distSq).sum(axis=1)/np.sum(1/distSq)
    return filled
#in  Ak station no missing data.

#filling  missing data for BT station by inverse distance method 
BTInput = RF.iloc[:,[1,3,4,5]]
BTDists = [32,19,24,30]
BTFillData = fillingIDW(BTInput,BTDists)
BTfilled2 = RF.BT.fillna(fillingIDW(BTInput,BTDists))

## EXPORTING
BTfilled2.to_csv('output/BTfill.csv')
BTfilled2.to_excel('output/BTfill.xlsx',sheet_name='BT')

#filling  missing data for We station by inverse distance method 

WeInput = RF.iloc[:,[1,2,4,5]]
WeDists = [32,20,24,30]
WeFillData = fillingIDW(WeInput,WeDists)
Wefilled2 = RF.We.fillna(fillingIDW(WeInput,WeDists))

## EXPORTING
Wefilled2.to_csv('output/Wefill.csv')
Wefilled2.to_excel('output/Wefill.xlsx',sheet_name='We')

#filling  missing data for Sh station by inverse distance method 

ShInput = RF.iloc[:,[1,2,3,5]]
ShDists = [32,20,19,30]
ShFillData = fillingIDW(ShInput,ShDists)
Shfilled2 = RF.Sh.fillna(fillingIDW(ShInput,ShDists))

##EXPORTING
Shfilled2.to_csv('output/Shfill.csv')
Shfilled2.to_excel('output/Shfill.xlsx',sheet_name='Be')

#filling  missing data for Be station by inverse distance method 

BeInput = RF.iloc[:,[1,2,3,4]]
BeDists = [32,20,19,24]
BeFillData = fillingIDW(BeInput,BeDists)
Befilled2 = RF.Be.fillna(fillingIDW(BeInput,BeDists))

## EXPORTING
Befilled2.to_csv('output/Befill.csv')
Befilled2.to_excel('output/Befill.xlsx',sheet_name='Be')