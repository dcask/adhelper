# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:11:53 2020

@author: kurinskiyas
"""
from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTabWidget, QLabel,  QVBoxLayout) #, QPushButton, QLabel
#from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import csvinfo
import pyodbc
import os.path

class DTabWidget(QTabWidget): 
    def __init__(self, parent): 
        super(QTabWidget, self).__init__(parent) 
        
        self.userlayout = QVBoxLayout(self)
        # Initialize tab screen 
        # self.tabs = QTabWidget() 
        self.tab1 = QTreeWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        #self.tabs.resize(300, 200) 
        
        #self.loadTree('ws-smng-0010')
  
        # Add tabs 
        self.addTab(self.tab1, "Host") 
        self.addTab(self.tab2, "User") 
        self.addTab(self.tab3, "Invet") 
  
        #self.tab1.layout.addWidget(self.l) 
        self.tab1.setHeaderHidden(True)
  
        # Add tabs to widget 
        #self.layout.addWidget(self.tabs) 
        #self.setLayout(self.layout)
    
    def loadTree(self, host):
        self.tab1.clear()
        top = self.tab1.invisibleRootItem()
        top.setText(0,host)
        fname = "K:\\Служба ИТ и ТО\\Куринский\\computers\\"+host+".csv"
        try:
            if os.path.isfile(fname): 
                with open(fname) as f_obj:
                    csvinfo.makeTree(f_obj, self.tab1)
        except IOError:
            print("no file")
            
    def loadUser(self, name):
        while self.userlayout.count():
            child = self.userlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # mssql connection
        server_sql = '10.48.100.216\\SQLSERVER2008' 
        database_sql = 'smngbase3' 
        username_sql = 'sa' 
        password_sql = '123456'
        photo = None
        conn_sql = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};SERVER='+server_sql+',49168;DATABASE='+database_sql+';UID='+username_sql+';PWD='+ password_sql)
        cursor_sql = conn_sql.cursor()
        query_string_sql = "SELECT  picture FROM plist WHERE Name+' '+FirstName+' '+MidName='"+name+"'"
        cursor_sql.execute(query_string_sql)
        rows_sql = cursor_sql.fetchall()
        for row_sql in rows_sql:
            photo = row_sql[0]
        
        cursor_sql.close()
        conn_sql.close()
        
        # Create widget
         
        
        self.label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(photo)
        pixmap_sc = pixmap.scaledToWidth(256)
        self.label.setPixmap(pixmap_sc)
        #self.label.resize(256,256)
        self.userlayout.addWidget(self.label) 
        self.tab2.setLayout(self.userlayout) 
        #self.show()