from builtins import Exception
import importlib
import re

terminals = importlib.import_module("src.models.terminals").terminals
state_machine_lib = importlib.import_module("src.lexical.statemachine")
token_lib = importlib.import_module("src.models.token")

class LexicalAnalyze:

    def __init__(self):
        self.text = None
        self.current_char = None
        self.next_char = None
        self.ident_buffer = ""
        self.tokens = []

    def set_current_char(self):
        if self.text:
            if len(self.text) > 1:
                self.text, self.current_char = \
                    self.text[1:], self.text[0]
            else:
                self.current_char, self.text = \
                    self.text[0], ''
        #else: #caso não exista mais characteres, sem terminar em estado 'end_state'
            #raise Exception('Programa não encerrado corretamente')


    def start_handler(self):
        self.set_current_char()
        if self.current_char.upper() == 'P':
            self.ident_buffer += self.current_char
            return "char_state"
        else:
            raise Exception("Programa inciciada incorretamente")
            return "erro_state",

    def expression_end_handler(self):
        self.set_current_char()
        if self.current_char.isspace() or \
            self.current_char == '\n':
            return "white_space_state"
        return "end_state"

    def char_handler(self):
        self.set_current_char()
        while self.current_char.isalnum():
            self.ident_buffer += self.current_char
            return "char_state"
        if self.current_char.isspace():
            self.register_identifier()
            return "white_space_state"
        elif self.current_char == ';':
            self.register_identifier()
            return "expression_end_state"

    def white_space_handler(self):
        self.set_current_char()
        while self.current_char.isspace() or \
                self.current_char == '\n':
            return "white_space_state"
        else:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state"
            #elif self.current_char.isdigit():

    def numerical_handler(self):
        pass

    def end_handler(self):
        pass

    def register_identifier(self):
        value = self.ident_buffer
        if self.is_reserved(value):
            token = token_lib.Token(list(terminals.keys())[list(terminals.values()).index(value)]
                          , value)
        else:
            token = token_lib.Token(list(terminals.keys())[list(terminals.values()).index('Identifier')],
                          value)
        self.tokens.append(token)
        self.ident_buffer = ""

    def is_reserved(self, identifier):
        return identifier in terminals.values()

    def run(self, text):
        self.text = text
        state_machine = state_machine_lib.StateMachine()
        state_machine.set_start("start_state")
        state_machine.add_state("start_state", self.start_handler)
        state_machine.add_state("char_state", self.char_handler)
        state_machine.add_state("expression_end_state", self.expression_end_handler)
        state_machine.add_state("white_space_state", self.white_space_handler)
        state_machine.add_state("numerical_state", self.numerical_handler)
        state_machine.add_state("end_state", self.end_handler, True)
        state_machine.add_state("error_state", None, True)
        state_machine.run(self.text)


if __name__ == "__main__":
    analyzer = LexicalAnalyze()
    f = open('lms.txt', 'r')
    analyzer.run(f.read())
