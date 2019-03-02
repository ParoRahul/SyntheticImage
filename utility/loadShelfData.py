# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:58:09 2019

@author: 683898
"""
from configparser import ConfigParser
import csv
import os
import random
from utility.shelfData import ShelfData

class LoadShelfData():
    
    def __init__(self,configFile_path,datatype=None):
        configFile = ConfigParser()
        configFile.read(configFile_path)        
        self.SDataList=[]
        self.Shelf_Measurement=configFile.get("PATHS","Shelf_Measurement")
        self.Shelf_Image=configFile.get("PATHS","Shelf_Image")
        assert(os.path.isfile(self.Shelf_Measurement)),\
        " Shelf Measurement file not found"
        assert(os.path.basename(self.Shelf_Measurement).split('.')[1] =='csv'),\
        " Shelf Measurement file is not *.csv type "
        assert(os.path.getsize(self.Shelf_Measurement)!= 0 ),\
        " shelf Measurement file is has no data "
        assert(os.path.isdir(self.Shelf_Image)),\
        " shelf Image Directrory not found "
        assert(len(os.listdir(self.Shelf_Image)) !=0),\
        " No Image found in shelf Image Directrory  "
        self.loadshelfRecors()
             
    def loadshelfRecors(self):
        with open(self.Shelf_Measurement, 'r') as csvfile:
             csvreader = csv.reader(csvfile)
             next(csvreader)
             for row in csvreader:
                 shelfimgpath=os.path.join(self.Shelf_Image,str(row[0]))
                 if not os.path.exists(shelfimgpath):
                    continue 
                 ShelfDict={
                 "path"           : shelfimgpath,
                 "shelf_count"    : int(row[1]),
                 "bit_thickness"  : int(row[2]),
                 "Shelf_position" :[int(row[3]),int(row[4]),int(row[5]),int(row[6])],
                 "left_end"       : int(row[7]),
                 "right_end"      : int(row[8]) 
                 }
                 self.SDataList.append(ShelfDict)
    
    def get_ShelfData(self,index):
        assert len(self.SDataList) > 0, " Prod Data Not Loaded "
        ShelfDict=self.SDataList[index]
        return ShelfData(**ShelfDict)             
    
    @property
    def get_random_ShelfData(self):
        assert len(self.SDataList) > 0, " Shelf Data Not Loaded "
        item_index = random.randint(0,len(self.SDataList)-1)
        ShelfDict=self.SDataList[item_index]
        return ShelfData(**ShelfDict)
                
if __name__=="__main__":
   configPath=os.path.abspath("../config/config.yaml") 
   Perser = LoadShelfData(configPath)   
   shelf = Perser.get_Data(2).returnData
   print(shelf)