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
import time

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
    
    def runGenerator(self,Process_id=0):
        print('Running from Thread {}'.format(Process_id))
        try:
            for img_index in range(self.Number_of_Images):
                ImageNeame="SImage_"+self.date+"_"+str(Process_id)+"_"+str(img_index)+".jpg"
                ImagePath=os.path.join(self.Output_dir,ImageNeame)
                print('Processing Image {}, Name {}'.format(img_index,ImagePath))
                shelfInfo=self.Synthesizer.PopulateData()
                if not shelfInfo:
                   print(" Error While Processing Shelf") 
                else:   
                   #print(shelfInfo.returnSData)
                   self.Image.PlotImage(shelfInfo.returnSData,ImagePath)
        except Exception as e:    
               print (e)
                       
    def PrintConfigs(self):
        print('-------------------------------------------------------------')
        print('')
        print('catgory_code               : {} '.format(self.Catgory_Code))
        print('Number_of_images           : {} '.format(self.Number_of_Images))
        print('Number_Of_Thread           : {} '.format(self.Number_of_Thread))
        print('Output_Dir                 : {} '.format(self.Output_dir))
        print('Annotation_Type            : {} '.format(self.Annotation_Type))
        print('')
        print('-------------------------------------------------------------')
                
    def __call__(self): 
        start = time.time()
        self.PrintConfigs()
#        ProcessList=[]
        self.runGenerator(1)
#        for index in range(self.Number_of_Thread):
#            process = mp.Process(target=self.runProcessing, args=(index,))
#            ProcessList.append(process)
#            process.start()
#        for process in ProcessList:
#            process.join()
        print((time.time() - start) / 60, "minutes") 