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
                if l2Node.nodeName == "tgtThunderbirdName":
                    tgtThunderbirdName = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "tgtGigasetName":
                    tgtGigasetName = l2Node.getAttribute("value").encode(defaultEncoding)
                if l2Node.nodeName == "tgtTSinusName":
                    tgtTSinusName = l2Node.getAttribute("value").encode(defaultEncoding)
                                 
             
    logging.debug("srcDirName = %s" % srcDirName) 
    logging.debug("tgtDirName = %s" % tgtDirName) 
    logging.debug("srcFilename = %s" % srcFilename) 
    logging.debug("tgtThunderbirdName = %s" % tgtThunderbirdName) 
    logging.debug("tgtGigasetName = %s" % tgtGigasetName) 
    logging.debug("tgtTSinusName = %s" % tgtTSinusName) 
    
    srcName=os.path.join(srcDirName, srcFilename)
    tgtThunderbirdAbsName=os.path.join(tgtDirName, tgtThunderbirdName)
    tgtGigasetAbsName=os.path.join(tgtDirName, tgtGigasetName)
    tgtTSinusAbsName=os.path.join(tgtDirName, tgtTSinusName)
    
    logging.info("srcName = %s" % srcName) 
    logging.info("tgtThunderbirdAbsName = %s" % tgtThunderbirdAbsName) 
    logging.info("tgtGigasetAbsName = %s" % tgtGigasetAbsName) 
    logging.info("tgtTSinusAbsName = %s" % tgtTSinusAbsName) 
    return (srcName, tgtThunderbirdAbsName,tgtGigasetAbsName,tgtTSinusAbsName)

############################################################################
def printDictionaryDynamic(inDict):
  for curKey in inDict.keys():
    logging.debug("Dictionary["+curKey+"]="+inDict[curKey])

############################################################################
def getNextLineEntry(inputString, keyname):
  #logging.debug("inputString="+inputString)
  inMiddleSeparator = inEnclosingChar+inSeparator
  if re.search(',',inputString):
    if inputString.startswith('\''+inEnclosingChar):
      # nextentry is inbetween ".."
      (next,rest)=inputString.split(inMiddleSeparator,1)
      # next = '"??
    else:
      (next,rest)=inputString.split(inSeparator,1)
    if next != '':
      if re.search(inEnclosingChar,next):
        #logging.debug("next="+next)
        nextEntry = next.replace('\''+inEnclosingChar,'')
        nextEntry =nextEntry.replace(inEnclosingChar,'')
      else:
        # this must be Geburstdatum 
        nextEntry = next.replace("\'",'')
    else:
      nextEntry = next
    rest = "'"+rest
  else:
    #last Entry eached  
    nextEntry = inputString.replace(inMiddleSeparator,'')
    nextEntry =nextEntry.replace(inEnclosingChar,'')
    rest = ''  
  curDict[keyname]=nextEntry  
  logging.debug("curDict["+keyname+"]="+curDict[keyname])
  return rest    

############################################################################
def handleSrcFileLine(curLine):
#  "Vorname","Nachname","Straße privat","Postleitzahl privat","Ort privat","Staat privat","Telefon privat","Pager","Telefon geschäftlich","Geburtstag",
#  "E-Mail-Adresse","E-Mail 2:Adresse","Nickname","Webseite"
    keyGeburtsdatum="Geburtsdatum"
    logging.debug("curLine="+curLine)
    #curLine = curLine.replace(',',separator)
    if curLine.startswith('#'):
      logging.debug("do nothing")
    elif curLine.startswith('\'"Vorname'):
      logging.debug("do not process headerline")
    else: 
      #(Telefonbucheintrag,Vorname, Nachname, Strasse, PLZ, Ort, Staat, Telefon, mobil, Telefongesch, Fax,Geburtstag, EMail1, EMail2, Nickname, Webseite,Kommentar)
      rest = getNextLineEntry(curLine,"Telefonbucheintrag")
      rest = getNextLineEntry(rest,"Vorname")
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
def processSrcFile(srcName):
    #logging.debug("addressLines[0] = %s " % str(addressLines[0]))
    try:
        fsock = codecs.open(srcName, "rb", "utf8")
        #fsock = open(srcName, "r")
        try:
            #nextLine=unicode(fsock.readline())
            nextLine=fsock.readline()
            curLine=nextLine.rstrip(lineEnd)
            curLine="'"+nextLine+"'"
            while nextLine:
                #logging.debug("curLine = %s" % curLine)
                #addressLinesIndex=handleSrcFileLine(curLine, fsock, addressLinesIndex)
                #printDictionary(addressLines[addressLinesIndex-1])
                handleSrcFileLine(curLine)
                curDict.clear() 
                nextLine=fsock.readline()
                curLine=nextLine.rstrip(lineEnd)
                curLine="'"+curLine+"'"
                #logging.debug("curline="+curLine)
        finally:
            fsock.close()
    except IOError:
        logging.debug("error opening file %s" % srcName) 
    return 1


