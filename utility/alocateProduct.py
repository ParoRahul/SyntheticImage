# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 19:52:27 2019

@author: 683898
"""

from utility.loadShelfData import  LoadShelfData
from utility.loadProdData import LoadProductData
import random
import logging

logger=logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter=logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('MainLog.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
stream_handler= logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.propagate = False

class SynthesizeData(LoadShelfData,LoadProductData):
    
    PROD_PER_RACK=20
    
    @classmethod
    def set_Property(cls, prod_per_rack=0):
        assert isinstance(prod_per_rack, int)
        cls.PROD_PER_RACK = prod_per_rack            
               
    def __init__(self,configFile_path=None):
        LoadShelfData.__init__(self,configFile_path)
        LoadProductData.__init__(self,configFile_path)
                
    def PopulateData(self):
        # select Shelf Image Randomly
        shelfdata=self.get_random_ShelfData
        # select N product At random
        indexList = self.get_Nindex_At_random(SynthesizeData.PROD_PER_RACK)
        # get The maximum Height From Index List
        Max_height = self.get_Nitems_MaxH(indexList)
        # Determin Size Ratio for pasting product Image
        for top,bottom,height in shelfdata.returnRackInfo:
            SizeRatio=height/Max_height
            pasteL2R=True if random.randint(0,1) == 1 else False
            left=shelfdata.left_end
            right=shelfdata.right_end
            for product in self.get_Data_from_index(indexList):
                delta=self.getDeltaW
                if product.fit_product(left,right,top,bottom,
                                    SizeRatio,pasteL2R,delta):
                   shelfdata.Product_array.append(product.returnPData)
                   if pasteL2R:
                      left=product.xmax + 1
                      if left > right -1:
                         break
                   else:
                      right=product.xmin - 1
                      if right < 0:
                         break
                else:
                    break
        if shelfdata.boxCount > 0:
           return shelfdata
        else :
           logger.error(" Error from PopulateImage")
           return False
       
    def printConfigs(self):
        logger.info("-------------------------------------------------------------")
        logger.info("")
        logger.info('Shelf_Measurement_path     : {} '.format(self.Shelf_Measurement))
        logger.info('Shelf_Image                : {} '.format(self.Shelf_Image))
        logger.info('Product_Measurement_path   : {} '.format(self.Product_Measurement))
        logger.info('Product_image              : {} '.format(self.Product_Image))
        logger.info('Product_mask               : {} '.format(self.Product_Mask))
        logger.info("")
        logger.info("-------------------------------------------------------------")