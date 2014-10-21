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
from mutagen.mp3 import MP3 # https://code.google.com/p/mutagen/wiki/Tutorial
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC,TXXX, POPM
from mutagen.easyid3 import EasyID3
import math
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
def tagFoundButUnratedFile(srcCompleteFileName, toolName, toolOptions,foundNoRating,foundWithRating,foundWithUpperCaseRating):
    # {'TITLE': ['Foot of the mountain'], 'FMPS_RATING': ['0.8'], 'TRACKNUMBER': ['04/10'], 'COMMENT': ['Created with EAC/REACT v2.0.akku.b03, 2010-01-13'], 'FMPS_RATING_AMAROK_SCORE': ['0.0975'], 'REPLAYGAIN_TRACK_PEAK': ['0.557932'], 'ALBUM': ['Foot of the mountain'], 'ENCODING': ['LAME 3.97 -V2 --vbr-new --noreplaygain --nohist'], 'MP3GAIN_ALBUM_MINMAX': ['136,251'], 'ARTIST': ['A-HA'], 'REPLAYGAIN_ALBUM_GAIN': ['-3.470000'], 'MP3GAIN_UNDO': ['+004,+004,N'], 'MP3GAIN_MINMAX': ['138,251'], 'REPLAYGAIN_ALBUM_PEAK': ['0.606102'], 'COMMENT:ID3V1 COMMENT': ['Created with EAC/REACT v2.0.'], 'REPLAYGAIN_TRACK_GAIN': ['-4.040000 dB'], 'GENRE': ['Pop'], 'DATE': ['2009'], 'ENCODEDBY': ['SZ']}
    # {'FMPS_RATING': ['0.8'],  'FMPS_RATING_AMAROK_SCORE': ['0.0975'] }
    # pytaglib can only write  tags in uppercase
    os.chdir(os.path.dirname(srcCompleteFileName))
    f = taglib.File(srcCompleteFileName)
    mutID3 = ID3(srcCompleteFileName)
    logging.debug("working dir: " + os.getcwd())
    rating='0.4'
    if 'FMPS_RATING' in f.tags:
      logging.info("Rating with wrong case set for " + srcCompleteFileName)
      rating=f.tags['FMPS_RATING'][0]
      logging.debug(str(f.tags['FMPS_RATING']) + str(f.tags))
      new_entry={'srcCompleteFileName' : srcCompleteFileName , 'TAGS' : f.tags }
      foundWithUpperCaseRating.append(new_entry)
      # pytaglib can only write  tags in uppercase so these 2 lines below do not work
      del f.tags['FMPS_RATING']
      mutID3.delall('TXXX:FMPS_RATING')
      mutID3.add(TXXX(encoding=3, desc='FMPS_Rating', text=rating))
      # add xbmcratings see http://kodi.wiki/view/Adding_music_to_the_library#Ratings_in_ID3_tags
    elif 'FMPS_Rating' in f.tags:
      logging.info("Rating set for " + srcCompleteFileName)
      logging.debug(str(f.tags['FMPS_Rating']) + str(f.tags))
      foundWithRating.append(new_entry)
      rating=f.tags['FMPS_Rating'][0]
    else:   
      logging.info("No Rating set for " + srcCompleteFileName)
      new_entry={'srcCompleteFileName' : srcCompleteFileName , 'TAGS' : f.tags }
      foundNoRating.append(new_entry)
      mutID3.add(TXXX(encoding=3, desc='FMPS_Rating', text=u'0.4'))
    xbmc_rating=math.trunc(float(rating)*5)
    mutID3.add(TXXX(encoding=3, desc='RATING', text=str(xbmc_rating)))
    popm_rating=math.trunc(float(rating)*255)
    mutID3.add(POPM(rating=popm_rating))
    MP3CARidx=srcCompleteFileName.find('MP3CAR') 
    szCarDir=srcCompleteFileName[MP3CARidx-3:MP3CARidx]
    mutID3.add(TXXX(encoding=3, desc='SZ_CarDir', text=szCarDir))
    #f.tags['SZ_CarDir']=szCarDir
    mutID3.save()
 
