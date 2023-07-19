import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

import os
from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

# Read in all the files
path = '/Users/gregsinnett/Google Drive/Shared drives/Projects/Altaussee/Data/Weather Station/'
os.chdir(path) #change to the desired working directory
filenames = find_csv_filenames('./') #find the .csv files in the current folder

for basefile in filenames:
    file = basefile
    outfile = basefile + '.nc'
    run_checks = 'yes'
    save_file = 'yes'


    Tme = []
    Tmp = []
    W_det = []

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
    
    ds = xr.Dataset(df)
    ds['SN'] = str(basefile[0:8]) # save the serial number

    # Calculate the mean sample rate
    times = pd.to_datetime(ds['Time'].values)
    dt = pd.Series(times).diff().mean()
    sample_rate = dt.total_seconds()


    if run_checks == 'yes':
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
        ax1.scatter(ds.Time,ds.Time)
        ax1.grid(True)
        ax1.set_title(f'Sample rate = {sample_rate:.2f} s')

        ax2.scatter(ds.Time,ds.temp_C)
        ax2.grid(True)
        ax2.set_ylabel('Temp C')
        plt.show()

    # Save the dataframe
    if save_file == 'yes':
        ds.to_netcdf(path + outfile)