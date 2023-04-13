import pandas as pd

from hoboreader import HoboReader

file = '21721695_test_data.csv'
dirpath = '/Users/gregsinnett/GitHub/Altaussee/Hobo_Data/'


Tme = []
Tmp = []
W_det = []

df = pd.read_csv(dirpath + file, header=0)
mask = df.columns.str.contains('Temp')
Tdata  = df.loc[:,mask] # selects mask
mask = df.columns.str.contains('Time')
Time  = df.loc[:,mask] # selects mask
mask = df.columns.str.contains('Water')
Water_Detect  = df.loc[:,mask] # selects mask
Tme.append(Time)
Tmp.append(Tdata)
W_det.append(Water_Detect)

Tme = pd.concat(Tme,ignore_index=True)
Tmp = pd.concat(Tmp,ignore_index=True)
W_det = pd.concat(W_det,ignore_index=True)

# Convert PD dataframe to an xarray dataset
print()