############################################################################
def processFoundDicts(inputParams, logging,foundNoRating,foundWithRating,foundWithUpperCaseRating):
  WithRatingFileName=os.path.join(inputParams['tgtDirName'], 'foundWithRating.lst')
  logging.debug("WithRatingFileName = " + WithRatingFileName)
  with open(WithRatingFileName, 'w') as withRatingfile:
     for entry in foundWithRating:
       #output=(str(entry['FMPS_RATING']) + '|' + str(entry['ARTIST']) + '|' + str(entry['TITLE']) + '|' + str(entry['srcCompleteFileName']) )
       output=(entry)
       logging.info(output)
       withRatingfile.write(str(output) + '\n') 
  NoRatingFileName=os.path.join(inputParams['tgtDirName'], 'NoRating.lst')
  logging.debug("NoRatingFileName = " + NoRatingFileName)
  with open(NoRatingFileName, 'w') as noRatingFile:
     for entry in foundNoRating:
       #output=(str(entry['ARTIST']) + '|' + str(entry['TITLE']) + '|' + str(entry['srcCompleteFileName']) )
       output=(entry)
       logging.info(output)
       noRatingFile.write(str(output)+ '\n')
  UpperCaseRatingFileName=os.path.join(inputParams['tgtDirName'], 'UpperCaseRating.lst')
  logging.debug("UpperCaseRatingFileName = " + UpperCaseRatingFileName)
  with open(UpperCaseRatingFileName, 'w') as upperCaseRatingFile:
     for entry in foundWithUpperCaseRating:
       #output=(str(entry['ARTIST']) + '|' + str(entry['TITLE']) + '|' + str(entry['srcCompleteFileName']) )
       output=(entry)
       logging.info(output)
       upperCaseRatingFile.write(str(output)+ '\n')

############################################################################

def testMutagen(logging, srcCompleteFileName):
    audio = MP3(srcCompleteFileName, ID3=EasyID3)
    logging.info(audio.pprint())
#         MPEG 1 layer 3, 160000 bps, 44100 Hz, 270.63 seconds (audio/mp3)
#         album=Odyssey
#         artist=Yngwie J. Malmsteen's Rising Force
#         date=1988
#         genre=Hard Rock
#         length=270628
#         media=DIG
#         title=Faster Than The Speed Of Light
#         tracknumber=10/12
    audio2 = ID3(srcCompleteFileName)
#          {'TALB': TALB(encoding=3, text=['Odyssey']), 
#           'TMED': TMED(encoding=0, text=['DIG']), 
#           'TXXX:SZ_CARDIR': TXXX(encoding=3, desc='SZ_CARDIR', text=['001']),
#           'TDRC': TDRC(encoding=3, text=['1988']), 
#           'TLEN': TLEN(encoding=0, text=['270628']),
#           'TCON': TCON(encoding=3, text=['Hard Rock']),
#           'TXXX:FMPS_RATING': TXXX(encoding=3, desc='FMPS_RATING', text=['0.4']),
#           'TIT2': TIT2(encoding=3, text=['Faster Than The Speed Of Light']),
#           'TPE1': TPE1(encoding=3, text=["Yngwie J. Malmsteen's Rising Force"]),
#           'TRCK': TRCK(encoding=3, text=['10/12']) }
    #audio.add(TIT2(encoding=3, text=u"An example"))
    audio2.add(TXXX(encoding=3, desc='FMPS_Rating', text=u'0.4'))
    audio2.save()
    logging.info(audio2)

############################################################################
def processDirFortagFoundButUnratedFile(inputParams, logging):
  foundNoRating = []
  foundWithRating = []
  foundWithUpperCaseRating = []
  inputParams["srcDirName"]=inputParams["linkDirName"]
  for Verz, VerzList, DateiListe in os.walk(inputParams["linkDirName"]):
    logging.debug(" VerzList = " + str(VerzList))
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
      srcCompleteFileName = os.path.join(Verz, Datei)
      logging.debug(" srcCompleteFileName  = " + srcCompleteFileName) 
      if fnmatch.fnmatch(srcCompleteFileName, '*.' + inputParams["fileFilter"]):
        #tgtCompleteFileName = findTGTFileName(srcCompleteFileName, inputParams["linkDirName"],inputParams["tgtDirName"])
        tagFoundButUnratedFile(srcCompleteFileName, inputParams["toolName"],inputParams["toolOptions"],foundNoRating,foundWithRating,foundWithUpperCaseRating)
        #testMutagen(logging, srcCompleteFileName)

  #processFoundDicts(inputParams, logging,foundNoRating,foundWithRating,foundWithUpperCaseRating) 


############################################################################
def processDirForCopyRatedMP3s(inputParams, logging):
  foundNoRating = []
  foundWithRating = []
  foundWithUpperCaseRating = []
  for Verz, VerzList, DateiListe in os.walk(inputParams["srcDirName"]):
    logging.debug(" VerzList = " + str(VerzList))
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
      srcCompleteFileName = os.path.join(Verz, Datei)
      logging.debug(" srcCompleteFileName  = " + srcCompleteFileName) 
      if fnmatch.fnmatch(srcCompleteFileName, '*.' + inputParams["fileFilter"]):
        copyRatedMp3ToTgtDir(srcCompleteFileName,inputParams,foundNoRating,foundWithRating)
  processFoundDicts(inputParams, logging,foundNoRating,foundWithRating,foundWithUpperCaseRating) 
  
