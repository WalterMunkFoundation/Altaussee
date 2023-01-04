import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('CC2040004_20210605_095056.csv', header=28)

plt.plot(df.Temp,df.Depth)
ax = plt.gca()
ax.invert_yaxis()
plt.grid()
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
plt.show()