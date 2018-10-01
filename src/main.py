from interface.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PipBoy")
    window = MainWindow()
    sys.exit(app.exec_())



