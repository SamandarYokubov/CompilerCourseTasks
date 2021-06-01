
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from graphviz import Digraph
import welcomescreen


if __name__=='__main__':

    app = QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()    
    welcome=welcomescreen.WelcomeScreen(widget)
    widget.addWidget(welcome)
    widget.setFixedHeight(700)
    widget.setFixedWidth(1000)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
