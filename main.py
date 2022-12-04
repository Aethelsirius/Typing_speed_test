from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton, QSizePolicy, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QShortcut, QComboBox, QGridLayout
from PyQt5.QtCore import *
import pyqtgraph as pg
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
        stacked.addWidget(Login())
        stacked.addWidget(Register())
 
        stacked.setCurrentIndex(4)          #* test only


class Menu(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.frameWidth = self.frameSize().width()
        self.frameHeight = self.frameSize().height() 
        self.initUI()
    def initUI(self):
        self.button_test = QPushButton(self)
        self.button_graph = QPushButton(self)
        self.button_login = QPushButton(self)
        self.button_register = QPushButton(self)

        self.button_test.setFixedWidth(50)

        self.button_test.setText('Test')
        self.button_graph.setText('Statistics')
        self.button_login.setText('Login')
        self.button_register.setText('Register')

    
        self.button_test.clicked.connect(lambda: stacked.setCurrentIndex(1))
        self.button_graph.clicked.connect(lambda: stacked.setCurrentIndex(2))
        self.button_login.clicked.connect(lambda: stacked.setCurrentIndex(3))
        self.button_register.clicked.connect(lambda: stacked.setCurrentIndex(4))
        

        self.button_test.move(200, 200) 
        self.button_graph.move(200,230)
        self.button_login.move(1150, 20)
        self.button_register.move(1150, 50)
    

class TS_Test(QWidget):
    def __init__(self):
        QWidget.__init__(self)     

        with open("styles.css", 'r') as f:
            sheet = f.read() 
        self.setStyleSheet(sheet)
        # self.setStyleSheet("QLabel{font-size: 15px;}")

        self.worker = Worker()
        self.worker_thread = QThread()
        self.worker.changed_signal.connect(self.difficulty)
        self.worker.float_signal.connect(self.update)
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.started.connect(self.worker.change_difficulty)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30,50)

        global lineEdit, dropDown
        lineEdit = QLineEdit()
        self.label = QLabel()
        self.accuracy_label = QLabel()
        self.wpm_label = QLabel()
        self.cpm_label = QLabel()
        self.reset_button = QPushButton()

        dropDown = QComboBox(self)
        dropDown.addItems(['Easy','Medium','Hard'])


        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(lineEdit)
        self.layout.addWidget(self.wpm_label)
        self.layout.addWidget(self.cpm_label)
        self.layout.addWidget(self.accuracy_label)
        self.layout.addWidget(self.reset_button)
        
        self.reset_button.clicked.connect(self.reset)
        self.label.setWordWrap(True)
    
        self.layout.setContentsMargins(250,250,250,300)
        self.setLayout(self.layout)                             
                
    def update(self, wpm_val, cpm_val, acc_val):
        self.wpm_label.setText(f'WPM: {wpm_val:0.3f}')
        self.cpm_label.setText(f'CPM: {cpm_val:0.3f}')
        data = [str(f'{wpm_val:0.3f}'), str(f'{cpm_val:0.3f}'), str(f'{acc_val:0.2f}')]
        if acc_val % 1 == 0:
            self.accuracy_label.setText(f'ACC: {int(acc_val)}%')
            data[2] = str(int(acc_val))
        else:
            self.accuracy_label.setText(f'ACC: {acc_val:0.2f}%')

        with open('text_files/data.txt', 'a') as f:
            f.write('\n'.join(data))
            f.write('\n')
    
    def difficulty(self, diff):
        with open('text_files/paragraphs.txt', 'r') as f: 
            f = f.read()
            difficulties = f.split('CHANGE DIFFICULTY\n')
            difficulty = difficulties[diff]

            sentences = difficulty.split('BREAK\n')
            global sentence
            sentence = random.choice(sentences)
            sentence = sentence.strip('\n')
            self.label.setText(sentence)
        
    def reset(self):
        print('reset')
        lineEdit.clear()
        self.difficulty(0)
        self.wpm_label.clear()
        self.cpm_label.clear()
        self.accuracy_label.clear()
        
        #self.Reset()
        #sentence = random.choice(self.sentences)
        #sentence = sentence.strip('\n')
        #self.label.setText(sentence)
        #self.worker.stop()
        self.worker.run()
        


