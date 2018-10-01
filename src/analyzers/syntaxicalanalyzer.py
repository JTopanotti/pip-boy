from builtins import Exception
from models.terminals import terminals
from models.productions import productions

class SyntaxicalAnalyzer():
    def __init__(self, input=None):
        self.input = input
        #51 = $, 52 = 'PROGRAMA'
        self.expansions = [52, 51]


    def run(self, input=None):
        self.input = input
        if not self.input:
            raise Exception('Need to define the input tokens!')
        self.a = self.input[0].identifier

        x = None
        while x != 51:
            x = self.expansions[0]
            a = self.input[0].identifier

            print("x: {0}, a: {1} ".format(x, a))

            if x in terminals.keys() or x == 51: #51 = $ / Fim da pilha
                if x == a:
                    self.expansions.pop(0)
                    self.input.pop(0)
                else:
                    raise Exception("Syntax Error 1")
            else:
                if (x, a) in productions.keys():
                    self.expansions.pop(0)
                    if productions[(x, a)][0] != 0: #0 = NULL / No productions
                        self.expansions = productions[(x, a)] + self.expansions
                else:
                    raise Exception("Syntax Error 2")



