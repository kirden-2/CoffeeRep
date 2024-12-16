import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QTableWidgetItem
from PyQt6.QtWidgets import QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.updateButton.clicked.connect(self.show_table)
        self.addButton.clicked.connect(self.add_coffee_func)
        self.editButton.clicked.connect(self.edit_coffee_func)
        self.show_table()

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

    def add_coffee_func(self):
        self.add_coffee = SecondWindow(parent=self)
        self.add_coffee.show()

    def edit_coffee_func(self):
        if self.tableWidget.currentRow() != -1:
            self.edit_coffee = SecondWindow(parent=self,
                                            coffee_id=self.tableWidget.item(self.tableWidget.currentRow(),
                                                                            0).text())
            self.edit_coffee.show()
        else:
            self.statusBar().showMessage('Ничего не выбрано')


class SecondWindow(QMainWindow):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.coffee_id = coffee_id
        if self.coffee_id is None:
            self.pushButton.setText('Добавить')
        else:
            self.pushButton.setText('Редактировать')
            self.get_elem()
        self.pushButton.clicked.connect(self.get_verdict)

    def get_elem(self):
        row = self.parent().tableWidget.currentRow()
        data = [self.parent().tableWidget.item(row, column).text()
                if self.parent().tableWidget.item(row, column).text() else ''
                for column in range(self.parent().tableWidget.columnCount())]

        self.name.setText(str(data[1]))
        self.roast_level.setText(str(data[2]))
        self.type.setText(str(data[3]))
        self.taste.setText(str(data[4]))
        self.price.setText(str(data[5]))
        self.volume.setText(str(data[6]))

    def get_verdict(self):
        if (self.name.text() and self.roast_level.text() and self.type.text()
                and self.price.text().isdigit() and self.volume.text().isdigit()):
            if self.coffee_id is None:
                self.add_coofe_secondWindow()
            else:
                self.edit_coofe_secondWindow()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def add_coofe_secondWindow(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('''INSERT INTO coffee (name,roast_level,type,taste,price,volume)
                        VALUES (?,?,?,?,?,?)''', (self.name.text(),
                                                  self.roast_level.text(),
                                                  self.type.text(),
                                                  self.taste.text(),
                                                  int(self.price.text()),
                                                  int(self.volume.text())))
        con.commit()
        cur.close()
        self.close()

    def edit_coofe_secondWindow(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('''REPLACE INTO coffee
        (id, name,roast_level,type,taste,price,volume) VALUES (?,?,?,?,?,?,?)''',
                    (self.coffee_id,
                     self.name.text(),
                     self.roast_level.text(),
                     self.type.text(),
                     self.taste.text(),
                     int(self.price.text()),
                     int(self.volume.text())))

        con.commit()
        cur.close()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
