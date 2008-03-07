#!/usr/bin/python
# -*- coding: utf-8 -*-
description = """This program searches a given Source Directory for mp3 files and performs 
reencoding of the mp3's. The reencoded files are stored under target directory
preserving the directory structure. ID3 tag information (album,songname,artist,year
genre) are also preserved.
It uses lame for reencoding. Configuration options must be set in an xml file.
In the xml file srcDir, tgtDir, path to Lame executable, and lame encoding options must be specified
For id3 scanning the module pytagger is used. see: http://www.liquidx.net/pytagger/
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
    
    return (srcDirName,tgtDirName,toolName,toolOptions,fileFilter)

############################################################################
def processFile(srcCompleteFileName, tgtCompleteFileName, toolName, toolOptions):
    command = "%s %s %s >%s" % (toolName,toolOptions,srcCompleteFileName,tgtCompleteFileName)
    print command
    os.system(command)


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
    configFileName = 'ConvertDirectoryTreeConfig.xml'
else:
    configFileName=sys.argv[1]

(srcDirName,tgtDirName,toolName,toolOptions,fileFilter) = readConfigFromXML(configFileName)

logging.info("srcDirName = %s" % srcDirName) 
logging.info("tgtDirName = %s" % tgtDirName) 
logging.info("toolName = %s" % toolName) 
logging.info("toolOptions = %s" % toolOptions) 
logging.info("fileFilter = %s" % fileFilter) 
    
 
for Verz, VerzList, DateiListe in os.walk (srcDirName):
    logging.debug(" VerzList = " + str(VerzList) )
    logging.debug(" DateiListe = " + str(DateiListe))
    for Datei in DateiListe:
        srcCompleteFileName  = os.path.join(Verz,Datei)
        logging.debug(" srcCompleteFileName  = " + srcCompleteFileName)
        if fnmatch.fnmatch(srcCompleteFileName, fileFilter):
            tgtCompleteFileName = findTGTFileName(srcCompleteFileName, srcDirName,tgtDirName)
            processFile(srcCompleteFileName, tgtCompleteFileName, toolName, toolOptions)
            
print ("successfully transfered %s " % srcDirName)

