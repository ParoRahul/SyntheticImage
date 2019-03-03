# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 19:01:22 2019

@author: 683898
"""
import numpy as np
import os
from PIL import Image
from configparser import ConfigParser

class Canvas:
    
    def __init__(self,outPtah):
        self.outpath=outPtah
        pass
    
    def PlotImage(self,imgdict,ImagePath):
        BGround_Image = Image.open(imgdict["path"])
        bgImageCopy = np.copy(BGround_Image)
        height,weidth = BGround_Image.size
        imgdict["ShelfHeight"]=height
        imgdict["ShelfWeidth"]=weidth
        for box in imgdict["Products"]:
            x_min,x_max,y_min,y_max = box["xmin"],box["xmax"],box["ymin"],box["ymax"]
            resizedW,resizedH=box["Rwidth"],box["Rheight"]
            maskFileName = box["MskPath"]
            has_mask = False
            if os.path.exists(maskFileName) :
               maskImage = Image.open(maskFileName)
               maskImage = maskImage.resize((resizedW,resizedH), Image.BICUBIC)
               np_maskImage = np.array(maskImage)
               #print("np_maskImage:"+str(np_maskImage.ndim))
               if np_maskImage.ndim == 3 :
                  maskTemp = np_maskImage[:,:,0]
               elif np_maskImage.ndim == 2 :
                  maskTemp = np_maskImage
               mask = (maskTemp>0)
               has_mask = True
            prodImage = Image.open(box["ImgPath"]) 
            prodImage = prodImage.resize((resizedW,resizedH), Image.BICUBIC)
            np_prodImage = np.array(prodImage)
            paste_flag = False
            try:
               if has_mask :
                  bgTemp = bgImageCopy[y_min:y_max,x_min:x_max,:]
                  bgTemp[(mask)] = np_prodImage[(mask)]
                  bgImageCopy[y_min:y_max,x_min:x_max,:] = bgTemp
               else :
                  bgImageCopy[y_min:y_max,x_min:x_max,:] = np_prodImage
               paste_flag = True
            finally:
               if paste_flag == False:
                  print("Exception while pasting")
                  break 
        im = Image.fromarray(bgImageCopy)
        outfile=os.path.join(self.outpath,ImagePath)
        im.save(outfile)
        
    def PrintOnlybox(self,imgdict,ImagePath):
        BGround_Image = Image.open(imgdict["path"])
        #bgImageCopy = np.copy(BGround_Image)
        height,weidth = BGround_Image.size
        blankimage = Image.new('RGB', BGround_Image.size)
        outfile=os.path.join(self.outpath,ImagePath)
        blankimage.save(outfile)
        pass
    
if __name__=="__main__":
    configFile_path=os.path.abspath("../config/config.yaml")
    configFile = ConfigParser()
    configFile.read(configFile_path)
    Output_dir=configFile.get("PATHS","output_dir")    
    canvas = Canvas(Output_dir)    
    ImagePath=os.path.join(Output_dir,"BluePrint.jpg")
    canvas.PrintOnlybox({},ImagePath)