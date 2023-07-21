import pandas as pd
import xarray as xr
import datetime
import matplotlib.pyplot as plt

import os
from os import listdir

run_checks = 'yes'
save_file = 'yes'

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/Weather Station/'
os.chdir(path) #change to the desired working directory
filenames = find_csv_filenames('./') #find the .csv files in the current folder
filenames.sort()

df_full = pd.DataFrame(columns=['Air Temp [C]', 'Bottom Water Temp [C]', 'Surface Water Temp [C]',
       'Reserve', 'Wind Speed [m/s]', 'Max Wind Speed [m/s]',
       'Wind Direction [deg]', 'Max Wind Direction [deg]', 'Air Temp [C]',
       'Relative Hum [pct rh]', 'Absolute Hum [g/m^3]', 'Dew Point Temp [C]',
       'Absolute air pressure [hPa]', 'Relative air pressure [hPa]',
       'Radiation [W/m^2]', 'Precip Indicator [0/1]', 'Precip [mm/h]',
       'Daily Precip [mm/day]', 'Precip Type'])
for basefile in filenames[-3:]:
    file = basefile

    df = pd.read_csv(path + file, thousands='.', decimal=',', sep=';', header=0, index_col=False)
    # Manipulate the date to create a standard index of datetime
    df['Datum'] = df['Datum'].astype(str)
    combined_datetime = df['Datum'] + ' ' + df['Zeit']
    df['datetime'] = pd.to_datetime(combined_datetime, format='%d%m%Y %H:%M:%S')
    df = df.drop(['Datum', 'Zeit'], axis=1)
    df.set_index('datetime',inplace = True)

    # NEED TO RENAME COLUMNS FOR CONVENIENCE

    df.rename(columns={'Temp. Aussen Nord': 'Air Temp [C]'}, inplace=True)
    df.rename(columns={'Wassertemp. unten Grad C': 'Bottom Water Temp [C]'}, inplace=True)
    df.rename(columns={'Wassertemp. oben Grad C': 'Surface Water Temp [C]'}, inplace=True)
    df.rename(columns={'30003 Wind Mittel m/s': 'Wind Speed [m/s]'}, inplace=True)
    df.rename(columns={'30011 Wind max m/s': 'Max Wind Speed [m/s]'}, inplace=True)
    df.rename(columns={'30203 Windrichtung Mittel Grad': 'Wind Direction [deg]'}, inplace=True)
    df.rename(columns={'30211 Windrichtung max. Grad': 'Max Wind Direction [deg]'}, inplace=True)
    df.rename(columns={'30401 Lufttemperatur Grad C': 'Air Temp [C]'}, inplace=True)
    df.rename(columns={'30601 Rel. Feuchte %': 'Relative Hum [pct rh]'}, inplace=True)
    df.rename(columns={'30603 Abs. Feuchte g/m2': 'Absolute Hum [g/m^3]'}, inplace=True)
    df.rename(columns={'30605 Taupunkttemperatur Grad C': 'Dew Point Temp [C]'}, inplace=True)
    df.rename(columns={'30801 Abs. Luftdruck hPa': 'Absolute air pressure [hPa]'}, inplace=True)
    df.rename(columns={'30803 Rel.  Luftdruck NHN hPa': 'Relative air pressure [hPa]'}, inplace=True)
    df.rename(columns={'31001 Globalstrahlung W/m2': 'Radiation [W/m^2]'}, inplace=True)
    df.rename(columns={'31401 Niederschlagsstatus 0/1': 'Precip Indicator [0/1]'}, inplace=True)
    df.rename(columns={'31403 Niederschlagsintensitaet mm/h': 'Precip [mm/h]'}, inplace=True)
    df.rename(columns={'31405 Niederschlagsmenge_mm/d': 'Daily Precip [mm/day]'}, inplace=True)
    df.rename(columns={'31407 Niederschlagsart': 'Precip Type'}, inplace=True)
    
    df_full = pd.concat([df_full, df], axis = 0)

ds = xr.Dataset(df_full)
ds = ds.rename({'dim_0':'time'})

if run_checks == 'yes':
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1.scatter(ds.time,ds['Air Temp [C]'],color = 'black')
    # Create a second y axis
    axb = ax1.twinx()
    axb.scatter(ds.time,ds['Surface Water Temp [C]'],color = 'red')
    
    ax1.grid(True)
    ax1.set_ylabel('Air Temp [C]')
    axb.set_ylabel('Surface Water Temp [C]', color = 'red')

    ax2.scatter(ds.time,ds['Radiation [W/m^2]'])
    ax2.grid(True)
    ax2.set_ylabel('Radiation [W/m^2]')
    plt.show()

    # Save the dataframe
if save_file == 'yes':
    # current_date = datetime.datetime.now()
    # formatted_date = current_date.strftime("%Y_%m_%d")
    outfile = 'AltausseeWeather' + '.nc'
    ds.to_netcdf(path + outfile)