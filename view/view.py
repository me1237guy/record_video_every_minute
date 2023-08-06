import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Signal, Slot
# 1. Ui_MainWindow is created by using qt designer and which is saved as main.ui
# 2. Use the following command to convert main.ui file to a single python script file (main_ui.py)  
#    pyside6-uic main.ui > main_ui.py
# 3. import UI_MainWindow from main_ui.py  
from  view.main_ui import Ui_MainWindow

class View(QMainWindow):  
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  
        
        # Set minimum size of the main window
        min_width = 400
        min_height = 300
        self.setMinimumSize(min_width, min_height)

        # Set maximum size of the main window
        max_width = 2560
        max_height = 1060        
        self.setMaximumSize(max_width, max_height)

        self.showMaximized()
        # self.show()
        

