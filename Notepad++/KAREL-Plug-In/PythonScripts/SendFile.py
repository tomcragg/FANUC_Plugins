#########################################
#Script that conects to the robot via ftp 
#and sending the pc file to MD: device
#Creator : Ilias Baferos
#Date : 14.09.2016
##########################################
from Tkinter import *
import ttk
from ftplib import *
import ctypes  # An included library with Python install.
import fileinput
import sys
#from pathlib import Path
import xml.etree.cElementTree as ET
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
ListFlile = os.getenv('APPDATA')+'\\Notepad++\\plugins\\Config\\PythonScript\\scripts\\Robot.dat'
####################################
Robotlines = ()
####################################
#Message box	
####################################
def RobotXML(path , RobotName, RobotIP, UserName, Password):

	if not os.path.exists(path):
		# file doesn't exists
		root = ET.Element("root")
		Robot = ET.SubElement(root, RobotName)
		ET.SubElement(Robot, "RobotIP", name= RobotIP).text = 'IP'
		ET.SubElement(Robot, "UserName", name= UserName).text = 'User name'
		ET.SubElement(Robot, "Password", name= Password).text = 'Password'
		tree = ET.ElementTree(root)
		tree.write(path)
	else:	
		# file exists
		tree  = ET.parse(path)
		root = tree.getroot()
		Robot = ET.SubElement(root, RobotName)
		ET.SubElement(Robot, "RobotName", name= RobotName)
		ET.SubElement(Robot, "RobotIP", name= RobotIP)
		ET.SubElement(Robot, "UserName", name= UserName)
		ET.SubElement(Robot, "Password", name= Password)
		tree.write(path)
		
def center(toplevel):
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2
	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))	

def Mbox(title, text, style):
    return (ctypes.windll.user32.MessageBoxA(0, text, title, style))
####################################
# Set the IP and the name of the robot (on double click)
####################################
def DeleteRobot(*args):
	idxs = l.curselection()
	idx = int(idxs[0])
	Selection = Robotlines[idx]
	#try:
	#f = open(ListFlile, 'w')
	
	#except:
	#	f.close()
	#	Mbox('Not posible to open file', 'Not posible to open robot.dat file', 0 | ICON_STOP)
####################################	
# Set the IP and the name of the robot (on double click)
def SetIP(*args):
	idxs = l.curselection()
	idx = int(idxs[0])
	Selection = Robotlines[idx]
	Select = Selection.split('-->')
	RobotIP.set(Select[1])
	RobotName.set(Select[0])
####################################	
def SaveRobot(*args):
	ListFlile = '%APPDATA%\\Notepad++\\plugins\\Config\\PythonScript\\scripts\\Robot.xml'
	RobotXML(ListFlile , str(RobotName.get()) , str(RobotIP.get()), '', '')
	
	#RobotXML(ListFlile)
	#IP = str(RobotIP.get())
	#Name = 	str(RobotName.get())
	#if IP.replace(" ", "") != '' and Name.replace(" ", "") != '':
	#	if (Name + ' --> ' + IP + '\n') not in open(ListFlile).read():
	#		try:
	#				f = open(ListFlile, 'a')
	#				f.write(Name + ' --> ' + IP + '\n')
	#				f.close()
	#		except:
	#			f.close()
	#			Mbox('Not posible to open file', 'Not posible to open robot.dat file', 0 | ICON_STOP)
	#		l.insert(END, Name + ' --> ' + IP + '\n')
			#RobotList = list(Robotlines)
			#RobotList.append(Name + ' --> ' + IP + '\n')
	#		for i in range(0,len(Robotlines),2):
	#				l.itemconfigure(i, background='#f0f0ff')
					
			#Robotlines = tuple(RobotList)		
