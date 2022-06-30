##########################################
#Script for building kl file
#**ftx (in the future)
#Creator : Ilias Baferos
#Date : 14.09.2016
# Version Salakis
##########################################
import os
import subprocess

import ctypes
import inspect
from shutil import move

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
def add_1_to_Build(m):
	return '-- Build:			' + str((int(m.group(1)) + 1))
####################################	
def add_1_to_COMMENT(m):
	Text = str(m.group()).split('-')
	BuiltNo = str(int(Text[1]) + 1)
	while len(BuiltNo) < 3:
		BuiltNo = '0' + BuiltNo
	return (Text[0] + '-' + BuiltNo)
####################################		
def sub_1_to_Build(m):
  return '-- Build:			' + str((int(m.group(1)) - 1))  
####################################	
def sub_1_to_COMMENT(m):
	Text = str(m.group()).split('-')
	BuiltNo = str(int(Text[1]) - 1)
	while len(BuiltNo) < 3:
		BuiltNo = '0' + BuiltNo
	return (Text[0] + '-' + BuiltNo)
####################################		
def IncBuildNo():
	if notepad.getCurrentFilename()[-3:] == '.kl':
		try:
			editor.rereplace("--\s*Build\s*:\s*([0-9]+)", add_1_to_Build)
		except:
			pass
			#Mbox('Oops! No Build comment... :)', 'Oops! No Build comment... :)', 0 | ICON_INFO)
		try:
			editor.rereplace("**\s*Build\s*:\s*([0-9]+)", add_1_to_Build) 
		except:
			pass
			#Mbox('Oops! No Build comment... :)', 'Oops! No Build comment... :)', 0 | ICON_INFO)	
		try:	
			editor.rereplace("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)\s*", add_1_to_COMMENT);
		except:
			#Mbox('Oops! No %COMMENT... :)', 'Oops! No %COMMENT... :)', 0 | ICON_INFO)
			pass
####################################						
def DecBuildNo():
	if notepad.getCurrentFilename()[-3:] == '.kl':
		try:
			editor.rereplace("--\s*Build\s*:\s*([0-9]+)", sub_1_to_Build)
		except:
			#Mbox('Oops! No Build comment... :)', 'Oops! No Build comment... :)', 0 | ICON_INFO)
			pass
		try:
			editor.rereplace("**\s*Build\s*:\s*([0-9]+)", sub_1_to_Build)
		except:
			pass
			#Mbox('Oops! No Build comment... :)', 'Oops! No Build comment... :)', 0 | ICON_INFO)	
		try:	
			editor.rereplace("\s*%COMMENT\s*=\s*'([A-Z]+)\s*([0-9]+)\s*([0-9]+)\s*.\s*([0-9]+)\s*.\s*([0-9]+)\s*-\s*([0-9]+)\s*", sub_1_to_COMMENT);
		except:
			#Mbox('Oops! No %COMMENT... :)', 'Oops! No %COMMENT... :)', 0 | ICON_INFO)
			pass
####################################	
def Mbox(title, text, style):
    return (ctypes.windll.user32.MessageBoxA(0, text, title, style))
