import numpy as np 
from matplotlib import pyplot as plt


r=np.load("produced/produced_2.npy")[0]

print(r.shape)
for x in r[::-1]:
    plt.plot(x.squeeze())
    plt.show()