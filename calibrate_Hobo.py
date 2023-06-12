import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


# basefile = '21721686_cal'
# file = basefile + '.nc'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/Cal_Data/'

file_pattern = dirpath + '*.nc'

# Open the files
datasets = xr.open_mfdataset(file_pattern, concat_dim="Num", combine="nested")
datasets = datasets.sortby('Time')

# plot all the data
fig, ax = plt.subplots()
[ax.scatter(datasets.Time,datasets.temp_C[Num]) for Num in datasets.Num]
ax.set_ylabel('Temp C')
ax.grid(True)

# Clip the dataset to isolate the calibration period
# Define the time range to clip to
start_time = '2023-06-11T16:08'
end_time = '2023-06-11T17:00'

# Select the instrument to plot
inst = 0

# Clip the dataset to the specified time range
ds_clipped = datasets.sel(Time=slice(start_time, end_time)).sel(Time=slice(start_time, end_time))

# Find the mean at each time step **working here
mean_vals = [ds_clipped.temp_C.isel(Time=alltime).mean().values for alltime in range(0,np.size(ds_clipped.Time))]
ds_clipped['cal_means'] = (('Time'), mean_vals)

# plot the clipped data and means for a given serial number
fig, ax = plt.subplots()
ax.scatter(ds_clipped.Time,ds_clipped.temp_C[inst])
ax.scatter(ds_clipped.Time,ds_clipped.cal_means,color = 'red')
ax.set_ylabel('Temp C')
ax.grid(True)

# Find the differences from the mean for each instrument
ds_clipped['epsilon'] = ds_clipped.temp_C - ds_clipped.cal_means

mean_eps = [ds_clipped.epsilon.isel(Num=allinst).mean().values for allinst in ds_clipped.Num]
ds_clipped['mean_eps'] = (('Num'), mean_eps) # mean offsets are stored here

# plot the selected data for a given serial number
x = np.array(ds_clipped.temp_C[inst])
y = np.array(ds_clipped.cal_means)
# Filter out rows with NaN values
valid_indices = np.logical_and(~np.isnan(x), ~np.isnan(y))
x_valid = x[valid_indices]
y_valid = y[valid_indices]

slope, intercept, r_value, p_value, std_err = stats.linregress(x_valid,y_valid)

fig, ax = plt.subplots()
ax.scatter(x_valid,y_valid)
ax.plot([x_valid.min(), y_valid.max()],[x_valid.min() * slope + intercept, x_valid.max() * slope + intercept],color = 'red')
ax.set_ylabel('Temp C')
ax.grid(True)
title = 'Serial number: '+ds_clipped.SN[inst].values + '\nSlope: ' + str(slope) + '\nIntercept: '+str(intercept)
ax.set_title(title,fontsize = 10)



# Find the linear correction
print()