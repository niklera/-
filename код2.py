import sys
from PyQt5 import uic
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import random
import sqlite3
import datetime as dt


class GameElias(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sptop = [] #  список отгаданных слов
        self.spbottom = [] #  список не отгаданных слов
        self.slovo = '' #  переменная для контроля вывода(если оно пустое, то ничего не выводит)
        self.df1 = [1]  #  список отгадываемых слов
        self.arrows = ['стрелка вверх.png', 'стрелка вниз.png']  #  картинки
        self.timestart = ''  #  время начала игры
        self.timeend = ''  #  время конца игры

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_timer)


        self.timetime = 1
        self.game_timer = 60  #  количество секунд

        self.t = uic.loadUi("page3game.ui", self)
        self.menu()





    def menu(self):
        self.d = uic.loadUi("page1.ui", self)
        self.timetime = 1
        self.sptop = []
        self.spbottom = []
        self.slovo = ''
        self.df1 = [1]
        self.timetime = 1
        self.game_timer = 60
        self.d.newgame.clicked.connect(self.newgame1)
        self.d.rules.clicked.connect(self.rules1)
        self.d.history.clicked.connect(self.history11)




    def newgame1(self):
        self.r = uic.loadUi("page2rejim.ui", self)
        self.r.menu2.clicked.connect(self.menu)
        self.r.tobegin.clicked.connect(self.tobegin1)
        self.sptop = []
        self.spbottom = []

        con = sqlite3.connect("elias_table.sqlite")
        cur = con.cursor()

        self.r.easy.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id = 1").fetchall()]
        self.r.easy.toggled.connect(self.onClicked)
        self.r.easy.setChecked(True)

        self.r.hard.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id <= 3").fetchall()]
        self.r.hard.toggled.connect(self.onClicked)

        self.r.average.country = [num[1] for num in cur.execute(f"SELECT * FROM words WHERE id <= 2").fetchall()]
        self.r.average.toggled.connect(self.onClicked)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.df1 = radioButton.country

    def show_timer(self):

        if self.game_timer:
            self.game_timer -= 1
            self.t.timerrr.setText(f"{self.game_timer} секунд")
        else:
            self.gameend1()

    def tobegin1(self):
        self.t = uic.loadUi("page3game.ui", self)


        if self.timetime:
            self.timestart = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
            self.timer.start(1500)
            self.timetime = 0

        self.t.timerrr.setText(f"{self.game_timer} секунд")

        self.t.menu3.clicked.connect(self.menu)
        self.t.end.clicked.connect(self.gameend1)

        self.pix = QPixmap(self.arrows[0])
        self.top.setIcon(QIcon(self.pix))
        self.top.setIconSize(QSize(75, 75))
        self.t.top.clicked.connect(self.top12)

        self.pix1 = QPixmap(self.arrows[1])
        self.bottom.setIcon(QIcon(self.pix1))
        self.bottom.setIconSize(QSize(75, 75))
        self.t.bottom.clicked.connect(self.bottom11)


        if self.df1:
            self.randomslovo = random.choice(self.df1)
        if (set(self.sptop) == set(self.df1)) or (set(self.spbottom) == set(self.df1)):
            self.gameend1()

        while (self.randomslovo in self.sptop) or (self.randomslovo in self.spbottom):
            if self.df1 == []:
                self.gameend1()
                break
            if (set(self.sptop) == set(self.df1)) or (set(self.spbottom) == set(self.df1)):
                self.gameend1()
                break
            self.randomslovo = random.choice(self.df1)

        if self.randomslovo:
            self.t.knopka.setText(str(self.randomslovo))
            self.df1 = list(set(self.df1) - set([self.randomslovo, self.randomslovo]))
        else:
            self.gameend1()

        self.slovo = self.t.knopka.text()



    def bottom11(self):
        if self.slovo != '':
            self.spbottom.append(self.slovo)

        self.tobegin1()

    def top12(self):
        if self.slovo != '':
            self.sptop.append(self.slovo)

        self.tobegin1()


    def resultss1(self):
        self.con = sqlite3.connect("elias_table.sqlite")  # Подключение к БД
        self.cur = self.con.cursor()
        self.j = uic.loadUi("page4resulte.ui", self)
        self.texttop.append(' /'.join(self.sptop))
        self.textbottom.append(' /'.join(self.spbottom))
        self.cur.execute(f"INSERT INTO history (timestart, timeend, guessed, notguessed) VALUES('{self.timestart}', '{self.timeend}', '{' /'.join(self.sptop)}', '{' /'.join(self.spbottom)}')""")
        self.menu4.clicked.connect(self.menu)
        self.con.commit()

    def gameend1(self):
        self.timer.stop()
        self.timeend = str(dt.datetime.now().strftime("%d-%B-%y %H:%M:%S"))
        self.h = uic.loadUi("page6gameend.ui", self)
        self.h.menu6.clicked.connect(self.menu)
        self.h.end6.clicked.connect(self.resultss1)

    def history11(self):
        self.x = uic.loadUi("page7gamehistory.ui", self)
        self.con = sqlite3.connect("elias_table.sqlite")  # Подключение к БД
        self.cur = self.con.cursor()
        a = (self.cur.execute("""SELECT* FROM history""")).fetchall()

        if a:
            self.x.texthistory.setRowCount(len(a))
            self.x.texthistory.setColumnCount(len(a[0]))
            self.titles = [description[0] for description in self.cur.description]
            for i, elem in enumerate(a):
                for j, val in enumerate(elem):
                    self.x.texthistory.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}

        self.x.menu7.clicked.connect(self.menu)
        self.x.cleanhistory.clicked.connect(self.cleanhistory11)


    def cleanhistory11(self):
        self.cur.execute(f"DELETE FROM history""")
        self.con.commit()
        self.history11()


    def rules1(self):
        self.e = uic.loadUi("page5rules.ui", self)
        self.e.newgame.clicked.connect(self.newgame1)
        self.e.menu1.clicked.connect(self.menu)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameElias()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
