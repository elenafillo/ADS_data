import numpy as np 
from matplotlib import pyplot as plt


r=np.load("produced/produced_6.npy")[0]

print(r.shape)
for x in r[::-1]:
    x[x< 3*np.mean(x)] = np.nan
    x=np.nan_to_num(x)*255
    print(x.shape)
    print(x.max())
    print(x.min())
    print(x)
    plt.imshow(x.squeeze(), cmap='gray', vmin=0, vmax=255)
    plt.show()