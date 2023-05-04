import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# basefile = '21721686_cal'
# file = basefile + '.nc'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/Cal_Data/'

file_pattern = dirpath + '*.nc'

# Open the files
datasets = xr.open_mfdataset(file_pattern, concat_dim="SN", combine="nested")
datasets = datasets.sortby('Time')

# plot all the data
# [plt.scatter(datasets.Time,datasets.temp_C[SN]) for SN in datasets.SN]

# Clip the dataset to isolate the calibration period
# Define the time range to clip to
start_time = '2023-04-26T16:00'
end_time = '2023-04-26T16:33'

# Clip the dataset to the specified time range
ds_clipped = datasets.sel(Time=slice(start_time, end_time)).sel(Time=slice(start_time, end_time))

# plot the clipped data
fig, ax = plt.subplots()
[ax.scatter(ds_clipped.Time,ds_clipped.temp_C[SN]) for SN in datasets.SN]
ax.set_ylabel('Temp C')
ax.grid(True)


# Find the mean at each time step **working here
means = [ds_clipped.temp_C[:,SN].mean().values for SN in ds_clipped.SN]
ds_clipped.temp_C.sel(SN = 0).mean().values

print()