####################################	
#Connect and send file to robot 
####################################		
def Send_file_to_robot(*args):
	try:
		ftp = FTP(str(RobotIP.get()).replace(" ", "").replace("\n", ""))
		ftp.login()# user anonymous, passwd anonymous
		
		PI = filePathName.split("\\")
		PCpath =''
		fileName = 	PI[-1]
		for word in range((len(PI)) - 1):
			PCpath = PCpath + PI[word] + '\\' 			
	
		if filePathName[-3:].lower() == '.pc':
			ftp.cwd('md:')
			os.chdir(PCpath + 'compiled' + '\\' + 'pc')
		else:
			ftp.cwd('fr:')
			os.chdir(PCpath)
			
		try:
			ftp.storbinary('STOR ' + fileName, open(fileName, 'rb'))
		except IOError:
			#Mbox('File is in use', 'The file :\n' + PI[-1] + ' is in use.\nPlease make an ABORT ALL ,check if ' + PI[-1] + ' is selected,\nif yes unselect the file and try again. ', 0 | ICON_INFO)
			Mbox('Can\'t find file', 'The file :\n' + PI[-1] + ' is missing.\nPlease make sure that the file is in compiled folder.', 0 | ICON_INFO)
			pass	
			
		except Exception as e:
			s = str(e)
			Mbox('INFO', s, 0 | ICON_INFO)
			pass
	
		#	Mbox('File is in use', 'The file :\n' + PI[-1] + ' is in use.\nPlease make an ABORT ALL ,check if ' + PI[-1] + ' is selected,\nif yes unselect the file and try again. ', 0 | ICON_INFO)
			#pass
			
		ftp.quit()  
		root.destroy()
	except ValueError:
		pass
####################################
#Start of the program
####################################
filePathName = ''

if notepad.getCurrentFilename()[-3:].lower() == '.kl':
	filePathName = notepad.getCurrentFilename()[0:-3] + '.pc'

if notepad.getCurrentFilename()[-3:].lower() == '.dt' or notepad.getCurrentFilename()[-4:].lower() =='.xml'or notepad.getCurrentFilename()[-4:].lower() =='.csv':
	filePathName = notepad.getCurrentFilename() 

if filePathName !='':	
#Set TK object	
	root = Tk()
	root.title("Send file to robot")
	
#input box values 
	RobotIP = StringVar()
	RobotName = StringVar()	
#Read Robot.dat file
	try:
		#Open file
		f = open(ListFlile, 'r') 
		Robotlines = tuple(f.readlines()) #Read all the lines of the file
		Rnames = StringVar(value=Robotlines)# Set Robot names object
		f.close()
	except:
			Mbox('Not posible to open file', 'Not posible to open robot.dat file', 0 | ICON_STOP)
	
####################################	
#Create main frame
#################################### sticky=(N, W, E, S)
	mainframe = ttk.Frame(root)
	mainframe ['padding'] = (5, 5)
	#mainframe ['borderwidth'] = 0
	#mainframe['relief'] = 'groove'
	
	mainframe.grid(column=0,row=0, columnspan=5, rowspan=5)
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)
	
	
#RobotName_entry
	RobotName_entry = ttk.Entry(mainframe, width=30, textvariable=RobotName)
	RobotName_entry.grid(column=1, row=1, sticky=(W, E))
	
#RobotIP_entry
	RobotIP_entry = ttk.Entry(mainframe, width=30, textvariable=RobotIP)
	RobotIP_entry.grid(column=1, row=0, sticky=(W, E))
	
#Saved robots list
	l = Listbox(mainframe, listvariable= Rnames, width=30, height= 12)
	l.grid(column=0, row=3, columnspan=2 ,sticky=(W, E))

	
#Send to robot button
	ttk.Button(mainframe, text="Send file", command=Send_file_to_robot).grid(column=3, row=0, sticky=W)
#Save robot button 
	ttk.Button(mainframe, text="Save Robot", command=SaveRobot).grid(column=3, row=3 , sticky=N)
	
#Delete robot button 
	ttk.Button(mainframe, text="Delete Robot", command=DeleteRobot).grid(column=3, row=3, sticky=S)

#Labels
	ttk.Label(mainframe, text="IP Adress: ").grid(column=0, row=0, sticky=W)
	ttk.Label(mainframe, text="Robot Name: ").grid(column=0, row=1, sticky=W)
	ttk.Label(mainframe, text="Saved robots: ").grid(column=0, row=2, sticky=W)
	
	for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

# Colorize alternating lines of the listbox
#	for i in range(0,len(Robotlines),2):
#			l.itemconfigure(i, background='#f0f0ff')
#Double click event
	l.bind('<Double-1>', SetIP)

#Set focus	
	RobotIP_entry.focus()
	#root.bind('<Return>', calculate)
	
	
	#win = Tk.Toplevel(root)
	#center(win)
	
	root.mainloop()