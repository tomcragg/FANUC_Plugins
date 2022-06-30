Notepad++ features for use with FANUC robots
============================================

10.06.2015	MK	FANUC_KAREL.xml updated for folding, Functionlist added
30.06.2015	IB	karel.xml for Autocomplete , Autocomplete added
25.01.2017	DB	python, compiling


1) Syntax highlighting
----------------------
Load FANUC language syntax definition files
	FANUC_TPE.xml		TP listing files (*.ls)
	FANUC_KAREL.xml		KAREL source files (*.kl)

In Notepad++: Language/Define your language/Import/Select files, ..


2) Function list
----------------
- Edit functionList.xml in C:\Program Files\Notepad++ and add KAREL stuff, see two marked areas in functionList_KAREL.xml
- On Windows 7: Make all folders visible in: Control Panel\Appearance and Personalization\Folder Options\
	Show hidden files and folders
- Close Notepad++
- Delete the personal copy of functionList.xml in %APPDATA%\notepad++\
- Open a .kl test file in Notepad++. This will copy the new functionList.xml to %APPDATA%\notepad++\
- Open/Hide function list: View\Function List or Icon


3) Autocomplete
----------------
- Copy karel.xml file from ..\Autocomplete\ to %ProgramFiles%\Notepad++\plugins\APIs
- Restart Notpad++
- Enable Auto-Completion from Setting -> Preferences ->  Auto-Completion 
- Tick Enable auto-Completion on each input
- select Function completion or Function and word completion
- At language menu the name for the user-difined language must be karel.
  
4) Use of Python Scripts and Compiling Karel Code
----------------
- install Plugin "Python Script" via Plugin Manager or download from internet
- download and install Python version 2.7.13 from here (32 bit):
- install ctypes from https://sourceforge.net/projects/ctypes/files/ctypes-win64/1.0.2-win64/
  https://www.python.org/downloads/release/python-2713/
- copy the folder "FANUC support" from Repository\Utilities\Notepad++\ to C:\Program Files (x86)\
- copy the Phyton Scripts (*.py) from Repository\Utilities\Notepad++\PythonScripts\User to %APPDATA%\Notepad++\plugins\Config\PythonScript\scripts
- copy the icon-folder from Repository\Utilities\Notepad++\PythonScripts\ to %APPDATA%\Notepad++\plugins\Config\PythonScript\
- goto Plugins->Phython Script->Configuration
- add the copied scripts to "toolbar icons" and change icons to whatever you like from icons in folder %APPDATA%\Notepad++\plugins\Config\PythonScript\icons\bmp
- uncheck "Prefer installed Python..."
- change "initialisation" from LAZY to ATSTARTUP
- copy the file "Robot.dat" from Repository\Utilities\Notepad++\ to %APPDATA%\Notepad++\plugins\Config\PythonScript\scripts
- restart NPP
-



