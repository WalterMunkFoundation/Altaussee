#%% Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import gsw

from os import listdir

# Collect the data and parse into a pandas dataframe

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/AllCastAwayFilew'
os.chdir(path) #change to the desired working directory
filenames = find_csv_filenames('./') #find the .csv files in the current folder

# Read in a specified file
# filenames = 'CC2040004_20210605_095056.csv'

Tmp = []
Den = []
Dpth = []
Press = []
Lat = []
Lon = []
for filename in filenames:
    dfh = pd.read_csv(filename, nrows=27) # Read the header (assuming 27 rows)
    lat = dfh[dfh['% Device'].str.contains('Start latitude')].values[0,1]
    lon = dfh[dfh['% Device'].str.contains('Start longitude')].values[0,1]
    df = pd.read_csv(filename, header=28)
    mask = df.columns.str.contains('Temp.*')
    Tdata  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Density.*')
    Ddata  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Depth.*')
    Dpthdata  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Pressure.*')
    Pressdata  = df.loc[:,mask] # selects mask
    latdata = pd.DataFrame({'Latitude': [lat]*Tdata.size})
    londata = pd.DataFrame({'Longitude': [lon]*Tdata.size})
    Lat.append(latdata)
    Lon.append(londata)
    Tmp.append(Tdata)
    Den.append(Ddata)
    Dpth.append(Dpthdata)
    Press.append(Pressdata)

Lat = pd.concat(Lat,ignore_index=True)
Lon = pd.concat(Lon,ignore_index=True)
Tmp = pd.concat(Tmp,ignore_index=True)
Den = pd.concat(Den,ignore_index=True)
Dpth = pd.concat(Dpth,ignore_index=True)
Press = pd.concat(Press,ignore_index=True)

PotTemp = gsw.pt0_from_t(0,Tmp,Press) # Option to calculate potential temperature for deep casts

df_full = pd.concat([Lat, Lon, Tmp, Den, -Dpth, Press], axis=1)
# Save the DataFrame as a CSV file
df_full.to_csv('/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/2021/Altaussee_CTD.csv', index=False)

#%% Plot Temperature vs. Density with Depth
ax = plt.subplot()
fig = ax.scatter(Den, Tmp, c = Dpth['Depth (Meter)'], cmap='viridis')

# Format the plot
# ax = plt.gca()
ax.ticklabel_format(useOffset=False, style='plain')
plt.grid()
plt.ylabel('Temperature (C)')
plt.xlabel('Density (kg/m^3)')
cbar = plt.colorbar(fig)
cbar.set_label('Depth (m)')
plt.show()

#%% Plot Temperature vs. Depth
ax = plt.subplot()
fig = ax.scatter(Tmp,Dpth,2,c = 'k')

plt.rcParams.update({'font.size': 20})

# Format the plot
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
plt.xticks(range(4, 21, 2)) # Change the font size here
plt.show()
# %%