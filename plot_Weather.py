import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import os



# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/Weather Station/'
os.chdir(path) #change to the desired working directory

ds = xr.open_dataset(path+'AltausseeWeather.nc')

fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6, ncols=1, sharex=True)

ds['Radiation [W/m^2]'].plot(ax = ax1)
ax1.grid()
ax1.set_xlabel(None)
ax1.set_ylabel(None)
ax1.set_title('Radiation [W/m^2]')
ds['Air Temp [C]'].plot(ax = ax2)
ax2.grid()
ax2.set_xlabel(None)
ax2.set_ylabel(None)
ax2.set_title('Air Temp [C]')
ds['Surface Water Temp [C]'].plot(ax = ax3)
ax3.grid()
ax3.set_xlabel(None)
ax3.set_ylabel(None)
ds['Wind Speed [m/s]'].plot(ax = ax4)
ax4.grid()
ax4.set_xlabel(None)
ax4.set_ylabel(None)

fig.subplots_adjust(hspace=0.5, top = 0.945)
fig.set_size_inches(8.5, 7.5)

print()
