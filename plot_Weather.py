import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import os



# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/Weather Station/'
os.chdir(path) #change to the desired working directory

ds = xr.open_dataset(path+'AltausseeWeather.nc')

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, ncols=1, sharex=True)

ds['Radiation [W_m^2]'].plot(ax = ax1, color = 'black')
ax1.grid()
ax1.set_xlabel(None)
ax1.set_ylabel('[W/m^2]')
ax1.set_title('Solar Radiation')

ds['Air Temp [C]'].plot(ax = ax2, color = 'black')
ax2.grid()
ax2.set_xlabel(None)
ax2.set_ylabel('Air Temp [C]')
ax2.set_title('Temperature')
# Create a second y axis
axb = ax2.twinx()
ds['Surface Water Temp [C]'].plot(ax=axb, color='red', label='Surf. Water [C]')
axb.set_ylabel('Surf. Water [C]', color='red')
# Set the same y-axis limits for both axes
y_min = min(ds['Surface Water Temp [C]'].min(), ds['Air Temp [C]'].min())
y_max = max(ds['Surface Water Temp [C]'].max(), ds['Air Temp [C]'].max())
axb.set_ylim(y_min-0.5, y_max+0.5)
ax2.set_ylim(y_min-0.5, y_max+0.5)

ds['Precip [mm_h]'].plot(ax = ax3, color = 'black')
ax3.grid()
ax3.set_xlabel(None)
ax3.set_ylabel('[mm/h]')
ax3.set_title('Precip')

ds['Wind Speed [m_s]'].plot(ax = ax4, color = 'black')
ax4.grid()
ax4.set_xlabel(None)
ax4.set_ylabel('Speed [m/s]')
ax4.set_title('Wind')
axc = ax4.twinx()
ds['Wind Direction [deg]'].plot(ax=axc, color='red', label='Wind Dir [deg]', linewidth = 0.5)
axc.set_ylabel('Direction [deg]', color='red')
ymin, ymax = -10, 370
axc.set_ylim(ymin, ymax)
yticks = [0, 180, 360] 
axc.set_yticks(yticks)


ds['Relative Hum [pct rh]'].plot(ax = ax5, color = 'black')
ax5.grid()
ax5.set_xlabel(None)
ax5.set_ylabel('[% rh]')
ax5.set_title('Relative Humidity')


fig.subplots_adjust(hspace=0.5, top = 0.945)
fig.set_size_inches(8.5, 7.5)

plt.savefig(path + 'AtmosPlot.pdf')
