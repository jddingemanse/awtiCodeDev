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

#Importing the data you want to feill  IMPORTANT NOTE YOU CAN GET THIS DATA FROM SHARED FILE Datap.xlsx

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
NX=np.mean([NA,NM,NC,NS])    #the normal annual rain fall of all


#code to calculate the normal ratio of each station, (PA=precipitation of arbaminch)
#(PM=precipitation of mirab),(PC=precipitation of chano),(PS=precipitation of shara)

PA=NX/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Chano.replace(np.nan,0)/NC+Data.Shara.replace(np.nan,0)/NS)
PM=NX/3*(Data.Arbaminch.replace(np.nan,0)/NA+Data.Chano.replace(np.nan,0)/NC+Data.Shara.replace(np.nan,0)/NS)
PC=NX/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Arbaminch.replace(np.nan,0)/NA+Data.Shara.replace(np.nan,0)/NS)
PS=NX/3*(Data.Mirab.replace(np.nan,0)/NM+Data.Chano.replace(np.nan,0)/NC+Data.Arbaminch.replace(np.nan,0)/NA)


# a code to fill the missing data via Normal Ratio merhod from the above formula

a=Data.fillna(value = {'Arbaminch':PA,'Mirab':PM,'Chano':PC,'Shara': PS})


# a code to save the filld data
a.to_excel('Normal_ratio.xlsx')  


#3) Inverse distance method

import pandas as pd
import numpy as np

#Importing the data you want to feill

Data =pd.read_excel('Datap.xlsx')

# The inverse distance method needs the distance b/n stations in km 
# if we know the the distance b/n stations in degree we can convert in to meter 1 degree=110km
# for this example randem number is used (not actual distance b/n station) but it is important to use the actual distance for other work

DAM=10   # MAM The distance b/n arbaminch and mirab(it is randon number not actual)
DAC=12   # DAC The distance b/n arbaminch and chano(it is randon number not actual)
DAS=14   # DAS The distance b/n arbaminch and shara(it is randon number not actual)
DMS=16   # DMS The distance b/n mirab and shara(it is randon number not actual)
DCM=18   # DCM The distance b/n chano and mirab(it is randon number not actual)
DCS=20   # DCS The distance b/n chano and shara(it is randon number not actual)

# a code to calculate missing data via inverse distance method
Parb=(Data.Mirab.replace(np.nan,0)/(DAM**2)+Data.Chano.replace(np.nan,0)/(DAC**2)+Data.Shara.replace(np.nan,0)/(DAS**2))/(1/(DAM**2)+1/(DAC**2)+1/(DAS**2))
Pmirab=( Data.Arbaminch.replace(np.nan,0)/(DAM**2)+Data.Chano.replace(np.nan,0)/(DCM**2)+Data.Shara.replace(np.nan,0)/(DMS**2))/(1/(DAM**2)+1/(DCM**2)+1/(DMS**2))
PCHANO=( Data.Arbaminch.replace(np.nan,0)/(DAC**2)+Data.Mirab.replace(np.nan,0)/(DCM**2)+Data.Shara.replace(np.nan,0)/(DCS**2))/(1/(DAC**2)+1/(DCM**2)+1/(DCS**2))
PSHARA=(Data.Arbaminch.replace(np.nan,0)/(DAS**2)+Data.Mirab.replace(np.nan,0)/(DMS**2)+Data.Chano.replace(np.nan,0)/(DCS**2))/(1/(DAS**2)+1/(DMS**2)+1/(DCS**2))

# a code to fill missing data via inverse disatnce method from the above calculated formula

Data.fillna(value = {'Arbaminch':Parb,'Mirab':Pmirab,'Chano':PCHANO,'Shara': PSHARA})











