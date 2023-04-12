# -*- coding: utf-8 -*-
"""
Created on Thu Nov  17 04:33:14 2022

@author: Israel
"""

#Methods for Estimation of Missing Data
# 1) Arithmetic Mean Method
# 2) Normal Ratio Method
# 3)Inverse distance method

#1)Arithmetic Mean Method

import pandas as pd
import numpy as np

#Importing the data you want to fill  IMPORTANT NOTE YOU CAN GET THIS DATA FROM SHARED FILE Datap.xlsx

Data =pd.read_excel('Datap.xlsx')

#a code to calculate the mean for each row

fillseries = Data.get(['Arbaminch','Mirab','Chano','Shara']).mean(axis=1)

# a code to fill the missing data from the above calculated mean in each row

Data.fillna(value = {'Arbaminch':fillseries,'Mirab':fillseries,'Chano':fillseries,'Shara':fillseries})


#2) Normal Ratio Method

import pandas as pd
import numpy as np

#Importing the data you want to feill

Data =pd.read_excel('Datap.xlsx')


#Normal ratio method requares the normal anual rain fall of each neghaboring stations and 
#the mean annual rain fall of all stations(NX)

NA=Data['Arbaminch'].mean()  #the normal annual rain fall of arbaminch
NM=Data['Mirab'].mean()      #the normal annual rain fall of Mirab
NC=Data['Chano'].mean()      #the normal annual rain fall of Chano
NS=Data['Shara'].mean()      #the normal annual rain fall of Shara
#NX=np.mean([NA,NM,NC,NS])    #the normal annual rain fall of all


#code to calculate the normal ratio of each station, (PA=precipitation of arbaminch)
#(PM=precipitation of mirab),(PC=precipitation of chano),(PS=precipitation of shara)

PA=NA/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Chano.replace(np.nan,0)/NC+Data.Shara.replace(np.nan,0)/NS)
PM=NM/3*(Data.Arbaminch.replace(np.nan,0)/NA+Data.Chano.replace(np.nan,0)/NC+Data.Shara.replace(np.nan,0)/NS)
PC=NC/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Arbaminch.replace(np.nan,0)/NA+Data.Shara.replace(np.nan,0)/NS)
PS=NS/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Chano.replace(np.nan,0)/NC+Data.Arbaminch.replace(np.nan,0)/NA)

# a code to fill the missing data via Normal Ratio merhod from the above formula

a=Data.fillna(value = {'Arbaminch':PA,'Mirab':PM,'Chano':PC,'Shara': PS})

# a code to save the filld data
a.to_excel('Normal_ratio.xlsx')  

#3) Inverse distance method

import pandas as pd
import numpy as np

#Importing the data you want to fill

Data =pd.read_excel('Datap.xlsx')

# The inverse distance method needs the distance b/n stations in km 
# if we know the the distance b/n stations in degree we can convert in to meter 1 degree=110km
# for this example randem number is used (not actual distance b/n station) but it is important to use the actual distance for other work

#DAM=10   DAM The distance b/n arbaminch and mirab(it is randon number not actual)
#DAC=12   DAC The distance b/n arbaminch and chano(it is randon number not actual)
#DAS=14   DAS The distance b/n arbaminch and shara(it is randon number not actual)
#DMS=16   DMS The distance b/n mirab and shara(it is randon number not actual)
#DCM=18   DCM The distance b/n chano and mirab(it is randon number not actual)
#DCS=20   DCS The distance b/n chano and shara(it is randon number not actual)

# a code to calculate missing data via inverse distance method

def fillingIDW(inputCols,distances):
    distances = np.array(distances)
    distSq = (distances**2).reshape((1,len(distances)))
    filled = (inputCols/distSq).sum(axis=1)/np.sum(1/distSq)
    return filled

#filling  missing data for Arbaminch station by inverse distance method 
ArbaminchInput = Data .iloc[:,[2,3,4]]
ArbaminchDists = [10,12,14]
ArbaminchFillData = fillingIDW(ArbaminchInput,ArbaminchDists)
Arbaminchfilled2 = Data.Arbaminch.fillna(fillingIDW(ArbaminchInput,ArbaminchDists))

#filling  missing data for Mirab station by inverse distance method 

MirabInput = Data.iloc[:,[1,3,4]]
MirabDists = [10,18,16]
MirabFillData = fillingIDW(MirabInput,MirabDists)
Mirabfilled2 = Data.Mirab.fillna(fillingIDW(MirabInput,MirabDists))
 
#filling  missing data for Chano station by inverse distance method 

ChanoInput = Data.iloc[:,[1,2,4]]
ChanoDists = [12,18,20]
ChanoFillData = fillingIDW(ChanoInput,ChanoDists)
Chanofilled2 = Data.Chano.fillna(fillingIDW(ChanoInput,ChanoDists))

#filling  missing data for Shara station by inverse distance method 

 SharaInput = Data.iloc[:,[1,2,3]]
 SharaDists = [14,16,20]
 SharaFillData = fillingIDW( SharaInput,SharaDists)
 Sharafilled2 = Data.Shara.fillna(fillingIDW( SharaInput, SharaDists))
 
# a code to save the filld data

Final=Data.fillna(value = {'Arbaminch':Arbaminchfilled2,'Mirab':Mirabfilled2,'Chano':Chanofilled2,'Shara':  Sharafilled2})

#Finally save like this

Final.to_csv('output/FinalIDW.csv')
Final.to_excel('output/FinalIDW1.xlsx')









