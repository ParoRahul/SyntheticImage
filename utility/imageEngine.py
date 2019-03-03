# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 13:19:37 2019

@author: 683898
"""

from configparser import ConfigParser
import multiprocessing as mp
import datetime
from utility.alocateProduct import SynthesizeData
from utility.Image import Canvas
import os
import logging

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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

class ImageGenerator():
    def __init__(self, configFile_path):
        configFile = ConfigParser()
        configFile.read(configFile_path)
        self.Catgory_Code=configFile.get("DEFAULT","Category_Code")
        self.Number_of_Images= configFile.getint("DEFAULT","Number_Of_image")
        self.Number_of_Thread = configFile.getint("DEFAULT","Number_Of_Thread")
        self.Annotation_Type=configFile.get("DEFAULT","Annotation_type")
        self.Output_dir=configFile.get("PATHS","output_dir")
        self.date=str(datetime.datetime.now().date())
        SynthesizeData.set_Property(20)
        self.Synthesizer=SynthesizeData(configFile_path)
        self.imgBlueprint=[]
        self.Image=Canvas(self.Output_dir)
        logger.info(" ImageGenerator Instance created")
    
    def runGenerator(self,Process_id=0):
        logger.info('Running from Thread {}'.format(Process_id))
        try:
            for img_index in range(self.Number_of_Images):
                ImageNeame="SImage_"+self.date+"_"+str(Process_id)+"_"+str(img_index)+".jpg"
                ImagePath=os.path.join(self.Output_dir,ImageNeame)
                logger.info('Processing Image {}, Name {}'.format(img_index,ImagePath))
                shelfInfo=self.Synthesizer.PopulateData()
                if not shelfInfo:
                   logger.error(" Error While Processing Shelf") 
                else:   
                   #print(shelfInfo.returnSData)
                   #self.Image.PlotImage(shelfInfo.returnSData,ImagePath)
                   self.Image.PrintOnlybox(shelfInfo.returnSData,ImagePath)
        except Exception as e:    
               logger.exception(str(e))
                       
    def PrintConfigs(self):
        logger.info('-------------------------------------------------------------')
        logger.info('')
        logger.info('catgory_code               : {} '.format(self.Catgory_Code))
        logger.info('Number_of_images           : {} '.format(self.Number_of_Images))
        logger.info('Number_Of_Thread           : {} '.format(self.Number_of_Thread))
        logger.info('Output_Dir                 : {} '.format(self.Output_dir))
        logger.info('Annotation_Type            : {} '.format(self.Annotation_Type))
        logger.info('')
        logger.info('-------------------------------------------------------------')
                
    def __call__(self): 
        self.PrintConfigs()
#        ProcessList=[]
        self.runGenerator(1)
#        for index in range(self.Number_of_Thread):
#            process = mp.Process(target=self.runProcessing, args=(index,))
#            ProcessList.append(process)
#            process.start()
#        for process in ProcessList:
#            process.join()
