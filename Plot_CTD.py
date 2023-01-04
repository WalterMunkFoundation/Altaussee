import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

filenames = find_csv_filenames('./') #find the .csv files in the current folder

# Read in a file
for filename in filenames:
    df = pd.read_csv(filename, header=28)
    mask = df.columns.str.contains('Temp.*')
    T  = df.loc[:,mask] # selects mask
    mask = df.columns.str.contains('Depth.*')
    D  = df.loc[:,mask] # selects mask

    # Plot the thermal profile
    plt.plot(T,D)

# Format the plot
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
plt.show()