# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 19:52:27 2019

@author: 683898
"""
import random
from utility.shelfData import ShelfData
from utility.itemImage import itemImage
from utility.loadProdData import LoadProductData

class ShelfImage():
    
    PRODUCT_DATA=None
    PROD_PER_RACK=20
    
    @classmethod
    def set_Property(cls, prodData=None,number_prod=0):
        assert isinstance(prodData, LoadProductData)
        assert isinstance(number_prod, int)
        cls.PRODUCT_DATA = prodData
        cls.PROD_PER_RACK = number_prod            
           
    @classmethod        
    def getXshift(cls):
        xShift = int(cls.PRODUCT_DATA.max_prod_width*random.randint(1,200)/100)
        delta = int(50*random.randint(1,200)/100)
        if random.randint(1,20) > 19 :
            xShift = xShift + delta
        return xShift                   
    
    @classmethod
    def from_shelfData(cls,shelf=None,height=0,weidth=0,outImageName=None):
        assert isinstance(shelf, ShelfData)
        shelfImage = shelf.path
        shelfCount = shelf.shelf_count
        bit_thickness = shelf.bit_thickness
        left_bound = shelf.left_end
        right_bound = shelf.right_end
        selfPos =  shelf.Shelf_position
        outImgPath = outImageName
        return cls(shelfImage=shelfImage,height=height,weidth=weidth,shelfCount=shelfCount,
                 bit_thickness=bit_thickness,left_bound=left_bound,right_bound=right_bound,
                 selfPos=selfPos,outImageName=outImgPath)
    
    def __init__(self,shelfImage=None,height=0,weidth=0,shelfCount=0,
                 bit_thickness=0,left_bound=0,right_bound=0,
                 selfPos=[],outImageName=None):
        self.shelfImage = shelfImage
        self.height = height
        self.weidth = weidth
        self.shelfCount = shelfCount
        self.bit_thickness = bit_thickness
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.self_pos = selfPos
        self.outImgPath = outImageName
        self.itemImgArray = []  
        
    def push_Prod_Img(self):
        for shelfNo in range(self.shelfCount):
            if shelfNo < len(self.self_pos) - 1 :
               top_bound = self.self_pos[shelfNo+1]
               bottom_bound = self.self_pos[shelfNo]
            else:
               top_bound = 0
               bottom_bound = self.self_pos[shelfNo]
            height = bottom_bound - top_bound - int(self.bit_thickness)
            effective_height = height - (height*random.randint(0,10)/100)
            indexList = ShelfImage.PRODUCT_DATA.get_Nindex_At_random(ShelfImage.PROD_PER_RACK)
            Max_height = ShelfImage.PRODUCT_DATA.get_Nitems_MaxH(indexList)
            SizeRatio=effective_height/Max_height
            pasteL2R=random.randint(0,1)
            self.pushImages(indexList,SizeRatio,pasteL2R,top_bound,bottom_bound)
        
    def pushImages(self,indexList,SizeRatio,pasteL2R,top_bound,bottom_bound):
        if pasteL2R == 1:
           x_min = self.left_bound
        else:
           x_max = self.right_bound
        y_max = bottom_bound
        index=0
        for product in ShelfImage.PRODUCT_DATA.get_Data_from_index(indexList):
            if pasteL2R == 1:
               x_min = x_min + ShelfImage.getXshift()
            else :
               x_max = x_max - ShelfImage.getXshift()
            resizedW = int(SizeRatio*product.width)
            resizedH = int(SizeRatio*product.height)
            if pasteL2R == 1:
               x_max = x_min + resizedW
            else :
               x_min = x_max - resizedW
            y_min = y_max - resizedH
            if x_max > self.left_bound - 1 :
      	        break
            if x_min < 0:
               break
            if x_max <= x_min:
               break
            if y_max <= y_min:
               break
            if y_min < top_bound :
               continue
            prdW, prdH = product.getImageHW
            aspectFactor = prdW/prdH
            resizedW_old = resizedW
            resizedW = int(aspectFactor*resizedH) 
            if pasteL2R == 1:
               x_max = x_max + resizedW - resizedW_old 
            else:
               x_min = x_min - resizedW + resizedW_old 
            if x_max <= (x_min + 1):
               break
            if y_max <= (y_min + 1):
               break
            Bbox = {"id"       : index,
                    "class"    : product.className,
                    "ImgPath"  : product.ImgPath,
                    "MskPath"  : product.MASKPath,
                    "Height"   : resizedH,
                    "Weidth"   : resizedW,
                    "Xmin"     : x_min,
                    "Ymin"     : y_min,
                    "Xmax"     : x_max,
                    "Ymax"     : y_max
                   }
            self.ProdImgArray.append(itemImage(**Bbox))
            if pasteL2R == 1:
               x_min = x_max + 1
            if x_min > self.right_bound - 1 :
               break
            else:
               x_max = x_min - 1
            if x_max < 0 :
               break
    
    @property       
    def returndata(self):
        boxList=[]
        for item in self.itemImgArray:
            boxList.append(item.returnData)
        return {
                "EmptyShelf"    : self.shelfImage,
                "outImgPath"    : self.outImgPath,
                "height"        : 0,
                "weidth"        : 0,
                "Shelf_count"   : self.shelfCount,
                "Bbox"          : boxList
        }