#!/usr/bin/python
# -*- coding: utf-8 -*-
description = """This program handles handles directories with favorite Photos and creates a directory with absolute links to the original file
if found on the originals dir  

SearchAndCopyFile.py <option> [<xml_configfile>]

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
import json
import shutil
from FileObject import FileObject
from functions import initLogger
#import scriptutil as SU
    

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
            if newFile.foundOriginal == False:
              notFoundFileObjects.append(newFile) 
            else:
              fileObjects.append(newFile) 
  return (fileObjects,notFoundFileObjects)

###########################################################################
def processFileObject(fileObject):
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
    if inputParams["SIMULATE"] == False: 
      os.makedirs(newTgtDir )#,'0775')
    
  logging.debug("calling os.chdir("+newTgtDir+")")
  if inputParams["SIMULATE"] == False: 
    os.chdir(newTgtDir)
  
  newRelLink=os.path.join("../"*fileObject.copiesLinkDepthToBaseDir,fileObject.dateiNameOnOriginalRelativeToRootDir)
  logging.debug("checking os.symlink("+newRelLink+","+fileObject.fileBaseName+")")
  newAbsLink=os.path.join(fileObject.ip['ROOT-DIR'],fileObject.dateiNameOnOriginalRelativeToRootDir)
  logging.debug("checking os.symlink("+newAbsLink+","+fileObject.fileBaseName+")")
  if  not os.path.exists(fileObject.fileBaseName):
    logging.debug("calling os.symlink("+newRelLink+","+fileObject.fileBaseName+")")
    logging.debug("calling os.symlink("+newAbsLink+","+fileObject.fileBaseName+")")
    if inputParams["SIMULATE"] == False: 
      #os.symlink(newRelLink,fileObject.fileBaseName)
      os.symlink(newAbsLink,fileObject.fileBaseName)  

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

#############################################################################################
def processNotFoundFile(fileObject):
    """
    fileBaseName = 20100320100413FamilieZinkbeimPhotograph.jpg
    absCopiesOrigDateiName = /links/persdata/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/Photo/src/1_bisherigeBestellungen/2010/20101107_FotobuchItalienUndSchweden/FotobuchBilder/20100320100413FamilieZinkbeimPhotograph.jpg
    copiesPathRelativeToRootDir = src/1_bisherigeBestellungen/2010/20101107_FotobuchItalienUndSchweden/FotobuchBilder/20100320100413FamilieZinkbeimPhotograph.jpg
    copiesDirRelativeToRootDir = src/1_bisherigeBestellungen/2010/20101107_FotobuchItalienUndSchweden/FotobuchBilder
    copiesTgtDirRelativeToRootDir = Entwickeln_Not_Found_Files_Dir/1_bisherigeBestellungen/2010/20101107_FotobuchItalienUndSchweden/FotobuchBilder
    copiesLinkDepthToBaseDir = 0
    absDateiNameOnOriginal = 
    dateiNameOnOriginalRelativeToRootDir = 
    directoryNameOnOriginalRelativeToRootDir = 
    foundOriginal = False
    fileId = 20100320100413FamilieZinkbeimPhotograph.jpg
    """
    
  
    newTgtDir = os.path.join(fileObject.ip['ROOT-DIR'],fileObject.copiesTgtDirRelativeToRootDir)
    if  not os.path.exists(newTgtDir):
        logging.debug("calling   os.makedirs("+newTgtDir+",'0775')")
        if inputParams["SIMULATE"] == False: 
            os.makedirs(newTgtDir )#,'0775')
    if  not os.path.exists(os.path.join(newTgtDir, fileObject.fileBaseName)):
        logging.debug("checking shutil.copy("+ fileObject.absCopiesOrigDateiName+","+newTgtDir)
        if inputParams["SIMULATE"] == False: 
            shutil.copy(fileObject.absCopiesOrigDateiName,newTgtDir)
            
  

############################################################################
# main starts here


if sys.platform == "win32":
  #defaultEncoding="latin1"
  defaultEncoding="UTF-8"
else:
  defaultEncoding="UTF-8"


if len(sys.argv) == 1 :
    print description
    print sys.argv[0] + "<xml_configfile>"
    configFileName = 'SearchAndCopyFileFromOriginalDir_Photos.json'
else:
    configFileName=sys.argv[1]


with open(configFileName, 'rb') as cfgfile:
    config = json.load(cfgfile)
if config["loglevel"] == "DEBUG":
    rootLogger = initLogger(logging.DEBUG)
else:    
    rootLogger = initLogger(logging.INFO)
configuration=  config["configuration"]  
inputParams=config[configuration]
inputParams = extendInputParams(inputParams)

(fileObjects,notFoundFileObjects) = createFileObjectsList(inputParams)
for curFileObj in fileObjects:
  processFileObject(curFileObj)
writeNotFoundFilesToFile(notFoundFileObjects)
for curNofFoundFileObj in notFoundFileObjects:
  processNotFoundFile(curNofFoundFileObj)

####################################################################
######## Old methods
####################################################################
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
                    inputParams["SIMULATE"] = l2Node.firstChild.nodeValue
                if l2Node.nodeName == "linkPrefix":
#                    linkPrefix = l2Node.getAttribute("value").encode(defaultEncoding)
                    linkPrefix = l2Node.getAttribute("value")
                                 
             
    
    logging.debug("inputParams = \n%s" % inputParams) 
    #logging.debug("tgtDirName = %s" % tgtDirName) 
    return (inputParams)

