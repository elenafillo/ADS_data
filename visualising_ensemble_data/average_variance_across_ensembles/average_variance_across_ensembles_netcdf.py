import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import os
import subprocess


def plot_stdev_and_max(firstMember, lower_lat, upper_lat, lower_lon, upper_lon, folder_name):
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
    # plt.figure(figsize=(12,12))
    plt.figure(figsize=(48,48))
    for index, ensemble_member in enumerate(ensemble_members):
        # print(index, ensemble_member)
        ax = plt.subplot(3,3,index+1, projection=ccrs.PlateCarree((lower_lon+upper_lon)/2)) #+1 because subplot counts from 1
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)

        cut_to_size = data.loc[dict(forecast_period = ensemble_member[0], forecast_reference_time = ensemble_member[1], latitude=slice(lower_lat, upper_lat), longitude=slice(lower_lon, upper_lon))]['wind_speed_of_gust']
        cut_to_size.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=np.linspace(0,100,11))
        plt.title(f'{ensemble_member[0]} , {ensemble_member[1]}')
        # plt.title('')

    # plt.suptitle('9 ensemble members of the same time stamp')
    plt.savefig(f'{folder_name}/images/{folder_name}_9ensemble_members_of_same_time_stamp_{firstMember}.png',bbox_inches='tight', transparent=False)
    plt.close()
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
        # print(f'{ii+1}/{np.size(cut_to_size[0].values[0][:])}') #print progress
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
    plt.title('Maximum Wind Speed of Gust across Ensemble')
    plt.colorbar(label='wind speed of gust [ms-1]')
    plt.savefig(f'{folder_name}/images/{folder_name}_max_{firstMember}.png', transparent=False)
    plt.close()

    #plot stdev
    ax = plt.subplot(1,1,1, projection=ccrs.PlateCarree((lower_lon+upper_lon)/2))
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    # cut_to_size[0].plot.contourf(ax=ax, transform=ccrs.PlateCarree())
    plt.contourf(lons,lats, stdev_values, transform=ccrs.PlateCarree(), levels=np.linspace(0,40,11))
    plt.title('Standard Deviation of Wind Speed of Gust across Ensemble')
    plt.colorbar(label='standard deviation [ms-1]')
    plt.savefig(f'{folder_name}/images/{folder_name}_stdev_{firstMember}.png', transparent=False)
    plt.close()
    return stdev_values, max_values
    # return np.sum(stdev_values), np.max(max_values), np.avg(max_values), np.mode(max_values)

if __name__ == "__main__":
    hurricane = 'bob01'
    # data = xr.open_dataset(hurricane + '/' + 'fg.nc')

######## 
# Setup 

    # data = xr.open_dataset("../../../../MetOfficeData/tsens.tc01b/fg.T1Hpoint.UMRA2T.19970518_19970521.TC01B.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.viyaru/fg.T1Hpoint.UMRA2T.20130514_20130517.VIYARU.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.sidr/fg.T1Hpoint.UMRA2T.20071114_20071117.SIDR.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.bob07/fg.T1Hpoint.UMRA2T.19951123_19951126.BOB07.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.aila/fg.T1Hpoint.UMRA2T.20090523_20090526.AILA.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.bob01/fg.T1Hpoint.UMRA2T.19910428_19910501.BOB01.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.akash/fg.T1Hpoint.UMRA2T.20070513_20070516.AKASH.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.roanu/fg.T1Hpoint.UMRA2T.20160520_20160523.ROANU.4p4km.nc")
    # data = xr.open_dataset("../../../../MetOfficeData/tsens.mora/fg.T1Hpoint.UMRA2T.20170528_20170531.MORA.4p4km.nc")
    data = xr.open_dataset("../../../../MetOfficeData/tsens.fani/fg.T1Hpoint.UMRA2T.20190502_20190505.FANI.4p4km.nc")

    
    folder_name = 'fani' #existing folder with 'images' and 'results' subfolders

    lower_lon = 82
    upper_lon = 94

    lower_lat = 14.5
    upper_lat = 26.5

    # lower_lat = 15
    # upper_lat = 23

    # lower_lon = 85
    # upper_lon = 93.05

    framerate = '8'
