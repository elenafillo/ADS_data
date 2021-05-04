import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
from PIL import Image
import random

def remove_empty_keys(d):
    ks=list(d.keys())
    for k in ks:
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
        cyclones.append(np.load(str(pathlib.Path(__file__).parent)+"/eyes/"+f,allow_pickle=True)["arr_0"])


f = open("data_progress.txt", "a")
f.write("Loaded all cyclones \n")
f.close()


#get image pairs
mx = 0
mn = 10000
print('number of cyclones:', len(cyclones))

dataindex={}
l=0
for c in range(len(cyclones)):
    dataindex[c]={}
    for i in range(9):
        dataindex[c][i]=[]
        for j in range(47):
            temp=cyclones[c]
            if temp[i*48+j].shape == (256,256) and temp[i*48+j+1].shape == (256,256):
                mx=max(mx,np.nanmax(temp[i*48+j]))
                mn=min(mn,np.nanmin(temp[i*48+j]))
                if j==46:
                    mx=max(mx,np.nanmax(temp[i*48+j+1]))
                    mn=min(mn,np.nanmin(temp[i*48+j+1]))
                dataindex[c][i].append(j)
                l+=1

f = open("data_progress.txt", "a")
f.write("Got all  image pair\n Normalising the data \n")
f.close()

#create relevant directories

path_to_data = '/work/ef17148/ADS/pytorch-CycleGAN-and-pix2pix/ADS_data'

# path_to_data=str(pathlib.Path(__file__).parent)+"/path/to/data/"

split={"train":0.8,"test":0.1,"val":0.1}

#save the data
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
        t1=(cyclones[cyclone][ensemble*48+timepoint]-mn)/(mx-mn)*255
        t2=(cyclones[cyclone][ensemble*48+timepoint+1]-mn)/(mx-mn)*255
        t1int=np.array(t1).astype(np.uint8)
        t2int=np.array(t2).astype(np.uint8)
        #save images
        im = Image.fromarray(t1int)
        im.save(path_to_data + "/A/"+s+"/"+str(i)+".jpg")
        im = Image.fromarray(t2int)
        im.save(path_to_data + "/B/"+s+"/"+str(i)+".jpg")
        #delete datapoint so it isn't duplicated
        dataindex[cyclone][ensemble].remove(timepoint)
        #remove any empty subdictionaries
        for c in list(dataindex.keys()):
            remove_empty_keys(dataindex[c])
            if dataindex[c]=={}:
                del dataindex[c]