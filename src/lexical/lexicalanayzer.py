from builtins import Exception
import importlib

terminals = importlib.import_module("src.models.terminals").terminals
token_lib = importlib.import_module("src.models.token")


class LexicalAnalyze:

    def __init__(self):
        self.text = None
        self.current_char = None
        self.ident_buffer = ""
        self.value_buffer = ""
        self.tokens = []
        self.handlers = {
            "START_STATE": self.start_handler,
            "CHAR_STATE": self.char_handler,
            "ARITH_OPERATOR_STATE": self.arith_operator_handler,
            "BINARY_OPERATOR_STATE": self.binary_operator_handler,
            "SPECIAL_CHAR_STATE": self.special_char_handler,
            "WHITE_SPACE_STATE": self.white_space_handler,
            "DIGIT_STATE": self.digit_handler,
            "END_STATE": self.end_handler
        }
        self.start_state = "START_STATE"
        self.end_states = ["ERROR_STATE", "END_STATE"]

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
        if self.current_char.isalpha():
            self.ident_buffer += self.current_char
            return "char_state"
        else:
            return "error_state"

    def char_handler(self):
        if self.current_char:
            while self.current_char.isalnum():
                self.ident_buffer += self.current_char
                return "char_state"

            if self.current_char in self.operators:
                self.register_identifier()
                self.register_number()
                self.tokens.append(token_lib.Token(self.current_char))
                return "arith_operator_state"
            elif self.current_char in self.binary_operators:
                self.register_identifier()
                self.register_number()
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
        if self.current_char:
            while self.current_char.isspace():
                return "white_space_state"
            else:
                if self.current_char.isalpha():
                    self.ident_buffer += self.current_char
                    return "char_state"
                elif self.current_char in self.specials:
                    self.tokens.append(token_lib.Token(self.current_char))
                    return "special_char_state"
                elif self.current_char in self.operators:
                    self.register_number()
                    self.register_identifier()
                    return "operator_state"
                elif self.current_char in self.binary_operators:
                    self.register_number()
                    self.register_identifier()
                    return "binary_operator_state"
                elif self.current_char.isdigit():
                    self.value_buffer += self.current_char
                    return "digit_state"
        else:
            return "end_state"

    def special_char_handler(self):
        if self.current_char:
            if self.current_char.isalpha():
                self.ident_buffer += self.current_char
                return "char_state"
            elif self.current_char.isdigit():
                self.value_buffer += self.current_char
                return "digit_state"
            elif self.current_char.isspace():
                return "white_space_state"
            elif self.current_char in self.specials:
                self.tokens.append(token_lib.Token(self.current_char))
                return "special_char_state"
        else:
            return "end_state"

    def binary_operator_handler(self):
        if self.current_char in ['<', '>'] and \
                self.text[0] in ['=', '>']:
            operator = self.current_char
            self.set_current_char()
            operator = operator + self.current_char
            self.tokens.append(token_lib.Token(operator))
        else:
            self.tokens.append(token_lib.Token(self.current_char))
        if self.current_char:
            if self.current_char.isspace():
                return "white_space_state"
            else:
                self.ident_buffer += self.current_char
                return "char_state"

    def digit_handler(self):
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

        try:
            handler = self.handlers[self.start_state]
        except:
            raise Exception("Precisa chamar .set_start() antes de .run()")
        if not self.end_states:
            raise Exception("Pelo menos um estado final deve existir")

        while True:
            self.set_current_char()
            new_state = handler()
            print(new_state)
            if new_state.upper() in self.end_states:
                handler = self.handlers[new_state.upper()]
                handler()
                print("chegou ao estado", new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]


if __name__ == "__main__":
    analyzer = LexicalAnalyze()
    f = open('lms.txt', 'r')
    analyzer.run(f.read())
