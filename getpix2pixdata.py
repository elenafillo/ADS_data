import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from PIL import Image
import random

#load cyclones
cyclones=[]
for f in os.listdir( str(pathlib.Path(__file__).parent)+"/eyes"):
    # print(f)
    if f.endswith("full.npz"):
        cyclones.append(np.load(str(pathlib.Path(__file__).parent)+"/eyes/"+f,allow_pickle=True))

#get image pairs
t1=[]
t2=[]
for c in [cyclones[0]]:
    print(c["arr_0"].shape)
    for i in range(9):
        for j in range(47):
            print(j)
            t1.append(c["arr_0"][i*48+j])
            t2.append(c["arr_0"][i*48+j+1])

#normalise the data to the 0-255 range
mn=min(np.nanmin(t1),np.nanmin(t2))
mx=min(np.nanmax(t1),np.nanmax(t2))
t1=(t1-mn)/(mx-mn)*255
t2=(t2-mn)/(mx-mn)*255
t1int=np.array(t1).astype(np.uint8)
t2int=np.array(t2).astype(np.uint8)

#create relevant directories
if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path"):
    os.mkdir(str(pathlib.Path(__file__).parent)+"/path")
if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to"):
    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to")
if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data"):
    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data")
if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/A"):
    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/A")
if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/B"):
    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/B")

split={"train":0.8,"test":0.1,"val":0.1}

#randomise the order of the samples
order=list(range(len(t1)))
random.shuffle(order)
t1=[t1[i] for i in order]
t2=[t2[i] for i in order]

#save the data
l=len(t1)
for s in list(split.keys()):
    if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/A/"+s):
        os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/A/"+s)
    if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/B/"+s):
        os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/B/"+s)
    for i in range(int(l*split[s])):
        im = Image.fromarray(t1int[0])
        im.save(str(pathlib.Path(__file__).parent)+"/path/to/data/A/"+s+"/"+str(i)+".jpg")
        im = Image.fromarray(t2int[0])
        im.save(str(pathlib.Path(__file__).parent)+"/path/to/data/B/"+s+"/"+str(i)+".jpg")
        t1int=np.delete(t1int,0,0)
        t2int=np.delete(t2int,0,0)

#plots data pairs
# rows=1
# columns=2
# for i in range(len(t1)):
#     ax1=plt.subplot(rows,columns, 1)
#     ax1.set_box_aspect(1)
#     ax1.imshow(t1[i].squeeze())
#     ax2=plt.subplot(rows,columns, 2)
#     ax2.set_box_aspect(1)
#     ax2.imshow(t2[i].squeeze())
#     plt.show()
