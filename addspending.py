from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3, style, globalvariable

con = sqlite3.connect("money.db")
cur = con.cursor()

class AddSpending(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(350,200,350,550)
        self.setFont(QFont("Times", 13))
        self.setStyleSheet("background-color:red; color:white;") 
        self.setWindowTitle('Add Spending')
        self.setWindowIcon(QIcon('icons/coin.png'))
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.addSpendingTitle = QLabel("ADD SPENDING")
        self.addSpendingTitle.setFont(QFont("Times", 18))
        self.addSpendingTitle.setAlignment(Qt.AlignCenter)

        self.addSpendingImg = QLabel()
        currencypixmap = QPixmap('icons/buy.png')
        self.addSpendingImg.setPixmap(currencypixmap)
        self.addSpendingImg.setAlignment(Qt.AlignCenter)
        self.addSpendingImg.setContentsMargins(0,50,0,0) #(left, top, right, bottom)

        self.amountEntry = QLineEdit()
        self.amountEntry.setPlaceholderText("Price...")
        self.amountEntry.setContentsMargins(20,0,20,0)
        self.amountEntry.setStyleSheet("color:white; font-size:15pt;")
        self.activityEntry = QLineEdit()
        self.activityEntry.setPlaceholderText("What...")
        self.activityEntry.setContentsMargins(20,0,20,20)
        self.activityEntry.setStyleSheet("color:white; font-size:15pt;")

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet(style.addSpendingSubmitBtn())
        self.submitBtn.clicked.connect(self.addSpending)

        self.chooseCategoryLabel = QLabel("CHOOSE CATEGORY")
        self.chooseCategoryLabel.setAlignment(Qt.AlignCenter)
        self.chooseCategory = QComboBox()
        self.chooseCategory.addItems(["household expenses", "public transport", "clothes", "food", "gadgets", "car", "economy"])

    def layouts(self):
        self.addSpendingMainLayout = QVBoxLayout()
        self.addSpendingForm = QVBoxLayout()

        self.addSpendingMainLayout.addWidget(self.addSpendingTitle)
        self.addSpendingMainLayout.addWidget(self.addSpendingImg)
        self.addSpendingMainLayout.addStretch()

        self.addSpendingForm.addWidget(self.amountEntry)
        self.addSpendingForm.addWidget(self.activityEntry)
        self.addSpendingForm.addWidget(self.chooseCategoryLabel)
        self.addSpendingForm.addWidget(self.chooseCategory)
        self.addSpendingMainLayout.addLayout(self.addSpendingForm)
        self.addSpendingForm.setAlignment(Qt.AlignCenter)

        self.addSpendingMainLayout.addWidget(self.submitBtn)

        self.setLayout(self.addSpendingMainLayout)

    def addSpending(self):
        amount = self.amountEntry.text()
        name = self.activityEntry.text()
        category = self.chooseCategory.currentText()

        if float(amount) <= (globalvariable.salary - globalvariable.spend):
            globalvariable.homespending = 0.0
            globalvariable.busspending = 0.0
            globalvariable.clothesspending = 0.0
            globalvariable.eatspending = 0.0
            globalvariable.phonespending = 0.0
            globalvariable.carspending = 0.0
            globalvariable.economy = 0.0
            if category == "household expenses":
                globalvariable.homespending += float(amount)
            elif category == "public transport":
                globalvariable.busspending += float(amount)
            elif category == "clothes":
                globalvariable.clothesspending += float(amount)
            elif category == "food":
                globalvariable.eatspending += float(amount)
            elif category == "gadgets":
                globalvariable.phonespending += float(amount)
            elif category == "car":
                globalvariable.carspending += float(amount)
            elif category == "economy":
                globalvariable.economy += float(amount)

            if (name and amount != ""):
                try:
                    query1 = "INSERT INTO 'spending' (spendingamount, spendingname, spendingcategory) VALUES(?,?,?)"
                    cur.execute(query1, (amount, name, category))
                    con.commit()

                    query2 = "INSERT INTO 'spendingcategories' (homespending, busspending, clothesspending, eatspending, phonespending, carspending, economy) VALUES(?,?,?,?,?,?,?)"
                    cur.execute(query2, (globalvariable.homespending, globalvariable.busspending, globalvariable.clothesspending, globalvariable.eatspending, globalvariable.phonespending, globalvariable.carspending, globalvariable.economy))
                    con.commit()
                    QMessageBox.information(self,"Warning","Spend has been added to data base!")
                    self.close()
                except:
                    QMessageBox.information(self,"Warning","Spend has not been added to data base!")

            else:
                QMessageBox.information(self,"Warning","Fields cannot be empty!")
        else:
            QMessageBox.information(self,"Warning","You do not have as much money!")