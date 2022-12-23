# -*- coding: utf-8 -*-

from ortools.sat.python import cp_model
import pandas as pd
import numpy as np


# from ortools.sat.python import cp_model
model = cp_model.CpModel()


# Settings
crops = ['x1','x2','x3','x4','x5','x6','x7','x8']
cropcycle = dict(zip(crops,[3,4,4,4,5,12,4,4]))
no_months = 12
waterconstraint = np.array([32,31,27,30,32,58,26,35])
profit = [74750,38711,93600,192805,90060,135919,62483,123744]
available_water_per_month = [1706]*no_months


# Create the variables
var_upper_bound = 100000
months = str(list(range(1,no_months+1)))[1:-1].split(', ')
cropvars = {}
sowvars = {}
for crop in crops:
    for month in months:
        cropvar = crop+'m'+month
        sowvar = crop+'m'+month+'sow'
        cropvars[cropvar] = model.NewIntVar(0, var_upper_bound ,cropvar)
        sowvars[cropvar] = model.NewBoolVar(sowvar)

cropsDf = pd.DataFrame({'names':cropvars.keys(),'variables':cropvars.values()}).set_index('names')

cropsDf['crop'] = cropsDf.index.str.slice(stop=2)
cropsDf['month'] = cropsDf.index.str.slice(start=2)
cropsDf['waterconstraint'] = cropsDf.crop.replace(crops,waterconstraint)
cropsDf['profit'] = cropsDf.crop.replace(crops,profit)
cropsDf['cropcycle'] = cropsDf.crop.replace(crops,cropcycle.values())
cropsDf['monthInt'] = cropsDf.month.str.slice(1).astype(int)


# create water constraints
for i, month in enumerate(months):
    monthname = 'm'+month
    multiply = cropsDf.variables*cropsDf.waterconstraint
    monthmultiply = multiply[cropsDf.index.str.slice(2)==monthname]
    model.Add(sum(monthmultiply)<= available_water_per_month[i])


# sowing constraints

#### Depending on cropcycle: if crop is sown (sowvar[crop]==True), the following cropvars should be equal
#### Also, then all next sowvar[crop] should be false
for cropvar,sowvar in sowvars.items():          # Take all cropvars and sowvars one by one
    crop = cropvar[:2]                          # Take cropname
    cycle = cropcycle[crop]                     # Take cycle that matches cropname
    month = cropvar[2:]                         # Take month from cropvar
    monthno = int(month[1:])                    # Take month as integer
    print('cycle length: '+str(cycle))
    for i in range(monthno+1,monthno+cycle):    # Go over all months succeeding the cropvar month 
        if i == no_months+1:                             # Break if outside of 12 month range
            break
        varname = crop+'m'+str(i)               # Create cropvar names succeeding the cropvar 
        model.Add(cropvars[cropvar]==cropvars[varname]).OnlyEnforceIf(sowvar)   # Succeeding months must be 
                                                                                # equal to cropvar month when
                                                                                # sowvar of original month 
                                                                                # is true.
        model.Add(sowvars[varname]==0).OnlyEnforceIf(sowvar)    # Succeeding sowvars must be False because 
                                                                # you cannot sow again on same ground until
                                                                # cropcycle is finished.
        print('added '+cropvar+' should equal '+varname+' if sowvar['+cropvar+']',
              'and sowvar['+varname+'] should equal 0 if sowvar['+cropvar+']')


#### A month must be zero, if within it's preceding cropcycle all sowvariables are zero or own sowvar is zero
for cropvar, sowvar in sowvars.items():         # Go over all cropvars
    crop = cropvar[:2]                          # Take cropname
    cycle = cropcycle[crop]                     # Take cycle that matches cropname
    month = cropvar[2:]                         # Take month from cropvar
    monthno = int(month[1:])                    # Take month as integer
    print('cropvar: '+cropvar)
    print('cycle length: '+str(cycle))
    
    constraint = f'model.Add(cropvars[\'{cropvar}\']==0)'       # Start basic constraint string

    for i in list(range(monthno-cycle+1, monthno+1))[::-1]:   # For the length of cropcycle, go over all preceding cropvars (limited by size of year) 
        if i <= 0: 
            break
        varname = crop + 'm' + str(i)
        constraint = constraint + f'.OnlyEnforceIf(sowvars[\'{varname}\'].Not())'   
                # Add OnlyEnforceIf(sowvars[preceding_cropvar].Not()) to constraint string
    print(constraint) 
    exec(constraint)    # Execute constraint string


#### A month cannot be zero, if the corresponding sowvariable is one
for cropvar, sowvar in sowvars.items():
    model.Add(cropvars[cropvar]>0).OnlyEnforceIf(sowvar)
    print(f'model.Add(cropvars[{cropvar}]>0).OnlyEnforceIf({sowvar})')
  
    
#### You cannot sow when cropcycle does not fit into the remaining year
for cropvar, sowvar in sowvars.items():         # Go over all cropvars
    crop = cropvar[:2]                          # Take cropname
    cycle = cropcycle[crop]                     # Take cycle that matches cropname
    month = cropvar[2:]                         # Take month from cropvar
    monthno = int(month[1:])                    # Take month as integer

    if monthno + cycle - 1 > no_months:
        model.Add(sowvar==0)
    
    
### Weird constraints, just for trial
# model.Add(cropvars['x4m6']==0)


# solve it
# to make up for crop cycles, //cropcycle
profitweight = cropsDf.profit//cropsDf.cropcycle
model.Maximize(sum(cropsDf.variables*profitweight))
solver = cp_model.CpSolver()
status = solver.Solve(model)

for name,variable in zip(cropsDf.index,cropsDf.variables):
    print(name+': '+str(solver.Value(variable))+'\t\t'+sowvars[name].Name()+': '
          +str(solver.Value(sowvars[variable.Name()])))
    cropsDf.loc[name,'hectare'] = solver.Value(variable)
    cropsDf.loc[name,'result'] = str((solver.Value(sowvars[name]),solver.Value(variable)))

cropsResult = cropsDf.pivot(index='monthInt',columns='crop',values='result')
cropsResult

import seaborn as sn
%matplotlib
sn.heatmap(cropsDf.pivot(index='monthInt',columns='crop',values='hectare'),cmap='coolwarm')

