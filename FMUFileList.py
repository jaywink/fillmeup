#!/usr/bin/env python

__author__ = "Jason Robinson // http://www.basshero.org // jaywink@basshero.org"
__doc__ = """
Fill Me Up
    
FMUFileList module contains the FileList class that contains data about a generated file list   
"""

class FileList():
    list = []
    size = 0
    count = 0
    path = ''
    targetPath = ''
    space = 0
    fileExtensions = []
    invalidFields = []
    targetNeeded = True
    
    def __init__(self, space=0, path='', fileExtensions=[],targetPath='',targetNeeded=True):
        self.path = path
        self.space = space
        self.fileExtensions = fileExtensions
        self.targetPath = targetPath
        self.targetNeeded = targetNeeded
        
    def listToText(self):
        text = ''
        for item in self.list:
            text = text + item + '<br>'
        return text
    
    def typesToText(self):
        return str(self.fileExtensions).strip('[]').replace("'","")
        
    def isDataOK(self):
        ok = True
        self.invalidFields = []
        if self.space == 0:
            ok = False
            self.invalidFields.append('Maximum size (mb)')
        if self.fileExtensions == []:
            ok = False
            self.invalidFields.append('File extensions')
        if self.targetPath == '' and self.targetNeeded == True:
            ok = False
            self.invalidFields.append('Target path')
        if self.path == '':
            ok = False
            self.invalidFields.append('Source path')
        return ok
    
