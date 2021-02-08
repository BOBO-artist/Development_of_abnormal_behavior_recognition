from __future__ import division
from torch.utils.data import Dataset, DataLoader
import getpass
import os
import socket
import numpy as np
from .preprocess_data import *
from PIL import Image, ImageFilter
import pickle
import glob
#import dircache
import pdb

label_index = ['abandonment',  'escalator_fall',  'fainting',  'surrounding_fall',  'theft']

def get_cctv(opt, frame_path, Total_frames, train):
    clip = []
    clip_image = []
    path_list = glob.glob(frame_path+'/*')
    path_list.sort()
    i = 0
    for a in range(len(path_list)):
        clip.append(path_list[a])
    
   
    path_len = len(path_list) -1
   

    if train == 1:
        ran_idx = np.random.randint(0, path_len)
    else:
        ran_idx = np.random.randint(int(len(path_list)/2), int(len(path_list)*3/4) )
        
        ran_idx = int(len(path_list)/4) 
        

    
    return clip[ran_idx]


class CCTV_loader_2d(Dataset):
    def __init__(self, train, opt,transform=None):
        self.transform = transform
        if train == 1:
            self.clips = glob.glob('/workspace/final_mars/MARS/dataset/action/dataset/train/*/*')
        else:
            self.clips = glob.glob('/workspace/final_mars/MARS/dataset/action/dataset/test/*/*')
            self.clips.sort()
        self.opt = opt
        self.train_val_test = train
        self.train = train
    def __len__(self):
        return len(self.clips)
    def __getitem__(self, idx):
        path = self.clips[idx]
        label = path.split('/')[8]
        
        if self.train != 1:
            label_name = path.split('/')[9]
        else:
            label_name=0
            
        label = label_index.index(label)
        Total_frames = len(glob.glob(path+'/*.jpg'))
#         print("label : ", label)
        
        clip = get_cctv(self.opt, path, Total_frames, self.train)
#         print(type(clip))
        image = Image.open(clip).convert("RGB")
#         print(type(image))
        if self.transform:
            image = self.transform(image)
        return(image, label, label_name)