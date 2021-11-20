import os
from os import listdir
import re

def getImagesInDir(dir, match = '', limit = -1):
    fullPaths = []
    imageNames = listdir(dir)
    for f in imageNames:
        doesMatch = 0 if not match else re.match(match, f)
        if doesMatch:
            fullPaths.append(os.path.join(os.getcwd(), dir, f))

    if limit > -1:
        fullPaths = fullPaths[0:limit]
    return fullPaths
