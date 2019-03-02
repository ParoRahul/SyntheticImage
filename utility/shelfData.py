# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:42:57 2019

@author: 683898
"""
import random

class ShelfData:
     
    def __init__(self,path=None,shelf_count=0,bit_thickness=0,
                 Shelf_position=[],left_end=0,right_end=0):
        assert isinstance(shelf_count, int),\
        "shelf_count Should be instance of int "
        assert isinstance(bit_thickness, int),\
        "bit_thickness Should be instance of int "
        assert isinstance(Shelf_position, list),\
        "bit_thickness Should be instance of int "
        assert isinstance(left_end, int),\
        "left_end Should be instance of int "
        assert isinstance(right_end, int),\
        "right_end Should be instance of int "
        self.path=path
        self.shelf_count=shelf_count
        self.bit_thickness=bit_thickness
        self.Shelf_position=Shelf_position
        self.left_end=left_end
        self.right_end=right_end
        self.Product_array=[]
        
    @property
    def returnSData(self):
        return {
                 "path"           : self.path,
                 "shelf_count"    : self.shelf_count,
                 "bit_thickness"  : self.bit_thickness,
                 "Shelf_position" : self.Shelf_position,
                 "left_end"       : self.left_end,
                 "right_end"      : self.right_end,
                 "Products"       : self.Product_array,
                 "ShelfHeight"    : 0,
                 "ShelfWeidth"    : 0,
                 "OutImageName"   : None
                 }
    
    @property
    def returnRackInfo(self):
        for rack in range(self.shelf_count):
            if rack < len(self.Shelf_position) - 1 :
               top = self.Shelf_position[rack+1]
               bottom = self.Shelf_position[rack]
            else:
               top = 0
               bottom = self.Shelf_position[rack]
            height = (bottom - top - self.bit_thickness)
            height = round(height*random.uniform(0.9,1),2)
            yield self.left_end,self.right_end,top,bottom,height 
            
    @property
    def boxCount(self):
        return len(self.Product_array)        
   