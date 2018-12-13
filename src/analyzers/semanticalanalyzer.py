from models.symbol import Symbol
from models.semanticflags import semanticdeclarations
from models.semanticflags import semantictypes
from models.token import Token


class SemanticalAnalyzer:

    def __init__(self):
        self.symbol_table = []
        self.input = []
        self.scope = 0

    def declaration_handler(self):
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
                symbol.name = self.input[0].value.upper()
                symbol.line = self.input[0].line
                if category in [2, 3]:
                    symbol.category = category
                    if category == 3:
                        symbol.type = 8
                    self.include(symbol)
                elif category == 4:
                    symbol.category = category
                    var_table.append(symbol)
                elif category == 5:
                    if isparam:
                        symbol.category = 6
                        var_table.append(symbol)
                    else:
                        self.scope = self.input[0].scope
                        symbol.category = category
                        self.include(symbol)
                        isparam = True
            self.input.pop(0)

    def run(self, input):
        self.symbol_table = []
        self.input = input
        while self.input:
            try:
                if self.input[0].identifier in semanticdeclarations.keys():
                    self.declaration_handler()
                elif self.input[0].identifier == 6:
                    self.body_handler()
                else:
                    if len(self.input) > 0:
                        self.input.pop(0)
            except IndexError as err:
                raise Exception(err)

    def clear_scope(self):
        temp = []
        for s in self.symbol_table:
            if s.category in [5, 6]:
                temp.append(s)
            elif s.scope <= self.scope:
                temp.append(s)
        self.symbol_table = temp

    def include(self, symbol):
        if self.symbol_table:
            for s in self.symbol_table:
                if symbol.category == 5:
                    if s.name == symbol.name:
                        raise Exception(
                            "{0} '{1}' na linha {2} duplicado".format(semanticdeclarations.get(symbol.category),
                                                                      symbol.name, symbol.line))
                elif s.name == symbol.name and s.scope == symbol.scope:
                    raise Exception("{0} '{1}' na linha {2} duplicado". format(semanticdeclarations.get(symbol.category),
                                                                              symbol.name, symbol.line))
            self.symbol_table.append(symbol)
        else:
            self.symbol_table.append(symbol)

    def body_handler(self):
        while self.input[0].identifier != 7:
            if self.input[0].identifier == 25:
                s = self.is_declared(self.input[0], 4)
                type = None
                line = self.input[0].line
                if self.input[1].identifier == 38:
                    if s.category == 3:
                        raise Exception("Atribuição de valor em constante na linha {}".format(self.input[0].line))
                    expression = self.pop_line()
                    expression.pop(0)
                    type = self.is_valid(expression, False)
                    if s.type != type:
                        raise Exception("Operação retornou tipo '{0}', esperado tipo '{1}' na linha {2}".format(type,
                                                                                                                s.type,
                                                                                                                line))

            elif self.input[0].identifier == 11:
                self.input.pop(0)
                param = []
                expression = []
                s = self.is_declared(self.input[0], 5)
                line = self.input[0].line
                expression = self.pop_line()
                expression.pop(0)
                while expression:
                    type, expression = self.is_valid(expression, True)
                    param.append(type)
                self.check_procedure(s, param, line)

            elif self.input[0].identifier == 12:
                self.input.pop(0)
                self.is_declared(self.input[0], 2)
            self.input.pop(0)
        self.scope = 0
        self.clear_scope()

    def is_declared(self, symbol, category):

        for s in self.symbol_table:
            if category == 2 and s.category == 2 and s.scope == symbol.scope and s.name.upper() == symbol.value.upper():
                return s
            elif category == 5 and symbol.value.upper() == s.name.upper() and s.category == category:
                return s
            elif category == 4 and symbol.value.upper() == s.name.upper() and s.scope <= symbol.scope:
                return s
        else:
            raise Exception("Identificador '{0}' na linha {1} não declarado".format(symbol.value,
                                                                                    self.input[0].line))

    def check_procedure(self, symbol, call_p, line):
        procedure_p = []
        for s in self.symbol_table:
            if s.category == 6 and s.scope == symbol.scope:
                procedure_p.append(s.type)
        count_p = len(procedure_p)
        count_c = len(call_p)
        if count_p != count_c:
            raise Exception("Quantidade de parametros declarada: {0}, quantidade esperada {1}".format(count_c, count_p))
        for p, c in zip(procedure_p, call_p):
            if p != c:
                raise Exception("Tipo '{0}' declarado na linha {1}, tipo '{2}' esperado".format(c, p, line))

    def is_valid(self, expression, param):
        type = None
        while expression:
            if expression[0].identifier == 25:
                s = self.is_declared(expression[0], 4)
                if not type:
                    type = s.type
                elif type != s.type:
                    raise Exception("Operação com tipos diferentes na linha {}".format(s.line))
            elif expression[0].identifier == 26:
                if not type:
                    type = 8
                elif type != 8:
                    raise Exception("Operação com tipos diferentes na linha {}".format(s.line))
            elif expression[0].identifier in [46, 47, 7]:
                expression.pop(0)
                if param:
                    return type, expression
                return type
            expression.pop(0)
        raise Exception("Operação não identificada")

    def pop_line(self):
        expression = []
        while self.input[0].identifier != 47:
            expression.append(self.input[0])
            self.input.pop(0)
        expression.append(self.input[0])
        return expression
