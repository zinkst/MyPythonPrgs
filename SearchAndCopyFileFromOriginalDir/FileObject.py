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
'ROOT-DIR': '/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/'
'ORIGINALS-DIR': u'src/Alben'
'COPIES-TGT-DIR': u'test/car_new'
'COPIES-ORIG-DIR': u'test/car'
'ABS-COPIES-TGT-DIR': u'/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car_new'
'ABS-ORIGINALS-DIR': u'/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/src/Alben'
'ABS-COPIES-ORIG-DIR': u'/home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car'

fileBaseName = 01_Atlantic.mp3
absCopiesOrigDateiName = /home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/test/car/010MP3CAR/01_Keane_Under The Iron Sea/01_Atlantic.mp3
copiesPathRelativeToRootDir = test/car/010MP3CAR/01_Keane_Under The Iron Sea/01_Atlantic.mp3
copiesDirRelativeToRootDir = test/car/010MP3CAR/01_Keane_Under The Iron Sea
copiesTgtDirRelativeToRootDir=
copiesLinkDepthToBaseDir = 4
absDateiNameOnOriginal = /home/zinks/Stefan/myPrg/MyPythonPrgs/SearchAndCopyFileFromOriginalDir/testdata/src/Alben/Keane/Under The Iron Sea/01_Atlantic.mp3
dateiNameOnOriginalRelativeToRootDir = src/Alben/Keane/Under The Iron Sea/01_Atlantic.mp3
directoryNameOnOriginalRelativeToRootDir = src/Alben/Keane/Under The Iron Sea
  """
  ip = {}
  # keys :
  # ROOT-DIR ,ORIGINALS-DIR,ABS-COPIES-TGT-DIR,COPIES-TGT-DIR,COPIES-ORIG-DIR,ABS-ORIGINALS-DIR,ABS-COPIES-ORIG-DIR'}
  absCopiesOrigDateiName = u""
  fileBaseName    = u""
  absDateiNameOnOriginal = u""
  copiesPathRelativeToRootDir = u"" 
  copiesDirRelativeToRootDir = u""
  copiesTgtDirRelativeToRootDir=u""
  copiesLinkDepthToBaseDir = 0
  dateiNameOnOriginalRelativeToRootDir = u""
  directoryNameOnOriginalRelativeToRootDir = u""
  foundOriginal = 1 
   
  def printOut(self):
    output = "\r\nfileBaseName = " + self.fileBaseName + \
             "\r\nabsCopiesOrigDateiName = " + self.absCopiesOrigDateiName + \
             "\r\ncopiesPathRelativeToRootDir = " + self.copiesPathRelativeToRootDir + \
             "\r\ncopiesDirRelativeToRootDir = " + self.copiesDirRelativeToRootDir + \
             "\r\ncopiesTgtDirRelativeToRootDir = " + self.copiesTgtDirRelativeToRootDir + \
             "\r\ncopiesLinkDepthToBaseDir = " + str(self.copiesLinkDepthToBaseDir) + \
             "\r\nabsDateiNameOnOriginal = " + self.absDateiNameOnOriginal + \
             "\r\ndateiNameOnOriginalRelativeToRootDir = " + self.dateiNameOnOriginalRelativeToRootDir + \
             "\r\ndirectoryNameOnOriginalRelativeToRootDir = " + self.directoryNameOnOriginalRelativeToRootDir + \
             "\r\nfoundOriginal = " + str(self.foundOriginal) + \
             "\r\n"
    return output
  
  def initialize(self,inputParams,in_absCopiesOrigDateiName):
    self.ip = inputParams
    self.absCopiesOrigDateiName = in_absCopiesOrigDateiName
    self.fileBaseName = os.path.basename(self.absCopiesOrigDateiName) 
    filesOnOriginal = self.findFileInDir(self.ip["ABS-ORIGINALS-DIR"],self.fileBaseName)
    # TODO handle mutiple hits
    logging.debug("filesOnOriginal = ") , filesOnOriginal
    if filesOnOriginal == "":
      self.foundOriginal = -1
    else:  
      self.absDateiNameOnOriginal=filesOnOriginal
      self.copiesPathRelativeToRootDir=self.absCopiesOrigDateiName[self.ip["ROOT-DIR_LENGTH"]:]          
      self.copiesDirRelativeToRootDir=os.path.dirname(self.copiesPathRelativeToRootDir)
      lengthCopiesOrigDir= len(self.ip['COPIES-ORIG-DIR'])
      self.copiesTgtDirRelativeToRootDir=os.path.join(self.ip['COPIES-TGT-DIR'],self.copiesDirRelativeToRootDir[lengthCopiesOrigDir+1:] )
      self.copiesLinkDepthToBaseDir=self.copiesTgtDirRelativeToRootDir.count(os.sep) +1
      self.dateiNameOnOriginalRelativeToRootDir=self.absDateiNameOnOriginal[self.ip["ROOT-DIR_LENGTH"]:]
      self.directoryNameOnOriginalRelativeToRootDir=os.path.dirname(self.dateiNameOnOriginalRelativeToRootDir)
      
      

  def findFileInDir(self,dirName,filePattern):
    tgtCompleteFileName = u""
    found= -1
    for dir, dirList, fileList in os.walk (dirName):
#      logging.debug(" dirList = " + str(dirList) )
#      logging.debug(" fileList = " + str(fileList))
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
