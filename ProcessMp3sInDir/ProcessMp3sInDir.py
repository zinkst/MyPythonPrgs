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
def tagFoundButUnratedFile(srcCompleteFileName, toolName, toolOptions,foundNoRating,foundWithRating):
    # {'TITLE': ['Foot of the mountain'], 'FMPS_RATING': ['0.8'], 'TRACKNUMBER': ['04/10'], 'COMMENT': ['Created with EAC/REACT v2.0.akku.b03, 2010-01-13'], 'FMPS_RATING_AMAROK_SCORE': ['0.0975'], 'REPLAYGAIN_TRACK_PEAK': ['0.557932'], 'ALBUM': ['Foot of the mountain'], 'ENCODING': ['LAME 3.97 -V2 --vbr-new --noreplaygain --nohist'], 'MP3GAIN_ALBUM_MINMAX': ['136,251'], 'ARTIST': ['A-HA'], 'REPLAYGAIN_ALBUM_GAIN': ['-3.470000'], 'MP3GAIN_UNDO': ['+004,+004,N'], 'MP3GAIN_MINMAX': ['138,251'], 'REPLAYGAIN_ALBUM_PEAK': ['0.606102'], 'COMMENT:ID3V1 COMMENT': ['Created with EAC/REACT v2.0.'], 'REPLAYGAIN_TRACK_GAIN': ['-4.040000 dB'], 'GENRE': ['Pop'], 'DATE': ['2009'], 'ENCODEDBY': ['SZ']}
    # {'FMPS_RATING': ['0.8'],  'FMPS_RATING_AMAROK_SCORE': ['0.0975'] }
    os.chdir(os.path.dirname(srcCompleteFileName))
    f = taglib.File(srcCompleteFileName)
    logging.debug("working dir: " + os.getcwd())
    if 'FMPS_RATING' in f.tags:
      logging.debug("Rating set for " + srcCompleteFileName)
      logging.debug(str(f.tags['FMPS_RATING']) + str(f.tags))
      new_entry={'srcCompleteFileName' : srcCompleteFileName , 'FMPS_RATING' : f.tags['FMPS_RATING'], 'TITLE' : f.tags['TITLE'], 'ARTIST' : f.tags['ARTIST'] }
      foundWithRating.append(new_entry)
      if not ('FMPS_RATING_AMAROK_SCORE' in f.tags):
        logging.debug("no amarok Rating set for " + srcCompleteFileName)
        f.tags['FMPS_RATING_AMAROK_SCORE']=f.tags['FMPS_RATING']
    else:   
      logging.debug("No Rating set for " + srcCompleteFileName)
      new_entry={'srcCompleteFileName' : srcCompleteFileName , 'TITLE' : f.tags['TITLE'], 'ARTIST' : f.tags['ARTIST'] }
      foundNoRating.append(new_entry)
      f.tags['FMPS_RATING']='0.2'
    inputParams['srcDirName']='/links/Musik/car_links/001MP3CAR_KlassikHardRock/01Accept_Staying A Life'
    MP3CARidx=inputParams['srcDirName'].find('MP3CAR') 
    szCarDir=inputParams['srcDirName'][MP3CARidx-3:MP3CARidx]
    f.tags['SZ_CARDIR']=szCarDir
    f.save()
    logging.debug(f.tags)
    #command = "%s %s %s >%s" % (toolName,toolOptions,srcCompleteFileName,tgtCompleteFileName)
    #print (command)
    #os.system(command)

############################################################################
def processFoundDicts(inputParams, logging,foundNoRating,foundWithRating):
  WithRatingFileName=os.path.join(inputParams['tgtDirName'], 'foundWithRating.lst')
  logging.debug("WithRatingFileName = " + WithRatingFileName)
  with open(WithRatingFileName, 'w') as withRatingfile:
     for entry in foundWithRating:
       output=(str(entry['FMPS_RATING']) + '|' + str(entry['ARTIST']) + '|' + str(entry['TITLE']) + '|' + str(entry['srcCompleteFileName']) )
       logging.debug(output)
       withRatingfile.write(output + '\n') 
  NoRatingFileName=os.path.join(inputParams['tgtDirName'], 'NoRating.lst')
  logging.debug("NoRatingFileName = " + NoRatingFileName)
  with open(NoRatingFileName, 'w') as noRatingFile:
     for entry in foundNoRating:
       output=(str(entry['ARTIST']) + '|' + str(entry['TITLE']) + '|' + str(entry['srcCompleteFileName']) )
       logging.debug(output)
       noRatingFile.write(output+ '\n')


