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

    df.rename(columns={'Date-Time (CEST)': 'Time'}, inplace=True)
    df.rename(columns={'#': 'Obs_num'}, inplace=True)
    df.rename(columns={'Ch: 1 - Temperature   (°C)': 'temp_C'}, inplace=True)
    df.rename(columns={'Water Detect': 'Water_Detect'}, inplace=True)
    df.rename(columns={'Host Connected': 'Host_Connect'}, inplace=True)
    df.rename(columns={'End of File': 'EOF'}, inplace=True)

    df['Time'] = pd.to_datetime(df['Time'])


    df = df.set_index('Time')

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