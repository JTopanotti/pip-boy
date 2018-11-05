from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, \
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QAction, QLabel

from analyzers.lexicalanalyzer import LexicalAnalyzer
from analyzers.syntaxicalanalyzer import SyntaxicalAnalyzer

from models.terminals import terminals
from models.nonterminals import non_terminals

lineBarColor = QColor(255, 255, 255)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.width = 150
        self.height = 400
        self.setWindowIcon(QIcon('resources/pip-boy.png'))

        self.menu = self.menuBar()
        self.compile_act = QAction('Compile')
        self.clear_act = QAction('Clear Tables')
        self.new_derivation_act = QAction('Derivation')
        self.proceed_act = QAction('Next')
        self.process_act = QAction('Process Syntax')
        self.compile_act.triggered.connect(self.compile)
        self.clear_act.triggered.connect(self.clear_tables)
        self.proceed_act.triggered.connect(self.proceed)
        self.new_derivation_act.triggered.connect(self.new_derivation)
        self.process_act.triggered.connect(self.process)
        self.menu.addAction(self.compile_act)
        self.menu.addAction(self.clear_act)
        self.menu.addAction(self.process_act)
        self.menu.addAction(self.proceed_act)
        self.lexical_analyzer = LexicalAnalyzer()
        self.syntaxical_analyzer = SyntaxicalAnalyzer()
        self.syntaxical_analyzer.register_action(self.new_derivation_act)

        self.editor = QPlainTextEdit()
        self.editor.setFixedWidth(400)
        self.numberColumn = NumberColumn(self.editor)
        self.automaton_table = QTableWidget()
        self.automaton_table.setColumnCount(2)
        automaton_table_header = self.automaton_table.horizontalHeader()
        automaton_table_header.setSectionResizeMode(0,  QtWidgets.QHeaderView.ResizeToContents)
        automaton_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.automaton_table.setHorizontalHeaderLabels(['Id', 'Palavra'])

        self.derivation_table = QTableWidget()
        self.derivation_table.setColumnCount(2)
        derivation_table_header = self.derivation_table.horizontalHeader()
        derivation_table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        derivation_table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.derivation_table.setHorizontalHeaderLabels(['Id', 'Simbolo'])

        layout_vertical = QVBoxLayout()
        self.process_dislpay = QLabel()
        layout_vertical.addWidget(self.process_dislpay)
        layout_vertical.addWidget(self.automaton_table)
        layout_vertical.addWidget(self.derivation_table)

        layout = QHBoxLayout()
        layout.addWidget(self.numberColumn)
        layout.addWidget(self.editor)
        layout.addLayout(layout_vertical)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.setWindowTitle("Pip-Boy")
        self.show()

    def compile(self):
        tokens = self.lexical_analyzer.run(self.editor.toPlainText())
        if isinstance(tokens, str):
            self.process_dislpay.setText("Erro: " + tokens)
        else:
            for token in tokens:
                row_count = self.automaton_table.rowCount()
                self.automaton_table.insertRow(row_count)
                self.automaton_table.setItem(row_count, 0, QTableWidgetItem(str(token.identifier)))
                self.automaton_table.setItem(row_count, 1, QTableWidgetItem(str(token.value)))

            self.syntaxical_analyzer.run(tokens)

    def clear_table(self, table_name):
        table = self.automaton_table if table_name == "automaton_table" else self.derivation_table
        row_count = table.rowCount()
        while row_count > -1:
            table.removeRow(row_count)
            row_count -= 1

    def clear_tables(self):
        self.clear_table("automaton_table")
        self.clear_table("derivation_table")

        self.syntaxical_analyzer.clear_cache()

    def proceed(self):
        try:
            if self.syntaxical_analyzer:
                self.syntaxical_analyzer.proceed()
        except Exception as err:
            self.process_dislpay.setText("Erro: {}".format(err))



    def process(self):
        try:
            if self.syntaxical_analyzer:
                self.syntaxical_analyzer.process_syntax_whole()
        except Exception as err:
            self.process_dislpay.setText("Erro: {}".format(err))

    def new_derivation(self):
        self.process_dislpay.setText(self.syntaxical_analyzer.current_derivation)

        self.clear_table("derivation_table")
        self.clear_table("automaton_table")

        if self.syntaxical_analyzer.expansions:
            for expansion in self.syntaxical_analyzer.expansions:
                row_count = self.derivation_table.rowCount()
                self.derivation_table.insertRow(row_count)
                self.derivation_table.setItem(row_count, 0, QTableWidgetItem(str(expansion)))
                if expansion in terminals:
                    self.derivation_table.setItem(row_count, 1, QTableWidgetItem(str(terminals[expansion])))
                else:
                    self.derivation_table.setItem(row_count, 1, QTableWidgetItem(str(non_terminals[expansion])))

        if self.syntaxical_analyzer.input:
            for input_token in self.syntaxical_analyzer.input:
                row_count = self.automaton_table.rowCount()
                self.automaton_table.insertRow(row_count)
                self.automaton_table.setItem(row_count, 0, QTableWidgetItem(str(input_token.identifier)))
                self.automaton_table.setItem(row_count, 1, QTableWidgetItem(str(input_token.value)))


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
