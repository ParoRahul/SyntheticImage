# -*- coding: utf-8 -*-
"""

Created on Tue Oct 23 15:19:30 2018

@author: 683898

"""
from os.path import abspath
from utility.imageEngine import ImageGenerator
import time
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

def Main():
    try:
        start_time = time.time()
        configPath=abspath("./config/config.yaml")
        #logger.info("config Files Loaded From Path ")
        logger.info("config Files Loaded From Path {}".format(configPath))
        imageGenerator = ImageGenerator(configPath)
        imageGenerator()  
        logger.info("Completion Time :{} minutes".format((time.time() - start_time)/60)) 
    except Exception as e:
        logger.exception(str(e))
                
if __name__ == '__main__':
    Main()