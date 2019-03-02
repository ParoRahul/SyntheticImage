# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 18:26:15 2019

@author: 683898
"""

class itemImage:
    
    def __init__(self,index=0,className=None,ImagePath=None,MaskPath=None,
                 Height=0,Weidth=0,Xmin=0,Ymin=0,Xmax=0,Ymax=0):
        self.id=index
        self.className=className
        self.ImagePath=ImagePath
        self.MaskPath=MaskPath
        self.Height=Height
        self.Weidth=Weidth
        self.Xmin=Xmin
        self.Ymin=Ymin
        self.Xmax=Xmax
        self.Ymax=Ymax
        
    @property
    def returnData(self):
        return {
        "id":        self.id,
        "className": self.className,
        "ImagePath": self.ImagePath,
        "MaskPath" : self.MaskPath,
        "Height"   : self.Height,
        "Weidth"   : self.Weidth,
        "Xmin"     : self.Xmin,
        "Ymin"     : self.Ymin,
        "Xmax"     : self.Xmax,
        "Ymax"     : self.Ymax
        }
         
        