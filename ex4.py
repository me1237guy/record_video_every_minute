from PySide6 import QtWidgets
from controller.controller import Controller
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    
    # controller.ini_process_frame()
    sys.exit(app.exec())