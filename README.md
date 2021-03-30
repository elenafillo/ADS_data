# ADS_data
Applied Data Science project

Data from https://oasishub.co/dataset/bangladesh-tropical-cyclone-historical-catalogue

Variables: fg (point wind gust), prlst (mean precipitation)

Hurricanes:
- [x] Bob1
- [x] Bob7
- [x] TC01B
- [x] Akash
- [x] Sidr
- [x] Rashmi
- [x] Aila
- [x] Roanu
- [x] Viyaru
- [x] Mora
- [x] Fani
- [ ] Bulbul (corrupted)

### Data format:
There are six files for each hurricane (three for wind, three for fg and three for prlst). They are organised as follows:
```
full_cyclones (contains data in the full 4.4km range)
 * hurricane_fg (data only for the eye of the hurricane, rest is nans)
 * hurricane_prlst (as above)
eyes (contains data centered around the eye of the hurricane, size 257x257)
 * hurricane_fg_cut (data only for the eye of the hurricane, rest is nans)
 * hurricane_prlst_cut (as above)
 * hurricane_fg_full (data for the whole range)
 * hurricane_prlst_full (as above)

```
This is a sample of how item 160 from hurricane Bob07 looks in each file:
![sample_hurricane_files](https://github.com/elenafillo/ADS_data/blob/main/sample_image.png)


The file `summary.csv` contains information for each item in the files:
 * Hurricane - hurricane name (see above list of hurricane data available, variable is a string all in lowercase)
 * Item - index of image in the hurricane files
 * WindReferenceTime - Initialisation date and time of each model run for wind data (should be the same as rain data) (see [data documentation](https://myololobuckert213913653.s3.amazonaws.com/documentation/bangladesh-tropical-cyclone-historical-catalogue/HistoricalCatalogueDataDescription.pdf?) for more)
 * WindPeriod - Time of the data relative to the forecast reference time (formatted as timedelta, ranges from 1 day 1h to 3 days, on the hour)(see [data documentation](https://myololobuckert213913653.s3.amazonaws.com/documentation/bangladesh-tropical-cyclone-historical-catalogue/HistoricalCatalogueDataDescription.pdf?) for more)
  * RainReferenceTime - Initialisation date and time of each model run for rain data (should be the same as wind data) (see [data documentation](https://myololobuckert213913653.s3.amazonaws.com/documentation/bangladesh-tropical-cyclone-historical-catalogue/HistoricalCatalogueDataDescription.pdf?) for more)
 * RainPeriod - Time dimension of the data in hours relative to the forecast reference time (formatted as timedelta, ranges from 1 day 30min to 2 days 23hours 30mins, on the half an hour) (see [data documentation](https://myololobuckert213913653.s3.amazonaws.com/documentation/bangladesh-tropical-cyclone-historical-catalogue/HistoricalCatalogueDataDescription.pdf?) for more) 
 * Centre - Coordinates for the centre of the hurricane (see how it was calculated below)
 * Valid - Boolean, indicates (roughly) if the hurricane has a good "hurricane shape" (see how it was calculated below)

Note that item i will have the same Reference Time for rain and wind but not the Period

### How to load and use the data

Import modules, load the summary and convert to the correct units.
 
 ```
 import pandas as pd
 import numpy as np
 import matplotlib.pyplot as plt

summary = pd.read_csv('summary.csv')
summary['WindReferenceTime'] = pd.to_datetime(summary['WindReferenceTime'])
summary['WindPeriod'] = pd.to_timedelta(summary['WindPeriod'])
summary['RainReferenceTime'] = pd.to_datetime(summary['RainReferenceTime'])
summary['RainPeriod'] = pd.to_timedelta(summary['RainPeriod'])

 ```
 
 Load the data from the .npz files
 
 ```
 with np.load('full_cyclones/bob01_fg.npz', allow_pickle=True) as data:
    wind = data['arr_0']
 ```
 
 Find the information about item i from file hurricane_variable, and visualize that item.
 
 ``` 
summary.loc[(summary.Hurricane == 'bob01') & (summary.Item == i) ]
plt.contourf(wind[i])
plt.show()
  ```
  
  Load data of a type for all hurricanes 
  ```
all_hurricanes = []
for name in summary.Hurricane.unique():
    print(name)
    try:
        with np.load('ADS_data/eyes/' + name + '_fg_cut.npz', allow_pickle=True) as data:
            wind = data['arr_0'] 
        all_hurricanes.extend(wind)
    except:
        print(name + ' did not work. File is probably corrupted')
  ```
  
 ### Some bits and bobs about how the data was calculated / possible needed improvements
 ##### Isolating the hurricane:
 The points shown are those that have a value higher than 3 times the mean of the image, those below that threshold are NaN.
 Any remaining values that are outside of a 257x257 window centered around the eye of the hurricane are also set to NaN. 
 
 ##### Calculating the centre of the hurricane:
Scipy function `unif2D` calculates the uniform filter of an image (replaces the value of a pixel by the mean value of an area centered at the pixel). Function largest_sum returns the position of the pixel with the highest average (which when applied to wind or rain data, will be around the centre of the hurricane). n determines size of the area.
 ```
 from scipy.ndimage.filters import uniform_filter as unif2D
def largest_sum(a, n):
    idx = unif2D(a.astype(float),size=n, mode='constant').argmax()
    return np.unravel_index(idx, a.shape)
 ```
 
  ##### Calculating validity:
  Slightly lazy but roughly works - samples where the isolated hurricane has less than 3000 non-nan pixels are classed as False. (potential improvement here)
  
  
  ##### Other good way of removing noise:
  Another good way to remove noise nearer to the hurricane (meaning small, non-connected spots) is the following (method inspired by [this doc](https://scikit-image.org/docs/stable/auto_examples/filters/plot_tophat.html). This is not yet implemented.
  ```
from skimage import morphology 
im = centre_winds_cut[2].copy()

selem =  morphology.disk(3) 
# Generates a flat, disk-shaped structuring element of radius 3. 

res = morphology.black_tophat(im, selem)
# Returns image except the dark spots that are smaller than the structuring element (ie selem)

mask = np.isnan(im - res) # Mask returns True if a value is NaN is either the full image or it's black tophat
im_new = im.copy()
im_new[mask == True] = np.nan # Change to nan those values that have changed after doing the black tophat

```
The effect can be seen here (bigger disk size will remove bigger spots):
![sample_tophat_processing](https://github.com/elenafillo/ADS_data/blob/main/sample_tophat.png)



