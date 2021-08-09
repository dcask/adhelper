# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 17:12:14 2020

@author: kurinskiyas
"""
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5 import QtGui
import csv

def makeTree(file_obj, tree):
    top = tree.invisibleRootItem()
    #tree.addTopLevelItem(top)
    instIcon = QtGui.QIcon('arrow.png')
    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:
        sec = line['Секция отчета']
        param = line['Параметр']
        number = line['Номер экземпляра']
        val = line['Значение']
        
        secItem = findItem(top, sec)
        if secItem == None:
            secItem = QTreeWidgetItem(top)
            secItem.setText(0, sec)
            top.addChild(secItem)
        
        numberItem = secItem.child(int(number)-1)
        if numberItem == None:
            numberItem = QTreeWidgetItem(secItem)
            numberItem.setIcon(0,instIcon)
            secItem.addChild(numberItem)
          
  
        txt = numberItem.text(0)
        if len(txt)>0: txt+='\n'
        numberItem.setText(0, txt+param+' : '+val)
        
def findItem(treeItem,txt):
    # root = self.treeWidget.invisibleRootItem()
    children_count = treeItem.childCount()
    res = None
    for i in range(children_count):
        if treeItem.child(i).text(0) == txt:
           res = treeItem.child(i)
    return res

    
def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    for line in reader:
        print(line)
  
 
if __name__ == "__main__":
    tr = QTreeWidget()
    with open("K:\\Служба ИТ и ТО\\Куринский\\computers\\ws-smng-0010.csv") as f_obj:
        makeTree(f_obj, tr)