############################################################################
def formatDictAsThunderbirdLine(inDict):
    tbSeparator = ','
    tbEnclosingChar='"'
    outSep = tbEnclosingChar+tbSeparator+tbEnclosingChar
    #printDictionary(inDict)
    printDictionaryDynamic(inDict)
    line = tbEnclosingChar + inDict["Nachname"] + \
           outSep +  inDict["Vorname"] + \
           outSep + inDict["Nickname"] + \
           outSep + inDict["Nickname"] + \
           outSep + inDict["EMail1"] + \
           outSep + inDict["EMail2"] + \
           outSep + inDict["Telefongesch"] + \
           outSep + inDict["Telefon"] + \
           outSep + inDict["Fax"] + \
           outSep + \
           outSep + inDict["mobil"] + \
           outSep + inDict["Strasse"] + \
           outSep + \
           outSep + inDict["Ort"] + \
           outSep + \
           outSep + inDict["PLZ"] + \
           outSep + inDict["Staat"] + \
           '",,,,,,,,,"' + \
           outSep + inDict["Webseite"] + \
           outSep + \
           outSep + inDict["Geburtsjahr"] + \
           outSep + inDict["Geburtsmonat"] + \
           outSep + inDict["Geburtstag"] + \
           '",,,,,'
    return line

###########################################################################
def writeThunderbirdOutput(tgtThunderbirdAbsName):
    try:
        outfile = codecs.open(tgtThunderbirdAbsName, "wb","latin1","xmlcharrefreplace")
        #outfile = codecs.open(tgtName, "wb", "utf8")
        try:
            for curAddressDict in addressLines:
                #logging.info("curAddress = %s" % curAddress)
                outline=formatDictAsThunderbirdLine(curAddressDict)
                logging.info("outline="+outline)
                outLine=outline + lineEnd
                outfile.write(outLine)
        finally:
            outfile.close()
    except IOError:
        logging.info("error opening file %s" % tgtThunderbirdName) 
    return 1
    
###########################################################################
def writeGigasetOutput(tgtGigasetAbsName):
#BEGIN:VCARD
#VERSION:2.1
#N:Röhm;Martin
#TEL;HOME:373039
#TEL;WORK:07051168135
#TEL;CELL:0162811892
#EMAIL:martin.roehm@gmx.net
#END:VCARD  
  try:
    # nested try necessary for finally in Python 2.4
    try:
      #outfile = codecs.open(tgtGigasetAbsName, "wb","latin1","xmlcharrefreplace")
      outfile = codecs.open(tgtGigasetAbsName, "wb", "utf8")
      for curAddressDict in addressLines:
        createEntry=curAddressDict["Telefonbucheintrag"]
        if createEntry == 'j':
          outfile.write(lineEnd)
          outfile.write('BEGIN:VCARD'+lineEnd)
          outfile.write('VERSION:2.1'+lineEnd)
          nameLine='N:'+curAddressDict["Nachname"] + ";" + curAddressDict["Vorname"] + lineEnd
          logging.info("nameLine="+nameLine)
          outfile.write(nameLine)
          telHome=formatTelefonForGigaset(curAddressDict["Telefon"])
          if len(telHome) != 0:
            telHomeLine='TEL;HOME:'+telHome + lineEnd
            logging.info("telHomeLine="+telHomeLine)
            outfile.write(telHomeLine)
          telWork=formatTelefonForGigaset(curAddressDict["Telefongesch"])
          if len(telWork) != 0:
            telWorkLine='TEL;WORK:'+telWork + lineEnd
            logging.info("telWorkLine="+telWorkLine)
            outfile.write(telWorkLine)
          telCell=formatTelefonForGigaset(curAddressDict["mobil"])
          if len(telCell) != 0:
            telCellLine='TEL;CELL:'+telCell + lineEnd
            logging.info("telCellLine="+telCellLine)
            outfile.write(telCellLine)
          outfile.write('END:VCARD'+lineEnd)
      outfile.write(preconfiguredGigasetNumbers())  
    except IOError:
      logging.info("error opening file %s" % tgtGigasetAbsName) 
  finally:
    outfile.close()
  return 1

###########################################################################
def formatTelefonForGigaset(srcPhoneNumber):
    tgtPhoneNumber = srcPhoneNumber.replace('-','')
    tgtPhoneNumber = tgtPhoneNumber.replace('07054','')
    return tgtPhoneNumber

