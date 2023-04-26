import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from hoboreader import HoboReader

basefile = '21721695_test_data'
file = basefile + '.csv'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/'
outfile = basefile + '.nc'


Tme = []
Tmp = []
W_det = []

df = pd.read_csv(dirpath + file, header=0)
df.rename(columns={'Date-Time (PDT)': 'Time'}, inplace=True)
df.rename(columns={'#': 'Obs_num'}, inplace=True)
df.rename(columns={'Ch: 1 - Temperature   (°C)': 'temp_C'}, inplace=True)
df.rename(columns={'Water Detect': 'Water_Detect'}, inplace=True)
df.rename(columns={'Host Connected': 'Host_Connect'}, inplace=True)
df.rename(columns={'End of File': 'EOF'}, inplace=True)

df['Time'] = pd.to_datetime(df['Time'])


df = df.set_index('Time')

ds = xr.Dataset(df)

# Need to QC to remove nans and replace variables with attributes


# Save the dataframe
ds.to_netcdf(outfile)