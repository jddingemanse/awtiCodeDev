# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 18:52:11 2022

@author: Demiso
"""
#Optimizations using calculus
# Optimization of a Function of a Single Variable 
# Step-1: Finding Stationary points
        # Method 1:The solvers module in SymPy implements methods for solving equations.
"""
Use solve() to solve algebraic equations.
f = X**2+5*X+6--this is an example to be solved
"""
# Step-1: Finding Stationary points
from sympy.solvers import solve
from sympy import Symbol
X = Symbol('X')
Stationary_points = solve(X**2+5*X+6, X)
print('Stationary points are' +'=' + str(Stationary_points))

# Step-2: Decide Stationary points [wether it is max, min, or saddle]
"""
This is a necessary condition for f(x) to be a maximum or minimum at x==stationary pnt.
Sufficient condition is examined as follows:
1. If d2f/dx2>0 for all x, f(x) is convex and the stationary point is a global minimum.
2. If d2f/dx2<0 for all x, f(x) is concave and the stationary point is a global maximum.
3. If d2f/dx2=0, we should investigate further.
    find the first non zero higher order derivative. 
    Let this be the derivative of nth order.
    Thus, at the stationary point, x =xo

    dnf/dxn<,=,>0

    A. If n is even, xo is a local minimum or a local maximum.
        If dnf/dxn |xo> 0, xo is a local minimum 
        If dnf/dxn |xo< 0, xo is a local maximum
    B. If n is odd, xo is a saddle point.

--Let df,dff = first derivative and second derivative respectivily--
Note: The first parameter of the diff function should be the function you want to take the derivative of. 
    The second parameter should be the variable you are taking the derivative with respect to.
"""
import sympy as sym
X = sym.symbols('X')
f = X**2+5*X+6
dff  = sym.diff(f,X,2)  #The number '2' endicates second order derivatives
dfff = sym.diff(f,X,3) #The number '3' endicates second order derivatives
dffff = sym.diff(f,X,4) #The number '4' endicates second order derivatives
if dff.subs(X,Stationary_points[:]) > 0: #Needs modification at stationary_point[:]
    print ('The fuction is convex and stationary point is a global minimum.')
elif dff.subs(X,Stationary_points[:]) < 0:
    print('The function is concave and stationary point is a global maximum.')
else:
    if dff.subs(X,Stationary_points[:])==0:
        if ((dfff.subs(X,Stationary_points[:]) > 0)&(3%2==0)): # '3' third order derivative
            print('The function is convex and stationary point is local minimum.')
        elif ((dfff.subs(X,Stationary_points[:]) < 0)&(3%2==0)):
            print('The function is concave and stationary point is local maximum')
        else:
            print('Stationary point is saddle point')
            
    
