# -*- coding: utf-8 -*-

from ortools.sat.python import cp_model
import pandas as pd
import numpy as np

# model = cp_model.CpModel()

# var_upper_bound = 100000

# x1m1 = model.NewIntVar(0, var_upper_bound ,'x1m1')
# x2m1 = model.NewIntVar(0,var_upper_bound,'x2m1')
# x1m2 = model.NewIntVar(0,var_upper_bound,'x1m2')
# x2m2 = model.NewIntVar(0,var_upper_bound,'x2m2')
# x1m3 = model.NewIntVar(0,var_upper_bound,'x1m3')
# x2m3 = model.NewIntVar(0,var_upper_bound,'x2m3')
# x1m4 = model.NewIntVar(0,var_upper_bound,'x1m4')
# x2m4 = model.NewIntVar(0,var_upper_bound,'x2m4')

# x2m1sow = model.NewBoolVar('x2m1b')
# x2m2sow = model.NewBoolVar('x2m2b')
# x2m3sow = model.NewBoolVar('x2m3b')

# model.Add(x2m1>0).OnlyEnforceIf(x2m1sow)
# model.Add(x2m1==0).OnlyEnforceIf(x2m1sow.Not())
# model.Add(x2m2==0).OnlyEnforceIf(x2m2sow.Not()).OnlyEnforceIf(x2m1sow.Not())
# model.Add(x2m2>0).OnlyEnforceIf(x2m1sow)
# model.Add(x2m2>0).OnlyEnforceIf(x2m2sow)
# model.Add(x2m3>0).OnlyEnforceIf(x2m2sow)
# model.Add(x2m3>0).OnlyEnforceIf(x2m3sow)
# model.Add(x2m4>0).OnlyEnforceIf(x2m3sow)
# model.Add(x2m4==0).OnlyEnforceIf(x2m3sow.Not()) #for our 4month system: not possible to have m4 if you did not sow in m3

# model.Add(x2m2==x2m1).OnlyEnforceIf(x2m1sow)
# model.Add(x2m3==x2m2).OnlyEnforceIf(x2m2sow)
# model.Add(x2m4==x2m3).OnlyEnforceIf(x2m3sow)

# model.Add(x2m2sow==0).OnlyEnforceIf(x2m1sow)
# model.Add(x2m3sow==0).OnlyEnforceIf(x2m2sow)

# # Water maximum
# model.Add(3 * x1m1 + 2 * x2m1 <= 1000)
# model.Add(3 * x1m2 + 2 * x2m2 <= 1000)
# model.Add(3 * x1m3 + 2 * x2m3 <= 1000)
# model.Add(3 * x1m4 + 2 * x2m4 <= 1000)

# model.Maximize(12 * (x1m1 + x1m2 + x1m3 + x1m4) + 20 / 2 * (x2m1 + x2m2 + x2m3 + x2m4))

# solver = cp_model.CpSolver()
# status = solver.Solve(model)

# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
#     print(f'x1m1 = {solver.Value(x1m1)}')
#     print(f'x1m2 = {solver.Value(x1m2)}')
#     print(f'x1m3 = {solver.Value(x1m3)}')
#     print(f'x1m4 = {solver.Value(x1m4)}')
#     print(f'x2m1 = {solver.Value(x2m1)}')
#     print(f'x2m2 = {solver.Value(x2m2)}')
#     print(f'x2m3 = {solver.Value(x2m3)}')
#     print(f'x2m4 = {solver.Value(x2m4)}')
# else:
#     print('No solution found.')
    

# from ortools.sat.python import cp_model
model = cp_model.CpModel()

var_upper_bound = 100000

# Create the variables
crops = ['x1','x2','x3','x4','x5','x6','x7','x8']
months = str(list(range(1,13)))[1:-1].split(', ')
cropvars = {}
sowvars = {}
for crop in crops:
    for month in months:
        cropvar = crop+'m'+month
        sowvar = crop+'m'+month+'sow'
        cropvars[cropvar] = model.NewIntVar(0, var_upper_bound ,cropvar)
        sowvars[cropvar] = model.NewBoolVar(sowvar)

cropcycle = dict(zip(crops,[3,4,4,4,5,12,4,4]))

cropsDf = pd.DataFrame({'names':cropvars.keys(),'variables':cropvars.values()}).set_index('names')

waterconstraint = np.array([32,31,27,300,32,58,26,35])
profit = [74750,38711,93600,192805,90060,135919,62483,123744]

cropsDf['crop'] = cropsDf.index.str.slice(stop=2)
cropsDf['month'] = cropsDf.index.str.slice(start=2)
cropsDf['waterconstraint'] = cropsDf.crop.replace(crops,waterconstraint)
cropsDf['profit'] = cropsDf.crop.replace(crops,profit)
cropsDf['cropcycle'] = cropsDf.crop.replace(crops,cropcycle.values())

# create water constraints
for month in months:
    monthname = 'm'+month
    multiply = cropsDf.variables*cropsDf.waterconstraint
    monthmultiply = multiply[cropsDf.index.str.slice(2)==monthname]
    model.Add(sum(monthmultiply)<= 1706)

# sowing constraints

#### First month cannot have harvest if there was no sowing
for cropvar in cropsDf.index[cropsDf.month=='m1']:
    model.Add(cropsDf.crop[cropvar]==0).OnlyEnforceIf(sowvars[cropvar].Not())

#### depending on cropcycle: if crop is sown (sowvar[crop]==True), the following cropvars should be equal
#### Also, then all next sowvar[crop] should be false
for cropvar,sowvar in sowvars.items():
    crop = cropvar[:2]
    cycle = cropcycle[crop]
    month = cropvar[2:]
    monthno = int(month[1:])
    print('cycle length: '+str(cycle))
    for i in range(monthno+1,monthno+cycle):
        if i == 13:
            break
        varname = crop+'m'+str(i)
        model.Add(cropvars[cropvar]==cropvars[varname]).OnlyEnforceIf(sowvar)
        model.Add(sowvars[varname]==0).OnlyEnforceIf(sowvar)
        print('added '+cropvar+' should equal '+varname+' if sowvar['+cropvar+']',
              'and sowvar['+varname+'] should equal 0 if sowvar['+cropvar+']')

#### To be added: a month must be zero, if within it's preceding cropcycle all sowvariables are zero
# for cropvar in cropsDf.index[cropsDf.month.str.slice(start=1).astype(int)>4]:
#     cropcycle = cropsDf.cropcycle[cropvar]
#     if cropcycle == 3:
#         model.Add(cropvars[cropvar]==0).OnlyEnforceIf(sowvars[cropvar].Not()).OnlyEnforceIf(sowvars['x1m2'].Not()).OnlyEnforceIf(sowvars['x1m1'].Not())

model.Add(cropvars['x1m3']==0).OnlyEnforceIf(sowvars['x1m3'].Not()).OnlyEnforceIf(sowvars['x1m2'].Not()).OnlyEnforceIf(sowvars['x1m1'].Not())
    
### Weird constraints, just for trial
model.Add(cropvars['x8m5']==0)


# solve it
# to make up for crop cycles, //cropcycle
profitweight = cropsDf.profit//cropsDf.cropcycle
model.Maximize(sum(cropsDf.variables*profitweight))
solver = cp_model.CpSolver()
status = solver.Solve(model)

solveValues = []
for variable in cropsDf.variables:
    solveValues.append(solver.Value(variable))
    print(variable.Name()+': '+str(solver.Value(variable)))