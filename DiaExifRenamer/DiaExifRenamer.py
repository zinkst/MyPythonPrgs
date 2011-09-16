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
#from xml import dom
from xml.dom import minidom
from xml.dom import Node
import time
import pyexiv2
from stat import *
import datetime
import codecs
import fileinput



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
        os.makedirs(tgtSubdirName, 0775)
    return tgtCompleteFileName
     
############################################################################
def initLogger():
    try: 
        rootLogger = logging.getLogger()
        logging.config.fileConfig("pyLoggerConfig.cfg")
    except:    
        logHandler = logging.StreamHandler(sys.stdout)
        #logging.basicConfig(stream=logHandler)
        rootLogger.addHandler(logHandler)
        rootLogger.setLevel(logging.DEBUG)
        rootLogger.setLevel(logging.INFO)
    return rootLogger

############################################################################
def readConfigFromXML(configFileName):
    try:
        xmldoc = minidom.parse(configFileName)
    except IOError:
        print "config file " + configFileName + " not found"
        sys.exit(1)
        
    #print xmldoc.toxml().encode("utf-8")
    logging.debug(xmldoc.toxml(defaultEncoding))
    configNode = xmldoc.firstChild
    for l1Node in configNode.childNodes:
        if l1Node.nodeName == sys.platform:
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "srcDirName":
                    """ Zugriff auf den Wert des tags """
                    #srcDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                    srcDirName=l2Node.firstChild.nodeValue.encode(defaultEncoding)
                if l2Node.nodeName == "tgtDirName":
                    """ Zugriff auf ein Attribut des tags """
                    tgtDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "toolName":
                    toolName = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "fileList":
                    """ Zugriff auf den Wert des tags """
                    #srcDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                    fileList=l2Node.firstChild.nodeValue.encode(defaultEncoding)
                
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "toolOptions":
                    toolOptions = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "fileFilter":
                    fileFilter = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "useList":
                    useListStr = l2Node.getAttribute("value").encode(defaultEncoding)
    
    logging.debug("srcDirName = %s" % srcDirName) 
    logging.debug("tgtDirName = %s" % tgtDirName) 
    logging.debug("toolName = %s" % toolName) 
    logging.debug("toolOptions = %s" % toolOptions) 
    logging.debug("fileFilter = %s" % fileFilter) 
    logging.debug("fileList = %s" % fileList) 
    logging.debug("useListStr = %s" % useListStr) 
    if useListStr == "True" :
      useList = True
    else:  
      useList = False
       
     
    
    inputParams["srcDirName"]=srcDirName.encode(defaultEncoding)
    inputParams["tgtDirName"]=tgtDirName.encode(defaultEncoding)
    inputParams["toolName"]=toolName.encode(defaultEncoding)
    inputParams["toolOptions"]=toolOptions.encode(defaultEncoding)
    inputParams["fileFilter"]=fileFilter.encode(defaultEncoding)
    inputParams["fileList"]=fileList.encode(defaultEncoding)
    inputParams["useList"]=useList
    
    return (inputParams)

###################################################################################################

############################################################################
def writeExifWithExiftool(srcCompleteFileName, toolName, toolOptions):    
    originalDateTag='-DateTimeOriginal="%s:%s:%s"' % (fileInfo["YEAR"],fileInfo["MONTH"],fileInfo["DAY"])
    createDateTag='-CreateDate="%s"' % (fileInfo["FILEDATE"])
    commentTag='-comment="%s"' % (fileInfo["COMMENT"])
    if fileInfo["EXIF_DATETIME"] == "not set":
      tags = originalDateTag + " " +createDateTag + " " + commentTag
    else:
      tags = commentTag
    command = '%s %s %s "%s"' % (toolName,toolOptions,tags,srcCompleteFileName)
    print command
    #os.system(command)

############################################################################
def getMetadata(srcCompleteFileName,fileInfo):
  metadata = pyexiv2.ImageMetadata(srcCompleteFileName)
  metadata.read()
  try:
    exifDateTimeTag = metadata['Exif.Image.DateTime']
    exifDateTimeString = exifDateTimeTag.value.strftime('%Y%m%d_%H%M%S')
  except KeyError :
    exifDateTimeString = "not set"  
  fileInfo["EXIF_DATETIME"]=exifDateTimeString

