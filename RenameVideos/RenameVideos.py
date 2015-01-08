#!/usr/bin/python
# -*- coding: utf-8 -*-

description = """This program searches a given Source Directory for files and performs 
a given operation (encode from asciii to utf8). The reencoded files are stored under target directory
preserving the directory structure. 
"""

import os
import fnmatch
import shutil
#import glob
import sys
import re
import string
import logging
import logging.config 

import json
import yaml
import taglib # https://pypi.python.org/pypi/pytaglib
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC,TXXX, POPM, TCMP, ID3NoHeaderError
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3, HeaderNotFoundError

import math
import subprocess
#from xml import dom
#from xml.dom import minidom
#from xml.dom import Node



     
############################################################################
def initLogger(config):
    handler = logging.StreamHandler(sys.stdout)
    frm = logging.Formatter("%(asctime)s [%(levelname)-5s]: %(message)s", "%Y%m%d %H:%M:%S")
    handler.setFormatter(frm)
    logger = logging.getLogger()
    logger.addHandler(handler)
    print('config["loglevel"] = ' + config["loglevel"])
    if config["loglevel"] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


############################################################################
# main starts here
# global variables

if len(sys.argv) == 1 :
    print(description)
    print(sys.argv[0] + "<configfile>")
    configFileName = 'RenameVideos.yaml'
else:
    configFileName = sys.argv[1]


# Python2 
#with open(configFileName, 'r') as cfgfile:
# Python3 
with open(configFileName, 'r',encoding='utf-8') as cfgfile:
    #config = json.load(cfgfile)
    config = yaml.load(cfgfile)
logger = initLogger(config)
logging.info(config)

videos = config["videos"]  
logging.info(videos)

#processDirForUpdateTagsForFile(inputParams, logging)
#processDirForMP3s(inputParams, logging)
            
#print ("successfully transfered %s " % inputParams["srcDirName"])

