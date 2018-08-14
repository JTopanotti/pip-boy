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
        self.ident_buffer = ""
        self.value_buffer = ""
        self.tokens = []

        self.operators = ["+", "-", "/", "*"]
        self.binary_operators = ["=", "<", ">"]
        self.specials = [":", ";", ",", ".", "(", ")", "[", "]", "\'"]

    def set_current_char(self):
        if self.text:
            if len(self.text) > 1:
                self.current_char, self.text, = \
                    self.text[0], self.text[1:]
            else:
                self.current_char, self.text = \
                    self.text[0], ''
        else:
            self.current_char = None


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
        if self.current_char:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state"
            if self.current_char.isspace() or \
                    self.current_char == '\n':
                return "white_space_state"
        else:
            return "end_state"

    def char_handler(self):
        self.set_current_char()
        if self.current_char:
            while self.current_char.isalnum():
                self.ident_buffer += self.current_char
                return "char_state"

            if self.current_char in self.operators:
                self.tokens.append(token_lib.Token(self.current_char))
                return "arith_operator_state"
            elif self.current_char in self.binary_operators:
                return "binary_operator_state"
            elif self.current_char in self.specials:
                self.register_identifier()
                self.tokens.append(token_lib.Token(self.current_char))
                return "special_char_state"
            elif self.current_char.isspace():
                self.register_identifier()
                return "white_space_state"
        else:
            return "end_state"

    def arith_operator_handler(self):
        self.set_current_char()
        if self.current_char:
            if self.current_char.isspace:
                return "white_space_state"
            elif self.current_char.isalpha():
                return "char_state"
            elif self.current_char.isdigit():
                self.value_buffer += self.current_char
                return "digit_state"
        else:
            return "end_state"

    def white_space_handler(self):
        self.set_current_char()
        if self.current_char:
            while self.current_char.isspace() or \
                    self.current_char == '\n':
                return "white_space_state"
            else:
                if self.current_char.isalpha():
                    self.ident_buffer += self.current_char
                    return "char_state"
                elif self.current_char in self.specials:
                    self.tokens.append(token_lib.Token(self.current_char))
                    return "special_char_state"
                elif self.current_char.isdigit():
                    self.value_buffer += self.current_char
                    return "numerical_state"
        else:
            return "end_state"

    def special_char_handler(self):
        self.set_current_char()
        if self.current_char:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state"
            elif self.current_char.isalnum():
                self.value_buffer += self.current_char
                return "numerical_state"
            elif self.current_char.isspace():
                return "white_space_state"
            elif self.current_char in self.specials:
                self.tokens.append(token_lib.Token(self.current_char))
                return "special_char_state"
        else:
            return "end_state"

    def binary_operator_handler(self):
        self.register_identifier()
        self.register_number()
        if self.current_char in ['<', '>'] and \
            self.text[0] == '=':
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.tokens.append(token_lib.Token(operator))
        ##Stopped here



    def numerical_handler(self):
        pass

    def end_handler(self):
        for token in self.tokens:
            print(token.value)

    def register_number(self):
        value = self.value_buffer
        if value:
            value = int(value)
            self.tokens.append(token_lib.Token(value))

    def register_identifier(self):
        value = self.ident_buffer
        if value:
            if self.is_reserved(value):
                token = token_lib.Token(value, reserved=True)
            else:
                token = token_lib.Token(value)
            self.tokens.append(token)
            self.ident_buffer = ""

    def is_reserved(self, identifier):
        return identifier in terminals.values()

    def run(self, text):
        self.text = text.replace('\n', '')
        state_machine = state_machine_lib.StateMachine()
        state_machine.set_start("start_state")
        state_machine.add_state("start_state", self.start_handler)
        state_machine.add_state("char_state", self.char_handler)
        state_machine.add_state("arith_operator_state", self.arith_operator_handler)
        state_machine.add_state("binary_operator_state", self.binary_state_handler)
        state_machine.add_state("special_char_state", self.special_char_handler)
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
