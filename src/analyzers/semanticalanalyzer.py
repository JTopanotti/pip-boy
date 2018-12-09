from models.symbol import Symbol
from models.semanticflags import semanticdeclarations
from models.semanticflags import semantictypes


class Semantical2:

    def __init__(self):
        self.symbol_table = []
        self.input = []
        self.scope = 0

    def declaration_handler(self):
        self.clear_scope()

        var_table = []
        category = self.input[0].identifier
        isparam = False
        self.input.pop(0)

        while self.input[0].identifier not in semanticdeclarations and self.input[0].identifier != 6:
            if self.input[0].identifier in semantictypes:
                if self.input[0].identifier == 9:
                    for var in var_table:
                        var.type = 9
                        self.include(var)
                    while self.input[0].identifier not in semantictypes:
                        self.input.pop(0)
                    self.input.pop(0)
                elif self.input[0].identifier == 8:
                    for var in var_table:
                        var.type = 8
                        self.include(var)
                var_table.clear()
            if self.input[0].identifier == 25:
                symbol = Symbol()
                symbol.scope = self.input[0].scope
                symbol.name = self.input[0].value
                symbol.line = self.input[0].line
                if category in [2, 3]:
                    symbol.category = category
                    self.include(symbol)
                elif category == 4:
                    symbol.category = category
                    var_table.append(symbol)
                elif category == 5:
                    if isparam:
                        symbol.category = 4
                        var_table.append(symbol)
                    else:
                        self.scope = self.input[0].scope
                        symbol.category = category
                        symbol.scope = 0
                        self.include(symbol)
                        isparam = True
            self.input.pop(0)

    def run(self, input):
        self.input = input
        while self.input:
            try:
                if self.input[0].identifier in semanticdeclarations.keys():
                    self.declaration_handler()
                elif self.input[0].identifier == 6:
                    self.body_handler()
                else:
                    self.input.pop(0)
            except Exception as err:
                raise Exception(err)

    def clear_scope(self):
        temp = []
        for s in self.symbol_table:
            if s.category == 5:
                temp.append(s)
            if s.scope <= self.scope:
                temp.append(s)
        self.symbol_table = temp

    def include(self, symbol):
        if self.symbol_table:
            for s in self.symbol_table:
                if s.name == symbol.name and s.scope == symbol.scope:
                    raise Exception("{0} {1} na linha {2} duplicado".format(semanticdeclarations.get(symbol.category),
                                                                            symbol.name, symbol.line))
            self.symbol_table.append(symbol)
        else:
            self.symbol_table.append(symbol)

    def body_handler(self):
        while self.input[0].identifier != 7:
            self.input.pop(0)

    def is_declared(self, symbol):
        for s in self.symbol_table:
            if symbol.name == s.name and symbol.category == s.category and symbol.scope <= s.scope and \
                    symbol.type == s.type:
                return True
        return False
