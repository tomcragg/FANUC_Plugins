
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
## Python script:	      GetBlueprint
################################################################################
## Copyright (c): 		  FANUC Deutschland GmbH
##                 		  Bernhaeuser Str. 36
##                 		  73765 Neuhausen auf den Fildern
##						          Germany
################################################################################
## Release#version:		  0.0.1
################################################################################
## Created:             15.02.2017			
## Created by:          Willi Sengmueller		
## Last Update:         22.02.2017			
## Updated by:          Willi Sengmueller
################################################################################
## Function:			      # This script will read a 
##                      # Blueprint for an application package
##                      # and generates a Release version incl. Zip file
################################################################################
## Arguments:			      # none
################################################################################
## Return value:		    # none
################################################################################

def Mbox(title, text, style):
  return (ctypes.windll.user32.MessageBoxA(0, text, title, style))
    
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
  
  return PackageName, FileExtension, PackagePath

def GetBlueprintName(PackageName, PackagePath):
  # Searches for the Blueprint of application
  os.chdir(PackagePath)
  file = os.listdir(".")
  BlueprintFileName = []
  for entrys in range(len(file)):
    if "blueprint" in file[entrys]:
      BlueprintFileName = file[entrys]
   
  return BlueprintFileName
  
def readXMLFile(BlueprintFileName):
  # reads the XML File and retrieves the file locations for the installation
  xmlDataRoot = ET.parse(BlueprintFileName).getroot()
  xmlLoadOrderRoot = xmlDataRoot.find('LoadOrder')
  xmlFileOrderRoot = xmlLoadOrderRoot.findall('File')

  # walk through all File elements in XML to get the Filelocation in "id" tag
  FileLocations = []
  for FileElement in xmlFileOrderRoot:
    FileElement.attrib["id"]
    FileLocations = FileLocations + [FileElement.attrib["id"]]
       
  return FileLocations 

def createPackageFolderStructure(PackageName, PackagePath):
 
  # get the name of the install dir and path
  PackageSplit = PackageName.split("_")
  InstallFolderName = PackageSplit[0]
  PackageInstallPath = PackagePath + "Install\\" + InstallFolderName
  
  deleteFolder(PackageInstallPath)
  
  # create PackageFolder like "A04" and SubFolders

  os.makedirs(PackageInstallPath)
  console.write("Folder " + InstallFolderName + " Created\n")
  createFolder(PackageInstallPath, "CONF")
  createFolder(PackageInstallPath, "FORMS")
  createFolder(PackageInstallPath, "FORMS" + "\\VR")
  createFolder(PackageInstallPath, "FORMS" + "\\TX")
  createFolder(PackageInstallPath, "gif")
  createFolder(PackageInstallPath, "PC")
  createFolder(PackageInstallPath, "TP") 
   
  return PackageInstallPath
  
def createFolder(FolderPath, FolderName):
  if not os.path.exists(FolderPath + "\\" + FolderName):
    os.makedirs(FolderPath + "\\" + FolderName)

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
    
def fetchFilesByType(FileLocations, FileType):
  # fetches all files from a specific type from a FileLocation list
  FileList = [element for element in FileLocations if "." + FileType in element]
  return FileList

def getFileNameFromPath(FilePath):
  FilePathParts = FilePath.split("\\")
  FilenameWithExtension = FilePathParts[(len(FilePathParts)) - 1]
  FileNameParts = FilenameWithExtension.split(".")
  Filename = FileNameParts[0]
  FileExtension = FileNameParts[1]
  return Filename, FileExtension  
  
