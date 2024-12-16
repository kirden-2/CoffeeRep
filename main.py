import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QTableWidgetItem
from PyQt6.QtWidgets import QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.pushButton.clicked.connect(self.show_table)

    def show_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()

        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()

        titles = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                  'объем упаковки']
        self.tableWidget.setColumnCount(len(titles))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.setRowCount(0)
        i = 0
        for row in result:
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j in range(len(row)):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(row[j])))
            i += 1
        self.tableWidget.resizeColumnsToContents()
        cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
