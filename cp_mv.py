''' Right now the sourcefile and destination could also be paths, but the
    variables need to be passed as strings. This could easily be changed for
    convenience. '''

import shutil
import os

def copySingleFile(sourcefile,destination):

    shutil.copy(sourcefile,destination)

def copyDirectory(sourcefile,destination):

    shutil.copytree(sourcefile,destination)

def makeDirectory(directoryName):

    os.mkdir(directoryName)

def move(sourcefile,destination):

    shutil.move(sourcefile,destination)

def removeSingleFile(sourcefile):

    os.remove(sourcefile)

def removeDirectory(sourcefile):

    shutil.rmtree(sourcefile)
