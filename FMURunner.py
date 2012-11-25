#!/usr/bin/env python

import FMUFileList, FMUFileRunner

__author__ = "Jason Robinson // http://www.basshero.org // jaywink@basshero.org"
__doc__ = """
Fill Me Up
    
FMURunner module contains logic part for core functionality common to running Fill Me Up in GUI or command line mode
"""

class Runner():
    settings = {}
    targetPath = ''
    fileList = FMUFileList.FileList()
    fileGroups = {'MUSIC':['mp3','wma','ogg','wav','flac'],
                  'DOCUMENT':['txt','doc','xls'],
                  'IMAGE':['jpg','gif','png']}
    
    def __init__(self,settings={},targetPath=''):
        self.settings = settings
        self.targetPath = targetPath
        self.fileList = FMUFileList.FileList(space=settings["space"],path=settings["path"],fileExtensions=self.popFileExtensions(settings["file-types"]),targetPath=self.targetPath,targetNeeded=settings["targetNeeded"])
        
    def popFileExtensions(self,fileType):
        if fileType in self.fileGroups.keys():
            return self.fileGroups[fileType]
        elif len(fileType) == 0:
            return []
        else:
            return fileType.split(',')
            
    def setNewFileTypes(self,groups):
        fileExts = []
        for group in groups:
            fileExts = fileExts + self.popFileExtensions(str(group))
        self.fileList.fileExtensions = fileExts
    
    def generateFiles(self):
        self.fileList = FMUFileRunner.generateFiles(self.fileList)
        self.fileList.count = len(self.fileList.list)
            
    def doConsole(self):
        self.generateFiles()
        if len(self.fileList.list) > 0:
            print "File Runner returned "+str(self.fileList.count)+" files"
            if self.settings["targetNeeded"] == False:
                print "File list generated:"
                for fileName in self.fileList.list:
                    print fileName
                print "\nNo files have been copied as generate-only was specified."
            else:
                print "Starting to copy files..."
                self.copyFiles()
        else:
            print "File list was empty, no files copied."
            if len(self.fileList.invalidFields) > 0:
                print "The following attributes were missing during file list generation: ",self.fileList.invalidFields
        
    def copyFile(self,name):
        result = FMUFileRunner.copyFile(name,self.fileList.targetPath)
        return result
        
    def copyFiles(self):
        for name in self.fileList.list:
            print name
            result = self.copyFile(name)
            if result == True:
                print "OK"
            else:
                print "ERROR"       
    
    

        
    
