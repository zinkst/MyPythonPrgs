#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import logging
import logging.config 
import os

import scriptutil as SU

    
class FileObject:
 
  """
baseName = 20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
fileAbsLocation = /home/zinks/Stefan/myPrg/MyPythonPrgs/SwapLinkAndFile/testdata/test/2008/20080506_Schweden/20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
linkAbsLocation = /home/zinks/Stefan/myPrg/MyPythonPrgs/SwapLinkAndFile/testdata/test/2008/Favoriten/SchwedenLinksRel/20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
linkAbsLocationDir = /home/zinks/Stefan/myPrg/MyPythonPrgs/SwapLinkAndFile/testdata/test/2008/Favoriten/SchwedenLinksRel
linkAbsLocationSplit = Favoriten/SchwedenLinksRel
linkTarget = ../../20080506_Schweden/20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
linkSplit = 20080506_Schweden/20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
newLinkTarget = ../Favoriten/SchwedenLinksRel/20080514_123708_ZweiterHaltKurzVorAKHamburg.jpg
newLinkTargetDepth = 1
newLinkAbsoluteDir = /home/zinks/Stefan/myPrg/MyPythonPrgs/SwapLinkAndFile/testdata/test/2008/20080506_Schweden
  """
  ip = {}
  # keys :
  # ROOT-DIR ,ORIGINALS-DIR,ABS-COPIES-TGT-DIR,COPIES-TGT-DIR,COPIES-ORIG-DIR,ABS-ORIGINALS-DIR,ABS-COPIES-ORIG-DIR'}
  absCopiesOrigDateiName = u""
  fileBaseName    = u""
   
   
  def printOut(self):
    output = "\r\nfileBaseName = " + self.fileBaseName + \
             "\r\nabsCopiesOrigDateiName = " + self.absCopiesOrigDateiName + \
             "\r\nip.[ROOT-DIR] = "+ self.ip["ROOT-DIR"]

    return output
  
  def initialize(self,inputParams,in_absCopiesOrigDateiName):
    self.ip = inputParams
    self.absCopiesOrigDateiName = in_absCopiesOrigDateiName
    self.fileBaseName = os.path.basename(self.absCopiesOrigDateiName) 
    filesOnOriginal = SU.ffind(self.ip["ABS-ORIGINALS-DIR"],self.fileBaseName)
    logging.debug("filesOnOriginal = ") , filesOnOriginal

#    if os.path.islink(self.linkAbsLocation):
#      self.linkTarget = os.readlink(self.linkAbsLocation)
#      self.linkAbsLocationDir = os.path.dirname(self.linkAbsLocation) 
#      self.baseName = os.path.basename(self.linkAbsLocation) 
#      self.linkAbsLocationSplit = self.linkAbsLocationDir[len(rootDir)+1:] 
#      linkDepth=self.linkTarget.count(self.linkSeparator)
#      self.linkSplit=self.linkTarget[linkDepth*3:]
#      self.fileAbsLocation = os.path.join(rootDir,self.linkSplit)
#      newLinkTargetAbsName = self.fileAbsLocation[len(rootDir)+1:] 
#      self.newLinkTargetDepth = newLinkTargetAbsName.count('/')
#      self.newLinkTarget = os.path.join("../"*self.newLinkTargetDepth + self.linkAbsLocationSplit,self.baseName)  
#      self.newLinkAbsoluteDir = os.path.join(rootDir,os.path.dirname(self.linkSplit))
              


  def findFileInDir(dirName,filePattern):
    tgtCompleteFileName = u""
    for dir, dirList, fileList in os.walk (dirName):
      logging.debug(" dirList = " + str(dirList) )
      logging.debug(" fileList = " + str(fileList))
      for file in fileList:
        if file == filePattern:
          tgtCompleteFileName = os.path.join(dir,file)
          found = 1
          break
        else:
          found = -1   
      if found == 1:
        break  
    return tgtCompleteFileName        


################################################################################################      
#end class      
