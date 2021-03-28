# ADS_data
Applied Data Science project

Data from https://oasishub.co/dataset/bangladesh-tropical-cyclone-historical-catalogue

Variables: fg (point wind gust), prlst (precipitation)

Hurricanes:
- [x] Bob1
- [ ] Bob7
- [ ] TC01B
- [ ] Akash
- [ ] Sidr
- [ ] Rashmi
- [ ] Aila
- [ ] Roanu
- [ ] Viyaru
- [ ] Mora
- [ ] Fani
- [ ] Bulbul (corrupted)

### Data format:
Summary: Contains the information for each piece of data: Hurricane name, variable, reference time, period and its item number in its corresponding file.

Files: Name formatted as hurricane_variable.npz . Contain a list of all images for that hurricane and variable. Images only show highest values in the original data (the rest of the values are NaN). In most cases, only the eye of the hurricane is seen, but some images may contain noise.
Information about item i in a hurricane_variable.npz file is contained in the summary table, where Item = i, Hurricane = hurricane and Variable = variable.


### How to load and use the data

Import modules, load the summary and convert to the correct units.
 
 ```
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt

summary = pd.read_csv('summary.csv')
summary['ReferenceTime'] = pd.to_datetime(summary['ReferenceTime'])
summary['Period'] = pd.to_timedelta(summary['Period'])

 ```
 
 Load the data from the .npz files
 
 ```
 with np.load('bob01_fg.npz') as data:
    wind = data['arr_0']
 ```
 
 Find the information about item i from file hurricane_variable, and visualize that item.
 
 ``` 
 summary.loc[(summary.Hurricane == 'bob01') & (summary.Variable == 'fg') & (summary.Item == i) ]
plt.contourf(wind[i])
plt.show()
  ```
  
 
  
