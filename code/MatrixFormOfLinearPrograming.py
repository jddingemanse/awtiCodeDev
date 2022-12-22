# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 21:45:00 2022

@author: Demiso
"""
''''
Example of system of linear equation
# 3x - 9y = -42
# 2x + 4y = 2
It is easy and much more simpler if we solve system of
Linear Equation using matrix form.
Step-1:
    Prepare a matrix from list of list using numpay function
    For instance: M = np.array([[1,2],[3,4]]) #this is matrix.
    Thus, We can solve the above equations numpy function easly.
Step-2:
    Follow the matrix solving procedure to solve the equation.
    From matrix formula we have:
        [A][Z] = b  #Where:
                    [A] = matrix of the lefthand side
                    [Z] = the variables to be solved (unknown)
                    b   = right hand side numbers
        And then: We can easly solve the above equation as follows
        Anyone can change and add to make 3x3, 4x4, or above matrix
        And Anyone can follow to solve the matrix
Here are two examples 2X2 matrix and 3x3 matrix to be solved easly.
'''

# Example 1: The linier equation of two variables X & Y:
    # 3x - 9y = -42
    # 2x + 4y = 2
import numpy as np    ##Numpay function
A = np.array([[3,-9], [2,4]]) ##Matrix of lefthand side of equation
b = np.array([-42,2])         ## Martix of righthand side of equat.
z = np.linalg.solve(A,b)      ## Solving procedure
print(z)                      ## Answer or solutions

# Example 1: The linier equation of three variables X, Y & Z:
    # 3x + y  - 2z = 6
    # 1x + 2y + 1z = 1
    # 2x - y - z   = 1

M = np.array([ [3,1,-2], [1,2,1], [2,-1,-1]])
c = np.array([6,1,1])
y = np.linalg.solve(M,c)
print(y)

# Example 1: The linier equation of four variables h0, h1, h2, & h3:
    # -4*h0 + 1*h1  + 1*h2 + 0*h3 = -27
    # +1*h0 - 4*h1 + 0*h2 + 1*h3 = -10
    # +1*h0 + 0*h1 - 4*h2 + 1*h3 = -30
    # +0*h0 + 1*h1 + 1*h2 - 4*h3 = -9

A = np.array([[-4,1,1,0],[1,-4,0,1],[1,0,-4,1],[0,1,1,-4]])
B = np.array([-27,-10,-30,-9])
Z = np.linalg.solve(A, B)
print (Z)

