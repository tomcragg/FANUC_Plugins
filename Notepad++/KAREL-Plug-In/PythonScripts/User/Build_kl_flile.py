
from Npp import*
import shutil
import ctypes
import sys
import os
import subprocess
import inspect
import re
import xml.etree.ElementTree as ET # import entire module; use alias for clarity
from time import sleep
################################################################################
## Customer standard:	  BMW V8.2
## Python script:	      Build_kl_file
################################################################################
## Copyright (c): 		  FANUC Deutschland GmbH
##                 		  Bernhaeuser Str. 36
##                 		  73765 Neuhausen auf den Fildern
##						          Germany
################################################################################
## Release#version:		  0.0.1
################################################################################
## Created:             24.02.2017			
## Created by:          Willi Sengmueller		
## Last Update:         24.02.2017			
## Updated by:          Willi Sengmueller
################################################################################
## Function:			      # This script will read a 
##                      # Blueprint for an application package
##                      # and generates a complete Build
################################################################################
## Arguments:			      # none
################################################################################
## Return value:		    # none
################################################################################
def Mbox(title, text, style):
  return (ctypes.windll.user32.MessageBoxA(0, text, title, style))
  
def getFileNameFromPath(FilePath):
  FilePathParts = FilePath.split("\\")
  FilenameWithExtension = FilePathParts[(len(FilePathParts)) - 1]
  FileNameParts = FilenameWithExtension.split(".")
  Filename = FileNameParts[0]
  FileExtension = FileNameParts[1]
  return Filename, FileExtension 
  
def GetFileParameters():
  # Gets all File Related information
  Filepath = notepad.getCurrentFilename()
  Pathparts = Filepath.split("\\")
  Filename, FileExtension = getFileNameFromPath(Filepath)

  # Get the Path to the Package
  PackagePath = ""
  for words in range((len(Pathparts)) - 2):
    PackagePath = PackagePath + Pathparts[words] + '\\' 
   
  PackageName = Pathparts[(len(Pathparts)) - 3]
  
  return Filename, PackageName, FileExtension, PackagePath 

def copyFilesWithExtension(KLPackagePath, KLTempPath, Extension):    
  
  for basename in os.listdir(KLPackagePath):
    if basename.endswith(Extension):
      pathname = os.path.join(KLPackagePath, basename)
      if os.path.isfile(pathname):
        shutil.copy2(pathname, KLTempPath)  
    elif basename.endswith(Extension.upper()):
      pathname = os.path.join(KLPackagePath, basename)
      if os.path.isfile(pathname):
        shutil.copy2(pathname, KLTempPath)  

def createFolder(FolderPath, FolderName):
  if not os.path.exists(FolderPath + "\\" + FolderName):
    os.makedirs(FolderPath + "\\" + FolderName)
  return FolderPath + "\\" + FolderName 

def replace(file, pattern, subst):
  # Read contents from file as a single string
  file_handle = open(file, 'r')
  file_string = file_handle.read()
  file_handle.close()
  
  # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
  file_string = (re.sub(pattern, subst, file_string))
  
  # Write contents to file.
  # Using mode 'w' truncates the file.
  file_handle = open(file, 'w')
  file_handle.write(file_string)
  file_handle.close()

def insertTab(number):
  tabString = "\t" * number
  return tabString  

def findHighestBuildNumber(TempPath):

  SearchPatternVersion = ("\s*Release-version\s*:\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*")
  SearchPatternBuild = ("\s*Build:\s*([0-9]+)\s*")
  #SearchPatternComment = ("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)\s*")
  
  Filepath = notepad.getCurrentFilename()

  CodeFile = open(Filepath, 'r')
  # walk through all lines of codeFile
  for line in CodeFile:
    # find all lines with SearchPattern
    for match in re.finditer(SearchPatternBuild, line):
      # seperate release numbers
      buildNumber = line.split(":")
      MaxBuild    = buildNumber[1]
    for match in re.finditer(SearchPatternVersion, line):
      # seperate release numbers
      version = line.split(":")
      version = version[-1]

  CodeFile.close()
    
  return int(MaxBuild) + 1, version.lstrip()
  
