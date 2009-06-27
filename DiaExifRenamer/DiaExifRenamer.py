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
from stat import *


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
         
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "toolOptions":
                    toolOptions = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "fileFilter":
                    fileFilter = l2Node.getAttribute("value").encode(defaultEncoding)
             
    logging.debug("srcDirName = %s" % srcDirName) 
    logging.debug("tgtDirName = %s" % tgtDirName) 
    logging.debug("toolName = %s" % toolName) 
    logging.debug("toolOptions = %s" % toolOptions) 
    logging.debug("fileFilter = %s" % fileFilter) 
    
    inputParams["srcDirName"]=srcDirName.encode(defaultEncoding)
    inputParams["tgtDirName"]=tgtDirName.encode(defaultEncoding)
    inputParams["toolName"]=toolName.encode(defaultEncoding)
    inputParams["toolOptions"]=toolOptions.encode(defaultEncoding)
    inputParams["fileFilter"]=fileFilter.encode(defaultEncoding)
    
    return (inputParams)

###################################################################################################

############################################################################
def processFile(srcCompleteFileName, toolName, toolOptions):
    fileInfo = {}
    fileInfo = parseFile(srcCompleteFileName)
    #exiftool -P -CreateDate='2009.05.06 06:47:00' -DateTimeDigitized='2009.05.06 06:47:00' -DateTimeOriginal=1995:05:24 -comment='Löwensteiner Berge' -UserComment='Löwensteiner Berge User' 1995_Nordeuropatour/1995A/1995A02_0524_Löwensteiner\ Berge.jpg
    originalDateTag='-DateTimeOriginal="%s:%s:%s"' % (fileInfo["YEAR"],fileInfo["MONTH"],fileInfo["DAY"])
    createDateTag='-CreateDate="%s"' % (fileInfo["FILEDATE"])
    commentTag='-comment="%s"' % (fileInfo["COMMENT"])
    tags = originalDateTag + " " +createDateTag + " " + commentTag
    command = '%s %s %s "%s"' % (toolName,toolOptions,tags,srcCompleteFileName)
    print command
    os.system(command)

############################################################################
def parseFile(srcCompleteFileName):
    # 1995A02_0524_Löwensteiner Berge.jpg
    fileNameOnly=os.path.basename(srcCompleteFileName)
    fileInfo = {}
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

inputParms = readConfigFromXML(configFileName)

for Verz, VerzList, DateiListe in os.walk (inputParams["srcDirName"]):
    logging.debug(" VerzList = " + str(VerzList) )
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in sorted(DateiListe):
        srcCompleteFileName  = os.path.join(Verz,Datei)
        logging.debug(" srcCompleteFileName  = " + srcCompleteFileName)
        if fnmatch.fnmatch(srcCompleteFileName, inputParams["fileFilter"]):
            #tgtCompleteFileName = findTGTFileName(srcCompleteFileName, inputParams["srcDirName"],inputParams["tgtDirName"])
            processFile(srcCompleteFileName, inputParams["toolName"],inputParams["toolOptions"])
            
print ("successfully transfered %s " % inputParams["srcDirName"])

