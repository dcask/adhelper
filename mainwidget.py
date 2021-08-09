# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:59:03 2020

@author: kurinskiyas
"""

from PyQt5.QtWidgets import (QWidget, QMainWindow, QAction, QListWidget, 
                            QHBoxLayout, QListWidgetItem) #, QPushButton, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon
import pclist
import searchdialog
import mytabwidget
#from PyQt5.QtCore import QCoreApplication
#from PyQt5.QtCore import pyqtSignal


class MainWidget(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.initUI()
        
    def initUI(self):
        # main
        self.main_widget = QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # Actions
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        markAction = QAction(QIcon('off.png'), 'Ping all', self)
        markAction.setShortcut('Ctrl+M')
        markAction.setStatusTip('Check ping')
        markAction.triggered.connect(self.markEnabled)
        
        searchAction = QAction(QIcon('search.png'), 'Search in list', self)
        searchAction.setShortcut('Ctrl+S')
        searchAction.setStatusTip('Search user')
        searchAction.triggered.connect(self.searchString)
        
        rdpAction = QAction(QIcon('icon.png'), 'Connect', self)
        rdpAction.setShortcut('Ctrl+R')
        rdpAction.setStatusTip('Connect')
        rdpAction.triggered.connect(self.rdpConnect)
        # Toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(markAction)
        self.toolbar.addAction(searchAction)
        self.toolbar.addAction(rdpAction)
        
        # Menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        # Status bar
        self.statusBar().showMessage('ready')
        
        # Shape
        self.resize(800,600)
        self.setWindowTitle('Main Window')
        
        # Icon
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        #app_icon = QtGui.QIcon()
        #app_icon.addFile('icon16.png', QSize(16,16))
        #app_icon.addFile('icon24.png', QSize(24,24))
        #app_icon.addFile('icon32.png', QSize(32,32))
        #app_icon.addFile('icon48.png', QSize(48,48))
        #app_icon.addFile('icon256.png', QSize(256,256))
        #self.setWindowIcon(app_icon)
        # Form
        self.tab = mytabwidget.DTabWidget(self)
        # List widget
        self.listwidget = QListWidget(self)
        
        # Layout
        hbox = QHBoxLayout(self.main_widget)
        #hbox.addStretch(1)
        hbox.addWidget(self.listwidget)     
        hbox.addWidget(self.tab)

        # Load list
        
        self.loadList()
        self.listwidget.currentRowChanged.connect(self.itemSelected)
        
        # Show window
        self.show()
    # signal that item has been selected
    def itemSelected(self):
        i = self.listwidget.currentRow()
        if hasattr(self.listwidget.item(i), 'text'):
            host = self.listwidget.item(i).text()
            name = host[host.find(' ')+1:host.find('(')]
            host = host [:host.find(' ')]
            self.tab.loadTree(host)
            if name != "":
                self.tab.loadUser(name)
        
        # signal that item has been selected
    def rdpConnect(self):
        i = self.listwidget.currentRow()
        if hasattr(self.listwidget.item(i), 'text'):
            host = self.listwidget.item(i).text()
            host = host [:host.find(' ')]
            if pclist.ping(host):
                if pclist.ConnectRDP(host):
                    self.statusBar().showMessage('Done')
                else:
                    self.statusBar().showMessage('Connection error to '+host)
        
    # load domain pc list    
    def loadList(self):
        self.listwidget.clear();
        officon = QtGui.QIcon('off.png')
        mlist = pclist.GetDomainComputerList()
        #mlist.sort(key=lambda x: x.get("cn").lower())
        mlist.sort(key=lambda x: x[0].lower())
        for pc in mlist:
            mitem = QListWidgetItem(str(pc[0])+' '+str(pc[1]))
            mitem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            mitem.setIcon(officon)
            # mitem.setData(0, pc)
            self.listwidget.addItem(mitem)    
    # ping all
    def markEnabled(self):
        self.loadList();
        onicon = QtGui.QIcon('on.png')
        officon = QtGui.QIcon('off.png')
        self.statusBar().showMessage('Start pinging...')
        for i in range(self.listwidget.count()):
            host = self.listwidget.item(i).text()
            host = host [:host.find(' ')]
            if pclist.ping(host):
                self.listwidget.item(i).setIcon(onicon)
            else:
                self.listwidget.item(i).setIcon(officon)
            
            #if i%5 == 0: 
            self.listwidget.repaint()
            self.statusBar().showMessage('Pinging '+host)
    # create search dialog
    def searchString(self):
        dlg = searchdialog.SearchDialog()
        dlg.accepted.connect(lambda: self.findStringInList(dlg.editbox.text()))
        dlg.exec_()
    # search substring in the list    
    def findStringInList(self,s):
        for i in range(self.listwidget.count()):
            itemtext = self.listwidget.item(i).text()
            if itemtext.lower().find(s.lower()) != -1:
                self.listwidget.setCurrentRow(i)
                
            
        