from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton
import sys
import time
import random
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Typing Speed Test App")
        self.setMinimumSize(600,400)

        global stacked
        stacked = QStackedWidget(self)
        self.setCentralWidget(stacked)
        stacked.addWidget(Menu())
        stacked.addWidget(TS_Test())
        stacked.addWidget(Statistics())

        #self.stacked.setCurrentIndex(1)


class Menu(QWidget):
    def __init__(self):
        QWidget.__init__(self) 
        self.initUI()
    
    def initUI(self):
        self.button_test = QPushButton(self)
        self.button_graph = QPushButton(self)
    
        self.button_test.clicked.connect(lambda: stacked.setCurrentIndex(1))
        self.button_graph.clicked.connect(lambda: stacked.setCurrentIndex(2))
        self.button_graph.clicked.connect(lambda: print(self.frameSize()))

        #self.button_test.move(self.frameGeometry()*50//100,200)
        self.button_graph.move(200,230)
    

class TS_Test(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(500,300)


class Statistics(QWidget):
    def __init__(self):
        QWidget.__init__(self)        
        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(400,300)
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())



#TODO 1) Menu with two typing mods: 1. basic test 2. training mod similiar to keybr.com
#TODO 2) Collect data from both mods and save it to .txt file, than make statistics from said data