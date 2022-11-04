from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton, QSizePolicy, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QShortcut
from PyQt5.QtCore import *
import sys
import time
import random


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
 
        stacked.setCurrentIndex(1)          #* test only


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
        global sentence
        sentence = random.choice(self.sentences)
        sentence = sentence.strip('\n')

        self.setStyleSheet("QLabel{font-size: 15px;}")

        self.worker = Worker()
        self.worker_thread = QThread()
        self.worker.float_signal.connect(self.update)
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30,50)

        global lineEdit
        lineEdit = QLineEdit()
        self.label = QLabel()
        self.accuracy_label = QLabel()
        self.wpm_label = QLabel()
        self.reset_button = QPushButton()

        self.first_letter = sentence[0]

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(lineEdit)
        self.layout.addWidget(self.wpm_label)
        self.layout.addWidget(self.accuracy_label)
        self.layout.addWidget(self.reset_button)
        
        self.reset_button.clicked.connect(self.Reset)
        self.label.setText(sentence)
    
        self.layout.setContentsMargins(250,250,250,300)
        self.setLayout(self.layout)                             
                
    def update(self, wpm_val, acc_val):
        self.wpm_label.setText(f'WPM: {wpm_val:0.3f}')

        if acc_val % 1 == 0:
            self.accuracy_label.setText(f'ACC: {int(acc_val)}%')
        else:
            self.accuracy_label.setText(f'ACC: {acc_val:0.2f}%')

    def Reset(self):
        print('reset')
        lineEdit.clear()
        self.label.clear()
        self.wpm_label.clear()
        self.accuracy_label.clear()

        sentence = random.choice(self.sentences)
        sentence = sentence.strip('\n')
        self.label.setText(sentence)
        self.start()


class Worker(QObject):
    finished = pyqtSignal()
    float_signal = pyqtSignal(float, float)
    
    @pyqtSlot()
    def run(self):
        while True:
            print('important')
            if len(lineEdit.text()) > 0 and lineEdit.text()[0] == sentence[0]:
                timer_start = time.perf_counter()
                correct_char = 0
                break

        while True:     
            print('IMPORTANT')
            if (len(lineEdit.text()) == len(sentence)) and (lineEdit.text().split()[-1] == sentence.split()[-1]):
                #print(4)
                
                written_word = lineEdit.text().split(' ')
                timer_stop = time.perf_counter()
                timer = timer_stop - timer_start
                print(timer)

                wpm = len(written_word) / timer * 60

                for i in range(len(sentence)):
                    if lineEdit.text()[i] == sentence[i]:
                        correct_char += 1
                accuracy = correct_char / len(sentence) * 100

                print(f"Accuracy = {correct_char / len(sentence) * 100}")
                print(f'WPM: {wpm:0.3f}')
                
                self.float_signal.emit(wpm, accuracy)
                break
        self.finished.emit()


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
#TODO 4) Reset Button
#TODO 5) Saving WPM and Accuracy to data.txt