                                                                                                          # application to operate the photovoltaic panel with the use of a code reader and the ability to add new ones
                                                                                                          # panels and testing


from datetime import datetime
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
        self.insertDataTable.setColumnWidth(0,250)
        self.emptyTextLabel.setVisible(False)
        self.connectLabel.setVisible(False)
       
        self.comboBoxGetData()
        self.barCodeLine.textChanged.connect(self.newPanelForm)

        #self.comboBox.currentIndexChanged.connect(self.comboBoxUsing)
        self.datesComboBox.currentIndexChanged.connect(self.comboBoxGetData2)
            
        print(datetime.now())

        #x = keyboard.read_key()
        #print(x)

    #def comboBoxUsing(self):                                                                              # function to react after changing the tab 
    #    value = self.comboBox.currentText()
    #    print(value)

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
        
  
    def comboBoxGetData2(self):                                                                           # function for handling the comboBox - reads available names from the database
                                                                                                          # for comboBox - SEARCH 
        global value2                                                                                     # variables: value2 - current text on ComboBox ;  dataCount - counter for rows found in database
        global dataCount
        
        value2 = self.datesComboBox.currentText()
        if (value2 != "- select -") & (value2 != "0"):                                                    # comboBox support if the selected option changes
            table = self.table                                                                            # table - table which shows data from dataBase for BarCode 
            table.setVisible(True)
            table.setRowCount(dataCount)
            table.setColumnCount(2)                                                                       # data displayed in two columns (assumption)
            dataCount = 0
            for i in range(0, len(sheetsControl.link2)):                                                  # support for displaying and retrieving rows into a table
                if sheetsControl.link2[i] != None:
                    table.setItem(dataCount, 0, QTableWidgetItem(sheetsControl.record[i+1]))              # record -> heading 
                    table.setItem(dataCount, 1, QTableWidgetItem(sheetsControl.link2[i]))                 # link2 -> found data
                    dataCount = dataCount + 1
            dataSearch(value2)                                                                            # dataSearch() - function from sheetsControl.py - get vector with data from tests
            for j in range(2, len(sheetsControl.headingIndexValue)):                                      # support for displaying and retrieving rows into a table NEXT part 
                if sheetsControl.param[j] != None:
                    table.insertRow(table.rowCount())
                    table.setItem(dataCount, 0, QTableWidgetItem(sheetsControl.headingIndexValue[j]))     # headingIndexValue -> heading 
                    table.setItem(dataCount, 1, QTableWidgetItem(sheetsControl.param[j]))                 # param -> found data
                    dataCount = dataCount + 1
            
    def save(self):                                                                                       # function for checking whether the entered barcode is in the database, 
                                                                                                          # displaying its parameters or proposing to add a panel
        global value2 
        global dataCount
        

        temp = self.barCode.text()
        print("temp", temp)
        print("len", len(temp))
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
        self.insertDataTable.setItem(0,0, QTableWidgetItem(text))                                         # insert text to dataTable - first row - Serial No. - NEW BARCODE 

        
        
     


app = QtWidgets.QApplication(sys.argv)                                                                    # display app main window 
MainWindow = QtWidgets.QMainWindow()                                                                      
ui = main_ui(MainWindow)                                                                                  
                                                                                                          
MainWindow.show()                                                                                        
sys.exit(app.exec_())   
