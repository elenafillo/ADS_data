import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from PIL import Image
import random

def remove_empty_keys(d):
    for k in d.keys():
        if not d[k]:
            del d[k]

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

mx = 0
mn = 10000
print('number of cyclones:', len(cyclones))

dataindex={}

for c in range(len(cyclones)):
    print(c)
    dataindex[c]={}
    for i in range(9):
        print(i)
        dataindex[c][i]=[]
        for j in range(47):
            if cyclones[c]["arr_0"][i*48+j].shape == (256,256) and cyclones[c]["arr_0"][i*48+j+1].shape == (256,256):
                mx=max(mx,np.nanmax(cyclones[c]["arr_0"][i*48+j]))
                mn=min(mn,np.nanmin(cyclones[c]["arr_0"][i*48+j]))
                if j==46:
                    mx=max(mx,np.nanmax(cyclones[c]["arr_0"][i*48+j+1]))
                    mn=min(mn,np.nanmin(cyclones[c]["arr_0"][i*48+j+1]))
                dataindex[c][i].append(j)

f = open("data_progress.txt", "a")
f.write("Got all  image pairs, " + str(len(t1)) +  "\n Normalising the data \n")
f.close()

#create relevant directories

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
    for i in range(int(l*split[s])):
        #randomly select a datapoint
        cyclone=random.choice(list(dataindex.keys()))
        ensemble=random.choice(list(dataindex[cyclone].keys()))
        timepoint=random.choice(dataindex[cyclone][ensemble])
        #normalise
        t1=(cyclones[cyclone][ensemble][timepoint]-mn)/(mx-mn)*255
        t2=(cyclones[cyclone][ensemble][timepoint+1]-mn)/(mx-mn)*255
        t1int=np.array(t1).astype(np.uint8)
        t2int=np.array(t2).astype(np.uint8)
        #save images
        im = Image.fromarray(t1int[0])
        im.save(path_to_data + "/A/"+s+"/"+str(i)+".jpg")
        im = Image.fromarray(t2int[0])
        im.save(path_to_data + "/B/"+s+"/"+str(i)+".jpg")
        #delete datapoint so it isn't duplicated
        t1int=np.delete(t1int,0,0)
        t2int=np.delete(t2int,0,0)
        #remove any empty subdictionaries
        for c in list(dataindex.keys()):
            remove_empty_keys(dataindex[c])
            if dataindex[c]=={}:
                del dataindex[c]

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
