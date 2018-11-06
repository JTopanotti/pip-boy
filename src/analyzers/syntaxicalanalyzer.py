from builtins import Exception
from models.terminals import terminals
from models.productionsnew import productions


class SyntaxicalAnalyzer():
    def __init__(self, input=None):
        self.input = input
        self.actions = []
        self.clear_cache()

    def register_action(self, action):
        self.actions.append(action)

    def proceed(self):
        self.process_syntax()

    def process_syntax_whole(self):
        while self.x != 51:
            self.process_syntax()

    def clear_cache(self):
        self.expansions = [52, 51]
        self.current_derivation = None
        self.x = None
        self.a = None

        self.trigger_actions()

    def trigger_actions(self):

        if self.actions:
            for action in self.actions:
                action.trigger()

    def load_variables(self):
        self.x, self.a = None, None
        self.x = self.expansions[0]
        if self.input:
            self.a = self.input[0].identifier

        return self.x, self.a

    def process_syntax(self):

        self.load_variables()
        if self.x != 51:
            if self.x in terminals.keys() or self.x == 51:  # 51 = $ / Fim da pilha
                if self.x == self.a:
                    self.expansions.pop(0)
                    self.input.pop(0)
                else:
                    raise Exception(
                        "Erro de Syntax: expansao terminal {} nao encontrado no topo da pilha de tokens".format(self.x))
            else:
                if (self.x, self.a) in productions.keys():
                    self.expansions.pop(0)
                    if productions[(self.x, self.a)][0] != 0:  # 0 = NULL / No productions
                        self.expansions = productions[(self.x, self.a)] + self.expansions
                        self.current_derivation = "({0}, {1}) deriva em: {2}".format(self.x, self.a,
                                                                                     productions[(self.x, self.a)])
                        self.trigger_actions()

                else:
                    raise Exception(
                        "Derivacao para ({}, {}) nao foi encontrado na tabela de parsing".format(self.x, self.a))
            self.load_variables()
            print(self.x)
        else:
            print("End of derivation")

        self.trigger_actions()

    def run(self, input=None):
        self.input = input
        if not self.input:
            raise Exception('Need to define the input tokens!')

        self.process_syntax()
