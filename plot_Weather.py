import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import os



# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/Weather Station/'
os.chdir(path) #change to the desired working directory

ds = xr.open_dataset(path+'AltausseeWeather.nc')

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, ncols=1, sharex=True)

ds['Radiation [W/m^2]'].plot(ax = ax1)
ax1.grid()
ax1.set_xlabel(None)
ax1.set_ylabel('[W/m^2]')
ax1.set_title('Radiation')
ds['Air Temp [C]'].plot(ax = ax2)
ax2.grid()
ax2.set_xlabel(None)
ax2.set_ylabel('[C]')
ax2.set_title('Air Temp')
ds['Surface Water Temp [C]'].plot(ax = ax3)
ax3.grid()
ax3.set_xlabel(None)
ax3.set_ylabel('[C]')
ax3.set_title('Surface Water Temp')
ds['Wind Speed [m/s]'].plot(ax = ax4)
ax4.grid()
ax4.set_xlabel(None)
ax4.set_ylabel('[m/s]')
ax4.set_title('Wind Speed')
ds['Relative Hum [pct rh]'].plot(ax = ax5)
ax5.grid()
ax5.set_xlabel(None)
ax5.set_ylabel('[pct rh]')
ax5.set_title('Relative Hum')


fig.subplots_adjust(hspace=0.5, top = 0.945)
fig.set_size_inches(8.5, 7.5)

print()