############################################################################
def processDir(inputParams, logging):
  foundNoRating = []
  foundWithRating = []
  for Verz, VerzList, DateiListe in os.walk(inputParams["srcDirName"]):
    logging.debug(" VerzList = " + str(VerzList))
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
      srcCompleteFileName = os.path.join(Verz, Datei)
      logging.debug(" srcCompleteFileName  = " + srcCompleteFileName) 
      if fnmatch.fnmatch(srcCompleteFileName, '*.' + inputParams["fileFilter"]):
        #tgtCompleteFileName = findTGTFileName(srcCompleteFileName, inputParams["linkDirName"],inputParams["tgtDirName"])
        tagFoundButUnratedFile(srcCompleteFileName, inputParams["toolName"],inputParams["toolOptions"],foundNoRating,foundWithRating)
        #copyRatedMp3ToTgtDir(srcCompleteFileName,inputParams)
  #processFoundDicts(inputParams, logging,foundNoRating,foundWithRating) 

############################################################################
def copyRatedMp3ToTgtDir(srcCompleteFileName,inputParams):
    # {'TITLE': ['Foot of the mountain'], 'FMPS_RATING': ['0.8'], 'TRACKNUMBER': ['04/10'], 'COMMENT': ['Created with EAC/REACT v2.0.akku.b03, 2010-01-13'], 'FMPS_RATING_AMAROK_SCORE': ['0.0975'], 'REPLAYGAIN_TRACK_PEAK': ['0.557932'], 'ALBUM': ['Foot of the mountain'], 'ENCODING': ['LAME 3.97 -V2 --vbr-new --noreplaygain --nohist'], 'MP3GAIN_ALBUM_MINMAX': ['136,251'], 'ARTIST': ['A-HA'], 'REPLAYGAIN_ALBUM_GAIN': ['-3.470000'], 'MP3GAIN_UNDO': ['+004,+004,N'], 'MP3GAIN_MINMAX': ['138,251'], 'REPLAYGAIN_ALBUM_PEAK': ['0.606102'], 'COMMENT:ID3V1 COMMENT': ['Created with EAC/REACT v2.0.'], 'REPLAYGAIN_TRACK_GAIN': ['-4.040000 dB'], 'GENRE': ['Pop'], 'DATE': ['2009'], 'ENCODEDBY': ['SZ']}
    sep='_'
    #logging.debug(" srcCompleteFileName = " + srcCompleteFileName)
    #logging.debug(" tgtDirName = " + inputParams["tgtDirName"])
    os.chdir(os.path.dirname(srcCompleteFileName))
    f = taglib.File(srcCompleteFileName)
    logging.debug(f.tags)
    if 'FMPS_RATING' in f.tags:
        tgtFullDirName=os.path.join(inputParams["tgtDirName"],f.tags['ARTIST'][0])   
        if not os.path.exists(tgtFullDirName):
            logging.debug("Creating" + tgtFullDirName)
            os.makedirs(tgtFullDirName, 0o775)
        if 'DISCNUMBER' in f.tags:
            tgtFileName=f.tags['TRACKNUMBER'][0].split('/')[0]+sep+'D'+f.tags['DISCNUMBER'][0]+sep+f.tags['ALBUM'][0]+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        else: 
            tgtFileName=f.tags['TRACKNUMBER'][0].split('/')[0]+sep+f.tags['ALBUM'][0]+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        tgtCompleteFilename=os.path.join(tgtFullDirName,tgtFileName)
        logging.debug(srcCompleteFileName + " => " + tgtCompleteFilename)
        if not os.path.exists(tgtCompleteFilename):
            shutil.copy(srcCompleteFileName,tgtCompleteFilename)
        else:
            logging.debug("already existing " +tgtCompleteFilename  )     
    else:
        logging.debug("untagged file " + srcCompleteFileName)
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

