from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QStackedWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QComboBox, QMessageBox
from PyQt6.QtCore import *
import pyqtgraph as pg
import sys
import time
import random

username = ''


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
 
        stacked.setCurrentIndex(0)          #* test only

        with open("styles/main_style.css", 'r') as f:
            self.setStyleSheet(f.read())


class Menu(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.frameWidth = self.frameSize().width()
        self.frameHeight = self.frameSize().height()

        with open("styles/menu_style.css", 'r') as f:
            self.setStyleSheet(f.read())

        self.initUI()
    def initUI(self):
        self.button_test = QPushButton(self)
        self.button_graph = QPushButton(self)
        self.button_login = QPushButton(self)
        self.button_register = QPushButton(self)
        self.head_label = QLabel(self)

        self.button_test.setText('Test')
        self.button_graph.setText('Statistics')
        self.button_login.setText('Login')
        self.button_register.setText('Register')
        self.head_label.setText('Typing Speed Test')
    
        self.button_test.clicked.connect(lambda: stacked.setCurrentIndex(1))
        self.button_graph.clicked.connect(lambda: stacked.setCurrentIndex(2))
        # self.button_graph.clicked.connect(Statistics().graph)
        self.button_login.clicked.connect(lambda: stacked.setCurrentIndex(3))
        self.button_register.clicked.connect(lambda: stacked.setCurrentIndex(4))
        # self.button_register.clicked.connect(self.logged_in)
        

        self.button_test.move(575, 300) 
        self.button_graph.move(575, 360)
        self.button_login.move(1170, 20)
        self.button_register.move(1170, 60)
        self.head_label.move(234, 150)

        self.button_test.setProperty('class', 'one')
        self.button_graph.setProperty('class', 'one')
        self.button_login.setProperty('class', 'two')
        self.button_register.setProperty('class', 'two')

        self.button_test.setFixedWidth(130)
        self.button_graph.setFixedWidth(130)
        self.button_login.setFixedWidth(90)
        self.button_register.setFixedWidth(90)

    def logged_in(self):
        print('logged in')
        self.button_login.setText(username)
        self.button_register.hide()
    

class TS_Test(QWidget):
    quit_thread = pyqtSignal()
    def __init__(self):
        QWidget.__init__(self)     

        with open("styles/test_style.css", 'r') as f:
            self.setStyleSheet(f.read())
        
        self.worker = Worker()
        self.worker_thread = QThread()
        self.worker.changed_signal.connect(self.difficulty)
        self.worker.float_signal.connect(self.update)
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker_thread.quit)
        self.quit_thread.connect(self.worker_thread.quit)
        self.worker_thread.started.connect(self.worker.change_difficulty)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30,30)
        self.button_back.setText('Back')

        global lineEdit, dropDown
        lineEdit = QLineEdit(self)
        self.label = QLabel(self)
        self.accuracy_label = QLabel(self)
        self.wpm_label = QLabel(self)
        self.cpm_label = QLabel(self)
        self.reset_button = QPushButton(self)

        dropDown = QComboBox(self)
        dropDown.addItems(['Easy','Medium','Hard'])
        dropDown.move(70,250)

        lineEdit.move(440, 260)
        self.wpm_label.move(575, 300)
        self.cpm_label.move(575, 330)
        self.accuracy_label.move(575, 360)
        self.reset_button.move(603, 410)

        self.label.setGeometry(440, 200, 400, 50)

        lineEdit.setFixedWidth(400)
        self.wpm_label.setFixedWidth(130)
        self.cpm_label.setFixedWidth(130)
        self.accuracy_label.setFixedWidth(130)

        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setText('Reset')

        self.label.setWordWrap(True)
                    
    def update(self, wpm_val, cpm_val, acc_val):
        self.wpm_label.setText(f'WPM: {wpm_val:0.3f}')
        self.cpm_label.setText(f'CPM: {cpm_val:0.3f}')
        data = [str(f'{wpm_val:0.3f}'), str(f'{cpm_val:0.3f}'), str(f'{acc_val:0.2f}')]
        if acc_val % 1 == 0:
            self.accuracy_label.setText(f'ACC: {int(acc_val)}%')
            data[2] = str(int(acc_val))
        else:
            self.accuracy_label.setText(f'ACC: {acc_val:0.2f}%')

        if username == '':
            print(1)
            with open('text_files/user_data/guest_data.txt', 'a') as f:
                f.write('\n'.join(data))
                f.write('\n')
        else:
            print(2)
            with open(f'text_files/user_data/{username}_data.txt', 'a') as f:
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
        # self.worker.stop()
        # self.worker_thread.quit()
        #self.worker.change_difficulty()
        #self.worker.run()
        # self.worker_thread.wait()
        # self.quit_thread.emit()
        Worker().skuska()
        print('stop')
        


