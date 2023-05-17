import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# basefile = '21721686_cal'
# file = basefile + '.nc'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/Cal_Data/'

file_pattern = dirpath + '*.nc'

# Open the files
datasets = xr.open_mfdataset(file_pattern, concat_dim="SN", combine="nested")
datasets = datasets.sortby('Time')

# plot all the data
fig, ax = plt.subplots()
[ax.scatter(datasets.Time,datasets.temp_C[SN]) for SN in datasets.SN]
ax.set_ylabel('Temp C')
ax.grid(True)

# Clip the dataset to isolate the calibration period
# Define the time range to clip to
start_time = '2023-04-26T16:00'
end_time = '2023-04-26T16:15'

# Clip the dataset to the specified time range
ds_clipped = datasets.sel(Time=slice(start_time, end_time)).sel(Time=slice(start_time, end_time))

# Find the mean at each time step **working here
mean_vals = [ds_clipped.temp_C.isel(Time=alltime).mean().values for alltime in range(0,np.size(ds_clipped.Time))]
ds_clipped['cal_means'] = (('Time'), mean_vals)

# plot the clipped data and means
fig, ax = plt.subplots()
[ax.scatter(ds_clipped.Time,ds_clipped.temp_C[SN]) for SN in datasets.SN]
ax.scatter(ds_clipped.Time,ds_clipped.cal_means,color = 'red')
ax.set_ylabel('Temp C')
ax.grid(True)

# Find the differences from the mean for each instrument
ds_clipped['epsilon'] = ds_clipped.temp_C - ds_clipped.cal_means

mean_eps = [ds_clipped.epsilon.isel(SN=allinst).mean().values for allinst in ds_clipped.SN]
ds_clipped['mean_eps'] = (('SN'), mean_eps) # mean offsets are stored here

print()