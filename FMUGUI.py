#!/usr/bin/env python

from PyQt4 import QtGui, QtCore
import FMURunner, math

__author__ = "Jason Robinson // http://www.basshero.org // jaywink@basshero.org"
__doc__ = """
Fill Me Up
    
FMUGUI is the GUI application of Fill Me Up 
"""

class GUIApp():
    def __init__(self,targetPath,settings):
        y = 0
        x = 0
        self.settings = settings
        self.runner = FMURunner.Runner(settings,targetPath)
        self.runner.generateFiles()
        self.app = QtGui.QApplication([])
        self.mainWindow = QtGui.QMainWindow()
        self.mainWindow.setWindowTitle('Fill Me Up '+settings['version'])
        self.window = QtGui.QWidget()
        self.center(self.mainWindow)
        self.grid = QtGui.QGridLayout()
        menuQuitAction = QtGui.QAction('Quit',self.mainWindow)
        self.mainWindow.connect(menuQuitAction,QtCore.SIGNAL('triggered()'),self.app.exit)
        #~ menuHelpAction = QtGui.QAction('Help',self.mainWindow)
        #~ self.mainWindow.connect(menuHelpAction,QtCore.SIGNAL('triggered()'),self.showHelp)
        menuAboutAction = QtGui.QAction('About',self.mainWindow)
        self.mainWindow.connect(menuAboutAction,QtCore.SIGNAL('triggered()'),self.showHelp)
        menuBar = self.mainWindow.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(menuQuitAction)
        helpMenu = menuBar.addMenu("&Help")
        #~ helpMenu.addAction(menuHelpAction)
        helpMenu.addAction(menuAboutAction)
        self.grid.addWidget(QtGui.QLabel('Source path'), y, 0)
        self.pathField = QtGui.QLineEdit(self.runner.fileList.path)
        self.grid.addWidget(self.pathField, y, 1)
        self.pathBrowseButton = QtGui.QPushButton('...')
        self.grid.addWidget(self.pathBrowseButton,y,2)
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('Target path'), y, 0)
        self.targetField = QtGui.QLineEdit(self.runner.fileList.targetPath)
        self.grid.addWidget(self.targetField, y, 1)
        self.targetBrowseButton = QtGui.QPushButton('...')
        self.grid.addWidget(self.targetBrowseButton,y,2)
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('File extensions'), y, 0)
        self.fileTypesField = QtGui.QLineEdit(self.runner.fileList.typesToText())
        self.grid.addWidget(self.fileTypesField, y, 1)
        self.fileGroupBrowseButton = QtGui.QPushButton('...')
        self.grid.addWidget(self.fileGroupBrowseButton,y,2)
        self.fileTypesY = y
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('Maximum size (mb)'), y, 0)
        self.spaceField = QtGui.QLineEdit(str(self.runner.fileList.space/1048576))
        self.grid.addWidget(self.spaceField, y, 1)
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('Collected size (mb)'), y, 0)
        self.sizeField = QtGui.QLineEdit(str(self.runner.fileList.size/1048576))
        self.grid.addWidget(self.sizeField, y, 1)
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('Files collected'), y, 0)
        self.countField = QtGui.QLineEdit(str(self.runner.fileList.count))
        self.grid.addWidget(self.countField, y, 1)
        y = y + 1
        self.grid.addWidget(QtGui.QLabel('File list'), y, 0)
        self.fileListBox = QtGui.QTextEdit('<small>'+self.runner.fileList.listToText()+'</small>')
        self.grid.addWidget(self.fileListBox, y, 1)
        y = y + 1
        self.generate = QtGui.QPushButton('Generate')
        self.grid.addWidget(self.generate,y,0)
        self.copyButton = QtGui.QPushButton('Copy to target')
        self.grid.addWidget(self.copyButton,y,1)
        self.progressBarY = y
        self.window.connect(self.generate,QtCore.SIGNAL('clicked()'),self.generateNewData)
        self.window.connect(self.copyButton,QtCore.SIGNAL('clicked()'),self.copyFiles)
        self.window.connect(self.pathBrowseButton,QtCore.SIGNAL('clicked()'),self.choosePath)
        self.window.connect(self.targetBrowseButton,QtCore.SIGNAL('clicked()'),self.chooseTargetPath)
        self.window.connect(self.fileGroupBrowseButton,QtCore.SIGNAL('clicked()'),self.browseFileGroups)
        self.window.setLayout(self.grid)
        self.countField.setReadOnly(True)
        self.sizeField.setReadOnly(True)
        self.fileListBox.setReadOnly(True)
        self.mainWindow.setCentralWidget(self.window)
        self.mainWindow.show()
        self.app.exec_()
        
    def showHelp(self):
        self.helpWindow = QtGui.QMainWindow()
        self.helpWindow.setWindowTitle('About')
        self.helpWindow.setGeometry(0,0,600,400)
        self.center(self.helpWindow)
        textBox = QtGui.QTextEdit('<pre>'+self.settings['doc']+'</pre>')
        textBox.setReadOnly(True)
        self.helpWindow.setCentralWidget(textBox)
        self.helpWindow.show()
    
    def toggleFormWidgets(self,status):
        self.fileGroupBrowseButton.setDisabled(status)
        self.targetBrowseButton.setDisabled(status)
        self.pathBrowseButton.setDisabled(status)
        self.copyButton.setDisabled(status)
        self.generate.setDisabled(status)
        self.spaceField.setDisabled(status)
        self.pathField.setDisabled(status)
        self.targetField.setDisabled(status)
        self.fileTypesField.setDisabled(status)
    
    def browseFileGroups(self):
        self.toggleFormWidgets(True)
        self.groupStringList = QtGui.QTreeWidget() 
        self.groupStringList.setColumnCount(1)
        self.groupStringList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.groupStringList.setHeaderLabels(['Select file groups'])
        items = []
        for key in self.runner.fileGroups.keys():
            items.append(QtGui.QTreeWidgetItem([key]))
        self.groupStringList.insertTopLevelItems(0, items);
        self.setGroupsButton = QtGui.QPushButton('Set')
        self.grid.addWidget(self.groupStringList,self.fileTypesY,2,5,1)
        self.grid.addWidget(self.setGroupsButton,self.fileTypesY+5,2)
        self.window.connect(self.setGroupsButton,QtCore.SIGNAL('clicked()'),self.setFileGroups)
    
    def setFileGroups(self):
        iterator = QtGui.QTreeWidgetItemIterator(self.groupStringList,QtGui.QTreeWidgetItemIterator.All)
        groupNames = []
        while (iterator.value() <> None):
            if iterator.value().isSelected():
                groupNames.append(iterator.value().text(0))
            iterator.__iadd__(1)
        self.grid.removeWidget(self.groupStringList)
        self.groupStringList.setParent(None)
        self.grid.removeWidget(self.setGroupsButton)
        self.setGroupsButton.setParent(None)
        self.toggleFormWidgets(False)
        self.runner.setNewFileTypes(groupNames)
        self.fileTypesField.setText(self.runner.fileList.typesToText())
    
    def choosePath(self):
        folderName = QtGui.QFileDialog.getExistingDirectory(self.window, "Select source path")
        self.pathField.setText(folderName)
        self.runner.fileList.path = folderName

    def chooseTargetPath(self):
        folderName = QtGui.QFileDialog.getExistingDirectory(self.window, "Select target path")
        self.targetField.setText(folderName)
        self.runner.fileList.targetPath = folderName
        
    def center(self,widget):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  widget.geometry()
        widget.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
    def generateNewData(self):
        self.toggleFormWidgets(True)
        self.copyButton.setHidden(True)
        self.app.processEvents()
        self.runner.fileList.path = str(self.pathField.text())
        self.runner.fileList.space = int(self.spaceField.text())*1048576
        if len(self.fileTypesField.text()) > 0:
            self.runner.fileList.fileExtensions = str(self.fileTypesField.text()).replace(' ','').split(',')
        else:
            self.runner.fileList.fileExtensions = []
        self.runner.fileList.targetPath = self.targetField.text()
        self.runner.fileList.size = 0
        self.runner.fileList.list = []
        self.runner.generateFiles()
        if len(self.runner.fileList.invalidFields) > 0:
            messageBox = QtGui.QMessageBox()
            messageBox.setText("The following fields are missing: "+str(self.runner.fileList.invalidFields).strip('[]'))
            messageBox.setWindowTitle("File list generation failed")
            messageBox.setIcon(QtGui.QMessageBox.Warning)
            messageBox.exec_()
        self.sizeField.setText(str(self.runner.fileList.size/1048576))
        self.countField.setText(str(self.runner.fileList.count))
        self.fileListBox.setText('<small>'+self.runner.fileList.listToText()+'</small>')
        self.copyButton.setHidden(False)
        self.toggleFormWidgets(False)
        
    def cancelFileCopy(self):
        self.fileCopyCancelled = True
        
    def copyFiles(self):
        self.runner.fileList.targetPath = str(self.targetField.text())
        self.toggleFormWidgets(True)
        self.copyButton.setHidden(True)
        progressBar = QtGui.QProgressBar(self.window)
        self.grid.addWidget(progressBar,self.progressBarY,1)
        cancelButton = QtGui.QPushButton('Stop')
        self.grid.addWidget(cancelButton,self.progressBarY,0)
        self.window.connect(cancelButton,QtCore.SIGNAL('clicked()'),self.cancelFileCopy)
        counter = 0
        self.fileCopyCancelled = False
        if len(self.runner.fileList.targetPath) > 0:
            for name in self.runner.fileList.list:
                if self.fileCopyCancelled == False:
                    result = self.runner.copyFile(name)
                    if result == True:
                        counter = counter +1
                        progress = int(math.modf((float(counter)/self.runner.fileList.count)*100)[1])
                        progressBar.setValue(progress)
                        self.app.processEvents()
                    else:
                        pass
                else:
                    break
        self.grid.removeWidget(progressBar)
        progressBar.setParent(None)
        self.grid.removeWidget(cancelButton)
        cancelButton.setParent(None)
        self.copyButton.setHidden(False)
        self.toggleFormWidgets(False)
        
        
        
    
