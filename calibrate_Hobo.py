import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

basefile = '21721695_test_data'
file = basefile + '.nc'

# Open the file
ds = xr.open_dataset(file)


print()