#!/usr/bin/python
# -*- coding: utf-8 -*-
description = """This program handles handles directories with relativeLinks to 
favorite Photos and swap the links with the files  

SwapAndLinkFile.py <option> [<xml_configfile>]

"""

import os
import shutil
import glob
import sys
import re
import string
import logging
import logging.config 
#from xml import dom
from xml.dom import minidom
from xml.dom import Node
import codecs
from FileObject import FileObject
from functions import initLogger
#import scriptutil as SU
    
############################################################################
"""
    <ROOT-DIR value="/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/" />
    <ORIGINALS-DIRS>src/Alben</ORIGINALS-DIRS> 
    <COPIES-ORIG-DIR>src/car</COPIES-ORIG-DIR> 
    <COPIES-TGT-DIR>test/car_new</COPIES-TGT-DIR> 
"""

def readConfigFromXML(configFileName):
    try:
        xmldoc = minidom.parse(configFileName)
    except IOError:
        print "config file " + configFileName + " not found"
        sys.exit(1)
    listOfOrigDirs = []    
    #print xmldoc.toxml().encode("utf-8")
    logging.debug(xmldoc.toxml(defaultEncoding))
    configNode = xmldoc.firstChild
    for l1Node in configNode.childNodes:
        if l1Node.nodeName == sys.platform:
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "ROOT-DIR":
                    """ Zugriff auf ein Attribut des tags """
                    inputParams["ROOT-DIR"]=l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "ORIGINALS-DIRS":
                    """ Zugriff auf den Wert des tags """
                    for l3Node in l2Node.childNodes: 
                      if l3Node.nodeName == "el":
                        listOfOrigDirs.append(l3Node.firstChild.nodeValue)
                    inputParams["ORIGINALS-DIRS"] = listOfOrigDirs
                if l2Node.nodeName == "COPIES-ORIG-DIR":
                    """ Zugriff auf den Wert des tags """
                    inputParams["COPIES-ORIG-DIR"] = l2Node.firstChild.nodeValue
                if l2Node.nodeName == "COPIES-TGT-DIR":
                    """ Zugriff auf den Wert des tags """
                    inputParams["COPIES-TGT-DIR"] = l2Node.firstChild.nodeValue
                  
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "debug":
                    inputParams["DEBUG"] = l2Node.firstChild.nodeValue
                if l2Node.nodeName == "linkPrefix":
#                    linkPrefix = l2Node.getAttribute("value").encode(defaultEncoding)
                    linkPrefix = l2Node.getAttribute("value")
                                 
             
    
    logging.debug("inputParams = \n%s" % inputParams) 
    #logging.debug("tgtDirName = %s" % tgtDirName) 
    return (inputParams)