class Worker(QObject):
    finished = pyqtSignal()
    changed_signal = pyqtSignal(int)
    float_signal = pyqtSignal(float, float, float)
    
    @pyqtSlot()
    def run(self):
        while True:
            print('important')         #?2
            if len(lineEdit.text()) > 0 and lineEdit.text()[0] == sentence[0]:
                timer_start = time.perf_counter()
                correct_char = 0
                break

        while True:     
            print('IMPORTANT')         #?2
            if (len(lineEdit.text()) == len(sentence)) and (lineEdit.text().split()[-1] == sentence.split()[-1]):
                #print(4)
                
                written_word = lineEdit.text().split(' ')
                timer_stop = time.perf_counter()
                timer = timer_stop - timer_start

                wpm = len(written_word) / timer * 60
                cpm = len(lineEdit.text()) / timer * 60

                for i in range(len(sentence)):
                    if lineEdit.text()[i] == sentence[i]:
                        correct_char += 1
                accuracy = correct_char / len(sentence) * 100

                print(f"Accuracy = {correct_char / len(sentence) * 100}")
                print(f'WPM: {wpm:0.3f}')
                print(f'CPM: {cpm:0.3f}')
                
                self.float_signal.emit(wpm, cpm, accuracy)
                break
        self.finished.emit()

    def change_difficulty(self):
        time.sleep(0.5)           #?1
        check = -1
        while len(lineEdit.text()) == 0:            
            if dropDown.currentIndex() == 0 and check != 0:
                self.changed_signal.emit(0)
                check = 0
            elif dropDown.currentIndex() == 1 and check != 1:
                self.changed_signal.emit(1)
                check = 1
            elif dropDown.currentIndex() == 2 and check != 2:
                self.changed_signal.emit(2)
                check = 2


class Statistics(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        with open('text_files/data.txt', 'r') as f:
            f = f.readlines()
            self.wpm = []
            self.cpm = []
            self.acc = []
            self.lenght = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
         
            for i in range(0, 46, 3):
                if i != 0:
                    self.wpm.insert(0,float(f[-(i)].strip('\n')))
            for i in range(2, 47, 3):
                self.cpm.insert(0,float(f[-(i)].strip('\n')))
            for i in range(1, 46, 3):
                self.acc.insert(0,float(f[-(i)].strip('\n')))
  
        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.setText('Back')
        self.button_back.move(30,20)

        self.wpm_graph = pg.PlotWidget(self)
        self.cpm_graph = pg.PlotWidget(self)
        self.acc_graph = pg.PlotWidget(self)

        self.stat_layout = QVBoxLayout()
        self.stat_layout.addWidget(self.wpm_graph)
        self.stat_layout.addWidget(self.cpm_graph)
        self.stat_layout.addWidget(self.acc_graph)

        self.wpm_graph.showGrid(x=True,y=True)
        self.cpm_graph.showGrid(x=True,y=True)
        self.acc_graph.showGrid(x=True,y=True)

        self.wpm_graph.plot(self.lenght, self.wpm)
        self.cpm_graph.plot(self.lenght, self.cpm)
        self.acc_graph.plot(self.lenght, self.acc)

        self.wpm_graph.setTitle('WPM')
        self.cpm_graph.setTitle('CPM')
        self.acc_graph.setTitle('ACC')

        self.stat_layout.setContentsMargins(150,10,50,10)
        self.setLayout(self.stat_layout)


class Login(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)  
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(0,0)

        self.username_label = QLabel(self)
        self.username_label.setText('Username: ')
        self.username_label.move(500, 200)

        self.username_entry = QLineEdit(self)
        self.username_entry.move(500, 220)

        self.password_label = QLabel(self)
        self.password_label.setText('Password: ')
        self.password_label.move(500, 250)

        self.password_entry = QLineEdit(self)
        self.password_entry.move(500, 270)
        self.password_entry.setEchoMode(QLineEdit.Password)


class Register(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)  
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(0,0)

        self.set_username_label = QLabel(self)
        self.set_username_label.setText('Username: ')
        self.set_username_label.move(500, 200)

        self.set_username_entry = QLineEdit(self)
        self.set_username_entry.move(500, 220)

        self.set_password_label = QLabel(self)
        self.set_password_label.setText('Password: ')
        self.set_password_label.move(500, 250)

        self.set_password_entry = QLineEdit(self)
        self.set_password_entry.move(500, 270)
        self.set_password_entry.setEchoMode(QLineEdit.Password)

        self.set_confirm_password_label = QLabel(self)
        self.set_confirm_password_label.setText('Confirm Password: ')
        self.set_confirm_password_label.move(500, 300)

        self.set_confirm_password_entry = QLineEdit(self)
        self.set_confirm_password_entry.move(500, 320)
        self.set_confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.set_confirm_password_entry.editingFinished.connect(self.register)

        self.register_button = QPushButton(self)
        self.register_button.clicked.connect(self.register)
        self.register_button.move(500, 350)

    def register(self):
        with open('text_files/user_info.txt', 'r') as f_r:
            f_r = f_r.read().split('\n')
            if (self.set_username_entry.text() not in f_r) and (self.set_password_entry.text() == self.set_confirm_password_entry.text()):
                with open('text_files/user_info.txt', 'a') as f_a:
                    f_a.write(self.set_username_entry.text() + '\n' + self.set_password_entry.text() + '\n')
                print('Done')
            else:
                print(234)
                   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())



#TODO 1) Login
#TODO 2) Reset Button
#TODO 3) Update graph right after test is performed
#* IDEA: dynamicly change position of widgets in new thread
#* IDEA: locknut dropDown ked lineEdit nie je prazdny
#?1 kod niekedy spracuje worker thread pomalsie a vyhodi to error, kvoli tomu tam je sleep na 0.5s 
#?2 bez tychto printov worker thread pada