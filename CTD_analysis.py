import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from os import listdir

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
for filename in filenames:
    df = pd.read_csv(filename, header=28)
    mask = df.columns.str.contains('Temp.*')
    Tdata  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Density.*')
    Ddata  = df.loc[:,mask] # selects mask
    Tmp.append(Tdata)
    Den.append(Ddata)

Tmp = pd.concat(Tmp,ignore_index=True)
Den = pd.concat(Den,ignore_index=True)
# Plot the thermal profile
plt.scatter(Den,Tmp)

# Format the plot
ax = plt.gca()
ax.ticklabel_format(useOffset=False, style='plain')
plt.grid()
plt.ylabel('Temperature (C)')
plt.xlabel('Density (kg/m^3)')
plt.show()