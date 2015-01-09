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
def renameVideoFiles(videos,config):

  if not os.path.exists(config['tgtDir']):
    os.mkdir(config['tgtDir'], mode=0o775)
  sep='_'  
  
  subdirs = []
  #tbd this iteration only works on 2 level depth
  for k,v in videos.items():
    subdirs.append(k) 
    if isinstance(v,dict):
      videos=next(iter (v.values()))
      subdirs.extend(iter (v.keys()))  
    else:
      videos=v
  
  srcBasePath=config['srcDir']
  tgtBasePath=config['tgtDir']
  for subdir in subdirs:
    srcBasePath=os.path.join(srcBasePath,subdir)
    tgtBasePath=os.path.join(tgtBasePath,subdir)
  
  for curVideo in videos:
    logging.debug(curVideo)
    """ Number: "00126"
    Title: Sternsinger Georg und Henry
    Extension: MTS """
      
    srcCompleteFileName=os.path.join(srcBasePath,curVideo['Number']+'.'+curVideo['Extension'])
    tgtCompleteFileName=os.path.join(tgtBasePath,curVideo['Number']+sep+curVideo['Title']+'.'+curVideo['Extension'])
    logging.debug("src="+srcCompleteFileName)
    logging.debug("tgt="+tgtCompleteFileName)
    #shutil.move(srcCompleteFileName, tgtCompleteFileName)
    #subprocess.call(['ffmpeg', '-i', srcCompleteFileName])
    
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

renameVideoFiles(videos,config)
            
#print ("successfully transfered %s " % inputParams["srcDirName"])

