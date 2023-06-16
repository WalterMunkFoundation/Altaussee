import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

pathname = '/Users/gregsinnett/GitHub/Altaussee/Heat_2023/CTD casts/'
filenames = find_csv_filenames(pathname) #find the .csv files in the specified directory

Temp = []
Depth = []

# Read in a file and plot temperature
color = ['blue', 'red', 'green', 'black', 'orange']
for i, filename in enumerate(filenames):
    df = pd.read_csv(pathname + filename, header=0)
    mask = df.columns.str.contains('Temp.*')
    T  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Depth.*')
    D  = df.loc[:,mask] # selects mask
    plt.plot(T,D - D.min(), color=color[i]) # normalize to zero depth

# Format the plot
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
plt.show()

# Read in a file and plot conductivity
color = ['blue', 'red', 'green', 'black', 'orange']
for i, filename in enumerate(filenames):
    df = pd.read_csv(pathname + filename, header=0)
    mask = df.columns.str.contains('Cond.*')
    C  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Depth.*')
    D  = df.loc[:,mask] # selects mask
    plt.plot(C,D - D.min(), color=color[i]) # normalize to zero depth

# Format the plot
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Conductivity (uS/cm)')
plt.ylabel('Depth (m)')
plt.show()