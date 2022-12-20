# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:50:12 2021

@author: jandi
"""
import numpy as np

##1 ARRAY BASICS
#Creating an array
array1 = np.array([1,2,3])
#Mathematical operations
array2 = array1*3 #All values of arr1 are multiplied with 3
array3 = array1+3 #All values of arr1 are increased with 3
#Logical operations
array4 = array1<3 #An array with booleans for each item of array1
array5 = array1[array4] #An array with only the items of arr1 for which arr2 was True
array6 = array1[array1<3] #Similar to array5; the step of array4 integrated

##2 EXAMPLE
#Creating lists of location names and (random) temperatures
locationList = ['Addis Ababa','Hawassa','Sodo','Arba Minch']*100
locationArray = np.array(locationList)
temperatureArray = np.random.randint(240,290,400)/10

#Creating an average for only the Arba Minch data
AM = locationArray=='Arba Minch'  #An array with booleans
AMtemp = temperatureArray[AM]
AMavg = np.mean(AMtemp)
#or, all in one step:
AMavg2 = np.mean(temperatureArray[locationArray=='Arba Minch'])