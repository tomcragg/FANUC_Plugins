##########################################
#Script for building kl file
#Creator : Ilias Baferos
#Date : 14.09.2016
##########################################
import os
import subprocess
import Npp  
import ctypes
import inspect
#import shutil  
import re
import math
from shutil import *
from distutils.dir_util import copy_tree
####################################
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_QUESRM = 0x20
ICON_STOP = 0x10
####################################
karel_version = 'V8.36-1'
####################################	
def Mbox(title, text, style):
	return (ctypes.windll.user32.MessageBoxA(0, text, title, style))
####################################
#Program start
####################################
Answer = Mbox('Translate package', 'Do you want to translate all package?', 4 | ICON_QUESRM)
if Answer != 6 :
	stop()
	
#Get path of the file
FileName = notepad.getCurrentFilename()
PathSplit=FileName.split("\\")
Path =''
for word in range((len(PathSplit)) - 1):
	Path = Path + PathSplit[word] + '\\'
	
logPath = ''
for word in range((len(PI)) - 1):
	logPath = logPath + PI[word] + '\\' 
os.chdir(logPath)	
#Read files that needed for pack	
ListFlile = 'PackFiles.DT'
try:
	#Open file
	f = open(ListFlile, 'r') 
	FileList = f.readlines() #Read all the lines of the file
	#	Rnames = StringVar(value=Robotlines)# Set Robot names object
	f.close()
except:
	Mbox('Not posible to open file', 'Not posible to open PackFiles.DT file', 0 | ICON_STOP)

#Set search pattern	
pattern1 = re.compile("--\s*Build\s*:\s*([0-9]+)")
pattern2 = re.compile("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)\s*")
pattern3 = re.compile("\s*Build\s*:\s*([0-9]+)")
#Clear file list
for item in range(len(FileList)):
	FileList[item] = 	FileList[item].replace('\n', '').replace('\r', '')
#Reset max of build No
List_Build = []
#####################################
#Find max build No
for fileName in FileList:	
	with open(Path + fileName) as CodeFile:
		try:
			int_CurrentBuild = 0
			List_char = []
			
			for line in CodeFile:
					#Pattern 1
					if pattern1.search(line):
						line = line.replace('\n', '').replace('\r', '').replace('\t', '')
						CurrentBuild = line.split(':')[-1]
						CurrentBuild = int(CurrentBuild)
						List_Build.append(CurrentBuild)
					#Pattern 2					
					if pattern2.search(line):
						line = line.replace('\n', '').replace('\r', '').replace('\t', '')
						CurrentBuild = line.split('-')[-1]
						CurrentBuild = CurrentBuild.split("'")[0]
						for ind in range(len(CurrentBuild)) :
							List_char.append(CurrentBuild[ind])
							int_CurrentBuild = int(List_char[ind])*math.pow(10, (len(CurrentBuild) - (ind + 1))) + int_CurrentBuild
						List_Build.append(int(int_CurrentBuild))
					#Pattern 3							
					if pattern3.search(line):
						line = line.replace('\n', '').replace('\r', '').replace('\t', '')
						CurrentBuild = line.split(':')[-1]
						CurrentBuild = int(CurrentBuild)
						List_Build.append(CurrentBuild)
		except:
			CodeFile.close
			pass
		finally:
			CodeFile.close
MaxBuild = max(List_Build)
#########################################################################################################################

#Write the new files	
for fileName in FileList:
	CodeFile = open(Path + fileName, 'r') 
	TempFile = open(Path + fileName + '.temp', 'w+')
	for line in CodeFile:	
		if (Path + fileName)[-3:] == '.kl':
			if pattern1.search(line):
				lineTemp = line.replace('\n', '').replace('\r', '').replace('\t', '')
				CurrentBuild = lineTemp.split(':')[-1]
				line = line.replace(str(CurrentBuild) , str(MaxBuild + 1))	
				
			if pattern2.search(line):
				lineTemp = line.replace('\n', '').replace('\r', '').replace('\t', '')
				CurrentBuild = lineTemp.split('-')[-1]
				CurrentBuild = CurrentBuild.split("'")[0]
				line = line.replace(CurrentBuild, str(MaxBuild + 1))
				
		elif (Path + fileName)[-4:] == '.ftx':	
			if pattern3.search(line):
				lineTemp = line.replace('\n', '').replace('\r', '').replace('\t', '')
				CurrentBuild = lineTemp.split(':')[-1]
				line = line.replace(str(CurrentBuild) , str(MaxBuild + 1))			
		#Write to temp file		
		TempFile.write(line)
	CodeFile.close()
	TempFile.close()		
