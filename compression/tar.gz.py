#!/usr/bin/python
import tarfile

ext = ".tar.gz"

def compress(extensions,location,title):
	tar = tarfile.open(location + "/" + title + ext, "w:gz")
	for extension in extensions:
		tar.add(location + "/" + title + extension, arcname=str(title + extension))	
	tar.close()
	return location + "/" + title + ".tar.gz"
	
def getExtension():
	return ext