def preconfiguredGigasetNumbers():
    val= lineEnd
    val= val+'BEGIN:VCARD'+lineEnd
    val= val+'VERSION:2.1'+lineEnd
    val= val+'N: Gigaset.net;'+lineEnd
    val= val+'TEL;HOME:1188#9'+lineEnd
    val= val+'END:VCARD'+lineEnd
    val= val+lineEnd
    val= val+'BEGIN:VCARD'+lineEnd
    val= val+'VERSION:2.1'+lineEnd
    val= val+'N: kT Bran.buch;'+lineEnd
    val= val+'TEL;HOME:2#91'+lineEnd
    val= val+'END:VCARD'+lineEnd
    val= val+lineEnd
    val= val+'BEGIN:VCARD'+lineEnd
    val= val+'VERSION:2.1'+lineEnd
    val= val+'N: kT Tel.buch;'+lineEnd
    val= val+'TEL;HOME:1#91'+lineEnd
    val= val+'END:VCARD'+lineEnd
    return val


###########################################################################
def writeTSinusOutput(tgtTSinusAbsName):
  # nested try necessary for finally in Python 2.4
  try:
    try:
      outfile = codecs.open(tgtTSinusAbsName, "wb","latin-1","xmlcharrefreplace")
      #outfile = codecs.open(tgtTSinusAbsName, "wb", "utf8")
      for curAddressDict in addressLines:
        createEntry=curAddressDict["Telefonbucheintrag"]
        if createEntry == 'j':
          nameMax10=curAddressDict["Nachname"]+ "," + curAddressDict["Vorname"]
          if len(nameMax10)>=10:
            nameMax10=nameMax10[0:11]#.encode('latin1')
          logging.info("nameMax10="+nameMax10)
          telHome=formatTelefonForGigaset(curAddressDict["Telefon"])
          if len(telHome) != 0:
            outfile.write(lineEnd)
            outfile.write('BEGIN:VCARD'+lineEnd)
            outfile.write('VERSION:2.1'+lineEnd)
            outfile.write('N:'+nameMax10+' hom'+lineEnd)
            telHomeLine='TEL;HOME:'+telHome + lineEnd
            logging.info("telHomeLine="+telHomeLine)
            outfile.write(telHomeLine)
            outfile.write('END:VCARD'+lineEnd)
            
          telWork=formatTelefonForGigaset(curAddressDict["Telefongesch"])
          if len(telWork) != 0:
            outfile.write(lineEnd)
            outfile.write('BEGIN:VCARD'+lineEnd)
            outfile.write('VERSION:2.1'+lineEnd)
            outfile.write('N:'+nameMax10+' wrk'+lineEnd)
            telWorkLine='TEL;HOME:'+telWork + lineEnd
            logging.info("telWorkLine="+telWorkLine)
            outfile.write(telWorkLine)
            outfile.write('END:VCARD'+lineEnd)
  
          telCell=formatTelefonForGigaset(curAddressDict["mobil"])
          if len(telCell) != 0:
            outfile.write(lineEnd)
            outfile.write('BEGIN:VCARD'+lineEnd)
            outfile.write('VERSION:2.1'+lineEnd)
            outfile.write('N:'+nameMax10+' hdy'+lineEnd)
            telCellLine='TEL;HOME:'+telCell + lineEnd
            logging.info("telCellLine="+telCellLine)
            outfile.write(telCellLine)
            outfile.write('END:VCARD'+lineEnd)
    except IOError:
      logging.info("error opening file %s" % tgtTSinusAbsName) 
  finally:
    outfile.close()
  return 1



############################################################################
# main starts here
# global variables


rootLogger = initLogger()
if sys.platform == "win32":
  #defaultEncoding="latin1"
  defaultEncoding="UTF-8"
else:
  defaultEncoding="UTF-8"
lineEnd='\r\n'
#testsnippets()

if len(sys.argv) == 1 :
    print description
    print sys.argv[0] + "<xml_configfile>"
    configFileName = 'ConvertAdressCSV.xml'
else:
    configFileName=sys.argv[1]


# global Variables
inSeparator = ','
inEnclosingChar='"'
addressLines = []
curDict = {}
(srcName, tgtThunderbirdAbsName,tgtGigasetAbsName,tgtTSinusAbsName) = readConfigFromXML(configFileName)
processSrcFile(srcName)
#writeThunderbirdOutput(tgtThunderbirdAbsName)
#writeGigasetOutput(tgtGigasetAbsName)
writeTSinusOutput(tgtTSinusAbsName)


###########################################################################
def testsnippets():
  testString ='"test","2test2",,,'
  regexPattern = re.compile(r'\A".*"')
  matchObject = regexPattern.match(testString)
  if matchObject:
    print(matchObject.group())
    print(matchObject.span())
  else:
    print("no match found")  
  
  listOfmatches = regexPattern.findall(testString)
  print listOfmatches
  
  endindex = testString.find('test')
  result = testString[0:endindex+2]
  print (endindex)
  print ("result="+result)

  count = testString.count('test')
  print (count)
  
  (left,sep,right)=testString.partition('\A".*"')
  print("sep="+sep)      
