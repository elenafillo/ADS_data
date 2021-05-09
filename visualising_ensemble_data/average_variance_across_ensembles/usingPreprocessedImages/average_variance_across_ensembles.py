import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

summary = pd.read_csv('../../summary.csv')
summary['WindReferenceTime'] = pd.to_datetime(summary['WindReferenceTime'])
summary['WindPeriod'] = pd.to_timedelta(summary['WindPeriod'])
summary['RainReferenceTime'] = pd.to_datetime(summary['RainReferenceTime'])
summary['RainPeriod'] = pd.to_timedelta(summary['RainPeriod'])



# with np.load('../../full_cyclones/bob01_fg.npz', allow_pickle=True) as data:
with np.load('../../eyes/bob01_fg_full.npz', allow_pickle=True) as data:
   wind = data['arr_0']


initial_i = 27
#needs to have atleast 27hrs to go back on, i.e. be atleast 27 from first ensemble start.
#same time in next ensemble is: +48 - 3.
assert initial_i >= 27 and initial_i <=47, "initial_i not in overlapping part"

collection_across_ensembles = np.empty((len(wind[0]),len(wind[0][0]),9))

for ensembleCount in range(9):
    i = initial_i + ensembleCount * (48-3)
    print(f'i: {i}')
    summary.loc[(summary.Hurricane == 'bob01') & (summary.Item == i) ]

    for ii in range(len(wind[0])):
        for jj in range(len(wind[0][0])):
            collection_across_ensembles[ii][jj][ensembleCount] = wind[i][ii][jj]

    plt.subplot(3,3,ensembleCount+1) #+1 because subplot counts from 1
    plt.contourf(wind[i])
    # plt.imshow(wind[i])
plt.savefig("ensembles.svg")
plt.show()


stdev_img = np.empty((len(wind[0]),len(wind[0][0])))
variance_img = np.empty((len(wind[0]),len(wind[0][0])))
average_img = np.empty((len(wind[0]),len(wind[0][0])))
for ii in range(len(wind[0])):
    for jj in range(len(wind[0][0])):
        stdev_img[ii][jj] = statistics.stdev(collection_across_ensembles[ii][jj])
        variance_img[ii][jj] = statistics.variance(collection_across_ensembles[ii][jj])
        average_img[ii][jj] = statistics.mean(collection_across_ensembles[ii][jj])


plt.subplot(3,1,1)
plt.contourf(stdev_img)
plt.subplot(3,1,2)
plt.contourf(variance_img)
plt.subplot(3,1,3)
plt.contourf(average_img)
plt.savefig("stdev_variance_and_mean.svg")
plt.show()