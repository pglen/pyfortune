#!/usr/bin/env python

import time, sys, os, re, stat
import string, pickle
import subprocess, site
import distutils.sysconfig

installerdir = sys.argv[0][:sys.argv[0].rfind("/")] + "/"

depfailed = False

PROJNAME  = "pyfortune"
PROJDATA  = "datfiles"

# ------------------------------------------------------------------------
# Return True if exists

def isdir(fname):

    try:
        ss = os.stat(fname)
    except:
        return False
    if stat.S_ISDIR(ss[stat.ST_MODE]):
        return True
    return False

# ------------------------------------------------------------------------
# Make dir if it does not exist

def softmkdir(dirx):
    if not isdir(dirx):
        #print "Creating directory '" + dirx + "'"
        os.mkdir(dirx, 0o755)
        if not isdir(dirx):
            return False
    return True

# See if path contains user dirs:

path = os.environ['PATH']; home = os.environ['HOME']
user = os.environ['USER']

#print "path", path
#print "home", home, "user", user

if subprocess.getoutput("whoami").strip() != "root":

    '''gotbin = ""
    for aa in str.split(path, ":"):
        if aa.find(home) >= 0:
            gotbin = aa
    if  gotbin == "":
        print "FAILED: You must be root to install pangview."
        sys.exit()
    else:
        print "installing in", gotbin
        sys.exit()'''

    print("FAILED: You must be root to install", PROJNAME)
    sys.exit()

#print "Verifying dependencies:"

prefix = sys.prefix
if not isdir(prefix):
    print("  >>>  Missing Dependencies: sys prefix dir does not exist.")
    depfailed = True

pylib = distutils.sysconfig.get_python_lib()
if not isdir(pylib):
    print("  >>>  Missing Dependencies: Python Library dir does not exist.")
    depfailed = True

# ------------------------------------------------------------------------

if depfailed:
    print("FAILED: Dependencies not met. Exiting.")
    sys.exit(1)

print("All dependencies are met.")

shared  = "/usr/share" + "/" + PROJNAME
bindir = "/usr/bin"

    # --- file  ---  target dir ---- exec flag ----
filelist = \
    ['pyfortune.py',        bindir,         True ],     \
    ['README.md',           shared,         False ],    \
    ['HISTORY',             shared,         False ],    \
    ['Selection',           shared,         False ],    \

    # --- dir  ---  target dir ---- root owner flag ----
dirlist = \
    [PROJNAME,     "/usr/share",    True ], \
    [PROJDATA,      shared,         True ], \

# Copy all to target:

print("Making target directories:")

for source, dest, exe in dirlist:
    targ = dest + "/" + source
    print("   '" + targ + "'")
    softmkdir(targ)

print("Copying files:")

for source, dest, exe in filelist:
    try:
        targ =  dest +  "/" + source
        print("   '" + source + "'      \t->'" + targ + "'")
        # Do not overwrite newer stuff
        subprocess.getoutput("cp -u " + source + " " + targ)
        if exe:
            os.chmod(targ, 0o755) # Root can rwx; can rx
        else:
            os.chmod(targ, 0o644) # Root can rw; others r
    except:
        print(sys.exc_info())

print("Copying directories:")

for source, dest, exe in dirlist:
    try:
        print("   '" + source + "'      \t->'" + dest + "'")
        subprocess.getoutput ("cp -a " + source + " " + dest)
        if exe:
            subprocess.getoutput(" chown root.root " + dest + "/" + source + "/*")
    except:
        print(sys.exc_info())

print()
print("You may now use the", PROJNAME, "utility on your system.")
print()




