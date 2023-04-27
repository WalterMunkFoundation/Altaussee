import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

basefile = '21721686_cal'
file = basefile + '.csv'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/Cal_Data/'
outfile = basefile + '.nc'
run_checks = 'yes'
save_file = 'no'


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

# Save the dataframe
if save_file == 'yes':
    ds.to_netcdf(dirpath + outfile)