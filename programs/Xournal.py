#!/usr/bin/python
__extension__ = ".xoj"
import os


def createProgramLine(path):
	return "xournal '" + path + "'"

def getExtension():
	return __extension__

def createPDFLine(path):
	filename, file_extension = os.path.splitext(path)
	genpdf_line = "xournal '" + path + "' -e '" + filename +".pdf'"
	return genpdf_line
