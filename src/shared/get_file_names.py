import os
from os import listdir

def getImagesInDir(dir, match = '', limit = -1):
    fullPaths = []
    imageNames = listdir(dir)
    for f in imageNames:
        doesMatch = 0 if not match else f.find(match)
        if doesMatch > -1:
            fullPaths.append(os.path.join(os.getcwd(), dir, f))

    if limit > -1:
        fullPaths = fullPaths[0:limit]
    return fullPaths
