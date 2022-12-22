# -*- coding: utf-8 -*-

import numpy as np
from sympy import symbols,Eq,linsolve
import pandas as pd

# You can quickly make four symbols with the function symbols
h0,h1,h2,h3 = symbols('h:4')

# The equation -4*h0 + h1 + h2 + 27=0, and 3 others, can be made with the function Eq
Eq1 = Eq(-4*h0 + h1 + h2 + 27, 0)
Eq2 = Eq(h0 - 4*h1 + h3 + 10, 0)
Eq3 = Eq(h0 - 4*h2 + h3 + 30, 0)
Eq4 = Eq(h1 + h2 - 4*h3 + 9, 0)

# A system of linear equations can be solved with linsolve
linsolve([Eq1,Eq2,Eq3,Eq4],[h0,h1,h2,h3])

# To put all nicely in a DataFrame together:
eqlist = [Eq1,Eq2,Eq3,Eq4]
symbollist = [h0,h1,h2,h3]

output = linsolve(eqlist,symbollist)
dfOut=pd.DataFrame({'symbols':symbollist,'output':tuple(output)[0]})
dfOut.loc[:,'solution'] = dfOut.output.astype(float)
dfOut