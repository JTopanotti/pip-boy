from models.symbol import Symbol
from models.semanticflags import semanticdeclarations
from models.semanticflags import semantictypes


class SemanticalAnalyzer:

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
                        # symbol.scope = 0
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
                    self.input.pop(0)
            except Exception as err:
                raise Exception(err)

    def clear_scope(self):
        temp = []
        for s in self.symbol_table:
            if s.category in [5, 6]:
                temp.append(s)
            if s.scope <= self.scope:
                temp.append(s)
        self.symbol_table = temp

    def include(self, symbol):
        if self.symbol_table:
            for s in self.symbol_table:
                if s.name == symbol.name and s.scope == symbol.scope:
                    raise Exception("{0} '{1}' na linha {2} duplicado".format(semanticdeclarations.get(symbol.category),
                                                                            symbol.name, symbol.line))
            self.symbol_table.append(symbol)
        else:
            self.symbol_table.append(symbol)

    def body_handler(self):
        while self.input[0].identifier != 7:

            if self.input[0].identifier == 25:
                s = self.is_declared(self.input[0])
                type = None
                line = self.input[0].line
                if self.input[1].identifier == 38:
                    if s.category == 3:
                        raise Exception("Atribuição de valor em constante na linha {}".format(self.input[0].line))
                    expression = self.pop_line()
                    expression.pop(0)
                    type = self.is_valid(expression)
                    if s.type != type:
                        raise Exception("Operação retornou tipo '{0}', esperado tipo '{1}' na linha {2}".format(type,
                                                                                                            s.type,
                                                                                                            line))

            elif self.input[0].identifier == 11:
                self.input.pop(0)
                s = self.is_declared(self.input[0].value)
            #     self.check_procedure(expression)
            #     temp = []
            #     if self.is_declared(self.input[0]):
            #         while self.input[0].identifier !=0:
            #             temp.append(input[0])
            #             self.input.pop(0)
            #         self.check_parameters(temp)
            # if self.input[0].identifier == 25:
            #     if self.isdeclared(self.input[0]):
            #         while self.input[0].identifier != 47:
            self.input.pop(0)
        self.scope = 0

    def is_declared(self, symbol):
        for s in self.symbol_table:
            if symbol.value == s.name and symbol.scope <= s.scope:
                return s
        else:
            raise Exception("Identificador '{0}' na linha {1} não declarado".format(symbol.value,
                                                                                      self.input[0].line))

    def check_procedure(self, expression):
        name = expression[0].value
        expression.pop(0)
        call = []
        procedure = []

        p = self.is_declared(name)
        if p:
            for s in self.symbol_table:
                if s.category == 5 and s.scope == p.scope:
                    procedure.append(s)

    def is_valid(self, expression):
        type = None
        while expression:
            if expression[0].identifier == 25:
                s = self.is_declared(expression[0])
                if not type:
                    type = s.type
                elif type != s.type:
                    raise Exception("Operação com tipos diferentes na linha {}".format(s.line))
            elif expression[0].identifier == 26:
                if not type:
                    type = 8
                elif type != 8:
                    raise Exception("Operação com tipos diferentes na linha {}".format(s.line))
            elif expression[0].identifier in [46, 47]:
                return type
            expression.pop(0)
        raise Exception("Operação não identificada")

    def pop_line(self):
        line = self.input[0].line
        expression = []
        while self.input[0].identifier != 47:
            expression.append(self.input[0])
            self.input.pop(0)
        expression.append(self.input[0])
        return expression