def replaceBuildNumber(TempPath, version, MaxBuild, PackageName, FileName):

  #SearchPatternVersion = ("\s*Release-version\s*:\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*")
  SearchPatternComment = ("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)'\s*")
  SearchPatternBuild = ("\s*Build:\s*([0-9]+)\s*")
  
  PackageSplit = PackageName.split("_")
  ApplicationName = PackageSplit[0]

  strComment = "\n%COMMENT ='" + ApplicationName + " " + version.replace("\n", "") + "-" + str(MaxBuild) + "'\n"
  replace(TempPath + "\\" + FileName, SearchPatternComment, strComment)
    
  strBuild = " Build:" + insertTab(7) + str(MaxBuild) + "\n"
  replace(TempPath + "\\" + FileName, SearchPatternBuild, strBuild)  

def ktransCompileFile(FilePath, FileName, FileExtension):
  # Go to KAREL Folder of Package
  os.chdir(FilePath)
  logText = []
  
  # invoke KTRANS
  if "kl" in FileExtension:
    proc = subprocess.Popen('ktrans /ver ' + karel_version + ' ' + FileName, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    logText, stderr = proc.communicate('dir c:\\')
    console.write(logText)
  # invoke KCDICT 
  if "tx" in FileExtension:
    proc = subprocess.Popen('kcdict /ver ' + karel_version + ' ' + FileName + ".ftx", stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    logText, stderr = proc.communicate('dir c:\\')    
    console.write(logText)
  return logText 

def deleteFolder(FolderPath):
  try:
    FolderPath = FolderPath.replace("\\\\", '\\')
    os.chdir(FolderPath + "\\..")
    shutil.rmtree(FolderPath)
  except:
    pass

def deletFilesWithExtension(FolderPath, Extension):
 
  FolderContens=os.listdir(FolderPath)
  os.chdir(FolderPath)
  for item in FolderContens:
    if item.endswith(Extension):
      console.write(item + "\n")
      os.remove(item)
    if item.endswith(Extension.upper()):
      console.write(item + "\n")
      os.remove(item)    
##################################################################
# START OF PROGRAM
################################################################## 
##  Styles:
##  0 : OK
##  1 : OK    | Cancel
##  2 : Abort | Retry     | Ignore
##  3 : Yes   | No        | Cancel
##  4 : Yes   | No
##  5 : Retry | No 
##  6 : Cancel| Try Again | Continue
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_QUESRM = 0x20
ICON_STOP = 0x10
##################################################################    
karel_version = 'V8.36-1'
##################################################################  

FileName, PackageName, FileExtension, PackagePath = GetFileParameters()

KLPackagePath = PackagePath + "KAREL"

if not os.path.exists(KLPackagePath):
  Mbox('Wrong File Type', 'Could not find right File-Type\n', 0 | MB_OK)
else:
  TempPath = createFolder(PackagePath, "TEMP")

  #Copy File to temp Folder for restor
  copyFilesWithExtension(KLPackagePath, TempPath, FileName + ".kl")
  
  MaxBuild, version = findHighestBuildNumber(TempPath)
  
  replaceBuildNumber(KLPackagePath, version, MaxBuild, PackageName, FileName + "." + FileExtension)
  
  logText = ktransCompileFile(KLPackagePath, FileName, FileExtension)
  compiledFolderPath = createFolder(KLPackagePath, "Compiled")
  
  if "Translation not successful" in logText: 
    console.write(FileName + ": Translation not successful\n")
    # write file back to Karel folder from temp
    copyFilesWithExtension(TempPath, KLPackagePath, FileName + ".kl")
   
    copyFilesWithExtension(KLPackagePath, compiledFolderPath, "pc")
    copyFilesWithExtension(KLPackagePath, compiledFolderPath, ".tx")
    
    deleteFolder(TempPath)    
    Mbox('Translation Not Successful', 'Translation was arborted\n', 0 | MB_OK)
  else:

    copyFilesWithExtension(KLPackagePath, compiledFolderPath, "pc")
    copyFilesWithExtension(KLPackagePath, compiledFolderPath, ".tx")
    deletFilesWithExtension(KLPackagePath, "pc")
    deleteFolder(TempPath)
    Mbox('Success', "New Build " + version.replace("\n", "") + "-" + str(MaxBuild) + " Created", 0 | MB_OK)


