import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from PIL import Image
import random


f = open("data_progress.txt", "a")
f.write("Starting to generate data \n")
f.close()

#load cyclones
cyclones=[]
for f in os.listdir( str(pathlib.Path(__file__).parent)+"/eyes"):
    # print(f)
    if f.endswith("fg_full.npz"):
        cyclones.append(np.load(str(pathlib.Path(__file__).parent)+"/eyes/"+f,allow_pickle=True))



f = open("data_progress.txt", "a")
f.write("Loaded all cyclones \n")
f.close()


#get image pairs
t1=[]
t2=[]

mxs = []
mns = []
print('len:', len(cyclones))
for c in cyclones:
    for i in range(9):
        for j in range(47):
            if c["arr_0"][i*48+j].shape ==(256,256):
                mxs.append(np.nanmax(c["arr_0"][i*48+j]))
                mns.append(np.nanmin(c["arr_0"][i*48+j+1]))
            t1.append(c["arr_0"][i*48+j])
            t2.append(c["arr_0"][i*48+j+1])

f = open("data_progress.txt", "a")
f.write("Got all  image pairs, " + str(len(t1)) +  "\n Normalising the data \n")
f.close()


#normalise the data to the 0-255 range
mn=min(mns)
mx=min(mxs)
t1=(t1-mn)/(mx-mn)*255
t2=(t2-mn)/(mx-mn)*255
t1int=np.array(t1).astype(np.uint8)
t2int=np.array(t2).astype(np.uint8)

#create relevant directories
#if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path"):
#    os.mkdir(str(pathlib.Path(__file__).parent)+"/path")
#if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to"):
#    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to")
#if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data"):
#    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data")
#if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/A"):
#    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/A")
#if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/B"):
#    os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/B")


path_to_data = '/work/ef17148/ADS/pytorch-CycleGAN-and-pix2pix/ADS_data'


split={"train":0.8,"test":0.1,"val":0.1}



#randomise the order of the samples
order=list(range(len(t1)))
random.shuffle(order)
t1=[t1[i] for i in order]
t2=[t2[i] for i in order]

#save the data
l=len(t1)
for s in list(split.keys()):
    f = open("data_progress.txt", "a")
    f.write("Saving data in mode " + s)
    f.close()

#    if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/A/"+s):
#        os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/A/"+s)
#    if not os.path.exists(str(pathlib.Path(__file__).parent)+"/path/to/data/B/"+s):
#        os.mkdir(str(pathlib.Path(__file__).parent)+"/path/to/data/B/"+s)
    for i in range(int(l*split[s])):
        im = Image.fromarray(t1int[0])
        im.save(path_to_data + "/A/"+s+"/"+str(i)+".jpg")
        im = Image.fromarray(t2int[0])
        im.save(path_to_data + "/B/"+s+"/"+str(i)+".jpg")
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
