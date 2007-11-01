#!/usr/bin/python
# -*- coding: utf-8 -*-
description = """This program handles hadles directories with absolutelinks to 
favorite Photos, or files with lists to favorites Photos 

ManagePhotoFavorites.py <option> [<xml_configfile>]

where option is one of : 

1: as input a directory containing absolute links to Favorite Photos and create a file  
   containing a list with relative links to those Photos and a file containing absolute links
   
2: as input take a file with a list of relative links and create those links in <workDirName>/linksrel   

3: copy files contained in linksrel to folder files as new files ...

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



############################################################################
    
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
                    srcDirName=l2Node.firstChild.nodeValue.encode(defaultEncoding)
                if l2Node.nodeName == "workDirName":
                    """ Zugriff auf den Wert des tags """
                    workDirName = l2Node.firstChild.nodeValue.encode(defaultEncoding)
                    """ Zugriff auf ein Attribut des tags """
                    #workDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                  
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "srcFilename":
                    srcFilename = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "linkPrefix":
                    linkPrefix = l2Node.getAttribute("value").encode(defaultEncoding)
                                 
             
    logging.debug("srcDirName = %s" % srcDirName) 
    logging.debug("srcFilename = %s" % srcFilename) 
    #logging.debug("tgtDirName = %s" % tgtDirName) 
    logging.debug("linkPrefix = %s" % linkPrefix) 
    
    srcName=os.path.join(srcDirName, srcFilename)
    
    logging.info("srcName = %s" % srcName) 
    logging.info("workDirName = %s" % workDirName) 
    return (srcName, workDirName, linkPrefix)


############################################################################
def processFavoritesList_CreateRelativeLinks(srcName):
    #logging.debug("addressLines[0] = %s " % str(addressLines[0]))
    try:
        fsock = codecs.open(srcName, "rb", "utf8")
        #fsock = open(srcName, "r")
        try:
            #nextLine=unicode(fsock.readline())
            nextLine=fsock.readline()
            nextLine.rstrip('\r\n')
            logging.debug("curLine="+nextLine)
            while nextLine:
                generateRelativeLink(nextLine)
                nextLine=fsock.readline()
                nextLine=nextLine.rstrip('\r\n')
        finally:
            fsock.close()
    except IOError:
        logging.debug("error opening file %s" % srcName) 
    return 1

############################################################################
def generateRelativeLink(curLine):
  logging.debug("curLine="+curLine)
  linkBaseName=os.path.basename(curLine)
  tgtDirName=os.path.join(workDirName,"links")
  linkName=os.path.join(tgtDirName,linkBaseName)
  logging.debug("linkName="+linkName)
  linkDestName=linkPrefix+curLine
  logging.debug("linkDestName="+linkDestName)
  linkStatement="ln -sf "+linkDestName+" "+linkName
  print(linkStatement)
  #os.system(linkStatement)
  os.symlink(linkDestName, linkName)

############################################################################
def createFileListFromAbsoluteLinks(workDirName):
  absLinkDirName=os.path.join(workDirName,"linksabs")
  listOfFiles=os.listdir(absLinkDirName)
  listOfAbsoluteLinkNames=[]
  listOfRelativeLinkNames=[]
  for curFile in listOfFiles:
    curAbsoluteFileName = os.path.join(absLinkDirName,curFile)
    curLinkTgtName = os.readlink(curAbsoluteFileName)
    logging.debug("curLinkTgtName = " + curLinkTgtName)
    listOfAbsoluteLinkNames.append(curLinkTgtName)
    curRelLinkname=string.replace(curAbsoluteFileName, workDirName, "")
    logging.debug("curRelLinkname = "+ curRelLinkname)
    listOfRelativeLinkNames.append(curRelLinkname)
  return (listOfAbsoluteLinkNames,listOfRelativeLinkNames) 

############################################################################
def writeAbsoluteFilenamesList(workDirName,listOfAbsoluteFileNames):
    AbsoluteTgtListFileName=os.path.join(workDirName,"generatedAbsoluteLinks.txt")
    try:
        #outfile = codecs.open(tgtName, "wb","latin1","xmlcharrefreplace")
        outfile = codecs.open(AbsoluteTgtListFileName, "wb", "utf8")
        try:
            for curLinkName in listOfAbsoluteFileNames:
                #logging.info("curAddress = %s" % curAddress)
                logging.info("curLinkName="+curLinkName)
                outLine=curLinkName + '\r\n'
                outfile.write(outLine)
        finally:
            outfile.close()
    except IOError:
        logging.info("error opening file %s" % tgtName) 
    return 1

############################################################################
def writeRelativeFilenamesList(workDirName,listOfRelativeLinkNames):
    RelativeLinkListFileName=os.path.join(workDirName,"generatedRelativeLinks.txt")
    try:
        #outfile = codecs.open(tgtName, "wb","latin1","xmlcharrefreplace")
        outfile = codecs.open(RelativeLinkListFileName, "wb", "utf8")
        try:
            for curLinkName in listOfRelativeLinkNames:
                #logging.info("curAddress = %s" % curAddress)
                logging.info("curLinkName="+curLinkName)
                outLine=curLinkName + '\r\n'
                outfile.write(outLine)
        finally:
            outfile.close()
    except IOError:
        logging.info("error opening file %s" % tgtName) 
    return 1


############################################################################
# main starts here

rootLogger = initLogger()

if sys.platform == "win32":
  #defaultEncoding="latin1"
  defaultEncoding="UTF-8"
else:
  defaultEncoding="UTF-8"


if len(sys.argv) < 2 :
  print description
  print sys.argv[0] + "<xml_configfile>"
elif len(sys.argv) == 2:
  configFileName="ManagePhotoFavorites.xml" 
else:
  configFileName=sys.argv[2]
action=sys.argv[1]


(srcName, workDirName, linkPrefix) = readConfigFromXML(configFileName)

# select action
print "action = " + action 
if action == 1:
  (listOfAbsoluteLinkNames,listOfRelativeLinkNames) = createFileListFromAbsoluteLinks(workDirName)
  writeAbsoluteFilenamesList(workDirName, listOfAbsoluteLinkNames)
  writeRelativeFilenamesList(workDirName, listOfRelativeLinkNames)
elif action == 2:
  processFavoritesList_CreateRelativeLinks(srcName)

