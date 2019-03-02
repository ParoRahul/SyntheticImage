# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 23:26:50 2019

@author: Rahul
"""

from configparser import ConfigParser
import csv
import os
import random
from utility.productData import ProductData

class LoadProductData():
    
    PROD_IMG_DIR_TYPE1='directory'
    
    PROD_IMG_DIR_TYPE2='file'
    
    def __init__(self,configFile_path,datatype=None):
        configFile = ConfigParser()
        configFile.read(configFile_path)
        
        self.PDataList=[]
        self.Product_mask_found=False
        self.Directory_type=configFile.get("DEFAULT","Dir_Type")
        self.Product_Measurement=configFile.get("PATHS","Prod_Measurement")
        self.Product_Image=configFile.get("PATHS","Product_Image")
        self.Product_Mask=configFile.get("PATHS","Product_Mask")
        if os.path.isdir(self.Product_Mask):
           self.Product_mask_found=True
        assert(os.path.isfile(self.Product_Measurement)),\
        " Product Measurement file not found"
        assert(os.path.basename(self.Product_Measurement).split('.')[1] =='csv'),\
        " Product Measurement file is not *.csv type "
        assert(os.path.getsize(self.Product_Measurement)!= 0 ),\
        " Product Measurement file is has no data "
        assert(os.path.isdir(self.Product_Image)),\
        " Product Image Directrory not found "
        assert(len(os.listdir(self.Product_Image)) !=0),\
        " No Image found in Product Image Directrory  "
        assert self.ValidatteDirectoryType(),\
        "Product Image Directrory not Vaild "
        ProductData.set_Property(self.Product_Image,self.Product_Mask,self.Directory_type)
        self.loadProdRecords()
             
    def loadProdRecords(self): 
        with open(self.Product_Measurement, 'r') as csvfile:
             csvreader = csv.reader(csvfile)
             next(csvreader)
             cat_id=1
             for row in csvreader:
                 if self.Directory_type == LoadProductData.PROD_IMG_DIR_TYPE1:
                    prodimgpath=os.path.join(self.Product_Image,str(row[0]))
                    if not os.path.exists(prodimgpath):
                       continue
                    if len(os.listdir(prodimgpath)) <= 0:
                       continue
                 ProductDict={
                     "indx"           : int(cat_id),
                     "className"      : str(row[0]),
                     "height"         : float(row[1]),
                     "width"          : float(row[2]),
                 }
                 self.PDataList.append(ProductDict)
                 cat_id += 1
    
    def ValidatteDirectoryType(self):
        if self.Directory_type  in  \
           [LoadProductData.PROD_IMG_DIR_TYPE1,LoadProductData.PROD_IMG_DIR_TYPE2] :
            return True 
        return False 
    
    def get_Data(self,index):
        assert len(self.PDataList) > 0, " Prod Data Not Loaded "
        ProdDict=self.PDataList[index]
        return ProductData(**ProdDict)
    
    def get_Nrandom_Data(self,count):
        assert len(self.PDataList) > 0, " Prod Data Not Loaded "
        ProdIndex = random.sample(range(len(self.PDataList)), count)
        return [ ProductData(**self.PDataList[i]).returnData() for i in ProdIndex ]
    
    def get_Nindex_At_random(self,n):
        return [ random.randint(0,self.Product_count-1) for i in range(n)]
    
    def get_Data_from_index(self,indexList):
        assert len(self.PDataList) > 0, " Prod Data Not Loaded "
        assert isinstance(indexList, list)
        for index in indexList:
            yield ProductData(**self.PDataList[index]) 
    
    def get_Nitems_MaxH(self,indexList):
        return max([ self.PDataList[i] for i in indexList], 
                   key=lambda x:x['height'])['height']        
            
    @property
    def get_random_Data(self):
        assert len(self.PDataList) > 0, " Prod Data Not Loaded "
        item_index = random.randint(0,self.Product_count-1)
        ProdDict=self.PDataList[item_index]
        return ProductData(**ProdDict)
    
    @property
    def max_prod_height(self):
        return max(self.PDataList, key=lambda x:x['height'])['height']
    
    @property
    def max_prod_width(self):
        return max(self.PDataList, key=lambda x:x['width'])['width']
    
    @property
    def Product_count(self):
        return len(self.PDataList)
    
    @property
    def getDeltaW(self):
        xShift = int(self.max_prod_width*random.randint(1,200)/100)
        delta = int(50*random.randint(1,200)/100)
        if random.randint(1,20) > 19 :
            xShift = xShift + delta
        return xShift 
    
        
if __name__=="__main__":
   configPath=os.path.abspath("../config/config.yaml") 
   Perser = LoadProductData(configPath)  
   index=Perser.get_Nindex_At_random(2)
   for prod in Perser.get_Data_from_index(index):
       print(prod.className)