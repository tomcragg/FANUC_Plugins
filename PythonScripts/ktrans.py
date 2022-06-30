import os
import sys
version = input("1: V8.36 | 2: V9.10 | 3: V9.36 | 4: V9.40 | 99: V8.30 - ")
if version == 1:
    os.system("ktrans " + sys.argv[1] + " /ver V8.36-1")
elif version == 2:
    os.system("ktrans " + sys.argv[1] + " /ver V9.10-1")
elif version == 3:
    os.system("ktrans " + sys.argv[1] + " /ver V9.36-1")
elif version == 4:
    os.system("ktrans " + sys.argv[1] + " /ver V9.40-1")
elif version == 99:
    os.system("ktrans " + sys.argv[1] + " /ver V8.30-1")
version = input("END")