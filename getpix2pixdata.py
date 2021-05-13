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

contour=True
rgb= True
t=6
cut_to_centre = False
only_eyes = True
before_landfall = True

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
    print(c)
    for i in range(9):
        dataindex[c][i]=[]
        for j in range(48-t):
            temp=cyclones[c]
            try:
                local_max = np.max(temp[i*48+j])
                local_min = np.min(temp[i*48+j])
            except ValueError:  #raised if array is empty.
                local_max = 0
                local_min = 0
                pass
            if temp[i*48+j].shape == (256,256) and temp[i*48+j+t].shape == (256,256) and (not only_eyes or (local_max > 68 and local_min < 34)) and (not before_landfall or j < 35 - 3*i):
                mx=max(mx,local_max)
                mn=min(mn,local_min)
                if j>=48-t:
                    mx=max(mx,np.nanmax(temp[i*48+j+t]))
                    mn=min(mn,np.nanmin(temp[i*48+j+t]))
                dataindex[c][i].append(j)
                l+=1

f = open("data_progress.txt", "a")
f.write("Got all  image pairs, length " + str(l) + "\n Normalising the data \n")
f.close()

# remove items that are empty
for c in list(dataindex.keys()):
    remove_empty_keys(dataindex[c])
    if dataindex[c]=={}:
        del dataindex[c]

print("it worked")


#create relevant directories

#path_to_data = '/work/ef17148/ADS/pytorch-CycleGAN-and-pix2pix/all_data/eyes_contours_3_col'
path_to_data = '/work/ef17148/ADS/pytorch-CycleGAN-and-pix2pix/all_data/new_contours_6_col/'
# path_to_data=str(pathlib.Path(__file__).parent)+"/path/to/data/"

split={"train":0.8,"test":0.1,"val":0}

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
        t2=(cyclones[cyclone][ensemble*48+timepoint+t]-mn)/(mx-mn)*255
        if cut_to_centre:
            t1 = t1[128-32:128+32,128-32:128+32]
            t2 = t2[128-32:128+32,128-32:128+32]
        t1int=np.array(t1).astype(np.uint8)
        t2int=np.array(t2).astype(np.uint8)
        #save images
        im1 = Image.fromarray(t1int)
        im2 = Image.fromarray(t2int)

        if cut_to_centre:
            im1 = im1.resize((256,256))
            im2 = im2.resize((256, 256))
        if not rgb and not contour:
            im1.save(path_to_data + "/A/"+s+"/"+str(i)+".jpg")
            im2.save(path_to_data + "/B/"+s+"/"+str(i)+".jpg")
        elif contour:
            fig, ax = plt.subplots()
            if rgb:
                ax.contourf(im1, levels = 6, vmin = 0, vmax = 255)
            if not rgb:
                ax.contourf(im1,levels=6, cmap="Greys")
            ax.set_position([0, 0, 1, 1])
            plt.axis('off')
            plt.savefig(path_to_data + "/A/"+s+"/"+str(cyclone) + '_' + str(ensemble)+ '_' +str(timepoint)+".jpg")
            plt.close()
            fig, ax = plt.subplots()
            if not rgb:
                ax.contourf(im2,levels=6, cmap="Greys")
            if rgb:
                ax.contourf(im2, levels = 6, vmin = 0, vmax = 255)
            ax.set_position([0, 0, 1, 1])
            plt.axis('off')
            plt.savefig(path_to_data + "/B/"+s+"/"+str(cyclone) + '_' + str(ensemble)+ '_' +str(timepoint)+".jpg")
            plt.close()
        else:
            fig, ax = plt.subplots()
            ax.contourf(im1,levels=6)
            ax.set_position([0, 0, 1, 1])
            plt.axis('off')
            plt.savefig(path_to_data + "/A/"+s+"/"+str(i)+".jpg")
            plt.close()
            fig, ax = plt.subplots()
            ax.contourf(im2,levels=6)
            ax.set_position([0, 0, 1, 1])
            plt.axis('off')
            plt.savefig(path_to_data + "/B/"+s+"/"+str(i)+".jpg")
            plt.close()
        #delete datapoint so it isn't duplicated
        dataindex[cyclone][ensemble].remove(timepoint)
        #remove any empty subdictionaries
        for c in list(dataindex.keys()):
            remove_empty_keys(dataindex[c])
            if dataindex[c]=={}:
                del dataindex[c]
            
