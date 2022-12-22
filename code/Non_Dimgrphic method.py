# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 11:02:02 2022

@author: user
"""

import pandas as pd
import numpy as np
##Pi=Piave/pave*100

#Pi, is the none dimensional value of precipitation of the month in the station I,
#Pi, ave, is the over years averaged monthly precipitation for the station I, and      
#Pave, is overall years averaged yearly precipitation of the station i. 

Non_dim1=pd.read_csv('data/Non_dim1.csv')
Non_dim1.set_index('Month',inplace=True)
 
#then  Qualculate the orginal data by this formula Pi=Piave/pave*100

plotdata2 = Non_dim1 / Non_dim1.mean()*100
#saving the new data by csv format 
plotdata2.to_csv('data/plotdata2.csv')
plotdata2.set_axis(plotdata.Month,0)
import matplotlib.pyplot as plt
%matplotlib
import numpy as np
 #finally piloted by using  
fig,ax = plt.subplots()
ax.set_title('Homogeneity Test of Selected Rainfall Stations',c='r',size=10,fontstyle='italic',weight='extra bold')
ax.set_ylabel('Non-dimentsionalvalue')
ax.set_xlabel('Month')
ax.set_xticks(np.arange(0,12,1))
ax.set_xticks(np.arange(0.5,11,1),minor=True)
ax.set_xticklabels(plotdata2.Month)
ax.plot(plotdata2.ArbaMinch,c='k',label='ArbaMinch',ls='-')
ax.plot(plotdata2.Chincha,c='b',label='Chincha',lw=1,ls='-')
ax.plot(plotdata2.Zigit,c='r',label='Zigit',lw=1,ls='-')
fig.legend()
fig.savefig('output/figNondamional_graphi.jpg')