class Worker(QObject):
    finished = pyqtSignal()
    changed_signal = pyqtSignal(int)
    float_signal = pyqtSignal(float, float, float)
    
    @pyqtSlot()
    def run(self):
        while True:
            print('important')         #?2
            print('importaant')
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
    #@classmethod
    def skuska(self):
        print('skuska')
        self.quit()
        self.finished.emit()


class Statistics(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        global wpm, cpm, acc, lenght

        wpm = []
        cpm = []
        acc = []
        lenght = []

        with open("styles/statistics_style.css", 'r') as f:
            self.setStyleSheet(f.read())
        
        self.initUI()        
        self.update_graph()
        

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

        # self.wpm_graph.plot(lenght, wpm)
        # self.cpm_graph.plot(lenght, cpm)
        # self.acc_graph.plot(lenght, acc)

        self.wpm_graph.setTitle('WPM')
        self.cpm_graph.setTitle('CPM')
        self.acc_graph.setTitle('ACC')

        self.stat_layout.setContentsMargins(150,10,50,10)
        self.setLayout(self.stat_layout)

    def update_graph(self):
        if username != '':
            with open(f'text_files/user_data/{username}_data.txt', 'r') as fi:
                self.wpm_graph.clear()
                self.cpm_graph.clear()
                self.acc_graph.clear()
                self.update(fi)
                     
        elif username == '':
            print('empty')
            with open(f'text_files/user_data/guest_data.txt', 'r') as fi:
                self.update(fi)

    def update(self, f):
        f = f.readlines()
        global wpm, cpm, acc, lenght
        wpm = []
        cpm = []
        acc = []
        lenght = []

        for i in range(1,len(f)//3+1):
            lenght.append(i)

        for i in range(0, len(f)+1, 3):
            if i != 0:
                wpm.insert(0,float(f[-(i)].strip('\n')))
        for i in range(2, len(f)+2, 3):
            cpm.insert(0,float(f[-(i)].strip('\n')))
        for i in range(1, len(f)+1, 3):
            acc.insert(0,float(f[-(i)].strip('\n')))
        print(wpm, cpm, acc, lenght)
        
        print(f'username: "{username}"')
        
        self.wpm_graph.plot(lenght, wpm)
        self.cpm_graph.plot(lenght, cpm)
        self.acc_graph.plot(lenght, acc)
        
            


class Login(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # global username
        # username = ''

        with open("styles/login&reg_style.css", 'r') as f:
            self.setStyleSheet(f.read())

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)  
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30, 30)
        self.button_back.setText('Back')

        self.username_label = QLabel(self)
        self.username_label.setText('Username')
        self.username_label.move(553, 200)

        self.username_entry = QLineEdit(self)
        self.username_entry.move(553, 225)
        self.username_entry.setFixedWidth(175)

        self.password_label = QLabel(self)
        self.password_label.setText('Password')
        self.password_label.move(553, 270)

        self.password_entry = QLineEdit(self)
        self.password_entry.move(553, 295)
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setFixedWidth(175)

        self.login_button = QPushButton(self)
        self.login_button.setText('Login')
        self.login_button.clicked.connect(self.login)
        #self.login_button.clicked.connect(Statistics.update_graph)
        self.login_button.move(602, 350)

        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Icon.Warning)
        self.msg_box.setWindowTitle('Warning')        
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def login(self):
        with open('text_files/user_info.txt', 'r') as f:
            f = f.read().split('\n')
        
            if self.username_entry.text() in f:
                if self.password_entry.text() == f[f.index(self.username_entry.text())+1]:
                    global username
                    username = self.username_entry.text()
                    print('login succesful')
                    print(username)
                    Statistics().update_graph()
                    Menu().logged_in()
                    stacked.setCurrentIndex(0)
                else:
                    self.msg_box.setText('Incorrect password')
                    self.msg_box.exec()
            else:
                self.msg_box.setText('Username does not exist')
                self.msg_box.exec()


