# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:49:57 2020

@author: kurinskiyas
"""

import sys
from mainwidget import MainWidget
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWidget()
    sys.exit(app.exec_())