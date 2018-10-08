from builtins import Exception
from models.terminals import terminals
from models.productions import productions

class SyntaxicalAnalyzer():
    def __init__(self, input=None):
        self.input = input
        #51 = $, 52 = 'PROGRAMA'
        self.expansions = [52, 51]
        self.actions = []
        self.proceed = True

    def register_action(self, action):
        self.actions.append(action)

    def proceed(self):
        self.proceed = True

    def trigger_actions(self):

        if self.actions:
            for action in self.actions:
                action.trigger()

    def load_variables(self):
        x, a = None, None
        x = self.expansions[0]
        if self.input:
            a = self.input[0].identifier

        return x, a

    def run(self, input=None):
        self.input = input
        if not self.input:
            raise Exception('Need to define the input tokens!')

        x, a = self.load_variables()

        while x != 51:

            if self.proceed:
                if x in terminals.keys() or x == 51: #51 = $ / Fim da pilha
                    if x == a:
                        self.expansions.pop(0)
                        self.input.pop(0)
                    else:
                        raise Exception("Erro de Syntax: expansao terminal {} nao encontrado no topo da pilha de tokens".format(x))
                else:
                    if (x, a) in productions.keys():
                        self.expansions.pop(0)
                        if productions[(x, a)][0] != 0: #0 = NULL / No productions
                            self.expansions = productions[(x, a)] + self.expansions
                            self.current_derivation = "({0}, {1}) deriva em: {2}".format(x, a, productions[(x, a)])
                            self.trigger_actions()

                    else:
                        raise Exception("Derivacao para ({}, {}) nao foi encontrado na tabela de parsing".format(x, a))

                x, a = self.load_variables()
                print(x)
                self.proceed = False

        self.trigger_actions()
