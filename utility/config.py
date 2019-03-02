# -*- coding: utf-8 -*-
"""
Created on tue nov 13 01:19:28 2018

@author: 683898
"""
import os
import sys
from configparser import ConfigParser

config=ConfigParser() 

config[ "PATHS"]={
        "Shelf_Measurement"       : "D:/Img_Repo/Tf_Images/PW/WITH_GT/background_measurement.csv",
        "Shelf_Image"             : "D:/Img_Repo/Tf_Images/PW/WITH_GT/backgrounds",
        "Prod_Measurement"        : "D:/Img_Repo/Tf_Images/PW/WITH_GT/product_measurement_original.csv",
        "Product_Image"           : "D:/Img_Repo/Tf_Images/PW/WITH_GT/PW_output",  
        "Product_Mask"            : "D:/Img_Repo/Tf_Images/PW/WITH_GT/PW_masks",
        "Output_Dir"              : "D:/Img_Repo/Debug"
        }

config[ "DEFAULT"]={
        "Category_Code"     : "WPW",
        "Image_Type"        : ['jpg','JPEG','JPG','png','PNG'],
        "Dir_Type"          : "directory",
        "Write_Image"       : False ,
        "Number_Of_Thread"  : 2,
        "Number_Of_Image"   : 10,
        "Annotation_Type"   : "COCO"
        }


def generate_Config(configFileName):
    try :
        if (os.path.exists(configFileName)):
            print(" Amending Existing Config File")
            with open (configFileName,'w') as configFile:
                 config.write(configFile)
        else:
            print(" Writing Fresh Config File")
            with open (configFileName,'w') as configFile:
                 config.write(configFile)
    except Exception as e:
        sys.exit(e)
    else :
        print(" Config File Sucessfully created")
    finally:
        pass
    
def test_Config(configFileName):
    configFile = ConfigParser()
    configFile.read(configFileName)
    catgory_code=configFile.get("DEFAULT","Category_Code")
    Number_of_images= int(configFile.get("DEFAULT","Number_Of_image"))
    Number_Of_Thread = int(configFile.get("DEFAULT","Number_Of_Thread"))
    Shelf_Measurement=configFile.get("PATHS","Shelf_Measurement")
    Shelf_Image=configFile.get("PATHS","Shelf_Image")
    Product_Measurement_path=configFile.get("PATHS","Prod_Measurement")
    Product_image=configFile.get("PATHS","Product_Image")
    Product_mask=configFile.get("PATHS","Product_Mask")
    OUTPUTPATH=configFile.get("PATHS","Output_Dir")
    Annotation_format=configFile.get("DEFAULT","Annotation_Type")
    print('catgory_code               : {} '.format(catgory_code))
    print('Number_of_images           : {} '.format(Number_of_images))
    print('Number_Of_Thread           : {} '.format(Number_Of_Thread))
    print('BackGround_Measurement_path: {} '.format(Shelf_Measurement))
    print('BackGround_Image           : {} '.format(Shelf_Image))
    print('Product_Measurement_path   : {} '.format(Product_Measurement_path))
    print('Product_image              : {} '.format(Product_image))
    print('Product_mask               : {} '.format(Product_mask))
    print('OUTPUTPATH                 : {} '.format(OUTPUTPATH))
    print('Annotation_format          : {} '.format(Annotation_format))
    
if __name__=="__main__":
   configFileName='../config/config.yaml' 
   #test_Config(configFileName) 
   generate_Config(configFileName)   
    
