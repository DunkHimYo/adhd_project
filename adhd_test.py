from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtTest import QTest
import sys
import random
import numpy as np
import os
import server
import atexit
import math
from multiprocessing import Process, Manager, freeze_support

freeze_support()

class Main(QtWidgets.QMainWindow):
    question_list = {'닭': 'chicken', '강아지': 'dog', '코끼리': 'elephant', '기린': 'giraffe', '돼지': 'pig', '토끼': 'rabbit'}

    def __init__(self):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self.label.setPixmap(QPixmap(r"./img/background_image/background.png"))
        self.device_allow=False
        self.repeat_cnt=0
        self.limit_repeat_cnt=10
        self.score=0

        self.play.clicked.connect(self._start)
        self.connect.clicked.connect(self._device_connect)

    def _start(self):
        if self.device_allow==True:
            rcv['method'] = 'record_start'
        current_page = Question(self)
        widget.addWidget(current_page)
        widget.setCurrentWidget(current_page)

    def _device_connect(self):
        self.device_allow=True
        rcv['method'] = 'emotiv_create'
        self.overlay = Overlay(self)
        self.overlay.show()
        del self.overlay


class Question(QtWidgets.QMainWindow):
    qtm=[]
    def __init__(self, main_class):
        super().__init__()
        uic.loadUi('./ui/Question.ui', self)
        self.main=main_class
        self.main.answer = random.choice(tuple(self.main.question_list.keys()))
        self.Question_title.setText(f' {self.main.answer}의 개수를 고르세요')
        self._timer_start()

    def _timer_start(self):
        self.my_qtimer = QTimer(self)
        self.my_qtimer.timeout.connect(self._timer_timeout)
        self.my_qtimer.start(2000)
        self.qtm.append(self.my_qtimer)

    def _timer_timeout(self):
        current_page = Game(self.main)
        widget.addWidget(current_page)
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentWidget(current_page)
        self.my_qtimer.stop()



class Game(QtWidgets.QMainWindow):
    img_path = 'img/animal_image'
    animal_path = os.listdir(img_path)

    def __init__(self, main_class):
        super().__init__()
        uic.loadUi('./ui/game.ui', self)
        self.main=main_class
        self.image_layout()

    def image_layout(self):
        self.main.animal_cnt = 0
        self.main.repeat_cnt+=1

        self.image_count = random.randint(5, 16)
        for i in range(1, random.randint(5, self.image_count) + 1, 1):
            random_animal_img_path = random.choice(self.animal_path)
            if random_animal_img_path[:-4].lower() == self.main.question_list[self.main.answer]:
                self.main.animal_cnt += 1
            img = QPixmap(self.img_path + '/' + random_animal_img_path).scaledToWidth(200)
            getattr(self, f'img_{i}').setPixmap(img)

        self.operator_1.setPixmap(QPixmap(r"./img/operator_image/plus2.png").scaledToWidth(60))
        while True:
            select_answer = [self.main.animal_cnt + random.randint(1, 5) - random.randint(1, 5) for _ in range(2)]

            select_answer.append(self.main.animal_cnt)
            select_answer = np.array(select_answer)
            if len(select_answer) == len(set(select_answer)) and len(select_answer[select_answer < 0]) == 0:
                break;
        random.shuffle(select_answer)

        for idx, answer in enumerate(select_answer, start=1):
            getattr(self, f'checkBox_{idx}').setText(f'{answer} 마리')


        self.checkBox_1.clicked.connect(self._chkBox1)
        self.checkBox_2.clicked.connect(self._chkBox2)
        self.checkBox_3.clicked.connect(self._chkBox3)

    def _chkBox1(self):
        if int(self.checkBox_1.text()[:-3])==self.main.animal_cnt:
            self.main.score+=1
        self._next_question()

    def _chkBox2(self):
        if int(self.checkBox_2.text()[:-3])==self.main.animal_cnt:
            self.main.score+=1
        self._next_question()

    def _chkBox3(self):
        if int(self.checkBox_3.text()[:-3])==self.main.animal_cnt:
            self.main.score+=1
        self._next_question()

    def _next_question(self):
        if self.main.repeat_cnt<self.main.limit_repeat_cnt:

            current_page = Question(self.main)
            widget.addWidget(current_page)
            widget.removeWidget(widget.currentWidget())
            widget.setCurrentWidget(current_page)
        else:
            if self.main.device_allow == True:
                rcv['method'] = 'record_stop'
                QTest.qWait(100)
                rcv['method']='adhd_result'

                self.overlay = Overlay(self)
                self.overlay.show()

                while not rcv['loading_chk']:
                    QTest.qWait(1)
                else:
                    current_page = Finish(self.main)
                    widget.addWidget(current_page)
                    widget.removeWidget(widget.currentWidget())
                    widget.setCurrentWidget(current_page)

class Finish(QtWidgets.QMainWindow):

    def __init__(self, main_class):
        super().__init__()
        uic.loadUi('./ui/finish.ui', self)
        self.main=main_class
        self.home.clicked.connect(self._home)
        self.restart.clicked.connect(self._restart)
        self.adhd_score.setText(f'총 수치는 {np.mean(rcv["adhd_result"]) * 100:.0f} 입니다.')


    def _home(self):
        widget.removeWidget(widget.currentWidget())
        widget.setCurrentWidget(self.main)
        self._refresh()

    def _restart(self):
        widget.removeWidget(widget.currentWidget())
        self.main._start()
        self._refresh()

    def _refresh(self):
        self.main.repeat_cnt = 0
        self.main.score = 0


class Overlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.resize(200,200)
        self.move(self.width()*4, self.height()*2)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(14):
            if (self.counter / 5) % 14 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5) * 32, 0, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width() / 2 + 50 * math.cos(2 * math.pi * i / 14.0) - 5,
                self.height() / 2 + 50 * math.sin(2 * math.pi * i / 14.0) - 10,
                10, 10)
        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(30)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()

        if rcv['loading_chk']:
            rcv['loading_chk']=False
            self.killTimer(self.timer)
            self.hide()

def program_exit(process:list):
    for p in process:
        p.kill()

if __name__ == '__main__':

    manager=Manager()

    rcv = manager.dict()
    rcv['method'] = None
    rcv['loading_chk'] = False

    p = Process(target=server.get_eeg_data, args=(rcv,))
    p.start()
    atexit.register(program_exit, [p])

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(Main())
    widget.showMaximized()
    app.exec_()

