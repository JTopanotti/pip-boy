# from lexical.lexicalanayzer import LexicalAnalyzer
import sys

from interface.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    # analyzer = LexicalAnalyzer()
    # f = open('lms.txt', 'r')
    # analyzer.run(f.read())
    app = QApplication(sys.argv)
    app.setApplicationName("PipBoy")
    window = MainWindow()
    sys.exit(app.exec_())
