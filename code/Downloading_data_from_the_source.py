# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 08:21:44 2022

@author: Demiso
"""
#use this to download data from ftp

from ftplib import FTP
import os, sys, os.path
#Downloading
ftp = FTP('ftp.chc.ucsb.edu')
ftp.login()
#get 0.25 resolution files from CHRIPS
directory = '/pub/org/chg/products/CHIRPS-2.0/global_daily/netcdf/p25/'
print ('Changing to ' + directory)
ftp.cwd(directory)
filenames = ftp.nlst()
#first element in list is a monthly directory link
for filename in filenames[1:3]:
    local_filename = os.path.join('output', filename)
    print(local_filename)
    file = open(local_filename, 'wb')
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()
ftp.quit() #This is the 'polite' way to close a connenction
#Data analysis: This is depends up on the personal intersest and,
# mainy can be imported by the help of xarray.
#For instance,
import xarray as xr
ds = xr.open_dataset('output/chirps-v2.0.1981.days_p25.nc')

#trial Kulfo
latmin,latmax,lonmin,lonmax=5.5,6.5,37.3,37.8
Kulfo = ds.precip[:,(ds.latitude>latmin)&(ds.latitude<latmax),(ds.longitude>lonmin)&(ds.longitude<lonmax)]


