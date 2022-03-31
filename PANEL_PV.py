                                                                                                          # aplikacja do obslugi panelu fotowoltaiczego z wykorzystaniem czytnika kodow oraz mozliwoscia dodawania nowych 
                                                                                                          # paneli oraz wykonywania badan 

import arkuszkalkulacyjny
from arkuszkalkulacyjny import *
from Main import *                                                                                        # Glowny template UI 
from formularz import Ui_Dialog
from form import *
from tk import *                                                                                          # Tkinter Library 

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
             
sprawdz = 2 

class Window(QMainWindow):
        """Main window."""
        def __init__(self, parent=None):
            """Initializer."""
            super().__init__(parent)
            # Use a QPushButton for the central widget
            self.centralWidget = QPushButton("Dodaj nowy panel")
            # Connect the .clicked() signal with the .onEmployeeBtnClicked() slot
            self.centralWidget.clicked.connect(self.onEmployeeBtnClicked)
            self.setCentralWidget(self.centralWidget)

        def onEmployeeBtnClicked(self):
            dlg = EmployeeDlg(self)
            dlg.exec()

class EmployeeDlg(QDialog):
        """Employee dialog."""
        def __init__(self, parent=None):
            super().__init__(parent)
            # Create an instance of the GUI
            self.ui = Ui_Dialog()
            # Run the .setupUi() method to show the GUI
            self.ui.setupUi(self)


