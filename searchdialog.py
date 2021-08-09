# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 15:47:11 2020

@author: kurinskiyas
"""
from PyQt5.QtWidgets import (QLineEdit, QVBoxLayout, QDialog,
                             QDialogButtonBox) #, QPushButton, QLabel
class SearchDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Find substring")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.editbox = QLineEdit(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.editbox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


