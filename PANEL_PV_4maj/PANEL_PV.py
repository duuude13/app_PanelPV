                                                                                                          # application to operate the photovoltaic panel with the use of a code reader and the ability to add new ones
                                                                                                          # panels and testing


from datetime import datetime
import csv
import sheetsControl
import Main                                                                                               # Main.py -> Main.ui -> glowne okno aplikacji 
import not1

from sheetsControl import *
from Main import *                                                                                         
from not1 import *
from tk import *                                                                                          # Tkinter Library 
import keyboard

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
             
value = 0
value2 = "0"
dataCount = 0

class main_ui(Ui_MainWindow):                                                                             # Main class, MAIN WINDOW                                                                                                                                                                              # INIT 
   

    def __init__(self, window):                                                                           # INITIALIZATION 
        self.setupUi(window)
        
                                                                                                          # NEW PANEL
        
        self.info2.setVisible(False)
        self.table.setVisible(False)                                                                                                  
        self.okButton.clicked.connect(self.save)
       
        self.emptyTextLabel.setVisible(False)
        self.connectLabel.setVisible(False)
        self.notFillLabel.hide()
        self.testTable.setVisible(False)
      
       
        self.comboBoxGetData()
        self.barCodeLine.textChanged.connect(self.newPanelForm)
        self.referenceLabel.hide()
        self.testDataLabel.hide()


        #self.comboBox.currentIndexChanged.connect(self.comboBoxUsing)
        self.datesComboBox.currentIndexChanged.connect(self.comboBoxGetData2)
        self.startTestButton.clicked.connect(self.makeTest)  
        self.comboBox.currentIndexChanged.connect(self.comboBoxUsing)
        
        #x = keyboard.read_key()
        #print(x)

    def comboBoxUsing(self):                                                                             # function to react after changing the tab and FILL parameters from database
        value = self.comboBox.currentText()                                                              # get text of current tab on ComboBox --- comboBox - tab ADD NEW PANEL - 
        
        if value != "Other":                                                                            # if select exsisting panel barCode/serial No.  
            print("przepisz dane")
            cell = ws.find(value)                                                                       # get parameters from database 
            record = ws.row_values(1)                                                                   # get heading 
            if cell != None:
                barCodeID = ws.row_values(cell.row)                                                     
                print(barCodeID)
                print(record)
                self.serialNoLine.setText(barCodeID[1])
                self.vocLine.setText(barCodeID[2])
                self.iscLine.setText(barCodeID[3])
                self.pmLine.setText(barCodeID[4])
                self.vpmLine.setText(barCodeID[5])
                self.ipmLine.setText(barCodeID[6])
                self.ffLine.setText(barCodeID[7])
                        

    def comboBoxGetData(self):                                                                            # function for handling the comboBox - reads available names from the database
                                                                                                          # for comboBox - ADD PANEL FORM 
        global value
        global value2
        global dataCount
        
        self.comboBox.addItem("Other")
        serialNo()
        for i in range (1, len(sheetsControl.serial)):
            self.comboBox.addItem(sheetsControl.serial[i])

        value = self.comboBox.currentText()
        print(value)
        
    def comparisonData(self, refData, mesData):
        refData = float(refData)
        mesData = float(mesData)

        dev = format((refData - mesData) * 100 / refData , ".2f")
        print("dev",dev)

    def comboBoxGetData2(self):                                                                           # function for handling the comboBox - reads available names from the database
                                                                                                          # for comboBox - SEARCH 
        global value2                                                                                     # variables: value2 - current text on ComboBox ;  dataCount - counter for rows found in database
        global dataCount
        
        value2 = self.datesComboBox.currentText()
        if (value2 != "- select -") & (value2 != "0"):                                                    # comboBox support if the selected option changes
            table = self.table                                                                            # table - table which shows data from dataBase for BarCode 
            table.setVisible(True)
            self.referenceLabel.show()
            table.setRowCount(dataCount)
            table.setColumnCount(2)                                                                       # data displayed in two columns (assumption)
            dataCount = 0
            table.setHorizontalHeaderLabels(["Parameter", "Value"])
            for i in range(0, len(sheetsControl.link2)):                                                  # support for displaying and retrieving rows into a table
                if sheetsControl.link2[i] != None:
                    table.setItem(dataCount, 0, QTableWidgetItem(sheetsControl.record[i+1]))              # record -> heading 
                    table.setItem(dataCount, 1, QTableWidgetItem(sheetsControl.link2[i]))                 # link2 -> found data
                    dataCount = dataCount + 1
            dataSearch(value2)                                                                            # dataSearch() - function from sheetsControl.py - get vector with data from tests
            for j in range(2, len(sheetsControl.headingIndexValue)-1):                                      # support for displaying and retrieving rows into a table NEXT part 
                if sheetsControl.param[j] != None:
                    table.insertRow(table.rowCount())
                    table.setItem(dataCount, 0, QTableWidgetItem(sheetsControl.headingIndexValue[j]))     # headingIndexValue -> heading 
                    table.setItem(dataCount, 1, QTableWidgetItem(sheetsControl.param[j]))                 # param -> found data
                    dataCount = dataCount + 1
            
            csvFinder(value2)                                                                             # searching csv file -> chka sheet in database -> return global value (csvName)
            if sheetsControl.csvName != "":                                                               # if upper function found csv file enable 
                csvGet()                                                                                  # csvGet() -> GET DATA (U, I) -> function makes plot I(U) and P(U) using data from csv 
            self.testDataLabel.show()
            table2 = self.testTable                                                                       # table - table which shows data from dataBase for BarCode 
            table2.setVisible(True)
            table2.setColumnCount(3) 
            temp = 0
            for k in range(0, len(sheetsControl.data)):
                table2.insertRow(table2.rowCount())
                dev = (float(sheetsControl.link2[k+1]) - float(sheetsControl.data[k])) / float(sheetsControl.link2[k+1]) * 100  # dev - error -% difference from the reference value
               
                table2.setItem(temp, 0, QTableWidgetItem(sheetsControl.dataName[k]))                        # column 1 ---> parameter  
                table2.setItem(temp, 1, QTableWidgetItem(sheetsControl.data[k]))                            # column 2 ---> value 
                                                                                                            # column 3 ---> coverage of test parameters with reference data

                table2.setHorizontalHeaderLabels(["Parameter", "Value", ""])                                # set table's header 
                table2.setColumnWidth(2, 10)                                                                # 3rd column width
                item = QTableWidgetItem("")                                                                 # item = "" -> for 3rd column place
                if sheetsControl.statusTest == 1:
                    if dev <= 10:                                                                               # <= 10 % -> PASS
                        # green
                        item.setBackground(QColor(170, 255, 127))
                        table2.setItem(temp, 2, QTableWidgetItem(item))
                    elif dev <= 20:                                                                             # <= 20% -> WARNING                                                         
                        # orange 
                        item.setBackground(QColor(255, 170, 0))
                        table2.setItem(temp, 2, QTableWidgetItem(item))
                    else:                                                                                       # >20% -> FAIL
                        # red                   
                        item.setBackground(QColor(255, 52, 26))
                        table2.setItem(temp, 2, QTableWidgetItem(item))
                        
                temp = temp + 1
               
            
    

    def save(self):                                                                                       # function for checking whether the entered barcode is in the database, 
                                                                                                          # displaying its parameters or proposing to add a panel
        global value2 
        global dataCount
        
        temp = self.barCode.text()
        if len(temp) > 0:
            self.emptyTextLabel.setVisible(False)
            barCodeFinder(temp)                                                                               # barCodeFinder() - from sheetsControl.py - database handler function
        
            if (sheetsControl.link2[0] != "no data") & (sheetsControl.link2[0] != None):                      # display relevant data
                dataCount = 0
                for i in range(0, len(sheetsControl.link2)):                                                  # check the number of available parameters
                    if sheetsControl.link2[i] != None:
                        dataCount = dataCount + 1
                self.datesComboBox.addItem("- select -")                                                      # if data are available first element on comboBox is -select- 
                for j in range(8, len(sheetsControl.barCodeID)):
                    if sheetsControl.index[j-8] != "none":
                        self.datesComboBox.addItem(sheetsControl.barCodeID[j])
            else:
                self.window = Main.QtWidgets.QDialog()                                                        # dialog box asking if we want to add the panel to the database
                self.ui = Ui_Dialog()
                self.ui.setupUi(self.window)
                self.window.show()  
                self.ui.yesButton.clicked.connect(self.changeTab)                                             # yes -> transfer to form
        else:
            self.emptyTextLabel.setVisible(True)
            self.emptyTextLabel.setText("The field is empty")
           
    def changeTab(self):                                                                                  # function to change tab on TabWidget
        self.tabWidget.setCurrentWidget(self.addPanel)
  
        
    def newPanelForm(self):                                                                               # function for handling the form for adding a new panel
        text = self.barCodeLine.text()                                                                    # catching inserted text from barCodeLine 
        
    def makeTest(self):                                                                                     # makeTest -> function to start test -> create csv file with data from RasberryPie
        barCode = self.serialNoLine.text()
        voc = self.vocLine.text()
        isc = self.iscLine.text()
        pm = self.pmLine.text()
        vpm = self.vpmLine.text()
        ipm = self.ipmLine.text()
        ff = self.ffLine.text()

        if (barCode == "") | (voc == "") | (isc == "") | (pm == "") | (vpm == "") | (ipm == "") | (ff == ""):
            self.notFillLabel.show()
        else:
            panelData = [voc, isc, pm, vpm, ipm, ff]
            now = datetime.now()
            dateNow = now.strftime("%Y:%m:%d %H:%M:%S")
            self.testTimeLabel.setText(dateNow)
            saveDisk(barCode, dateNow, panelData)        
            

        
     


app = QtWidgets.QApplication(sys.argv)                                                                    # display app main window 
MainWindow = QtWidgets.QMainWindow()                                                                      
ui = main_ui(MainWindow)                                                                                  
                                                                                                          
MainWindow.show()                                                                                        
sys.exit(app.exec_())   