def ktransCompileFile(FilePath, FileName, FileExtension):
  # Go to KAREL Folder of Package
  os.chdir(FilePath)
  logText = []
  
  # invoke KTRANS
  if "pc" in FileExtension:
    proc = subprocess.Popen('ktrans /ver ' + karel_version + ' ' + FileName, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    logText, stderr = proc.communicate('dir c:\\')
    console.write(logText)
  # invoke KCDICT 
  if "tx" in FileExtension:
    proc = subprocess.Popen('kcdict /ver ' + karel_version + ' ' + FileName + ".ftx", stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    logText, stderr = proc.communicate('dir c:\\')    
    console.write(logText)
  return logText

def compileAllFiles(KarelPath, FileList, LogFile):
  
  logText = []

  for FilePath in FileList:
    FileName, FileExtension = getFileNameFromPath(FilePath)
    logText = ktransCompileFile(KarelPath, FileName, FileExtension)
    # write in Logfile
    LogFile.write(logText)
    
  if "Translation not successful" in logText: 
    console.write(FileName + ": Translation not successful\n")
    return False
      
  return True

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
        
def increaseReleaseVersion(FileList, PackagePath, PackageName):

  KLPackagePath = PackagePath + "KAREL"
  TempPath = PackagePath + "\\TEMP"

  # Go to KAREL Folder
  os.chdir(KLPackagePath)
  os.makedirs(TempPath)
  os.chdir(TempPath)
  
  copyFilesWithExtension(KLPackagePath, TempPath, "kl")
  copyFilesWithExtension(KLPackagePath, TempPath, "ftx")
  
  versionMajor, versionMid, versionMinor = findHighestReleaseNumber(TempPath)
  
  Version = str(versionMajor) + "." + str(versionMid) + "." + str(versionMinor)
  
  replaceReleaseNumber(TempPath, Version, PackageName)
  return TempPath, Version
   
def findHighestReleaseNumber(TempPath):
  
  SearchPatternVersion = ("\s*Release-version\s*:\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*")
  
  #SearchPatternComment = ("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)\s*")
  
  Filepath = notepad.getCurrentFilename()

  CodeFile = open(Filepath, 'r')
  # walk through all lines of codeFile
  for line in CodeFile:
    # find all lines with SearchPattern
    for match in re.finditer(SearchPatternVersion, line):
      # seperate release numbers
      version = line.split(":")
      version = version[-1].split(".")
      versionMajor = int(version[-3])
      versionMid = int(version[-2])
      versionMinor = int(version[-1])  

  CodeFile.close()
  
  for FileName in os.listdir(TempPath):

    CodeFile = open(TempPath + "\\" + FileName, 'r+')
    
    # walk through all lines of codeFile
    for line in CodeFile:
      # find all lines with SearchPattern
      for match in re.finditer(SearchPatternVersion, line):
        # seperate release numbers
        version = line.split(":")
        version = version[-1].split(".")
        
        if int(version[-3]) != versionMajor:
          CodeFile.close()
          return versionMajor, versionMid, versionMinor
        else:
          if int(version[-2]) != versionMid:
            CodeFile.close()
            return versionMajor, versionMid, versionMinor          
          else:
            if int(version[-1]) != versionMinor:
              CodeFile.close()
              return versionMajor, versionMid, versionMinor   
            
              
        ## extract highest releas numbers
        #if int(version[-3]) > versionMajor:
        #  versionMajor = int(version[-3])
        #  versionMid = int(version[-2])
        #  versionMinor = int(version[-1])
        #else:
        #  if int(version[-3]) == versionMajor and int(version[-2]) > versionMid:
        #    versionMid = int(version[-2])
        #    versionMinor = int(version[-1])
        #  else:          
        #    if int(version[-2]) == versionMid and int(version[-1]) > versionMinor:
        #      # increase version number
        #      versionMinor = int(version[-1]) + 1
        #    else:
        #      # increase version number
        #      versionMinor = int(version[-1]) + 1
              
    CodeFile.close()    
  return versionMajor, versionMid, versionMinor + 1

def replaceReleaseNumber(TempPath, Version, PackageName):

  SearchPatternVersion = ("\s*Release-version\s*:\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*")
  SearchPatternComment = ("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)'\s*")
  SearchPatternBuild = ("\s*Build:\s*([0-9]+)\s*")
  
  PackageSplit = PackageName.split("_")
  ApplicationName = PackageSplit[0]
  
  for FileName in os.listdir(TempPath):
    # Create Version String
    strVersion = " Release-version:" + insertTab(2) + Version + "\n"
    replace(TempPath + "\\" + FileName, SearchPatternVersion, strVersion)
    
    strComment = "\n%COMMENT ='" + ApplicationName + " " + Version + "-1'\n"
    replace(TempPath + "\\" + FileName, SearchPatternComment, strComment)
    
    strBuild = " Build:" + insertTab(7) + "1\n"
    replace(TempPath + "\\" + FileName, SearchPatternBuild, strBuild)
    
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

def moveAllFilesToInstallFolder(TempPath, PackageInstallPath):
  
  # move PC files to install folder
  copyFilesWithExtension(TempPath, PackageInstallPath + "\\PC", "pc")
  copyFilesWithExtension(TempPath, PackageInstallPath + "\\PC", "log")
  
  # move TX files to install folder
  copyFilesWithExtension(TempPath, PackageInstallPath + "\\FORMS\\TX", ".tx")
  
  # move TP and LS files to install folder
  copyFilesWithExtension(PackagePath + "\\TP", PackageInstallPath + "\\TP", "tp")
  
  # move gif files to install folder
  copyFilesWithExtension(PackagePath + "\\Configuration", PackageInstallPath + "\\gif", "gif")
  
  # move VR files to install folder
  copyFilesWithExtension(TempPath, PackageInstallPath + "\\FORMS\\VR", "vr")   
  
  # move DT files to install folder
  copyFilesWithExtension(PackagePath + "\\Configuration", PackageInstallPath + "\\CONF", "DT")     

  # move DT files to install folder
  copyFilesWithExtension(PackagePath + "\\Configuration", PackageInstallPath + "\\CONF", "xml")
  
  # move DT files to install folder
  copyFilesWithExtension(PackagePath + "\\Configuration", PackageInstallPath + "\\CONF", "csv")     

def createZip(ZipPath, destPath):
  ZipPath = ZipPath.replace(".", "_")
  shutil.make_archive(ZipPath , 'zip', destPath + "\\..")

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
 
PackageName, FileExtension, PackagePath = GetFileParameters()

BlueprintFileName = GetBlueprintName(PackageName, PackagePath)

if not BlueprintFileName:
  Mbox('No Blueprint', 'Could not find a Blueprint for Apllication.\nPlease check Path for Blueprint.\n', 0 | MB_OK)
else:

  FileLocations = readXMLFile(BlueprintFileName)

  PackageInstallPath = createPackageFolderStructure(PackageName, PackagePath)
  
  # need to take tx files due to Blueprint format, instead of ftx
  FtxFileList = fetchFilesByType(FileLocations, "tx")
  # need to take pc files due to Blueprint format, instead of kl
  PcFileList = fetchFilesByType(FileLocations, "pc")
  
  # copys Files to TEMP Folder and increases Version Number
  TempPath, Version = increaseReleaseVersion(PcFileList, PackagePath, PackageName)
  
  # create Logfile
  LogFile = open(TempPath + "\\ktrans.log", "w+")
  
  # start compiling all ftx 
  result = compileAllFiles(TempPath, FtxFileList, LogFile)
  # start compiling all KL 
  if not result:
    copyFilesWithExtension(TempPath, PackagePath, "log")
    deleteFolder(TempPath)
  else:
    result = compileAllFiles(TempPath, PcFileList, LogFile)
    
    LogFile.close()
  
    if not result:
      copyFilesWithExtension(TempPath, PackagePath, "log")
      deleteFolder(TempPath)
    else:
  
      moveAllFilesToInstallFolder(TempPath, PackageInstallPath)
      
      createZip(PackagePath + PackageName + "_v" + Version, PackageInstallPath)   
  
      # move new kl files to KAREL folder
      deletFilesWithExtension(PackagePath + "KAREL", "kl")
      deletFilesWithExtension(PackagePath + "KAREL", "ftx")
      
      copyFilesWithExtension(TempPath, PackagePath + "KAREL", "kl")
      copyFilesWithExtension(TempPath, PackagePath + "KAREL", "ftx")
      
      deleteFolder(TempPath)
      
      Mbox('Success', 'Release with Version Nr. ' + Version + " Created", 0 | MB_OK)
      
    console.write("DONE!\n")
  
  
  
 









