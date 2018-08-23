import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.editor = QPlainTextEdit()
        self.numberColumn = NumberColumn(self.editor)

        layout = QHBoxLayout()
        layout.addWidget(self.numberColumn)
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setWindowTitle("Pip-Boy")
        self.show()


class NumberColumn(QWidget):
    def __init__(self, parent=None, index=1):
        super(NumberColumn, self).__init__(parent)
        self.editor = parent
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')
        self.index = index

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 28
        if self.width() != width:
            self.setFixedWidth(width)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PipBoy")

    window = MainWindow()
    # sys.exit(app.exec_())
    app.exec_()
