# from lexical.lexicalanayzer import LexicalAnalyzer
from interface.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    # analyzer = LexicalAnalyzer()
    # f = open('lms.txt', 'r')
    # analyzer.run(f.read())
    mainWindow = MainWindow()
    app = QApplication()
    sys.exit(app.exec_())
