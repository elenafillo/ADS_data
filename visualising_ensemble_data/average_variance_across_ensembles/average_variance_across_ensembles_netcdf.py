import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


hurricane = 'bob01'

# data = xr.open_dataset(hurricane + '/' + 'fg.nc')
data = xr.open_dataset("../../../../MetOfficeData/tsens.bob01/fg.T1Hmax.UMRA2T.19910428_19910501.BOB01.4p4km.nc")

lower_lat = 16
upper_lat = 28

lower_lon = 85
upper_lon = 97

firstMember = 36

assert firstMember >= 24 and firstMember <= 47, f'firstMember ({firstMember}) not in overlapping range (24 - 47)'


#set up ensemble member forecast period and reference time values, to search by in data later.
ensemble_member_0 = (data.forecast_period[firstMember - 3 * 0], data.forecast_reference_time[0])
ensemble_member_1 = (data.forecast_period[firstMember - 3 * 1], data.forecast_reference_time[1])
ensemble_member_2 = (data.forecast_period[firstMember - 3 * 2], data.forecast_reference_time[2])
ensemble_member_3 = (data.forecast_period[firstMember - 3 * 3], data.forecast_reference_time[3])
ensemble_member_4 = (data.forecast_period[firstMember - 3 * 4], data.forecast_reference_time[4])
ensemble_member_5 = (data.forecast_period[firstMember - 3 * 5], data.forecast_reference_time[5])
ensemble_member_6 = (data.forecast_period[firstMember - 3 * 6], data.forecast_reference_time[6])
ensemble_member_7 = (data.forecast_period[firstMember - 3 * 7], data.forecast_reference_time[7])
ensemble_member_8 = (data.forecast_period[firstMember - 3 * 8], data.forecast_reference_time[8])
ensemble_members = [ensemble_member_0, ensemble_member_1, ensemble_member_2, ensemble_member_3, ensemble_member_4, ensemble_member_5, ensemble_member_6, ensemble_member_7, ensemble_member_8]


#Plot 9 ensemble members at same time stamp
plt.figure(figsize=(12,12))
for index, ensemble_member in enumerate(ensemble_members):
    print(index, ensemble_member)
    ax = plt.subplot(3,3,index+1, projection=ccrs.PlateCarree((lower_lon+upper_lon)/2)) #+1 because subplot counts from 1
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)

    cut_to_size = data.loc[dict(forecast_period = ensemble_member[0], forecast_reference_time = ensemble_member[1], latitude=slice(lower_lat, upper_lat), longitude=slice(lower_lon, upper_lon))]['wind_speed_of_gust']
    cut_to_size.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=np.linspace(0,100,11))
    # plt.title(f'{ensemble_member[0]} , {ensemble_member[1]}')
    plt.title('')

# plt.suptitle('9 ensemble members of the same time stamp')
plt.savefig('9ensemble_members_of_same_time_stamp.png',bbox_inches='tight', transparent=True)
plt.show()
plt.figure(figsize=(6.4,4.8))


# #initialise stdev and max holders (xarray.plot way)
# stddev_holder = data.loc[dict(forecast_period = ensemble_member_0[0], forecast_reference_time = ensemble_member_0[1], latitude=slice(lower_lat, upper_lat), longitude=slice(lower_lon, upper_lon))]['wind_speed_of_gust']
# max_holder = data.loc[dict(forecast_period = ensemble_member_0[0], forecast_reference_time = ensemble_member_0[1], latitude=slice(lower_lat, upper_lat), longitude=slice(lower_lon, upper_lon))]['wind_speed_of_gust']
# for idx, ensemble_member in enumerate(ensemble_members):
#     stddev_holder.values[idx] = -1
#     max_holder.values[idx] = -1

