from models.symbol import Symbol
from models.semanticflags import semanticdeclarations
from models.semanticflags import semantictypes


class SemanticalAnalyzer():

    def __init__(self):
        self.symbols = []
        self.input = []

    def declare(self, input):
        if input:
            self.input = input
            category = input[0].identifier
            var_list = []
        else:
            raise Exception("Lista de símbolos inválida")
        try:
            input.pop(0)
            while input[0].identifier not in (semanticdeclarations.keys() or 6):
                if self.input[0].identifier in semantictypes.keys():
                    x = self.input[0].identifier
                    if self.input[0].identifier == 9:
                        self.input.pop(0)
                        while self.input[0].identifier not in semantictypes.keys():
                            self.input.pop(0)
                        self.input.pop(0)
                    for var in var_list:
                        var.type = x
                        self.insert_check(var)
                        self.symbols.append(var)
                    var_list.clear()
                elif self.input[0].identifier == 25:
                    symbol = Symbol()
                    symbol.name = self.input[0].value
                    symbol.scope = self.input[0].scope
                    if category in [2,3]:
                        symbol.category = category
                        if category == 3:
                            symbol.type = 8
                    elif category == 4:
                        symbol.category = category
                        var_list.append(symbol)
                        self.input.pop(0)
                        continue
                    self.insert_check(symbol)
                    self.symbols.append(symbol)
                else:
                    #TODO: Declaração de Procedure
                    pass
                self.input.pop(0)
        except Exception as err:
            raise Exception(err)

    def insert_check(self, symbol):
        for s in self.symbols:
            if symbol == s:
                raise Exception("{0} {1} na linha {2} duplicado".format(semanticdeclarations.get(symbol.category),
                                                                        self.input[0].value, self.input[0].line))
            else:
                pass

    #TODO: Verificação de variável declarada