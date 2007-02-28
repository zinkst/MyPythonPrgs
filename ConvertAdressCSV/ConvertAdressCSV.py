#!/usr/bin/python
# -*- coding: utf-8 -*-
description = """This program converts Adresses obtained
from the import Internet into CSVs for importing into OpenOffice

it uses Unicode strings for internal processing. (For the Architekt part)
all Strings which have non 7-Bit chars must be proceeded with u'

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
                    #srcDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                    srcDirName=l2Node.firstChild.nodeValue.encode(defaultEncoding)
                if l2Node.nodeName == "tgtDirName":
                    """ Zugriff auf ein Attribut des tags """
                    tgtDirName = l2Node.getAttribute("value").encode(defaultEncoding)
                  
        elif l1Node.nodeName == "generic":
            for l2Node in l1Node.childNodes:
                if l2Node.nodeName == "srcFilename":
                    srcFilename = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "tgtFilename":
                    tgtFilename = l2Node.getAttribute("value").encode(defaultEncoding)
                                 
             
    logging.debug("srcDirName = %s" % srcDirName) 
    logging.debug("tgtDirName = %s" % tgtDirName) 
    logging.debug("srcFilename = %s" % srcFilename) 
    logging.debug("tgtFilename = %s" % tgtFilename) 
    
    return (srcDirName, tgtDirName, srcFilename, tgtFilename)

############################################################################
def printDictionaryDynamic(inDict):
  for curKey in inDict.keys():
    logging.debug("Dictionary["+curKey+"]="+inDict[curKey])

############################################################################
def printDictionary(inDict):
  logging.debug( "Vorname="+inDict["Vorname"]
              +", Nachname="+inDict["Nachname"]
              +", Strasse="+inDict["Strasse"]
              +", PLZ="+inDict["PLZ"]
              +", Ort="+inDict["Ort"]
              +", Staat="+inDict["Staat"]
              +", Telefon="+inDict["Telefon"]
              +", mobil="+inDict["mobil"]
              +", Telefongesch="+inDict["Telefongesch"]
              +", Fax="+inDict["Fax"]
              +", Geburtsdatum="+inDict["Geburtsdatum"]
              +", Geburtstag="+inDict["Geburtstag"]
              +", Geburtsmonat="+inDict["Geburtsmonat"]
              +", Geburtsjahr="+inDict["Geburtsjahr"]
              +", EMail1="+inDict["EMail1"]
              +", EMail2="+inDict["EMail2"]
              +", Nickname="+inDict["Nickname"]
              +", Webseite="+inDict["Webseite"]
              +", Kommentar="+inDict["Kommentar"]
              )
############################################################################
def getNextLineEntry(inputString, keyname):
  #logging.debug("inputString="+inputString)
  separator = ','
  if re.search(',',inputString):
    if inputString.startsWith('"'):
      # nexterty is inbetween "
      (next,rest)=inputString.split(separator,1)
    if next != '':
      if re.search('"',next):
        #logging.debug("next="+next)
        nextEntry = next.replace('\'"','')
        nextEntry =nextEntry.replace('"','')
      else:
        # this must be Geburstdatum 
        nextEntry = next.replace("\'",'')
    else:
      nextEntry = next
    rest = "'"+rest
  else:
    #last Entry eached  
    nextEntry = inputString.replace('\'"','')
    nextEntry =nextEntry.replace('"','')
    rest = ''  
  curDict[keyname]=nextEntry  
  logging.debug("curDict["+keyname+"]="+curDict[keyname])
  return rest    

############################################################################
def handleSrcFileLine(curLine):
#  "Vorname","Nachname","Straße privat","Postleitzahl privat","Ort privat","Staat privat","Telefon privat","Pager","Telefon geschäftlich","Geburtstag",
#  "E-Mail-Adresse","E-Mail 2:Adresse","Nickname","Webseite"
    separator = ','
    keyGeburtsdatum="Geburtsdatum"
    logging.debug("curLine="+curLine)
    #curLine = curLine.replace(',',separator)
    if curLine.startswith('#'):
      logging.debug("do nothing")
    elif curLine.startswith('\'"Vorname'):
      logging.debug("do not process headerline")
    else: 
      #(Vorname, Nachname, Strasse, PLZ, Ort, Staat, Telefon, mobil, Telefongesch, Fax,Geburtstag, EMail1, EMail2, Nickname, Webseite,Kommentar)
      rest = getNextLineEntry(curLine,"Vorname")
      rest = getNextLineEntry(rest,"Nachname")
      rest = getNextLineEntry(rest,"Strasse")
      rest = getNextLineEntry(rest,"PLZ")
      rest = getNextLineEntry(rest,"Ort")
      rest = getNextLineEntry(rest,"Staat")
      rest = getNextLineEntry(rest,"Telefon")
      rest = getNextLineEntry(rest,"mobil")
      rest = getNextLineEntry(rest,"Telefongesch")
      rest = getNextLineEntry(rest,"Fax")
      rest = getNextLineEntry(rest,keyGeburtsdatum)
      rest = getNextLineEntry(rest,"EMail1")
      rest = getNextLineEntry(rest,"EMail2")
      rest = getNextLineEntry(rest,"Nickname")
      rest = getNextLineEntry(rest,"Webseite")
      rest = getNextLineEntry(rest,"Kommentar")
      #logging.debug("curDict[Geburtsdatum]="+curDict[keyGeburtsdatum])
      computeBirthdayValues(curDict[keyGeburtsdatum])
      #printDictionary(curDict)
      addressLines.append(curDict.copy())
      
############################################################################
def computeBirthdayValues(Geburtsdatum):
  #logging.debug("Geburtsdatum="+Geburtsdatum)
  if re.match(u'\d\d\.\d\d\.\d\d..',Geburtsdatum):
    (Geburtstag,Geburtsrest)=Geburtsdatum.split('.',1)
    curDict["Geburtstag"]=Geburtstag
    (Geburtsmonat,Geburtsrest)=Geburtsrest.split('.',1)
    curDict["Geburtsmonat"]=Geburtsmonat
    Geburtsjahr=Geburtsrest
    curDict["Geburtsjahr"]=Geburtsjahr
  else:
    #logging.debug("Geburtsdatum is empty="+Geburtsdatum)
    curDict["Geburtsjahr"]=''
    curDict["Geburtsmonat"]=''
    curDict["Geburtstag"]=''



############################################################################
def handleSrcFileLineOld(curLine, fsock, addressLinesIndex):
#  "Vorname","Nachname","Straße privat","Postleitzahl privat","Ort privat","Staat privat","Telefon privat","Pager","Telefon geschäftlich","Geburtstag",
#  "E-Mail-Adresse","E-Mail 2:Adresse","Nickname","Webseite"
    separator = ';'
    curLine = curLine.replace(',',separator)
    if curLine.startswith('#'):
      logging.debug("do nothing")
    elif curLine.startswith('"Vorname'):
      logging.debug("do not process headerline")
    else: 
      #(Vorname, Nachname, Strasse, PLZ, Ort, Staat, Telefon, mobil, Telefongesch, Fax,Geburtstag, EMail1, EMail2, Nickname, Webseite,Kommentar)
      (Vorname,rest) = curLine.split(separator,1)
      Vorname = Vorname.replace('"','')
      curDict = {"Vorname" : Vorname}
      (Nachname,rest)=rest.split(separator,1)
      Nachname = Nachname.replace('"','')
      curDict["Nachname"]=Nachname
      (Strasse,rest)=rest.split(separator,1)
      Strasse = Strasse.replace('"','')
      curDict["Strasse"]=Strasse
      (PLZ,rest)=rest.split(separator,1)
      PLZ = PLZ.replace('"','')
      curDict["PLZ"]=PLZ
      (Ort,rest)=rest.split(separator,1)
      Ort = Ort.replace('"','')
      curDict["Ort"]=Ort
      (Staat,rest)=rest.split(separator,1)
      Staat = Staat.replace('"','')
      curDict["Staat"]=Staat
      (Telefon,rest)=rest.split(separator,1)
      Telefon = Telefon.replace('"','')
      curDict["Telefon"]=Telefon
      (mobil,rest)=rest.split(separator,1)
      mobil = mobil.replace('"','')
      curDict["mobil"]=mobil
      (Telefongesch,rest)=rest.split(separator,1)
      Telefongesch = Telefongesch.replace('"','')
      curDict["Telefongesch"]=Telefongesch
      (Fax,rest)=rest.split(separator,1)
      Fax = Fax.replace('"','')
      curDict["Fax"]=Fax
      (Geburtsdatum,rest)=rest.split(separator,1)
      Geburtsdatum = Geburtsdatum.replace('"','')
      curDict["Geburtsdatum"]=Geburtsdatum
      if re.match(u'\d\d\.\d\d\.\d\d..',Geburtsdatum):
        logging.debug("Geburtsdatum="+Geburtsdatum)
        (Geburtstag,Geburtsrest)=Geburtsdatum.split('.',1)
        curDict["Geburtstag"]=Geburtstag
        (Geburtsmonat,Geburtsrest)=Geburtsrest.split('.',1)
        curDict["Geburtsmonat"]=Geburtsmonat
        Geburtsjahr=Geburtsrest
        curDict["Geburtsjahr"]=Geburtsjahr
      else:
        logging.debug("Geburtsdatum is empty="+Geburtsdatum)
        curDict["Geburtsjahr"]=''
        curDict["Geburtsmonat"]=''
        curDict["Geburtstag"]=''
      (EMail1,rest)=rest.split(separator,1)
      EMail1 = EMail1.replace('"','')
      curDict["EMail1"]=EMail1
      (EMail2,rest)=rest.split(separator,1)
      EMail2 = EMail2.replace('"','')
      curDict["EMail2"]=EMail2
      (Nickname,rest)=rest.split(separator,1)
      Nickname = Nickname.replace('"','')
      curDict["Nickname"]=Nickname
      (Webseite,rest)=rest.split(separator,1)
      Webseite = Webseite.replace('"','')
      curDict["Webseite"]=Webseite
      Kommentar=rest
      Kommentar = Kommentar.replace('"','')
      curDict["Kommentar"]=Kommentar
      addressLines.append(curDict.copy())
      addressLinesIndex=addressLinesIndex + 1  
    return addressLinesIndex

############################################################################
def processSrcFile(srcName):
    #logging.debug("addressLines[0] = %s " % str(addressLines[0]))
    try:
        fsock = codecs.open(srcName, "rb", "utf8")
        #fsock = open(srcName, "r")
        try:
            #nextLine=unicode(fsock.readline())
            nextLine=fsock.readline()
            curLine=nextLine.rstrip('\r\n')
            curLine="'"+nextLine+"'"
            while nextLine:
                #logging.debug("curLine = %s" % curLine)
                #addressLinesIndex=handleSrcFileLine(curLine, fsock, addressLinesIndex)
                #printDictionary(addressLines[addressLinesIndex-1])
                handleSrcFileLine(curLine)
                curDict.clear() 
                nextLine=fsock.readline()
                curLine=nextLine.rstrip('\r\n')
                curLine="'"+curLine+"'"
                #logging.debug("curline="+curLine)
        finally:
            fsock.close()
    except IOError:
        logging.debug("error opening file %s" % srcName) 
    return 1


############################################################################
def formatDictAsThunderbirdLine(inDict):
    separator = '","'
    #printDictionary(inDict)
    printDictionaryDynamic(inDict)
    line = '"' + inDict["Nachname"] + \
           separator +  inDict["Vorname"] + \
           separator + inDict["Nickname"] + \
           separator + inDict["Nickname"] + \
           separator + inDict["EMail1"] + \
           separator + inDict["EMail2"] + \
           separator + inDict["Telefongesch"] + \
           separator + inDict["Telefon"] + \
           separator + inDict["Fax"] + \
           separator + \
           separator + inDict["mobil"] + \
           separator + inDict["Strasse"] + \
           separator + \
           separator + inDict["Ort"] + \
           separator + \
           separator + inDict["PLZ"] + \
           separator + inDict["Staat"] + \
           '",,,,,,,,,"' + \
           separator + inDict["Webseite"] + \
           separator + \
           separator + inDict["Geburtsjahr"] + \
           separator + inDict["Geburtsmonat"] + \
           separator + inDict["Geburtstag"] + \
           '",,,,,'


    return line

############################################################################


###########################################################################
def writeOutput(tgtName):
    try:
        outfile = codecs.open(tgtName, "wb","latin1","xmlcharrefreplace")
        #outfile = codecs.open(tgtName, "wb", "utf8")
        try:
            for curAddressDict in addressLines:
                #logging.info("curAddress = %s" % curAddress)
                outline=formatDictAsThunderbirdLine(curAddressDict)
                logging.debug("outline="+outline)
                outLine=outline + '\r\n'
                outfile.write(outLine)
        finally:
            outfile.close()
    except IOError:
        logging.info("error opening file %s" % srcName) 
    return 1
    
        

############################################################################
# main starts here
# global variables


rootLogger = initLogger()
if sys.platform == "win32":
  defaultEncoding="latin1"
  #defaultEncoding="UTF-8"
else:
  defaultEncoding="UTF-8"


if len(sys.argv) == 1 :
    print description
    print sys.argv[0] + "<xml_configfile>"
    configFileName = 'ConvertAdressCSV.xml'
else:
    configFileName=sys.argv[1]

(srcDirName, tgtDirName, srcFilename, tgtFilename) = readConfigFromXML(configFileName)

logging.info("srcDirName = %s" % srcDirName) 
logging.info("tgtDirName = %s" % tgtDirName) 
logging.info("srcFilename = %s" % srcFilename) 
logging.info("tgtFilename = %s" % tgtFilename) 

srcName=os.path.join(srcDirName, srcFilename)
tgtName=os.path.join(tgtDirName, tgtFilename)

logging.info("srcName = %s" % srcName) 

# global Array
addressLines = []
curDict = {}
processSrcFile(srcName)

writeOutput(tgtName)