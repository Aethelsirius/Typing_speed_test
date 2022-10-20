from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton, QSizePolicy, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtCore import *
import sys
import time
import random
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Typing Speed Test App")
        self.setMinimumSize(1280,720)

        global stacked
        stacked = QStackedWidget(self)
        self.setCentralWidget(stacked)
        stacked.addWidget(Menu())
        stacked.addWidget(TS_Test())
        stacked.addWidget(Statistics())

        stacked.setCurrentIndex(1)          #* len na test


class Menu(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.frameWidth = self.frameSize().width()
        self.frameHeight = self.frameSize().height() 
        self.initUI()
    def initUI(self):
        self.button_test = QPushButton(self)
        self.button_graph = QPushButton(self)
        self.button_test.setFixedWidth(50)

    
        self.button_test.clicked.connect(lambda: stacked.setCurrentIndex(1))
        self.button_graph.clicked.connect(lambda: stacked.setCurrentIndex(2))
        self.button_graph.clicked.connect(lambda: print(self.frameSize().width()))

        self.button_test.move(self.frameSize().width()*50//100-50,200)
        self.button_graph.move(200,230)
    

class TS_Test(QWidget, QObject):
    def __init__(self):
        QWidget.__init__(self)
        f = open('paragraphs.txt').read()
        self.sentences = f.split('BREAK\n')
        self.sentence = random.choice(self.sentences)
        self.setStyleSheet("QLabel{font-size: 15px;}")

        self.initUI()
        self.start_thread()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30,50)

        self.lineEdit = QLineEdit()
        self.label = QLabel()
        self.pismeno = self.lineEdit.text()
        self.prve = self.sentence[0]
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        
        self.label.setText(self.sentence)
       
        self.layout.setContentsMargins(250,250,250,300)
        self.setLayout(self.layout)

    def start_thread(self):                                                              #* while cyklus by bez tohto nefungoval
        t_start=threading.Thread(target=self.start)
        t_start.start()                              

    def start(self):
        while True:
            if len(self.lineEdit.text()) > 0:
                if self.lineEdit.text()[0] == self.prve:
                    print('gut')
                    t_time = threading.Thread(target=self.time_thread)
                    t_time.start()
                    break
                #else:
                #    print('zle')

    def time_thread(self):
        timer_start = time.perf_counter()
        
        while True:
            if len(self.lineEdit.text()) >= 10:
                timer_stop = time.perf_counter()
                print(f'time is {timer_stop - timer_start:0.3f}')
                break

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
#TODO 3) opravit v class TS_Test "f = open()" na "with open() as f:"