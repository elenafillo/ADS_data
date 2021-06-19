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

jump = 0
prev_steps = 24
t = 6
path_to_results = '/work/ef17148/ADS/pytorch-CycleGAN-and-pix2pix/jump_results/'

# preparing the data
if jump == 0:
    #load cyclones
    cyclones=[]
    for f in os.listdir( str(pathlib.Path(__file__).parent)+"/eyes"):
        # print(f)
        if f.endswith("fg_full.npz"):
            cyclones.append(np.load(str(pathlib.Path(__file__).parent)+"/eyes/"+f,allow_pickle=True)["arr_0"])



    #get image pairs
    mx = 0
    mn = 10000

    dataindex={}
    l=0

    only_eyes=False
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
                if temp[i*48+j].shape == (256,256) and temp[i*48+j+t].shape == (256,256) and (not only_eyes or (local_max > 68 and local_min < 34)):
                    mx=max(mx,local_max)
                    mn=min(mn,local_min)
                    if j>=48-t:
                        mx=max(mx,np.nanmax(temp[i*48+j+t]))
                        mn=min(mn,np.nanmin(temp[i*48+j+t]))
                    dataindex[c][i].append(j)
                    l+=1


    for c in list(dataindex.keys()):
        remove_empty_keys(dataindex[c])
        if dataindex[c] == {}:
            del dataindex[c]

    to_try = []
    for e in dataindex[c].keys():
        landfall = 35 - 3*e
        [to_try.append([c, e, j]) for i in dataindex[c][e] for j in dataindex[c][e] if i-j == prev_steps and i == landfall]
	
    
    for item in to_try:
        t1=(cyclones[item[0]][item[1]*48+item[2]]-mn)/(mx-mn)*255
        t2=(cyclones[item[0]][item[1]*48+item[2]+t]-mn)/(mx-mn)*255
        t1int=np.array(t1).astype(np.uint8)
        t2int=np.array(t2).astype(np.uint8)
        #save images
        im1 = Image.fromarray(t1int)
        im2 = Image.fromarray(t2int)    

        fig, ax = plt.subplots()
        ax.contourf(im1, levels = 6, vmin = 0, vmax = 255)
        ax.set_position([0, 0, 1, 1])
        plt.axis('off')
        plt.savefig(path_to_results + 'original_real/'+ str(item[0])+'_' + str(item[1]) + '_' + str(item[2])+'.jpg')
        plt.close()
        fig, ax = plt.subplots()
        ax.contourf(im2, levels = 6, vmin = 0, vmax = 255)
        ax.set_position([0, 0, 1, 1])
        plt.axis('off')
        plt.savefig(path_to_results + 'original_fake/'+ str(item[0])+'_' + str(item[1]) + '_' + str(item[2])+'.jpg')
        plt.close()            

