import os
import sys
import shutil
import ftplib

ftp = ftplib.FTP()
ftp.connect("127.0.0.1", 21)
print (ftp.getwelcome())
try:
    print ("Logging in...")
    ftp.login("", "")
except:
    "Failed to login"
print ("Success")
ftp.storbinary("STOR " + os.path.basename(sys.argv[1]), open(sys.argv[1], "rb"))
file.close()
ftp.quit()
version = input("END")