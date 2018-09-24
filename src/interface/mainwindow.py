from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, \
    QHBoxLayout, QApplication, QTableWidget, QTableWidgetItem, QAction

from analyzers.lexicalanalyzer import LexicalAnalyzer

lineBarColor = QColor(255, 255, 255)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.width = 150
        self.height = 400
        self.setWindowIcon(QIcon('resources/pip-boy.png'))

        self.menu = self.menuBar()
        self.compile_act = QAction('Compile')
        self.clear_act = QAction('Clear Table')
        self.compile_act.triggered.connect(self.compile)
        self.clear_act.triggered.connect(self.clear_table)
        self.menu.addAction(self.compile_act)
        self.menu.addAction(self.clear_act)
        self.lexicalAnalyzer = LexicalAnalyzer()
        self.syntaxicalAnalyzer = SyntaxicalAnalyzer()

        self.editor = QPlainTextEdit()
        self.editor.setFixedWidth(400)
        self.numberColumn = NumberColumn(self.editor)
        self.automatonTable = QTableWidget()
        self.automatonTable.setColumnCount(2)
        header = self.automatonTable.horizontalHeader()
        header.setSectionResizeMode(0,  QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.automatonTable.setHorizontalHeaderLabels(['Id', 'Palavra'])


        layout = QHBoxLayout()
        layout.addWidget(self.numberColumn)
        layout.addWidget(self.editor)
        layout.addWidget(self.automatonTable)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setWindowTitle("Pip-Boy")
        self.show()

    def compile(self):
        tokens = self.lexicalAnalyzer.run(self.editor.toPlainText())
        for token in tokens:
            row_count = self.automatonTable.rowCount()
            self.automatonTable.insertRow(row_count)
            self.automatonTable.setItem(row_count, 0, QTableWidgetItem(str(token.identifier)))
            self.automatonTable.setItem(row_count, 1, QTableWidgetItem(str(token.value)))

        self.syntaxicalAnalyzer.run(tokens)

    def clear_table(self):
        row_count = self.automatonTable.rowCount()
        while row_count > -1:
            self.automatonTable.removeRow(row_count)
            row_count -= 1

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

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), lineBarColor)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)

            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            while block.isValid():
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1
                rect = QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i' % number)

                if block_top > event.rect().bottom():
                    break

                block = block.next()

            painter.end()