############################################################################
def setDescriptionTags(srcCompleteFileName,fileInfo):
  metadata = pyexiv2.ImageMetadata(srcCompleteFileName)
  metadata.read()
  keys = [ 'Exif.Photo.UserComment' , 'Exif.Image.ImageDescription' , 'Xmp.dc.description' , 'Iptc.Application2.Caption']
  value = fileInfo["COMMENT"]
  for curKey in keys:
    try:
      if (curKey == 'Xmp.dc.description'):
        metadata[curKey] = {'x-default': value } 
      elif (curKey == 'Iptc.Application2.Caption'):
        metadata[curKey] = [ value ]
      else:
        metadata[curKey] = value 
    except KeyError :
      logging.ERROR("Error writing " + fileInfo["COMMENT"] + "in tag " + curKey + " to file " + srcCompleteFileName)       
  
  
  metadata.write(True)
  #  logging.ERROR("Error writing " + fileInfo["COMMENT"] + " to file " + srcCompleteFileName)       
    

############################################################################
def setKeywordTags(srcCompleteFileName,fileInfo):
  metadata = pyexiv2.ImageMetadata(srcCompleteFileName)
  metadata.read()
  key1 = 'Xmp.dc.subject'
  key_exists = 1
  xmpSubjectList = []
  try:
    xmpSubjectList = metadata[key1].raw_value
  except KeyError :
    xmpSubjectList = []
  appendValuesList = []
  appendValuesList.append(fileInfo["FILMID"])
  appendValuesList.append("Hausbau")
  #appendValuesList.append("test1")
  
  for curValue in appendValuesList:
    if (curValue not in xmpSubjectList): 
      logging.debug(curValue + " not in " + str(xmpSubjectList) )
      xmpSubjectList.append(curValue)
  try:  
    metadata[key1] = xmpSubjectList
    metadata.write(True)
  except KeyError :
      logging.ERROR("Error writing " + key_value + " to file " + srcCompleteFileName)       

############################################################################
def setFileDateToImageDigitizedDateTime(srcCompleteFileName,fileInfo):
  metadata = pyexiv2.ImageMetadata(srcCompleteFileName)
  metadata.read()
  try:
    #exifDateTimeTag = metadata['Exif.Image.DateTime']
    exifDateTimeTag = metadata['Exif.Photo.DateTimeDigitized']
    st = os.stat(srcCompleteFileName)
    atime = st[ST_ATIME] #access time

    exifDateTimetimetuple = exifDateTimeTag.value.timetuple()
    exifDateTimetimestamp = int(time.mktime(exifDateTimetimetuple))
    
    #modify the file exifDateTimetimestamp
    os.utime(srcCompleteFileName,(atime,exifDateTimetimestamp))
  except KeyError :
    "no dateteime tag in  " + srcCompleteFileName  

############################################################################
def setImageMetadataDateTimeFromFileNameTimeStamp(srcCompleteFileName,fileInfo):
  metadata = pyexiv2.ImageMetadata(srcCompleteFileName)
  metadata.read()
  keys = [ 'Exif.Image.DateTime' , 'Exif.Photo.DateTimeDigitized' ,  'Xmp.xmp.CreateDate', 'Iptc.Application2.DateCreated',]
  value = fileInfo["FILENAMEDT"]
  for curKey in keys:
    try:
      if (curKey == 'Iptc.Application2.DateCreated'):
        metadata[curKey] =  [value]
#     elif (curKey == 'Iptc.Application2.Caption'):
#        metadata[curKey] = [ value ]
      else:
        metadata[curKey] = value
    except KeyError,TypeError :
      logging.ERROR("Error writing " + fileInfo["FILENAMEDT"] + "in tag " + curKey + " to file " + srcCompleteFileName)       
  metadata.write(True)
  

  
############################################################################
def parseFileNameStatic(srcCompleteFileName):
    # 1995A02_0524_Löwensteiner Berge.jpg
    fileNameOnly=os.path.basename(srcCompleteFileName)
    fileInfo["YEAR"]=fileNameOnly[0:4]
    fileInfo["MONTH"]=fileNameOnly[8:10]
    fileInfo["DAY"]=fileNameOnly[10:12]
    fileInfo["COMMENT"]=fileNameOnly[13:-4] 
    fileCreationDate=os.stat(srcCompleteFileName)[ST_CTIME]
    fileInfo["FILEDATE"]=time.strftime('%Y:%m:%d',time.localtime(fileCreationDate))   
    logging.info("fileInfo List")
    logging.info(fileInfo)
    return fileInfo

