from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton, QSizePolicy, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
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
    

class TS_Test(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        f = open('paragraphs.txt').read()
        self.sentences = f.split('BREAK\n')
        self.sentence = random.choice(self.sentences)
        self.sentence = self.sentence.strip('\n')
        self.word = self.sentence.split()
        self.setStyleSheet("QLabel{font-size: 15px;}")

        self.initUI()
        self.start_thread()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30,50)

        self.lineEdit = QLineEdit()
        self.label = QLabel()
        self.accuracy_label = QLabel()
        self.wpm_label = QLabel()
        self.pismeno = self.lineEdit.text()
        self.prve = self.sentence[0]
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.accuracy_label)
        self.layout.addWidget(self.wpm_label)

        
        
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
                    t_time = threading.Thread(target=self.time_thread)
                    t_time.start()
                    break
                
    def time_thread(self):
        print('start')
        timer_start = time.perf_counter()
        self.correct_char = 0
        
        
        while True:
            if (len(self.lineEdit.text()) == len(self.sentence)) and (self.lineEdit.text().split()[-1] == self.word[-1]):
                self.written_word = self.lineEdit.text().split(' ')
                timer_stop = time.perf_counter()
                timer = timer_stop - timer_start

                self.wpm = len(self.written_word) / timer * 60

                for i in range(len(self.sentence)):
                    if self.lineEdit.text()[i] == self.sentence[i]:
                        self.correct_char += 1
                self.accuracy = self.correct_char / len(self.sentence) * 100

                print(f"Accuracy = {self.correct_char / len(self.sentence) * 100}")
                print(f'WPM: {self.wpm:0.3f}')
                
                self.accuracy_label.setText(f'Accuracy = {self.accuracy}%')
                self.wpm_label.setText(f'WPM: {self.wpm:0.3f}')

                break

    def Reset(self):
        pass

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