###############################################################################################
		
try: 
	os.mkdir('Backup')
except:
	pass  
os.chdir(Path)	
#Move files to backup folder
for fileName in FileList:
	move(Path + fileName, Path + 'Backup\\' + fileName + '.bak')
	os.rename(fileName+'.temp', fileName)
###############

showLog = 0
#ListFlile = 'PackFiles.DT'

#translate
LogFile = open('TRANS.log', 'w+')
for file in FileList:
	os.chdir(Path)	
	if file[-3:] == '.kl':
		proc = subprocess.Popen('ktrans /ver ' + karel_version + ' ' + file[0:-3], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		stdout, stderr = proc.communicate('dir c:\\')
	
		if stdout.find('Translation successful') == -1 :
			LogFile.write("---- " + file + " --------------------------------------------------------------------------------------------\n")
			LogFile.write (stdout)
			LogFile.write("---------------------------------------------------------------------------------------------------------------\n\n\n")
			#notepad.save()
			showLog = 1
		else:
			try: 
				os.mkdir('Compiled')
			except:
				pass
			os.chdir(Path + 'Compiled')	
			try: 
				os.mkdir('pc')
			except:
				pass 
			os.chdir(Path)	
			move(Path + file[0:-3] + '.pc', Path + 'Compiled' + '\\'  + 'pc' + '\\' + file[0:-3] + '.pc')
			
	elif file[-4:] == '.ftx':
		proc = subprocess.Popen('kcdict /ver ' + karel_version + ' ' + file, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
		stdout, stderr = proc.communicate('dir c:\\')
		if stdout.find('KCDict completed') == -1 :
			LogFile.write("---- " + file + " --------------------------------------------------------------------------------------------\n")
			LogFile.write (stdout)
			LogFile.write("---------------------------------------------------------------------------------------------------------------\n\n\n")
			showLog = 1
			##  Styles:
			##  0 : OK
			##  1 : OK | Cancel
			##  2 : Abort | Retry | Ignore
			##  3 : Yes | No | Cancel
			##  4 : Yes | No
			##  5 : Retry | No 
			##  6 : Cancel | Try Again | Continue
			Answer = Mbox('Translation was not successful', 'Translation was not successful.\nFor more details, please check TRANS.log file.\nDo you want to open TRANS.log file?', 4 | ICON_QUESRM)
		else:	
		
			try: 
				os.mkdir('Compiled')
			except:
				pass
				
				
			os.chdir(Path + 'Compiled')	
			try: 
				os.mkdir('Forms')
			except:
				pass

			os.chdir(Path + 'Compiled' + '\\'  + 'Forms')	
			
			FormFolder = file[2:]
			FormFolder = FormFolder[:-6]
		
			try: 
				os.mkdir(Path + + 'Compiled' + '\\'  + 'Forms' + '\\' + FormFolder)
			except:
				pass
		
			move(Path + file[0:-4] + '.tx', Path + 'Compiled' + '\\'  + 'Forms' + '\\' + FormFolder + '\\' + file[0:-4] + '.tx')
			move(Path + FormFolder + '.vr', Path + 'Compiled' + '\\'  + 'Forms' + '\\' + FormFolder + '\\' + FormFolder + '.vr')
		
			os.remove(Path + file[0:-6] + 'jp.ftx') 
			os.remove(Path + file[0:-6] + 'ch.ftx')
			os.remove(Path + file[0:-6] + 'kn.ftx')
			os.remove(Path + file[0:-6] + 'tw.ftx')
			os.chdir(Path + 'Compiled' + '\\' +  'Forms')
		
			InstFile = open('Ins_' + FormFolder + '.cm', 'w+')

			InstFile.write ('PRINT "Loadind ' + FormFolder + ' screen"\n') 
			InstFile.write ('VRLOAD ' + FormFolder + '\\' + FormFolder + '.vr\n' ) 
			InstFile.write ('TXPLOAD ' + FormFolder + '\\' + file[0:-6] + ' "' + FormFolder + '" ' + ' #1\n' ) 
			InstFile.write ('PRINT "Loadind ' + FormFolder + ' screen done"\n') 	
			InstFile.close()
		
			#find the form karel file
			pattern = ".kl"
			FormFile = 	open(Path + file, 'r')
			for line in FormFile:
				for match in re.finditer(pattern, line):
					KarelFileAr = line.split(' ')
					KarelFile = KarelFileAr[-1]
					KarelFile = KarelFile.replace('\n', '').replace('\r', '')
			FormFile.close()
			os.chdir(Path)
			try: 
			 os.mkdir('Forms_karel')
			except:
			 pass
			move(Path + KarelFile + '.kl', Path + 'Forms_karel' + '\\'  + KarelFile + '.kl')
			#  Styles:
					#  0 : OK
					#  1 : OK | Cancel
					#  2 : Abort | Retry | Ignore
					#  3 : Yes | No | Cancel
					#  4 : Yes | No
					#  5 : Retry | No 
					#  6 : Cancel | Try Again | Continue
LogFile.close()	
############################################################################################

os.chdir(Path)
os.chdir('..')
PackPath = os.getcwd()

try: 
 os.mkdir('InstalPack')
except:
 pass
 
os.chdir(PackPath + '\\' + 'InstalPack')



TempList = PackPath.split('\\')
PackName = TempList[-1]

try: 
 os.mkdir(PackName)
except:
 pass
 
PackCode = PackName.split('_')[0]
PackNo = PackCode[-2:]


IntallPackPath = PackPath + '\\' + 'InstalPack' + '\\' + PackName
os.chdir(IntallPackPath)

try: 
	os.mkdir('Pack')
except:
	pass 
IntallPackRoot = IntallPackPath	
IntallPackPath = PackPath + '\\' + 'InstalPack' + '\\' + PackName + '\\' +  'Pack'
#IntallPackPath  = IntallPackRoot
os.chdir(IntallPackPath)


try: 
	os.mkdir('TP')
except:
	pass 

try: 
	os.mkdir('Compiled')
except:
	pass 	
	
	
try: 
	os.mkdir('Configuration')
except:
	pass

os.chdir(IntallPackPath + '\\' + 'Compiled')

try: 
	os.mkdir('pc')
except:
	pass
	
try: 
	os.mkdir('Forms')
except:
	pass


copy_tree(Path + 'Compiled', IntallPackPath + '\\' + 'Compiled') 
copy_tree(PackPath + '\\' + 'TPE', IntallPackPath + '\\' + 'TP')

move(IntallPackPath + '\\' + 'Compiled' + '\\' + 'pc' + '\\' + 'inst_' + PackCode + '.pc', IntallPackPath + '\\'  + 'inst_' + PackCode + '.pc')

try: 
 os.mkdir(IntallPackPath + '\\' + 'Configuration')
except:
 pass
 
os.chdir(IntallPackPath)

 
 
ConfPath = IntallPackPath + '\\' + 'Configuration'


 
copyfile(PackPath + '\\' + 'Configuration' + '\\' + PackCode + '.xml'  , ConfPath + '\\' + PackCode + '.xml')

copyfile(PackPath + '\\' + 'Configuration' + '\\' + PackName + '_err.csv'  , ConfPath + '\\' + PackName + '_err.csv')

copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'ARGDISPEG' + PackNo + '.DT'  , ConfPath + '\\' + 'ARGDISPEG' + PackNo + '.DT')

copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'PackCopy.DT'  , IntallPackPath + '\\' + 'PackCopy.DT')
copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'PackFiles.DT'  , IntallPackPath + '\\' + 'PackFiles.DT')
copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'PackTP.DT'  , IntallPackPath + '\\' + 'PackTP.DT')
copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'PackVarialbes.DT'  , IntallPackPath + '\\' + 'PackVarialbes.DT')


#copyfile(IntallPackPath + '\\'  + 'inst_' + PackCode + '.pc', IntallPackRoot + '\\'  + 'inst_' + PackCode + '.ins')

if PackName == 'A01_cmn' :
	copyfile(PackPath + '\\' + 'Configuration' + '\\' + 'SupBMWManBut.xml'  , ConfPath + '\\' + 'SupBMWManBut.xml')
	copy_tree(PackPath + '\\' + 'Configuration' + '\\' + 'gif', IntallPackPath +  '\\' + 'Configuration' +  '\\' + 'gif' )

copyfile(IntallPackPath + '\\'  + 'inst_' + PackCode + '.pc'  , IntallPackRoot + '\\'  + 'inst_' + PackCode + '.ins')

if showLog == 1 :
	Answer = Mbox('Translation was not successful', 'Translation was not successful.\nFor more details, please check TRANS.log file.\nDo you want to open TRANS.log file?', 4 | ICON_QUESRM)
	if Answer == 6 :
		#notepad.open('TRANS.log')
		os.system('notepad TRANS.log')
