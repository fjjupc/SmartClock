# -*- coding: utf-8 -*-

from ast import If
from PyQt5.QtWidgets import QApplication
from UI import MainUI

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    uMain = MainUI()
    uMain.show()

    app.exec_()