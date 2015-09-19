#!/usr/bin/python
__extension__ = ".ipynb"
import os


def createProgramLine(path):
	return '/opt/inotebook/INotebook --notebook="' + path + '"'

def getExtension():
    return __extension__

def createPDFLine(path):
    filename, file_extension = os.path.splitext(path)
    file_dir = os.path.dirname(path)
    genpdf_line = 'cd "' + file_dir + '" && ipython nbconvert "' + filename + file_extension + '" --to latex --post PDF '
    genpdf_line = genpdf_line + ' && rm "' + filename + '.tex"'
    print genpdf_line
    return genpdf_line
