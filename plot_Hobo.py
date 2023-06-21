import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.dates as mdates



# basefile = '21721686_cal'
# file = basefile + '.nc'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Heat_2023/Mooring Data/'

file_pattern = dirpath + '*.nc'

# Open the files
datasets = xr.open_mfdataset(file_pattern, concat_dim="Num", combine="nested")
datasets = datasets.sortby('Time')

# # plot all the data
# fig, ax = plt.subplots()
# [ax.scatter(datasets.Time,datasets.temp_C[Num]) for Num in datasets.Num]
# ax.set_ylabel('Temp C')
# ax.grid(True)

# Clip the dataset to isolate the calibration period
# Define the time range to clip to
start_time = '2023-06-13T16:00'
end_time = '2023-06-17T10:00'

# Clip the dataset to the specified time range
ds_clipped = datasets.sel(Time=slice(start_time, end_time)).sel(Time=slice(start_time, end_time))

Depths = ['0.2m', '1m', '2m', '3m','5m', '7m','9m','11m', '13m','20m','35m','45m','65m']
# plot all the data
fig, ax = plt.subplots()
for inst in datasets.Num:
    ax.scatter(ds_clipped.Time,ds_clipped.temp_C[inst],5,label = Depths[inst.values])
    ax.set_ylabel('Temp [C]')
    ax.grid(True)
# Set the date formatter
date_formatter = mdates.DateFormatter('%b %d %H:%M')
ax.xaxis.set_major_formatter(date_formatter)
# Adjust x-axis tick label rotation and alignment
plt.xticks(rotation=45, ha='right')
# Adjust the position of the plot within the figure
plt.subplots_adjust(left=0.15, right=0.8, bottom=0.2, top=0.9)  # Adjust the values as desired
plt.legend()
# Add legend outside the plot on the right
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title = 'Inst Depths')

plt.show()

# plot a requested sensor
sensors = [3,4,5] #specify the desired sensor from the top (zero indexed)
fig, ax = plt.subplots()
for num in sensors:
    ax.scatter(ds_clipped.Time,ds_clipped.temp_C[num],4,label = Depths[num])
    ax.set_ylabel('Temp C')
    ax.grid(True)
# Set the date formatter
date_formatter = mdates.DateFormatter('%b %d %H:%M')
ax.xaxis.set_major_formatter(date_formatter)
# Adjust x-axis tick label rotation and alignment
plt.xticks(rotation=45, ha='right')
# Adjust the position of the plot within the figure
plt.subplots_adjust(left=0.15, right=0.8, bottom=0.2, top=0.9)  # Adjust the values as desired
plt.legend()
# Add legend outside the plot on the right
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title = 'Inst Depths')

ax.set_title('Serial Number: '+str(sensors))
plt.show()

# Analysis:
# 1) identify serial number/depth
# 2) Quantify N^2
# 3) Spectra for thermocline oscillations
# 4) Lake heat content
# 5) Lake heat flux