#collect all 9 ensemble members cut to specified size
cut_to_size = [] #array of the whole data for the 9 ensembles. I.e. cut_to_size[0] is all of ensemble member 0
for index, ensemble_member in enumerate(ensemble_members):
    cut_to_size.append(data.loc[dict(forecast_period = ensemble_member[0], forecast_reference_time = ensemble_member[1], latitude=slice(lower_lat, upper_lat), longitude=slice(lower_lon, upper_lon))]['wind_speed_of_gust'])


#set up arrays used in plt plot
lats = cut_to_size[0].latitude
lons = cut_to_size[0].longitude
stdev_values = np.empty((len(lons.values),len(lats.values)))
max_values = np.empty((len(lons.values),len(lats.values)))


#calculate standard deviation and max for each cell. Looking at all 9 ensemble members for each cell
for ii in range(np.size(cut_to_size[0].values[:][0])):
    print(f'{ii+1}/{np.size(cut_to_size[0].values[0][:])}')
    for jj in range(np.size(cut_to_size[0].values[0][:])):
        # stddev_holder.values[ii][jj] = np.std([cut_to_size[0].values[ii][jj], cut_to_size[1].values[ii][jj], cut_to_size[2].values[ii][jj], cut_to_size[3].values[ii][jj], cut_to_size[4].values[ii][jj], cut_to_size[5].values[ii][jj], cut_to_size[6].values[ii][jj], cut_to_size[7].values[ii][jj], cut_to_size[8].values[ii][jj]])
        stdev_values[ii][jj] = np.std([cut_to_size[0].values[ii][jj], cut_to_size[1].values[ii][jj], cut_to_size[2].values[ii][jj], cut_to_size[3].values[ii][jj], cut_to_size[4].values[ii][jj], cut_to_size[5].values[ii][jj], cut_to_size[6].values[ii][jj], cut_to_size[7].values[ii][jj], cut_to_size[8].values[ii][jj]])

        # max_holder.values[ii][jj] = np.max([cut_to_size[0].values[ii][jj], cut_to_size[1].values[ii][jj], cut_to_size[2].values[ii][jj], cut_to_size[3].values[ii][jj], cut_to_size[4].values[ii][jj], cut_to_size[5].values[ii][jj], cut_to_size[6].values[ii][jj], cut_to_size[7].values[ii][jj], cut_to_size[8].values[ii][jj]])
        max_values[ii][jj] = np.max([cut_to_size[0].values[ii][jj], cut_to_size[1].values[ii][jj], cut_to_size[2].values[ii][jj], cut_to_size[3].values[ii][jj], cut_to_size[4].values[ii][jj], cut_to_size[5].values[ii][jj], cut_to_size[6].values[ii][jj], cut_to_size[7].values[ii][jj], cut_to_size[8].values[ii][jj]])


#plot max
ax = plt.subplot(1,1,1, projection=ccrs.PlateCarree((lower_lon+upper_lon)/2))
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
# cut_to_size[0].plot.contourf(ax=ax, transform=ccrs.PlateCarree())
plt.contourf(lons,lats, max_values, transform=ccrs.PlateCarree(),levels=np.linspace(0,100,11))
plt.colorbar(label='max wind speed of gust [ms-1]')
plt.ylabel('wind speed of gust [ms-1]')
plt.xlabel('wind speed of gust [ms-1]')
plt.savefig('max.png', transparent=True)


#plot stdev
ax = plt.subplot(1,1,1, projection=ccrs.PlateCarree((lower_lon+upper_lon)/2))
ax.coastlines()
ax.add_feature(cfeature.BORDERS)
# cut_to_size[0].plot.contourf(ax=ax, transform=ccrs.PlateCarree())
plt.contourf(lons,lats, stdev_values, transform=ccrs.PlateCarree(), levels=np.linspace(0,40,11))
plt.colorbar(label='standard deviation [ms-1]')
plt.ylabel('wind speed of gust [ms-1]')
plt.xlabel('wind speed of gust [ms-1]')
plt.savefig('stdev.png', transparent=True)