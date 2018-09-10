from builtins import Exception
from models.terminals import terminals
from models.productions import productions

class SyntaxicalAnalyzer():
    def __init__(self, input=None):
        self.input = input
        #51 = $, 52 = 'PROGRAM'
        self.expansions = [51, 52]


    def run(self, input=None):
        self.input = input
        if not self.input:
            raise Exception('Need to define the input tokens!')
        self.a = self.input[0]

        x = None
        while x != 51:
            x = self.expansions[-1]
            a = self.input[0]

            if x in terminals.keys() or x == 51:
                if x == a:
                    self.expansions.pop()
                    self.input.pop(0)
                else:
                    raise Exception("Syntax Error")
            else:
                if productions[(x, a)][0] != "NULL":
                    pass