########
    
    #create arrays storing summaries across time steps
    #stdev: see how much variation there is
    stdev_sums = np.zeros(47-23) #24 different overlapping time stamps #sum over stdev image. #GOOD
    stdev_max = np.zeros(47-23) #highest stdev value in image #totally useless
    stdev_avg = np.zeros(47-23) #average stdev value in image #kinda same as sums
    stdev_median = np.zeros(47-23) #median stdev value in image #kinda useless

    #max: see when the speeds decrease
    max_max = np.zeros(47-23) #highest value in the whole image of the max of the 9 ensemble members per cell #GOOD
    max_avg = np.zeros(47-23) #average value in max image #kinda useless GOOD
    max_sum = np.zeros(47-23) #sum of all values in the max image #kinda useless
    max_median = np.zeros(47-23) #median value in max image #kinda useless VERY GOOD


    #create plots
    for firstMember in range(24,48): #24,48
        print(f'{firstMember-23}/{47-23}') #print progress
        assert firstMember >= 24 and firstMember <= 47, f'firstMember ({firstMember}) not in overlapping range (24 - 47)'
        stdev_values, max_values = plot_stdev_and_max(firstMember,lower_lat,upper_lat,lower_lon,upper_lon, folder_name)

        stdev_sums[firstMember-24]   = np.sum(stdev_values)
        # stdev_max[firstMember-24]    = np.max(stdev_values)
        stdev_avg[firstMember-24]    = np.average(stdev_values)
        # stdev_median[firstMember-24] = np.median(stdev_values)

        # max_max[firstMember-24]    = np.max(max_values)
        # max_sum[firstMember-24]    = np.sum(max_values)
        max_avg[firstMember-24]    = np.average(max_values)
        # max_median[firstMember-24] = np.median(max_values)

