import os
import sys
version = input("1: V8.36 | 2: V9.10 | 3: V9.40 - ")
if version == 1:
    os.system("kcdict " + sys.argv[1] + " /ver V8.36-1")
elif version == 2:
    os.system("kcdict " + sys.argv[1] + " /ver V9.10-1")
else:
    os.system("kcdict " + sys.argv[1] + " /ver V9.40-1")
version = input("END")
