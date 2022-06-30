import os
import sys
version = input("1: V8.36 | 2: V9.10 - ")
if version == 1:
    base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    #os.system("kconvars " + base + ".sv " + base + ".dt /ver V8.36-1")
    os.system("kconvars " + sys.argv[1].lower() + " " + base + ".dt /ver V8.36-1")
else:
    base = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    #os.system("kconvars " + base + ".sv " + base + ".dt /ver V9.10-1")
    os.system("kconvars " + sys.argv[1].lower() + " " + base + ".dt /ver V9.10-1")
version = input("END")
