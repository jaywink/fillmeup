#!/usr/bin/env python

import os,random,stat,sys,shutil

__author__ = "Jason Robinson // http://www.basshero.org // jaywink@basshero.org"
__doc__ = """
Fill Me Up
    
FMUFileRunner module contains functions for file processing and file list generation
"""

def generateFiles(fileList):
    allList = []
    if fileList.isDataOK() == True:
        try:
            # get all files in to a list
            fileTuple = os.walk(fileList.path)
            for dirPath,subDir,fileName in fileTuple:
                for name in fileName:
                    found = False
                    for ext in fileList.fileExtensions:
                        if name[-len(ext):].lower() == ext.lower():
                            found = True
                            allList.append(os.path.join(dirPath,name))
                            break
            while fileList.size < fileList.space and len(allList)>0:
                index = random.randint(0,len(allList)-1)
                fileSize = os.stat(allList[index])
                if fileList.size + fileSize[stat.ST_SIZE] <= fileList.space:
                    fileList.size = fileList.size + fileSize[stat.ST_SIZE]
                    fileList.list.append(allList.pop(index))
                else:
                    allList.remove(allList[index])
            return fileList
        except Exception,e:
            print "Error",e
            raise
    else:
        return fileList
        
def copyFile(fileName,to):
    try:
        shutil.copy2(fileName,to)
        return True
    except:
        return False
        
    

        
    