class main_ui(Ui_MainWindow):                                                                             # Main class, MAIN WINDOW                                                                                                                                                                              # INIT 
    def __init__(self, window):
        self.setupUi(window)
        
                                                                                                          # ukrycie wszystkich dostepnych obiektow 
        self.label1.setVisible(False)
        self.label.setVisible(False)
        self.barCode.setVisible(False)
        self.okButton.setVisible(False)
        self.pushButton.setVisible(False)

        self.serialNo.setVisible(False)
        self.serialNoValue.setVisible(False)
        self.Voc.setVisible(False)
        self.VocValue.setVisible(False)
        self.Isc.setVisible(False)
        self.IscValue.setVisible(False)  
        self.Pm.setVisible(False)
        self.PmValue.setVisible(False)
        self.Vpm.setVisible(False)
        self.VpmValue.setVisible(False)
        self.Ipm.setVisible(False)
        self.IpmValue.setVisible(False)
        self.FF.setVisible(False)
        self.FFvalue.setVisible(False)
        
                                                                                                          # dzialania przyciskow SKANUJ i SZUKAJ 
                                                                                                          # uruchomienie funkcji odpowiedzialnych za ich realizacje
        self.skanujButton.clicked.connect(self.clickSkanuj)
        self.szukajButton.clicked.connect(self.clickSzukaj)

        if self.nowyPanelButton.clicked:
            global sprawdz
            sprawdz = 1
            
        
                                                                                                         
        #self.zamknijButton.clicked.connect(QtCore.QCoreApplication.instance().quit)                      # dzialania przycisku ZAMKNIJ - zamkniecie calej aplikacji 
        
                                                                                                          # funkcja do przesy�ania link�w do google sheets na podstawie znalezionego kodu kreskowego
																				                          # funkcja zlicza ilo�� dost�pnych danych 

                                                                                                          # funkcja SKANOWANIA 
                                                                                                          # pozwala na zeskanowanie kodu kreskowego czytnikiem oraz potwierdzenie operacji 
    
        
       

    def clickSkanuj(self):
        skanInfo = "Zeskanuj kod kreskowy panelu"                                                         # komunikat 
        puste = ""                                                                                        # odkrycie pol przeznaczonych do skanowania 

        self.label1.setVisible(True)
        self.barCode.setVisible(True)
        self.okButton.setVisible(True)
        self.pushButton.setVisible(True)
        self.label.setVisible(False)
        self.ukryjPole()
                                                                                                          
        self.label1.setText(skanInfo)                                                                     # zmiana wyswiatlajacego sie komunikatu na zgodny z wykonywana funkcja
        self.barCode.setText(puste)                                                                                  # wyczyszczenie pola do wpisywania kodu 
        self.okButton.clicked.connect(self.zapiszKod)                                                     # wyszukanie kodu -> czesc wykonawcza tego bloku 
        self.pushButton.clicked.connect(self.wyczyscPole)
        
                                                                                                          # funkcja SZUKAJ - wyszukanie panelu poprzez wpisanie kodu kreskowego
    def clickSzukaj(self):
        szukajInfo = "Wpisz kod panelu"                                                                   # komunikat 
        puste = ""                                                                                        # odkrycie pol przeznaczonych do skanowania
        
        self.label1.setVisible(True)
        self.barCode.setVisible(True)
        self.okButton.setVisible(True)
        self.pushButton.setVisible(True)
        self.label.setVisible(False)
        self.ukryjPole()
        

        self.label1.setText(szukajInfo)                                                                   # zmiana wyswiatlajacego sie komunikatu na zgodny z wykonywana funkcja
        self.barCode.setText(puste)
                                                                                                          # wyczyszczenie pola do wpisywania kodu 

                                                                                                          # funkcja ZAPISANIA KODU ktory zostal wpisany/zeskanowany
                                                                                                          # wykorystane: barCodeFinder() - wyszukiwanie kodu wsrod kodow 
                                                                                                          # zpaisanych w bazie Google Sheet dostepnego na dysku Google
    
    def zapiszKod(self, zmienna):
        zmienna = self.barCode.toPlainText()                                                              # pobranie wpisanego kodu
        
        barCodeFinder(zmienna)  
        self.label.setVisible(True)                                                                       # wyswietlenie pola z kodem kreskowym
        
       
        self.label.setText(arkuszkalkulacyjny.link2[0])
        self.panelParametry()

    def wyczyscPole(self):                                              
        self.barCode.setText("")

    def panelParametry(self):                                                                             # funkcja obslugujaca wyswietlania parametrow panelu znalezionego w bazie 
        if arkuszkalkulacyjny.link2[1] != 0:
            self.serialNo.setVisible(True)
            self.serialNoValue.setVisible(True)
            self.Voc.setVisible(True)
            self.VocValue.setVisible(True)
            self.Isc.setVisible(True)
            self.IscValue.setVisible(True)  
            self.Pm.setVisible(True)
            self.PmValue.setVisible(True)
            self.Vpm.setVisible(True)
            self.VpmValue.setVisible(True)
            self.Ipm.setVisible(True)
            self.IpmValue.setVisible(True)
            self.FF.setVisible(True)
            self.FFvalue.setVisible(True)
            self.serialNo.setText("Serial Number ")
            self.Voc.setText("Voc ")
            self.Isc.setText("Isc ")
            self.Pm.setText("Pm ")
            self.Vpm.setText("Vpm ")
            self.Ipm.setText("Ipm ")
            self.FF.setText("FF ")
            self.serialNoValue.setText(arkuszkalkulacyjny.link2[0])
            self.VocValue.setText(arkuszkalkulacyjny.link2[1])
            self.IscValue.setText(arkuszkalkulacyjny.link2[2])
            self.PmValue.setText(arkuszkalkulacyjny.link2[3])
            self.VpmValue.setText(arkuszkalkulacyjny.link2[4])
            self.IpmValue.setText(arkuszkalkulacyjny.link2[5])
            self.FFvalue.setText(arkuszkalkulacyjny.link2[6])
        else:
            self.ukryjPole()

    def ukryjPole(self):                                                                                  # funkcja do ukrywania tabeli z parametrami panelu 
        self.serialNo.setVisible(False)
        self.serialNoValue.setVisible(False)
        self.Voc.setVisible(False)
        self.VocValue.setVisible(False)
        self.Isc.setVisible(False)
        self.IscValue.setVisible(False)  
        self.Pm.setVisible(False)
        self.PmValue.setVisible(False)
        self.Vpm.setVisible(False)
        self.VpmValue.setVisible(False)
        self.Ipm.setVisible(False)
        self.IpmValue.setVisible(False)
        self.FF.setVisible(False)
        self.FFvalue.setVisible(False)
                                                                                                          # zamkniecie okna aplikacji 
app = QtWidgets.QApplication(sys.argv)                                                                    # wyswietlenie okna aplikacji
MainWindow = QtWidgets.QMainWindow()                                                                      
ui = main_ui(MainWindow)                                                                                  
                                                                                                          
MainWindow.show()                                                                                        
sys.exit(app.exec_())   

#if __name__ == "__main__":
#        # Create the application
#        app = QApplication(sys.argv)
#        # Create and show the application's main window
#        win = Window()
#        win.show()
#        # Run the application's main loop
#        sys.exit(app.exec())
