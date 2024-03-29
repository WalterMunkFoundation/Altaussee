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

def clean_downcast( df,rate ):
    test_dc = [result for result in np.convolve(df.Depth.diff(),np.ones(8),mode='same')>rate]
    dc_start = np.where(test_dc)[0].min()
    test_uc = [result for result in np.convolve(df.Depth.diff(),np.ones(8),mode='same')<-1]
    uc_end = np.where(test_uc)[0].max()
    return dc_start, uc_end


# Read in all the files
path = '/Users/gregsinnett/GitHub/Altaussee/Heat_2023/CTD casts/Cast5'
os.chdir(path) #change to the desired working directory
filenames = find_csv_filenames('./') #find the .csv files in the current folder

# Read in a specified file
# filenames = 'CC2040004_20210605_095056.csv'

Time = []
Tmp = []
Cond = []
Dpth = []
Press = []
for filename in filenames:
    df = pd.read_csv(filename, header=0)
    Timedata = df.iloc[:,0]
    Cdata = df.iloc[:,1]
    Pressdata = df.iloc[:,2]
    Tdata = df.iloc[:,3]
    
    Time.append(Timedata)
    Tmp.append(Tdata)
    Cond.append(Cdata)
    Dpth.append(Pressdata)

Time = pd.concat(Time,ignore_index=True)
Tmp = pd.concat(Tmp,ignore_index=True)
Cond = pd.concat(Cond,ignore_index=True)
Dpth = pd.concat(Dpth,ignore_index=True)

# PotTemp = gsw.pt0_from_t(0,Tmp,Press) # Option to calculate potential temperature for deep casts

df_full = pd.concat([Time, Dpth, Cond, Tmp], keys=['Time', 'Depth', 'Conductivity', 'Temperature'], axis=1)
df_full = df_full.sort_values(by='Time')
df_full = df_full.reset_index(drop = True)

# Clip the time series based on downcast and upcast velocity > rate m/s
dc_start, uc_end = clean_downcast( df_full,1 )
df_clean = df_full[dc_start:uc_end].reset_index(drop = True)
# Use gsw to find salinity

# Save the DataFrame as a CSV file
df_clean.to_csv(path + '.csv', index=False)

#%% Plot Temperature vs. Depth
ax = plt.subplot()
fig = ax.scatter(df_clean['Temperature'],df_clean['Depth'],20,c = df_clean.index.to_numpy())

plt.rcParams.update({'font.size': 20})

# Format the plot
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
plt.xticks(range(4, 21, 2)) # Change the font size here
cbar = plt.colorbar(fig)
cbar.set_label('Sample number')
plt.show()
# %%