###########################################################################
def extendInputParams(inputParams):
#  inputParams["ABS-ORIGINALS-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["ORIGINALS-DIRS"])
  inputParams["ABS-COPIES-ORIG-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["COPIES-ORIG-DIR"])
  inputParams["ABS-COPIES-TGT-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["COPIES-TGT-DIR"])
  inputParams["ROOT-DIR_LENGTH"]=len(inputParams["ROOT-DIR"])
  logging.debug("extended inputParams = \n%s" % inputParams) 
  return inputParams

###########################################################################
def createFileObjectsList(inputParams):
  fileObjects = []
  notFoundFileObjects = []
  for verz, verzList, dateiListe in os.walk (inputParams["ABS-COPIES-ORIG-DIR"]):
    logging.debug(" verzList = " + str(verzList) )
    logging.debug(" dateiListe = " + str(dateiListe))
    for datei in dateiListe:
        resultRE2 = re.search('\.jpg',datei,re.IGNORECASE)
        if resultRE2 != None:
            absCopiesOrigDateiName  = os.path.join(verz,datei)
            logging.debug(" absCopiesOrigDateiName = " + str(absCopiesOrigDateiName) )
            newFile = FileObject()
            FileObject.initialize(newFile,inputParams,absCopiesOrigDateiName)
            logging.info(FileObject.printOut(newFile))
            if newFile.foundOriginal == -1:
              notFoundFileObjects.append(newFile) 
            else:
              fileObjects.append(newFile) 
  return (fileObjects,notFoundFileObjects)

###########################################################################
def processFileObjects(fileObject):
  """
'ROOT-DIR': '/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/'
'ORIGINALS-DIRS': u'src/Alben'
'COPIES-TGT-DIR': u'test/car_new'
'COPIES-ORIG-DIR': u'test/car'
'ABS-COPIES-TGT-DIR': u'/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car_new'
'ABS-COPIES-ORIG-DIR': u'/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car'

fileBaseName = 03_Rosenrot.mp3
absCopiesOrigDateiName = /home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car/010MP3CAR/02_Rammstein_Rosenrot/03_Rosenrot.mp3
copiesPathRelativeToRootDir = test/car/010MP3CAR/02_Rammstein_Rosenrot/03_Rosenrot.mp3
copiesDirRelativeToRootDir = test/car/010MP3CAR/02_Rammstein_Rosenrot
copiesTgtDirRelativeToRootDir = test/car_new/MP3CAR/02_Rammstein_Rosenrot
copiesLinkDepthToBaseDir = 4
absDateiNameOnOriginal = /home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/src/Alben/Rammstein/Rosenrot/03_Rosenrot.mp3
dateiNameOnOriginalRelativeToRootDir = src/Alben/Rammstein/Rosenrot/03_Rosenrot.mp3
directoryNameOnOriginalRelativeToRootDir = src/Alben/Rammstein/Rosenrot
  """
  
  logging.debug("calling   os.chdir("+fileObject.ip['ROOT-DIR']+")" )
  #os.chdir(fileObject.ROOT-DIR)
  newTgtDir = os.path.join(fileObject.ip['ROOT-DIR'],fileObject.copiesTgtDirRelativeToRootDir)
  if  not os.path.exists(newTgtDir):
    logging.debug("calling   os.makedirs("+newTgtDir+",'0775')")
    if inputParams["DEBUG"] != "true": 
      os.makedirs(newTgtDir )#,'0775')
    
  logging.debug("calling os.chdir("+newTgtDir+")")
  if inputParams["DEBUG"] != "true": 
    os.chdir(newTgtDir)
  
  newRelLink=os.path.join("../"*fileObject.copiesLinkDepthToBaseDir,fileObject.dateiNameOnOriginalRelativeToRootDir)
  logging.debug("checking os.symlink("+newRelLink+","+fileObject.fileBaseName+")")
  if  not os.path.exists(fileObject.fileBaseName):
    logging.debug("calling os.symlink("+newRelLink+","+fileObject.fileBaseName+")")
    if inputParams["DEBUG"] != "true": 
      os.symlink(newRelLink,fileObject.fileBaseName)

############################################################################
def writeNotFoundFilesToFile(notFoundFileObjects):
    try:
        #outfile = codecs.open(, "wb","latin1","xmlcharrefreplace")
        outFileName=os.path.join(inputParams['ROOT-DIR'],inputParams['COPIES-ORIG-DIR'],"notFoundFiles.txt" )
        outfile = codecs.open(outFileName, "wb", "utf8")
        try:
          for curNotFoundFileObj in notFoundFileObjects:
            outLine=curNotFoundFileObj.absCopiesOrigDateiName
            logging.info("outLine="+outLine)
            outfile.write(outLine + '\n')
        finally:
            outfile.close()
    except IOError:
        logging.info("error opening file %s" % outFileName) 
    return 1
  

############################################################################
# main starts here

rootLogger = initLogger()

if sys.platform == "win32":
  #defaultEncoding="latin1"
  defaultEncoding="UTF-8"
else:
  defaultEncoding="UTF-8"


if len(sys.argv) == 1 :
    print description
    print sys.argv[0] + "<xml_configfile>"
    configFileName = 'SearchAndCopyFileFromOriginalDir.xml'
else:
    configFileName=sys.argv[1]

inputParams={}

inputParams = readConfigFromXML(configFileName)
inputParams = extendInputParams(inputParams)
(fileObjects,notFoundFileObjects) = createFileObjectsList(inputParams)
for curFileObj in fileObjects:
  processFileObjects(curFileObj)
writeNotFoundFilesToFile(notFoundFileObjects)


#(rootDir, relPathToLinks) = readConfigFromXML(configFileName)
#linkObjects = createLinkObjectsList(rootDir, relPathToLinks)
#for curLinkObj in linkObjects:
#  processLinkObjects(curLinkObj)
