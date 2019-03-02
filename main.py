# -*- coding: utf-8 -*-
"""

Created on Tue Oct 23 15:19:30 2018

@author: 683898

"""
from os.path import abspath
import traceback
from utility.imageEngine import ImageGenerator


def Main():
    try:
        configPath=abspath("./config/config.yaml")
        print("config Files Loaded From Path {}".format(configPath))
        imageGenerator = ImageGenerator(configPath)
        imageGenerator()  
    except Exception as e:
        traceback.print_tb(e.__traceback__)
                
if __name__ == '__main__':
    Main()