class Register(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        with open("styles/login&reg_style.css", 'r') as f:
            self.setStyleSheet(f.read())

        self.initUI()

    def initUI(self):
        self.button_back = QPushButton(self)  
        self.button_back.clicked.connect(lambda: stacked.setCurrentIndex(0))
        self.button_back.move(30, 30)
        self.button_back.setText('Back')

        self.set_username_label = QLabel(self)
        self.set_username_label.setText('Username')
        self.set_username_label.move(553, 200)

        self.set_username_entry = QLineEdit(self)
        self.set_username_entry.move(553, 225)
        self.set_username_entry.setFixedWidth(175)

        self.set_password_label = QLabel(self)
        self.set_password_label.setText('Password')
        self.set_password_label.move(553, 270)

        self.set_password_entry = QLineEdit(self)
        self.set_password_entry.move(553, 295)
        self.set_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.set_password_entry.setFixedWidth(175)

        self.set_confirm_password_label = QLabel(self)
        self.set_confirm_password_label.setText('Confirmation Password')
        self.set_confirm_password_label.move(553, 340)

        self.set_confirm_password_entry = QLineEdit(self)
        self.set_confirm_password_entry.move(553, 365)
        self.set_confirm_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        #self.set_confirm_password_entry.editingFinished.connect(self.register)
        self.set_confirm_password_entry.setFixedWidth(175)

        self.register_button = QPushButton(self)
        self.register_button.setText('Register')
        self.register_button.clicked.connect(self.register)
        self.register_button.move(593, 420)

        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Icon.Warning)
        self.msg_box.setWindowTitle('Warning')        
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

    def register(self):
        with open('text_files/user_info.txt', 'r') as f_r:
            f_r = f_r.read().split('\n')
            if self.set_username_entry.text() != '' and self.set_password_entry.text() != '' and self.set_confirm_password_entry.text() != '':
                if (self.set_username_entry.text() not in f_r) and (self.set_password_entry.text() == self.set_confirm_password_entry.text()):
                    with open('text_files/user_info.txt', 'a') as f_a:
                        f_a.write(self.set_username_entry.text() + '\n' + self.set_password_entry.text() + '\n')
                    print('Done')
                elif self.set_username_entry.text() in f_r:
                    self.msg_box.setText('Username already exists')
                    self.msg_box.exec()
                elif self.set_password_entry.text() != self.set_confirm_password_entry.text():
                    self.msg_box.setText('Your password and confirmation password do not match')
                    self.msg_box.exec()
            else:
                self.msg_box.setText('Field can not be empty')
                self.msg_box.exec()
                   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec())



#TODO 1) Reset Button
#TODO 2) Update graph right after test is performed
#* IDEA: locknut dropDown ked lineEdit nie je prazdny
#?1 kod niekedy spracuje worker thread pomalsie a vyhodi to error, kvoli tomu tam je sleep na 0.5s 
#?2 bez tychto printov worker thread pada