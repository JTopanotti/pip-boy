from src.models.terminals import terminals
from src.lexical.statemachine import StateMachine
from src.models.token import Token


class LexicalAnalyze:

    def __init__(self):
        self.current_char = ''
        self.next_char = ''
        self.ident_buffer = ""
        self.tokens = []

    def start_handler(self, text):
        text, self.current_char = text[1:], text[0]
        if self.current_char.upper() == 'P':
            self.ident_buffer += self.current_char
            return "char_state", text
        else:
            raise Exception("Programa inciciada incorretamente")
            return "erro_state",

    def expression_end_handler(self, text):
        # Implementar isto
        return "end_state", text

    def char_handler(self, text):
        text, self.current_char = text[1:], text[0]
        while self.current_char.isalnum():
            self.ident_buffer += self.current_char
            return "char_state", text
        if self.current_char.isspace():
            self.register_identifier()
            return "white_space_state", text
        elif self.current_char == ';':
            self.register_identifier()
            return "expression_end_state", text


    def white_space_handler(self, text):
        text, self.current_char = text[1:], text[0]
        while self.current_char.isspace():
            return "white_space_state", text
        else:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state", text
            #elif self.current_char.isdigit():



    def numerical_handler(self, text):
        pass

    def end_handler(self, text):
        pass

    def register_identifier(self):
        value = self.ident_buffer
        if self.is_reserved(value):
            token = Token(list(terminals.keys())[list(terminals.values()).index(value)]
                          , value)
        else:
            token = Token(list(terminals.keys())[list(terminals.values()).index('Identifier')],
                          value)
        self.tokens.append(token)
        self.ident_buffer = ""

    def is_reserved(self, identifier):
        return identifier in terminals.values()

    def run(self, text):
        state_machine = StateMachine()
        state_machine.set_start("start_state")
        state_machine.add_state("start_state", self.start_handler)
        state_machine.add_state("char_state", self.char_handler)
        state_machine.add_state("expression_end_state", self.expression_end_handler)
        state_machine.add_state("white_space_state", self.white_space_handler)
        state_machine.add_state("numerical_state", self.numerical_handler)
        state_machine.add_state("end_state", self.end_handler, True)
        state_machine.add_state("error_state", None, True)
        state_machine.run(text)


if __name__ == "__main__":
    analyzer = LexicalAnalyze()
    # f = open('lms.txt', 'r')
    analyzer.run("Program testeproc1;")
