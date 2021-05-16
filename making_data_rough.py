import xarray as xr
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

from scipy.ndimage.filters import uniform_filter as unif2D
def largest_sum(a, n):
    idx = unif2D(a.astype(float),size=n, mode='constant').argmax()
    return np.unravel_index(idx, a.shape)
## change n below to have different "search areas"

## load hurricane 	
hurricane = 'bob01'
wind = xr.open_dataset(hurricane + '/' + 'fg.nc')
wind = wind['wind_speed_of_gust']

all_winds = []
centre_winds = []
centre_winds_cut = []
t_wind = []
p_wind = []
centres_cols = []
centres_rows = []
valid = []
size = 257
side = int((size-1)/2)


for wind_time in wind.forecast_reference_time:
    for wind_period in wind.forecast_period:
        single_wind = wind.loc[dict(forecast_reference_time=wind_time, forecast_period = wind_period)]
        single_wind = single_wind.values
         
        (r, c) = largest_sum(single_wind, n = 50)

        t_wind.append(wind_time.values)
        p_wind.append(wind_period.values)
        centres_cols.append(c)
        centres_rows.append(r)
        
        
        winds_centre = single_wind[r-side:r+side, c-side:c+side]
        centre_winds.append(winds_centre.copy())
              
        
        single_wind[single_wind < 3*np.mean(single_wind)] = 'NaN'
        back = np.zeros_like(single_wind)
        back[:] = np.nan
        back[r-side:r+side, c-side:c+side] = single_wind[r-side:r+side, c-side:c+side]
        # remove noise 
        all_winds.append(back.copy())
        
        if np.count_nonzero(~np.isnan(single_wind)) < 3000:
            valid.append(False)
        else:
            valid.append(True)
        
        winds_centre = single_wind[r-side:r+side, c-side:c+side]
        back[r-side:r+side, c-side:c+side] = winds_centre
        centre_winds_cut.append(winds_centre)
             

## save here the results