############################################################################
def copyRatedMp3ToTgtDir(srcCompleteFileName,inputParams,foundNoRating,foundWithRating):
    # {'TITLE': ['Foot of the mountain'], 'FMPS_RATING': ['0.8'], 'TRACKNUMBER': ['04/10'], 'COMMENT': ['Created with EAC/REACT v2.0.akku.b03, 2010-01-13'], 'FMPS_RATING_AMAROK_SCORE': ['0.0975'], 'REPLAYGAIN_TRACK_PEAK': ['0.557932'], 'ALBUM': ['Foot of the mountain'], 'ENCODING': ['LAME 3.97 -V2 --vbr-new --noreplaygain --nohist'], 'MP3GAIN_ALBUM_MINMAX': ['136,251'], 'ARTIST': ['A-HA'], 'REPLAYGAIN_ALBUM_GAIN': ['-3.470000'], 'MP3GAIN_UNDO': ['+004,+004,N'], 'MP3GAIN_MINMAX': ['138,251'], 'REPLAYGAIN_ALBUM_PEAK': ['0.606102'], 'COMMENT:ID3V1 COMMENT': ['Created with EAC/REACT v2.0.'], 'REPLAYGAIN_TRACK_GAIN': ['-4.040000 dB'], 'GENRE': ['Pop'], 'DATE': ['2009'], 'ENCODEDBY': ['SZ']}
    sep='_'
    #logging.debug(" srcCompleteFileName = " + srcCompleteFileName)
    #logging.debug(" tgtDirName = " + inputParams["tgtDirName"])
    os.chdir(os.path.dirname(srcCompleteFileName))
    f = taglib.File(srcCompleteFileName)
    logging.debug(f.tags)
    if 'FMPS_RATING' in f.tags:
        new_entry={'srcCompleteFileName' : srcCompleteFileName , 'TAGS' : f.tags }
        foundWithRating.append(new_entry)
        if 'ARTIST' in f.tags:
            tgtFullDirName=os.path.join(inputParams["tgtDirName"],f.tags['ARTIST'][0])
        else:
            tgtFullDirName=os.path.join(inputParams["tgtDirName"],'UNBEKANNT')
        if not os.path.exists(tgtFullDirName):
            logging.debug("Creating" + tgtFullDirName)
            os.makedirs(tgtFullDirName, 0o775)
        discnumber=None  
        tracknumber=None
        album=None  
        if 'TRACKNUMBER' in f.tags: tracknumber=f.tags['TRACKNUMBER'][0].split('/')[0]
        if 'DISCNUMBER' in f.tags: discnumber=f.tags['DISCNUMBER'][0].split('/')[0]
        if 'ALBUM' in f.tags: album=f.tags['ALBUM'][0]
        if discnumber and tracknumber and album:
             tgtFileName=album+sep+'D'+discnumber+sep+f.tags['ALBUM'][0]+sep+tracknumber+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        elif tracknumber and album:         
            tgtFileName=album+sep+tracknumber+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        elif tracknumber:         
            tgtFileName=tracknumber+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        elif album: 
            tgtFileName=album+sep+f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        else:
            tgtFileName=f.tags['TITLE'][0]+'.'+ inputParams["fileFilter"]
        tgtFileName=tgtFileName.replace('/','_') 
        tgtFileName=tgtFileName.replace(':','_') 
        tgtFileName=tgtFileName.replace('>','_') 
        tgtFileName=tgtFileName.replace('<','_') 
        tgtFileName=tgtFileName.replace('?','_') 
        #tgtFileName=tgtFileName.replace('!','_') 
        tgtCompleteFilename=os.path.join(tgtFullDirName,tgtFileName)
        logging.info(srcCompleteFileName + " => " + tgtCompleteFilename)
        if not os.path.exists(tgtCompleteFilename):
            shutil.copy(srcCompleteFileName,tgtCompleteFilename)
        else:
            logging.debug("already existing " +tgtCompleteFilename  )     
    else:
        new_entry={'srcCompleteFileName' : srcCompleteFileName , 'TAGS' : f.tags }
        foundNoRating.append(new_entry)
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

#processDirFortagFoundButUnratedFile(inputParams, logging)
processDirForCopyRatedMP3s(inputParams, logging)
            
print ("successfully transfered %s " % inputParams["srcDirName"])

