import os
import sys
import getpass

actPath = os.path.dirname(os.path.realpath(__file__))
UserPath = actPath + "\\User\\"
IconPath = UserPath + "Icons\\"

pyFileList = []
for file in os.listdir(UserPath):
  if file.endswith(".py"):
    pyFileList = pyFileList + [file]

NotepadConfigPath = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Notepad++\\plugins\\Config\\"
PythonScriptStartup = "PythonScriptStartup.cnf"

ConfFile = open(NotepadConfigPath + PythonScriptStartup, "w")

PythonFileString = []

for item in pyFileList:
  PythonFileString = "TOOLBAR/" + UserPath + item + "/"
  itemico = item.split(".")
  if os.path.isfile(IconPath + itemico[0] + ".bmp"):
    PythonFileString = PythonFileString + IconPath + itemico[0] + ".bmp"
  
  ConfFile.write(PythonFileString + "\n")
StartConfiguration = "SETTING/PREFERINSTALLEDPYTHON/0\nSETTING/STARTUP/ATSTARTUP"

ConfFile.write(StartConfiguration)
ConfFile.close()
console.write("DONE\n")