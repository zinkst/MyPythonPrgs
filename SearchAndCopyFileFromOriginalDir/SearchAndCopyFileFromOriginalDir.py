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
import scriptutil as SU
    
############################################################################
"""
    <ROOT-DIR value="/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/" />
    <ORIGINALS-DIR>src/Alben</ORIGINALS-DIR> 
    <COPIES-ORIG-DIR>src/car</COPIES-ORIG-DIR> 
    <COPIES-TGT-DIR>test/car_new</COPIES-TGT-DIR> 
"""

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
                if l2Node.nodeName == "ROOT-DIR":
                    """ Zugriff auf ein Attribut des tags """
                    inputParams["ROOT-DIR"]=l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "ORIGINALS-DIR":
                    """ Zugriff auf den Wert des tags """
                    inputParams["ORIGINALS-DIR"] = l2Node.firstChild.nodeValue
                if l2Node.nodeName == "COPIES-ORIG-DIR":
                    """ Zugriff auf den Wert des tags """
                    inputParams["COPIES-ORIG-DIR"] = l2Node.firstChild.nodeValue
                if l2Node.nodeName == "COPIES-TGT-DIR":
                    """ Zugriff auf den Wert des tags """
                    inputParams["COPIES-TGT-DIR"] = l2Node.firstChild.nodeValue
                  
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "srcFilename":
                    #srcFilename = l2Node.getAttribute("value").encode(defaultEncoding)
                    srcFilename = l2Node.getAttribute("value")
                if l2Node.nodeName == "linkPrefix":
#                    linkPrefix = l2Node.getAttribute("value").encode(defaultEncoding)
                    linkPrefix = l2Node.getAttribute("value")
                                 
             
    
    logging.debug("inputParams = \n%s" % inputParams) 
    #logging.debug("tgtDirName = %s" % tgtDirName) 
    return (inputParams)

###########################################################################
def extendInputParams(inputParams):
  inputParams["ABS-ORIGINALS-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["ORIGINALS-DIR"])
  inputParams["ABS-COPIES-ORIG-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["COPIES-ORIG-DIR"])
  inputParams["ABS-COPIES-TGT-DIR"]=os.path.join(inputParams["ROOT-DIR"],inputParams["COPIES-TGT-DIR"])
  logging.debug("extended inputParams = \n%s" % inputParams) 
  return inputParams

###########################################################################
def createFileObjectsList(inputParams):
  fileOjects = []
  for verz, verzList, dateiListe in os.walk (inputParams["ABS-COPIES-ORIG-DIR"]):
    logging.debug(" verzList = " + str(verzList) )
    logging.debug(" dateiListe = " + str(dateiListe))
    for datei in dateiListe:
        resultRE2 = re.search('\.mp3',datei,re.IGNORECASE)
        if resultRE2 != None:
            absCopiesOrigDateiName  = os.path.join(verz,datei)
            logging.debug(" absCopiesOrigDateiName = " + str(absCopiesOrigDateiName) )
            newFile = FileObject()
            FileObject.initialize(newFile,inputParams,absCopiesOrigDateiName)
            logging.debug(FileObject.printOut(newFile))


#  linkObjects = []
#  for curFile in listOfLinks:
#    newLink = LinkObject()
#    newLink.linkAbsLocation = os.path.join(absLinkDirName,curFile)
#    LinkObject.initialize(newLink,rootDir)
#    linkObjects.append(newLink)
#    logging.debug(LinkObject.printOut(newLink))
#  return linkObjects 

###########################################################################
def processFileObjects(linkObject):
  logging.debug("calling os.remove("+linkObject.linkAbsLocation+")" )
  #os.remove(linkObject.linkAbsLocation)
  logging.debug("calling shutil.move("+linkObject.fileAbsLocation+","+linkObject.linkAbsLocationDir +") )")
  #shutil.move(linkObject.fileAbsLocation,linkObject.linkAbsLocationDir )
  logging.debug("calling os.chdir("+linkObject.newLinkAbsoluteDir+")")
  #os.chdir(linkObject.newLinkAbsoluteDir)
  logging.debug("calling os.symlink("+linkObject.newLinkTarget+","+linkObject.baseName+")")
  #os.symlink(linkObject.newLinkTarget,linkObject.baseName)
  

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
createFileObjectsList(inputParams)
#(rootDir, relPathToLinks) = readConfigFromXML(configFileName)
#linkObjects = createLinkObjectsList(rootDir, relPathToLinks)
#for curLinkObj in linkObjects:
#  processLinkObjects(curLinkObj)
