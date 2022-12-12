# -*- coding: utf-8 -*-
# small change for test of pushing
def tempFtoK(tempF):
    """Input Fahrenheit, get Kelvin"""
    tempK = (tempF + 459.67)*5/9
    print('The temperature is: '+str(tempK)+'K')
    return tempK

def waterFlow(A,V):
    Q=A*V
    return Q

def pollution(Cprev,Cin,Q,KS=0.001,V=10000):
    VdC = Q*(Cin-Cprev)-KS*V*Cprev
    VCnew = V*Cprev+VdC
    Cnew = VCnew/V
    return Cnew

def nameSelect():
    import pandas as pd
    import random
    names = pd.read_csv('data/ParticipantNames.csv')
    name = random.choice(names.Name)
    print('For this task, '+name.upper()+' is randomly selected!')

def testFunction():
    print('test')