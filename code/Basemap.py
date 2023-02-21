
# -*- coding: utf-8 -*-
"""
Created on Tue feb 21 09:31:51 2023

@author: israel

"""

#This is a code to generate a base map(Global and to the area of interest) so that we can visualize our data(i.e Numerical forecast product, soil data and etc.... on a map).

#First, create a new environment in anaconda prompt by typing           


#conda create --name basemap

#then  type 

#conda activate basemap then 

#install the  required package  in a new environment  type

#conda install -c conda-forge basemap

#conda install -c conda-forge jupyter


#open jupyter notebook

#import the attached script in your notebook

#pls, let me know if there is a challenge...


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


fig = plt.figure(figsize = (12,12)) 
m = Basemap()
m.drawcoastlines()
plt.title("Coastlines", fontsize=20)
plt.show()

#let us add the color
fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='dashed', color='red')
plt.title("Coastlines", fontsize=20)
plt.show()

# let see the Country boundaries

fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries()
plt.title("Country boundaries", fontsize=20)
plt.show()


fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries(linewidth=1.0, linestyle='solid', color='k')
plt.title("Country boundaries", fontsize=20)
plt.show()


#  let add the Major rivers

fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries(linewidth=1.0, linestyle='solid', color='k')
m.drawrivers(linewidth=0.5, linestyle='solid', color='#0000ff')
plt.title("Major rivers", fontsize=20)
plt.show()

# to generate Color filled continents

fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries(linewidth=1.0, linestyle='solid', color='k')
m.fillcontinents()
plt.title("Color filled continents", fontsize=20)
plt.show()

# to add color

fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries(linewidth=1.0, linestyle='solid', color='k')
m.fillcontinents(color='coral',lake_color='aqua', alpha=0.9)
plt.title("Color filled continents", fontsize=20)
plt.show()

#to add lat and long and Grids

fig = plt.figure(figsize = (12,12))
m = Basemap()
m.drawcoastlines(linewidth=1.0, linestyle='solid', color='black')
m.drawcountries(linewidth=1.0, linestyle='solid', color='k')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmeridians(range(0, 360, 20), color='k', linewidth=1.0, dashes=[4, 4], labels=[0, 0, 0, 1])
m.drawparallels(range(-90, 100, 10), color='k', linewidth=1.0, dashes=[4, 4], labels=[1, 0, 0, 0])
plt.ylabel("Latitude", fontsize=15, labelpad=35)
plt.xlabel("Longitude", fontsize=15, labelpad=20)
plt.show()

#to see Orthographic Projection

fig = plt.figure(figsize = (10,8))
m = Basemap(projection='ortho', lon_0 = 25, lat_0 = 10)
m.drawcoastlines()
m.fillcontinents(color='tan',lake_color='lightblue')
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
m.drawmapboundary(fill_color='lightblue')
plt.title("Orthographic Projection", fontsize=18)

#to see Robinson Projection

fig = plt.figure(figsize = (10,8))
m = Basemap(projection='robin',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180, lon_0 = 0, lat_0 = 0)
m.drawcoastlines()
m.fillcontinents(color='tan',lake_color='lightblue')
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
m.drawmapboundary(fill_color='lightblue')
plt.title(" Robinson Projection", fontsize=20)

# to see Robinson Projection

fig = plt.figure(figsize = (10,8))
m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180)
m.drawcoastlines()
m.fillcontinents(color='tan',lake_color='lightblue')
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
m.drawmapboundary(fill_color='lightblue')
plt.title("Mercator Projection", fontsize=20)

# basemap for ethiopia

m = Basemap(projection='cyl',llcrnrlon=32.5,llcrnrlat=3,urcrnrlon=49,urcrnrlat=15)
m.drawcoastlines()
m.fillcontinents(color='tan',lake_color='lightblue')
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
m.drawmapboundary(fill_color='lightblue')
m.drawcoastlines()
plt.show()

# basemap for ethiopia zoomout

fig = plt.figure(figsize = (10,8))
m = Basemap(llcrnrlon=32.5,llcrnrlat=3,urcrnrlon=48.5, urcrnrlat=15, lat_0=7, lon_0 =37, resolution = 'l')
m.drawcoastlines()
m.fillcontinents(color='tan',lake_color='lightblue')
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
m.drawmapboundary(fill_color='lightblue')
plt.title("Make a regional map using the EPSG projection code", fontsize=18)

# basemap for ethiopia zoomout with Land-sea mask image

fig = plt.figure(figsize = (10,8))
m = Basemap(projection='cyl',llcrnrlon=32.5,llcrnrlat=3,urcrnrlon=49,urcrnrlat=15, resolution = 'l')
m.drawlsmask(land_color = "#ddaa66", ocean_color="#7777ff", resolution = 'i', lakes=True, grid=1.25)
m.drawcountries(linewidth=1, linestyle='solid', color='k' ) 
plt.title("Land-sea mask image", fontsize=20)
plt.show()



