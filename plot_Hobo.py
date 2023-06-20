import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


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

# plot all the data
fig, ax = plt.subplots()
for inst in datasets.Num:
    ax.scatter(ds_clipped.Time,ds_clipped.temp_C[inst],4)
    ax.set_ylabel('Temp C')
    ax.grid(True)
plt.show()

# plot a requested sensor
sensors = [3, 4, 5] #specify the desired sensor from the top (zero indexed)
fig, ax = plt.subplots()
for num in sensors:
    ax.scatter(ds_clipped.Time,ds_clipped.temp_C[num],4)
    ax.set_ylabel('Temp C')
    ax.grid(True)
ax.set_title('Serial Number: '+str(sensors))
plt.show()

# Analysis:
# 1) identify serial number/depth
# 2) Quantify N^2
# 3) Spectra for thermocline oscillations
# 4) Lake heat content
# 5) Lake heat flux
