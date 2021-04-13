import numpy as np 
from matplotlib import pyplot as plt
import scipy.ndimage

r=np.load("produced_new/produced_6.npy")[0]

print(r.shape)
for x in r[::-1]:
    x[x< 3*np.mean(x)] = np.nan
    x=np.nan_to_num(x)*255
    print(x.shape)
    print(x.max())
    print(x.min())
    print(x)
    plt.imshow(scipy.ndimage.gaussian_filter(x.squeeze(),5))
    # plt.imshow(x.squeeze())
    plt.show()