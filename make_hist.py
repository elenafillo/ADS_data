import numpy as np
import matplotlib.pyplot as plt
import os

## load provided data and append together
# also get max and min to de-normalise the produced data later
mx = 0

cyclones=[]
for f in os.listdir("eyes"):
    if f.endswith("fg_full.npz"):
        print(f)
        with np.load("eyes/"+f,allow_pickle=True) as data:
            wind = data['arr_0']
        for item in wind:
            if np.shape(item) == (256,256):
                cyclones.append(item[128-32:128+32, 128-32:128+32].flatten()) 
                mx=max(mx,np.max(item[128-32:128+32, 128-32:128+32]))

cyclones = np.array(cyclones)



## load produced data and append together (a particular iteration)
p = np.load('produced_small.npy')
iteration = 2

produced = []

for point in p[iteration]:
    produced.append(point[0].flatten()) 
produced = np.array(produced)

# de-normalise 
produced = (produced + 1)*0.5*mx

print(np.shape(cyclones), np.shape(produced))
           
    
# plot    
fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2, figsize = (20,10))

for (ax, name), data in zip([(ax1, 'provided'), (ax2, 'produced')], [cyclones, produced]):
    # weights command averages the data out over the number of samples
    ax.hist(x=data.flatten(), weights = [1/len(data)]*len(data.flatten()))
    ax.set_title("histogram for " + name + " data")
    ax.set_ylim(top=1500)
    ax.set_xlim(right=90)
    
plt.show()