# return np.sum(stdev_values), np.max(max_values), np.avg(max_values), np.mode(max_values)


    #bob01 results, for summary plot debugging
    # stdev_sums = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # max_of_max = np.asarray([93,    92.75,  91.5,   91,    91.25,  91.75,  92.5,   93.125, 94.5, 95.875, 98.125, 96.875, 98.5, 99.375, 97.25, 98.375, 93.5, 94.5, 93.125, 94.125, 94, 90.875, 89.125, 83.875])

    # stdev_sums = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # stdev_max = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # stdev_avg = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # stdev_median = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
 
    # max_max = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # max_sum = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # max_avg = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])
    # max_median = np.asarray([250997.02755856, 248445.24493813, 244770.20295459, 236962.1751681, 232843.81837617, 232504.11321471, 231861.14322055, 233850.62530518, 234368.02816844, 236545.08405288, 239030.19263342, 248104.40526206, 258067.28699425, 261589.23248871, 264272.19049302, 268147.57452989, 267760.7240743,  268217.04532954, 266472.33655153, 271153.88635387, 278981.93849636, 287776.05520988, 297568.78350887, 301100.61776089])

    # SIDR:
    # stdev_sums:
    # [154277.97039819 153382.02710371 157007.66580299 155884.34607063
    #  151565.25109859 146410.10945262 144341.77821381 141324.67759465
    #  140551.01235603 140455.982464   140350.94751762 140398.56549422
    #  140614.21807463 139605.00010695 137634.45187046 139541.98196188
    #  144955.91981098 147756.55352807 150857.69060913 152083.29689598
    #  152222.27614653 153071.63025926 152386.11296208 148420.85103507]
    # stdev_avg:
    # [1.76084243 1.75061664 1.79199765 1.7791767  1.72988097 1.67104307
    #  1.64743629 1.61300079 1.60417061 1.60308599 1.60188718 1.60243067
    #  1.60489201 1.59337336 1.57088262 1.5926541  1.65444576 1.68641063
    #  1.72180527 1.73579366 1.73737989 1.74707394 1.73924983 1.69399255]
    # max_avg:
    # [14.19498294 13.67182792 13.47120674 13.28877003 13.01332377 12.749893
    #  12.5259613  12.29396315 12.16258589 12.0634145  11.97662527 11.86713471
    #  11.73906592 11.59638936 11.44506711 11.45075243 11.71571402 11.88589698
    #  12.0287419  12.17550447 12.2779615  12.25798798 12.00344686 11.41891321]







    print('stdev_sums:')
    print(stdev_sums)
    print('stdev_avg:')
    print(stdev_avg)
    print('max_avg:')
    print(max_avg)

    # #plot summaries across time stamps

    # plt.bar(np.linspace(24,47, 47-23), normalized_stdev_sums)
    plt.bar(np.linspace(-11,12, 47-23), stdev_sums)
    plt.xlabel('time relative to landfall [hours]')
    plt.title('Total Standard Deviation of Wind Speed of Gust between Ensemble Members across Image')
    plt.ylabel('standard deviation')
    plt.savefig(f'{folder_name}/results/{folder_name}_stdev_sums.png')
    plt.close()


    normalized_stdev_sums = [x/np.max(stdev_sums) for x in stdev_sums]
    # plt.bar(np.linspace(24,47, 47-23), normalized_stdev_sums)
    plt.bar(np.linspace(-11,12, 47-23), normalized_stdev_sums)
    # plt.xlabel('time steps')
    plt.xlabel('time relative to landfall [hours]')
    plt.title('Normalised Total Standard Deviation of Speed of Gust between Ensemble Members across Image')
    plt.ylabel('standard deviation')
    plt.savefig(f'{folder_name}/results/{folder_name}_stdev_sums.png')
    plt.close()



    # plt.bar(np.linspace(-11,12, 47-23), stdev_max)
    # # plt.xlabel('time steps')
    # plt.xlabel('time relative to landfall [hours]')
    # plt.title('Maximum Standard Deviation between Ensemble Members across Image')
    # plt.ylabel('standard deviation [ms-1]')
    # plt.savefig(f'{folder_name}/results/{folder_name}_stdev_max.png')
    # plt.close()


    plt.bar(np.linspace(-11,12, 47-23), stdev_avg)
    plt.xlabel('time relative to landfall [hours]')
    plt.title('Average Standard Deviation across Image')
    plt.ylabel('standard deviation [ms-1]')
    plt.savefig(f'{folder_name}/results/{folder_name}_stdev_avg.png')
    plt.close()

    # plt.bar(np.linspace(-11,12, 47-23), stdev_median)
    # plt.xlabel('time relative to landfall [hours]')
    # plt.title('Median Standard Deviation across Image')
    # plt.ylabel('standard deviation [ms-1]')
    # plt.savefig(f'{folder_name}/results/{folder_name}_stdev_median.png')
    # plt.close()




    # plt.bar(np.linspace(24,47, 47-23), max_of_max)
    # plt.bar(np.linspace(-11,12, 47-23), max_max)
    # # plt.xlabel('time steps')
    # plt.xlabel('time relative to landfall [hours]')
    # plt.title('Maximum Gust Speed in the Image')
    # plt.ylabel('wind speed of gust [ms-1]')
    # plt.savefig(f'{folder_name}/results/{folder_name}_max_max.png')
    # plt.close()



    # plt.bar(np.linspace(-11,12, 47-23), max_sum)
    # # plt.xlabel('time steps')
    # plt.xlabel('time relative to landfall [hours]')
    # plt.title('Sum of All Maximum Gust Speeds across Image')
    # plt.ylabel('wind speed of gust [ms-1]')
    # plt.savefig(f'{folder_name}/results/{folder_name}_max_sum.png')
    # plt.close()

    plt.bar(np.linspace(-11,12, 47-23), max_avg)
    # plt.xlabel('time steps')
    plt.xlabel('time relative to landfall [hours]')
    plt.title('Maximum Gust Speed across Ensemble Members Averaged across Image')
    plt.ylabel('wind speed of gust [ms-1]')
    plt.savefig(f'{folder_name}/results/{folder_name}_max_avg.png')
    plt.close()

    # plt.bar(np.linspace(-11,12, 47-23), max_median)
    # # plt.xlabel('time steps')
    # plt.xlabel('time relative to landfall [hours]')
    # plt.title('Median Maximum Gust Speed across Ensemble Members across Image')
    # plt.ylabel('wind speed of gust [ms-1]')
    # plt.savefig(f'{folder_name}/results/{folder_name}_max_median.png')
    # plt.close()


    
    #make videos using ffmpeg
    subprocess.call(['sh', './shellscript.sh', framerate, f'{folder_name}/images/{folder_name}_max_%02d.png',  f'{folder_name}/results/{folder_name}_max.mp4', f'{folder_name}/results/{folder_name}_max.gif'])
    subprocess.call(['sh', './shellscript.sh', framerate, f'{folder_name}/images/{folder_name}_stdev_%02d.png', f'{folder_name}/results/{folder_name}_stdev.mp4', f'{folder_name}/results/{folder_name}_stdev.gif'])
    # subprocess.call(['sh', './shellscript.sh', framerate, f'{folder_name}/images/{folder_name}_9ensemble_members_of_same_time_stamp_%02d.png', f'{folder_name}/results/{folder_name}_9members.mp4', f'{folder_name}/results/{folder_name}_9members.gif'])
    