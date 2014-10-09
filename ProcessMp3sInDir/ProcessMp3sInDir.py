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

#from xml import dom
#from xml.dom import minidom
#from xml.dom import Node



############################################################################
def findTGTFileName(srcCompleteFileName,srcDirName,tgtDirName):
    logging.debug(" srcCompleteFileName = " + srcCompleteFileName)
    logging.debug(" srcDirName = " + srcDirName)
    logging.debug(" tgtDirName = " + tgtDirName)
    #fileName = os.path.basename(srcCompleteFileName)
    srcRelativePathName=srcCompleteFileName[len(srcDirName):]
    logging.debug(" srcRelativePathName = " + srcRelativePathName)
    tgtCompleteFileName = tgtDirName +srcRelativePathName
    logging.debug(" tgtCompleteFileName = " + tgtCompleteFileName)
    (tgtSubdirName,tail)=os.path.split(tgtCompleteFileName)
    logging.debug(" tgtSubdirName = " + tgtDirName)
    if not os.path.exists(tgtSubdirName):
        os.makedirs(tgtSubdirName, 0o775)
    return tgtCompleteFileName
     
############################################################################
def initLogger(inputParams):
    handler = logging.StreamHandler(sys.stdout)
    frm = logging.Formatter("%(asctime)s [%(levelname)-5s]: %(message)s", "%Y%m%d %H:%M:%S")
    handler.setFormatter(frm)
    logger = logging.getLogger()
    logger.addHandler(handler)
    print('inputParams["loglevel"] = ' + inputParams["loglevel"])
    if inputParams["loglevel"] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


############################################################################
def processFile(srcCompleteFileName, toolName, toolOptions):
    f = taglib.File(srcCompleteFileName)
    logging.debug(srcCompleteFileName)
    logging.debug(f.tags)
    #command = "%s %s %s >%s" % (toolName,toolOptions,srcCompleteFileName,tgtCompleteFileName)
    #print (command)
    #os.system(command)

def processDir(inputParams, logging):
  for Verz, VerzList, DateiListe in os.walk(inputParams["srcDirName"]):
    logging.debug(" VerzList = " + str(VerzList))
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
      srcCompleteFileName = os.path.join(Verz, Datei)
      logging.debug(" srcCompleteFileName  = " + srcCompleteFileName) 
      if fnmatch.fnmatch(srcCompleteFileName, inputParams["fileFilter"]):
        #tgtCompleteFileName = findTGTFileName(srcCompleteFileName, inputParams["srcDirName"],inputParams["tgtDirName"])
        processFile(srcCompleteFileName, inputParams["toolName"],inputParams["toolOptions"])


############################################################################
# main starts here
# global variables

if len(sys.argv) == 1 :
    print(description)
    print(sys.argv[0] + "<configfile>")
    configFileName = 'ProcessMp3sInDir.yaml'
else:
    configFileName = sys.argv[1]


# Python2 
#with open(configFileName, 'r') as cfgfile:
# Python3 
with open(configFileName, 'r',encoding='utf-8') as cfgfile:
    #config = json.load(cfgfile)
    inputParams = yaml.load(cfgfile)
logger = initLogger(inputParams)

logging.debug(inputParams)

processDir(inputParams, logging)
            
print ("successfully transfered %s " % inputParams["srcDirName"])

