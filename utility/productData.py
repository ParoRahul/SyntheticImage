# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:48:58 2019

@author: 683898
"""
import os
import random
from PIL import Image

class ProductData:
        
    DIRECTRY_TYPE=None
    PROD_IMG_DIR=None
    MASK_IMG_DIR=None

    @classmethod
    def set_Property(cls,Prod_dir=None,Mask_dir=None,Dir_Type=None):
        cls.PROD_IMG_DIR=Prod_dir
        cls.MASK_IMG_DIR=Mask_dir
        if Prod_dir is None:
           cls.DIRECTRY_TYPE= ProductData.getDirType() 
        else:   
           cls.DIRECTRY_TYPE= Dir_Type
           
    @classmethod
    def getDirType(cls):
        Prod_dir_type="NA"
        for file in os.listdir(cls.PROD_IMG_DIR):
            if os.path.isdir(os.path.join(cls.PROD_IMG_DIR,file)) == True:
               if Prod_dir_type=='directrory':
                  continue
               elif Prod_dir_type=="NA":
                    Prod_dir_type='directrory'
               else:
                    return "NA"
            elif (os.path.isfile(os.path.join(cls.PROD_IMG_DIR,file))) == True:
               if Prod_dir_type=='file':
                  continue
               elif Prod_dir_type=="NA":
                    Prod_dir_type='file'
               else:
                    return "NA"
            else:
                return False
        return True
    
    def __init__(self,indx=0,className=None,height=0,width=0):
        assert isinstance(indx, int) ,\
        "indx Should be instance of int "
        assert isinstance(height, float),\
        "height Should be instance of float "
        assert isinstance(width, float),\
        "width Should be instance of float "
        self.id=indx
        self.className=className
        self.ImgPath = self.getImagePath()
        self.Rheight = height
        self.Rwidth = width
        self.xmin=0
        self.ymin=0
        self.xmax=0
        self.ymax=0
       
    def getImagePath(self):
        if ProductData.DIRECTRY_TYPE == 'directory':
           Imgpath=os.path.join(ProductData.PROD_IMG_DIR,self.className) 
           if os.path.isdir(Imgpath):
              if len(os.listdir(Imgpath)) == 1 :
                  file = os.listdir(Imgpath)[0]
              else:    
                  file = random.choice(os.listdir(Imgpath)) 
              return os.path.join(Imgpath,file)
           else:
               return None
        elif ProductData.DIRECTRY_TYPE == 'file':
            pass
        else:
            return None
               
    @property
    def ImageCount(self):
        if ProductData.DIRECTRY_TYPE == "directory":
           Imgpath=os.path.join(ProductData.PROD_IMG_DIR,self.className) 
           if os.path.isdir(Imgpath):
              return len(os.listdir(Imgpath))
           else:
              return None
        elif ProductData.DIRECTRY_TYPE == 'file':
            return 1
        else:
            return None 
        
    @property
    def MASKPath(self):
        if ProductData.MASK_IMG_DIR is None:
           return None
        Imgfile=os.path.basename(self.ImgPath)
        maskfile=Imgfile.replace(".jpg","_mask.jpg")
        maskPath=os.path.join(ProductData.MASK_IMG_DIR,self.className,maskfile)
        if os.path.isfile(maskPath):
           return maskPath
        else:
           maskPath=os.path.join(ProductData.MASK_IMG_DIR,maskfile) 
           if os.path.isfile(maskPath):
              return maskPath
           else:
              return None 
       
    @property
    def getImageHW(self):
        prodImage = Image.open(self.ImgPath)
        return prodImage.size
    
    @property
    def MaskCount(self):
        if ProductData.MASK_IMG_DIR is None:
           return 0
        if ProductData.DIRECTRY_TYPE == "directory":
           Mskpath=os.path.join(ProductData.MASK_IMG_DIR,self.className) 
           if os.path.isdir(Mskpath):
              return len(os.listdir(Mskpath))
           else:
               return 0
        elif ProductData.DIRECTRY_TYPE == 'file':
            return 1
        else:
            return None
             
    def fit_product(self,left,right,top,bottom,SizeRatio,pasteL2R,delta):
        Wmodified = int(SizeRatio*self.Rwidth)
        Hmodified = int(SizeRatio*self.Rheight)
        if pasteL2R:
           self.xmin = left + delta 
           self.xmax = self.xmin + Wmodified
           if self.xmax > right - 1  :
      	      return False
        else:
           self.xmax = right - delta 
           self.xmin = self.xmax - Wmodified
           if self.xmin < 0:
              return False
        if self.xmax <= self.xmin:
           return False  
        self.ymax = bottom
        self.ymin = self.ymax - Hmodified
        if self.ymax <= self.ymin:
           return False
        if self.ymin < top :
           return False
        IWeidth,IHeight = self.getImageHW
        aspectRatio = IWeidth/IHeight
        newWeidth = int(aspectRatio*Hmodified) 
        self.Rheight=Hmodified
        self.Rwidth=newWeidth
        if pasteL2R:
           self.xmax = self.xmax + newWeidth - Wmodified 
        else:
           self.xmin = self.xmin - newWeidth + Wmodified 
        if self.xmax <= self.xmin + 1:
           return False
        if self.ymax <= self.ymin + 1:
           return False
        return  True 

    @property
    def returnPData(self):
        return  {
                 "id"             : self.id,
                 "ImgPath"        : self.ImgPath,
                 "MskPath"        : self.MASKPath,
                 "className"      : self.className,
                 "Rheight"        : self.Rheight,
                 "Rwidth"         : self.Rwidth,
                 "xmin"           : self.xmin,
                 "ymin"           : self.ymin,
                 "xmax"           : self.xmax,
                 "ymax"           : self.ymax
                }     