############################################################################
def parseFileNameLastUnderscore(srcCompleteFileName,fileInfo):
    # 20040320_181000_Kind1WandZuKind2_01.jpg
    #splits = fileNameOnly.split('_')
    #fileInfo["COMMENT"]=splits[2] 
    
    # 1995A02_0524_Löwensteiner Berge.jpg
    fileNameOnly=os.path.basename(srcCompleteFileName)
    (id, sep, last) = fileNameOnly.rpartition('_')
    (comment, sep, extension) = last.rpartition('.')
    fileInfo["COMMENT"]=comment 
    fileInfo["YEAR"]=int(id[0:4])
    fileInfo["MONTH"]=int(id[4:6])
    fileInfo["DAY"]=int(id[6:8])
    fileInfo["HOUR"]=int(id[9:11])
    fileInfo["MINUTE"]=int(id[11:13])
    fileInfo["SECOND"]=int(id[13:15])
    fileNameDT = datetime.datetime(fileInfo["YEAR"],fileInfo["MONTH"],fileInfo["DAY"],fileInfo["HOUR"],fileInfo["MINUTE"],fileInfo["SECOND"])
    fileInfo["FILENAMEDT"]=fileNameDT
    fileCreationDate=os.stat(srcCompleteFileName)[ST_CTIME]
    fileInfo["FILEDATE"]=time.strftime('%Y:%m:%d',time.localtime(fileCreationDate))   
    
    logging.info(fileInfo)
    return fileInfo


############################################################################
def parseFileNamePapierBilder(srcCompleteFileName,fileInfo):
    fileNameOnly=os.path.basename(srcCompleteFileName)
    (filmid, sep, extension) = fileNameOnly.rpartition('.')
    fileInfo["FILMID"]=filmid
    logging.info(fileInfo)

############################################################################
def walkList(inputParams):
  listName=inputParams["fileList"]
  logging.info("listName = "+ listName)
  # file:///home/zinks/Photos/Hausbau/digital/200410/20050522_183022_MartinHolzdeckeEG.jpg
  
  for line in fileinput.input(listName):
    if line.startswith("file://"):
      line = line[7:].rstrip()
    processFile(line,inputParams)
    
############################################################################
def walkDir(inputParams):
  for Verz, VerzList, DateiListe in os.walk (inputParams["srcDirName"]):
    logging.debug(" VerzList = " + str(VerzList) )
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
      srcCompleteFileName  = os.path.join(Verz,Datei)
      logging.debug(" srcCompleteFileName  = " + srcCompleteFileName)
      if fnmatch.fnmatch(srcCompleteFileName, inputParams["fileFilter"]):
        #tgtCompleteFileName = findTGTFileName(srcCompleteFileName, inputParams["srcDirName"],inputParams["tgtDirName"])
        processFile(srcCompleteFileName, inputParams)

############################################################################
def processFile(srcCompleteFileName, inputParams):
    logging.debug("Processing file "+ srcCompleteFileName)
    fileInfo = {}
    #fileInfo = parseFileNameStatic(srcCompleteFileName)
    #getMetadata(srcCompleteFileName,fileInfo)
    parseFileNameLastUnderscore(srcCompleteFileName,fileInfo)
    #parseFileNamePapierBilder(srcCompleteFileName, fileInfo)
    #setDescriptionTags(srcCompleteFileName, fileInfo)
    #exiftool -P -CreateDate='2009.05.06 06:47:00' -DateTimeDigitized='2009.05.06 06:47:00' -DateTimeOriginal=1995:05:24 -comment='Löwensteiner Berge' -UserComment='Löwensteiner Berge User' 1995_Nordeuropatour/1995A/1995A02_0524_Löwensteiner\ Berge.jpg
    #setKeywordTags(srcCompleteFileName,fileInfo)
    setFileDateToImageDigitizedDateTime(srcCompleteFileName, fileInfo)
    #setImageMetadataDateTimeFromFileNameTimeStamp(srcCompleteFileName, fileInfo)


############################################################################
# main starts here
# global variables
rootLogger = initLogger()
if sys.platform == "win32":
  defaultEncoding="latin1"
else:
  defaultEncoding="UTF-8"

if len(sys.argv) == 1 :
    print description
    print sys.argv[0] + "<xml_configfile>"
    configFileName = 'DiaExifRenamer.xml'
else:
    configFileName=sys.argv[1]

inputParams={}

inputParams = readConfigFromXML(configFileName)

if inputParams["useList"]:
  walkList(inputParams) 
  print ("successfully transfered %s " % inputParams["srcDirName"])
else:
  walkDir(inputParams) 
  print ("successfully transfered %s " % inputParams["fileList"])