####################################
#Program start
####################################
if notepad.getCurrentFilename()[-3:] == '.kl':
	FileName = notepad.getCurrentFilename()
	PI=FileName.split("\\")
	logPath = ''
	for word in range((len(PI)) - 1):
		logPath = logPath + PI[word] + '\\' 
	os.chdir(logPath)
	
	IncBuildNo()
	notepad.save()
	proc = subprocess.Popen('ktrans /ver ' + karel_version + ' ' + PI[-1][0:-3], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
	stdout, stderr = proc.communicate('dir c:\\')
	
	f = open('TRANS.log', 'w+')
	f.write (stdout)
	f.close()
	
	if stdout.find('Translation successful') == -1 :
		DecBuildNo() 
		notepad.save()
		##  Styles:
		##  0 : OK
		##  1 : OK | Cancel
		##  2 : Abort | Retry | Ignore
		##  3 : Yes | No | Cancel
		##  4 : Yes | No
		##  5 : Retry | No 
		##  6 : Cancel | Try Again | Continue
		Answer = Mbox('Translation was not successful', 'Translation was not successful.\nFor more details, please check TRANS.log file.\nDo you want to open TRANS.log file?', 4 | ICON_QUESRM)
		
		if Answer == 6 :
			notepad.open('TRANS.log')
			#os.system('notepad TRANS.log')
	else:
		logPath =''
		for word in range((len(PI)) - 1):
			logPath = logPath + PI[word] + '\\' 
		os.chdir(logPath)	
		try: 
			os.mkdir('Compiled')
		except:
			pass
		os.chdir(logPath + 'Compiled')	
		try: 
			os.mkdir('pc')
		except:
			pass
		os.chdir(logPath)	
		move(FileName[0:-3] + '.pc', logPath + 'Compiled' + '\\'  + 'pc' + '\\' + PI[-1][0:-3] + '.pc')
		
			
elif notepad.getCurrentFilename()[-4:] == '.ftx':
	FileName = notepad.getCurrentFilename()
	PI=FileName.split("\\")
	IncBuildNo()
	notepad.save()
	proc = subprocess.Popen('kcdict /ver ' + karel_version + ' ' + PI[-1], stdin = subprocess.PIPE, stdout = subprocess.PIPE)
	stdout, stderr = proc.communicate('dir c:\\')
	
	f = open('TRANS.log', 'w+')
	f.write (stdout)
	f.close()
	
	if stdout.find('KCDict completed') == -1 :
		DecBuildNo() 
		notepad.save()
		##  Styles:
		##  0 : OK
		##  1 : OK | Cancel
		##  2 : Abort | Retry | Ignore
		##  3 : Yes | No | Cancel
		##  4 : Yes | No
		##  5 : Retry | No 
		##  6 : Cancel | Try Again | Continue
		Answer = Mbox('Translation was not successful', 'Translation was not successful.\nFor more details, please check TRANS.log file.\nDo you want to open TRANS.log file?', 4 | ICON_QUESRM)
		if Answer == 6 :
			notepad.open('TRANS.log')
	else:
		logPath =''
		for word in range((len(PI)) - 1):
			logPath = logPath + PI[word] + '\\' 
		os.chdir(logPath)	
		try: 
			os.mkdir('Compiled')
		except:
			pass
		os.chdir(logPath + 'Compiled')	
		try: 
			os.mkdir('Forms')
		except:
			pass

		os.chdir(logPath + 'Compiled' + '\\'  + 'Forms')	
		PI3 = PI[-1][2:]
		PI3 = PI3[:-6]
		
		try: 
			os.mkdir(PI3)
		except:
			pass
		
		move(logPath + PI[-1][0:-4] + '.tx', logPath + 'Compiled' + '\\'  + 'Forms' + '\\' + PI3 + '\\' + PI[-1][0:-4] + '.tx')
		move(logPath + PI3 + '.vr', logPath + 'Compiled' + '\\'  + 'Forms' + '\\' + PI3 + '\\' + PI3 + '.vr')
		
		os.remove(logPath + PI[-1][0:-6] + 'jp.ftx') 
		os.remove(logPath + PI[-1][0:-6] + 'ch.ftx')
		os.remove(logPath + PI[-1][0:-6] + 'kn.ftx')
		os.remove(logPath + PI[-1][0:-6] + 'tw.ftx')
		os.chdir(logPath + '\\' +  'Compiled' + '\\' +  'Forms')
		
		f = open('Ins_' + PI3 + '.cm', 'w+')

		f.write ('PRINT "Loadind ' + PI3 + ' screen"\n') 
		f.write ('VRLOAD ' + PI3 + '\\' + PI3 + '.vr\n' ) 
		f.write ('TXPLOAD ' + PI3 + '\\' + PI[-1][0:-6] + ' "' + PI3 + '" ' + ' #1\n' ) 
		f.write ('PRINT "Loadind ' + PI3 + ' screen done"\n') 	
		f.close()

		#editor.setAnchor(0)
		#editor.addText(' # ')
    #editor.gotoLine(last_found_line + 1)
		


		start = editor.searchNext(0,'.kl')
		editor.searchAnchor()
		last_found_line = editor.lineFromPosition(start)
		end  = editor.searchNext(0,'\n')
		form_kl = editor.getTextRange(start, end)
		form_kl = form_kl.split(' ')
		form_kl = form_kl[-1]
		form_kl = form_kl.split('\r')
		form_kl = form_kl[0]
		os.chdir(logPath)
		try: 
			os.mkdir('Forms_karel')
		except:
			pass
			
		move(logPath + form_kl + '.kl', logPath + 'Forms_karel' + '\\'  + form_kl + '.kl')